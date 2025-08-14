import re
from typing import Dict, List, Optional
from .schemas import validate_toc_entry
import json

def extract_toc_entry(line: str, doc_title: str) -> Optional[Dict]:
    """Extract TOC entry from a line of text using multiple regex patterns"""
    line = line.strip()
    if not line:
        return None
    
    # Multiple regex patterns to handle different TOC formats
    patterns = [
        # Standard format: "2.1.2 Power Delivery Contract Negotiation .......... 53"
        r'^(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$',
        # Format without dots: "2.1.2 Power Delivery Contract Negotiation 53"
        r'^(\d+(?:\.\d+)*)\s+(.*?)\s+(\d+)$',
        # Format with parentheses: "2.1.2 (Power Delivery Contract Negotiation) 53"
        r'^(\d+(?:\.\d+)*)\s*\(?(.*?)\)?\s*\.+\s*(\d+)$',
        # Format with chapter prefix: "Chapter 2 Overview 53"
        r'^Chapter\s+(\d+)\s+(.*?)\s*\.+\s*(\d+)$',
        # Format with section prefix: "Section 2.1 Introduction 53"
        r'^Section\s+(\d+(?:\.\d+)*)\s+(.*?)\s*\.+\s*(\d+)$'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            section_id = match.group(1)
            title = match.group(2).strip()
            page = int(match.group(3))
            
            # Clean up title
            title = re.sub(r'^\s*[-–—]\s*', '', title)  # Remove leading dashes
            title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
            
            # Calculate level and parent_id
            level = section_id.count('.') + 1
            parent_id = '.'.join(section_id.split('.')[:-1]) if level > 1 else None
            
            # Generate full path
            full_path = f"{section_id} {title}"
            
            # Generate tags based on title content
            tags = generate_tags(title)
            
            entry = {
                "doc_title": doc_title,
                "section_id": section_id,
                "title": title,
                "page": page,
                "level": level,
                "parent_id": parent_id,
                "full_path": full_path,
                "tags": tags
            }
            
            try:
                validate_toc_entry(entry)
                return entry
            except Exception as e:
                print(f"Warning: Invalid TOC entry '{line}': {e}")
                continue
    
    return None

def generate_tags(title: str) -> List[str]:
    """Generate semantic tags based on section title"""
    title_lower = title.lower()
    tags = []
    
    # Technical terms
    if any(word in title_lower for word in ['power', 'voltage', 'current']):
        tags.append('power_management')
    if any(word in title_lower for word in ['negotiation', 'contract', 'agreement']):
        tags.append('negotiation')
    if any(word in title_lower for word in ['communication', 'protocol', 'message']):
        tags.append('communication')
    if any(word in title_lower for word in ['state', 'machine', 'transition']):
        tags.append('state_machine')
    if any(word in title_lower for word in ['cable', 'connector', 'plug']):
        tags.append('hardware')
    if any(word in title_lower for word in ['compatibility', 'revision', 'version']):
        tags.append('compatibility')
    if any(word in title_lower for word in ['overview', 'introduction', 'background']):
        tags.append('overview')
    if any(word in title_lower for word in ['table', 'figure', 'diagram']):
        tags.append('reference')
    
    return tags

def extract_section_content(text: str, start_marker: str, end_marker: str = None) -> str:
    """Extract content between start and end markers"""
    if not text:
        return ""
    
    # Find start of section
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return text
    
    # Extract from start marker to end
    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        if end_idx != -1:
            return text[start_idx:end_idx].strip()
    
    return text[start_idx:].strip()

def write_jsonl(data: List[Dict], filename: str):
    """Write data to JSONL file with error handling"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for entry in data:
                json_line = json.dumps(entry, ensure_ascii=False)
                f.write(json_line + '\n')
        print(f"✅ Successfully wrote {len(data)} entries to {filename}")
    except Exception as e:
        print(f"❌ Error writing to {filename}: {e}")
        raise

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page headers/footers (common patterns)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)  # Page numbers
    text = re.sub(r'^\s*USB.*?Specification.*?\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    
    # Clean up line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()
