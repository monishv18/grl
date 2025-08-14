#!/usr/bin/env python3
"""
Example usage of the USB PD Parser
This script demonstrates various ways to use the parser
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import the parser
sys.path.append(str(Path(__file__).parent.parent))

from parser.core import USBPDParser
from parser.validation import (generate_validation_report, analyze_toc_vs_parsed, 
                              generate_summary_statistics, save_validation_report, 
                              print_validation_summary)
from parser.document_configs import get_document_config, list_supported_document_types

def example_basic_usage():
    """Example 1: Basic usage with default settings"""
    print("🔧 Example 1: Basic Usage")
    print("=" * 40)
    
    # This would be your actual PDF file
    pdf_path = "path/to/your/usb_pd_spec.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        print("   Please provide a valid PDF file path")
        return
    
    # Create parser instance
    parser = USBPDParser(pdf_path)
    
    # Run complete parsing workflow
    success = parser.parse_complete()
    
    if success:
        print(f"✅ Parsed {len(parser.toc_entries)} TOC entries")
        print(f"✅ Extracted {len(parser.section_entries)} sections")
        print(f"✅ Document has {parser.metadata['total_pages']} pages")
    else:
        print("❌ Parsing failed")

def example_custom_configuration():
    """Example 2: Custom configuration and output"""
    print("\n🔧 Example 2: Custom Configuration")
    print("=" * 40)
    
    pdf_path = "path/to/your/document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF file not found: {pdf_path}")
        return
    
    # Custom configuration
    custom_output_dir = "custom_output"
    custom_doc_title = "My Custom USB PD Specification"
    custom_toc_pages = 20
    
    # Create parser with custom settings
    parser = USBPDParser(pdf_path, custom_doc_title)
    
    # Override config
    from parser.config import Config
    Config.OUTPUT_DIR = custom_output_dir
    Config.TOC_SCAN_PAGES = custom_toc_pages
    
    # Extract TOC first
    toc_entries = parser.extract_toc()
    print(f"📋 Found {len(toc_entries)} TOC entries")
    
    # Extract sections
    section_entries = parser.extract_sections()
    print(f"📄 Extracted {len(section_entries)} sections")
    
    # Save outputs
    parser.save_outputs()
    
    # Generate validation report
    report_df = generate_validation_report(toc_entries, section_entries, custom_output_dir)
    print(f"📊 Validation report generated with {len(report_df)} entries")

def example_document_type_configuration():
    """Example 3: Using different document type configurations"""
    print("\n🔧 Example 3: Document Type Configuration")
    print("=" * 40)
    
    # List supported document types
    print("📚 Supported document types:")
    for doc_type in list_supported_document_types():
        print(f"   • {doc_type}")
    
    # Get configuration for different document types
    usb_pd_config = get_document_config("usb_pd")
    generic_config = get_document_config("generic")
    ieee_config = get_document_config("ieee")
    
    print(f"\n🔍 USB PD Config:")
    print(f"   TOC scan pages: {usb_pd_config.toc_scan_pages}")
    print(f"   Max file size: {usb_pd_config.max_file_size_mb} MB")
    print(f"   TOC patterns: {len(usb_pd_config.toc_patterns)}")
    print(f"   Tag mappings: {len(usb_pd_config.tag_mapping)}")
    
    print(f"\n🔍 Generic Config:")
    print(f"   TOC scan pages: {generic_config.toc_scan_pages}")
    print(f"   Max file size: {generic_config.max_file_size_mb} MB")

def example_validation_and_analysis():
    """Example 4: Advanced validation and analysis"""
    print("\n🔧 Example 4: Validation and Analysis")
    print("=" * 40)
    
    # This would be your actual parsed data
    # For demonstration, we'll create sample data
    
    # Sample TOC entries
    sample_toc = [
        {
            "doc_title": "USB PD Spec",
            "section_id": "2.1",
            "title": "Power Management",
            "page": 15,
            "level": 2,
            "parent_id": "2",
            "full_path": "2.1 Power Management",
            "tags": ["power_management"]
        },
        {
            "doc_title": "USB PD Spec",
            "section_id": "2.1.1",
            "title": "Voltage Levels",
            "page": 16,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.1 Voltage Levels",
            "tags": ["power_management"]
        }
    ]
    
    # Sample section entries
    sample_sections = [
        {
            "doc_title": "USB PD Spec",
            "section_id": "2.1",
            "title": "Power Management",
            "page": 15,
            "level": 2,
            "parent_id": "2",
            "full_path": "2.1 Power Management",
            "content": "This section covers power management...",
            "tags": ["power_management"]
        },
        {
            "doc_title": "USB PD Spec",
            "section_id": "2.1.1",
            "title": "Voltage Levels",
            "page": 16,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.1 Voltage Levels",
            "content": "Supported voltage levels include...",
            "tags": ["power_management"]
        }
    ]
    
    # Generate comprehensive validation report
    report_df = generate_validation_report(sample_toc, sample_sections)
    print(f"📊 Validation report: {len(report_df)} entries")
    
    # Analyze TOC vs parsed
    analysis = analyze_toc_vs_parsed(sample_toc, sample_sections)
    print(f"📈 Analysis results:")
    print(f"   Coverage: {analysis['coverage_percentage']:.1f}%")
    print(f"   Missing: {len(analysis['missing_from_parsed'])}")
    print(f"   Extra: {len(analysis['extra_in_parsed'])}")
    
    # Generate summary statistics
    summary = generate_summary_statistics(sample_toc, sample_sections)
    print(f"📊 Summary:")
    print(f"   Total content length: {summary['total_content_length']}")
    print(f"   Average content length: {summary['avg_content_length']:.1f}")
    
    # Print validation summary
    print_validation_summary(analysis, summary)

def example_batch_processing():
    """Example 5: Batch processing multiple documents"""
    print("\n🔧 Example 5: Batch Processing")
    print("=" * 40)
    
    # Directory containing multiple PDFs
    pdf_directory = "path/to/pdf/directory"
    
    if not os.path.exists(pdf_directory):
        print(f"⚠️  Directory not found: {pdf_directory}")
        return
    
    # Find all PDF files
    pdf_files = list(Path(pdf_directory).glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in directory")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files")
    
    # Process each PDF
    for pdf_file in pdf_files:
        print(f"\n📄 Processing: {pdf_file.name}")
        
        try:
            # Create parser
            parser = USBPDParser(str(pdf_file))
            
            # Extract TOC
            toc_entries = parser.extract_toc()
            print(f"   📋 TOC entries: {len(toc_entries)}")
            
            # Extract sections
            section_entries = parser.extract_sections()
            print(f"   📄 Sections: {len(section_entries)}")
            
            # Save outputs with unique names
            output_dir = f"output_{pdf_file.stem}"
            os.makedirs(output_dir, exist_ok=True)
            
            # Save files
            from parser.utils import write_jsonl
            write_jsonl(toc_entries, os.path.join(output_dir, "toc.jsonl"))
            write_jsonl(section_entries, os.path.join(output_dir, "sections.jsonl"))
            
            print(f"   ✅ Saved to: {output_dir}")
            
        except Exception as e:
            print(f"   ❌ Error processing {pdf_file.name}: {e}")

def example_custom_validation():
    """Example 6: Custom validation rules"""
    print("\n🔧 Example 6: Custom Validation")
    print("=" * 40)
    
    # Sample data
    toc_entries = [
        {"section_id": "1", "title": "Introduction", "page": 1, "level": 1, "parent_id": None},
        {"section_id": "2", "title": "Overview", "page": 5, "level": 1, "parent_id": None},
        {"section_id": "2.1", "title": "Basics", "page": 5, "level": 2, "parent_id": "2"}
    ]
    
    section_entries = [
        {"section_id": "1", "title": "Introduction", "page": 1, "level": 1, "parent_id": None, "content": "Content here"},
        {"section_id": "2", "title": "Overview", "page": 5, "level": 1, "parent_id": None, "content": "Content here"},
        {"section_id": "2.1", "title": "Basics", "page": 5, "level": 2, "parent_id": "2", "content": "Content here"}
    ]
    
    # Custom validation checks
    print("🔍 Running custom validation checks...")
    
    # Check for missing sections
    toc_ids = {e["section_id"] for e in toc_entries}
    parsed_ids = {e["section_id"] for e in section_entries}
    missing = toc_ids - parsed_ids
    
    if missing:
        print(f"❌ Missing sections: {', '.join(sorted(missing))}")
    else:
        print("✅ All TOC sections found in parsed data")
    
    # Check for content quality
    empty_content = [e for e in section_entries if not e.get("content") or len(e["content"].strip()) < 10]
    if empty_content:
        print(f"⚠️  Sections with minimal content: {len(empty_content)}")
        for section in empty_content:
            print(f"   • {section['section_id']}: {section['title']}")
    else:
        print("✅ All sections have substantial content")
    
    # Check hierarchy consistency
    for entry in toc_entries:
        if entry["parent_id"]:
            parent_exists = any(e["section_id"] == entry["parent_id"] for e in toc_entries)
            if not parent_exists:
                print(f"⚠️  Orphaned section {entry['section_id']}: parent {entry['parent_id']} not found")
    
    print("✅ Custom validation complete")

def main():
    """Run all examples"""
    print("🚀 USB PD Parser - Usage Examples")
    print("=" * 60)
    
    try:
        example_basic_usage()
        example_custom_configuration()
        example_document_type_configuration()
        example_validation_and_analysis()
        example_batch_processing()
        example_custom_validation()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("\n💡 To use with real PDFs:")
        print("   python scripts/parse_usb_pd.py path/to/your/document.pdf")
        
    except Exception as e:
        print(f"\n❌ Example failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
