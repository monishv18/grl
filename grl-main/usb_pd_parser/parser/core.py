import pdfplumber
import os
import re
from tqdm import tqdm
from typing import List, Dict, Optional
from .utils import extract_toc_entry, write_jsonl, extract_section_content
from .config import Config

class USBPDParser:
    def __init__(self, pdf_path: str, doc_title: str = Config.DOC_TITLE):
        self.pdf_path = pdf_path
        self.doc_title = doc_title
        self.toc_entries = []
        self.section_entries = []
        self.metadata = {
            "doc_title": doc_title,
            "total_pages": 0,
            "toc_pages": [],
            "sections_count": 0,
            "tables_count": 0,
            "figures_count": 0
        }

    def extract_toc(self) -> List[Dict]:
        """Extract Table of Contents from the PDF"""
        print("Extracting Table of Contents...")
        self.toc_entries = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            self.metadata["total_pages"] = len(pdf.pages)
            
            # Scan first few pages for TOC
            for page_num in range(min(Config.TOC_SCAN_PAGES, len(pdf.pages))):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if not text:
                    continue
                
                for line in text.split("\n"):
                    entry = extract_toc_entry(line, self.doc_title)
                    if entry:
                        entry["page"] = page_num + 1  # Convert to 1-based page numbers
                        self.toc_entries.append(entry)
                        if page_num + 1 not in self.metadata["toc_pages"]:
                            self.metadata["toc_pages"].append(page_num + 1)
        
        # Sort TOC entries by section_id for proper hierarchy
        self.toc_entries.sort(key=lambda x: [int(n) for n in x["section_id"].split(".")])
        
        print(f"✅ TOC entries found: {len(self.toc_entries)}")
        return self.toc_entries

    def extract_sections(self) -> List[Dict]:
        """Extract all sections with content from the PDF"""
        if not self.toc_entries:
            self.extract_toc()
        
        print("Extracting sections with content...")
        self.section_entries = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for toc_entry in tqdm(self.toc_entries, desc="Processing sections"):
                section_content = self._extract_section_content(pdf, toc_entry)
                if section_content:
                    section_entry = toc_entry.copy()
                    section_entry["content"] = section_content
                    self.section_entries.append(section_entry)
        
        self.metadata["sections_count"] = len(self.section_entries)
        print(f"✅ Sections extracted: {len(self.section_entries)}")
        return self.section_entries

    def _extract_section_content(self, pdf, toc_entry: Dict) -> Optional[str]:
        """Extract content for a specific section"""
        start_page = toc_entry["page"]
        end_page = self._find_section_end_page(pdf, toc_entry)
        
        content_parts = []
        for page_num in range(start_page - 1, end_page):  # Convert to 0-based
            if page_num >= len(pdf.pages):
                break
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                content_parts.append(text)
        
        return "\n".join(content_parts) if content_parts else None

    def _find_section_end_page(self, pdf, current_section: Dict) -> int:
        """Find the end page for a section by looking for the next section"""
        current_id = current_section["section_id"]
        current_level = current_section["level"]
        
        # Find next section at same or higher level
        for toc_entry in self.toc_entries:
            if toc_entry["section_id"] == current_id:
                continue
            
            # Check if this is the next section at same or higher level
            if self._is_next_section(current_id, toc_entry["section_id"], current_level):
                return toc_entry["page"]
        
        # If no next section found, go to end of document
        return len(pdf.pages)

    def _is_next_section(self, current_id: str, next_id: str, current_level: int) -> bool:
        """Check if next_id represents the next section after current_id"""
        current_parts = [int(n) for n in current_id.split(".")]
        next_parts = [int(n) for n in next_id.split(".")]
        
        # Find common prefix length
        common_len = 0
        for i in range(min(len(current_parts), len(next_parts))):
            if current_parts[i] == next_parts[i]:
                common_len += 1
            else:
                break
        
        # Check if next section is at same or higher level
        if len(next_parts) <= current_level:
            return True
        
        # Check if it's a direct child of current section
        if len(next_parts) == len(current_parts) + 1 and common_len == len(current_parts):
            return False
        
        return True

    def count_tables_and_figures(self):
        """Count tables and figures in the document"""
        print("Counting tables and figures...")
        table_count = 0
        figure_count = 0
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # Count tables
                if page.find_tables():
                    table_count += len(page.find_tables())
                
                # Count figures (look for figure references in text)
                text = page.extract_text()
                if text:
                    figure_count += len(re.findall(r'Figure\s+\d+', text, re.IGNORECASE))
        
        self.metadata["tables_count"] = table_count
        self.metadata["figures_count"] = figure_count
        print(f"✅ Tables: {table_count}, Figures: {figure_count}")

    def save_outputs(self):
        """Save all outputs to JSONL files"""
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        # Save TOC entries
        toc_file = os.path.join(Config.OUTPUT_DIR, "usb_pd_toc.jsonl")
        write_jsonl(self.toc_entries, toc_file)
        print(f"✅ TOC saved to: {toc_file}")
        
        # Save section entries
        spec_file = os.path.join(Config.OUTPUT_DIR, "usb_pd_spec.jsonl")
        write_jsonl(self.section_entries, spec_file)
        print(f"✅ Sections saved to: {spec_file}")
        
        # Save metadata
        metadata_file = os.path.join(Config.OUTPUT_DIR, "usb_pd_metadata.jsonl")
        write_jsonl([self.metadata], metadata_file)
        print(f"✅ Metadata saved to: {metadata_file}")

    def parse_complete(self):
        """Complete parsing workflow"""
        try:
            self.extract_toc()
            self.count_tables_and_figures()
            self.extract_sections()
            self.save_outputs()
            print("✅ Complete parsing workflow finished successfully!")
            return True
        except Exception as e:
            print(f"❌ Error during parsing: {str(e)}")
            return False
