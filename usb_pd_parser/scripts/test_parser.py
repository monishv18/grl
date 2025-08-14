#!/usr/bin/env python3
"""
Test script for USB PD Parser
This script demonstrates the parser functionality with sample data
"""

import json
import os
import tempfile
from pathlib import Path
from parser.core import USBPDParser
from parser.validation import (generate_validation_report, analyze_toc_vs_parsed, 
                              generate_summary_statistics, save_validation_report, 
                              print_validation_summary)

def create_sample_pdf():
    """Create a sample PDF-like structure for testing"""
    # This is a mock function - in real usage, you would have actual PDF files
    print("📄 Note: This is a demonstration script.")
    print("   In real usage, you would provide actual USB PD specification PDFs.")
    return None

def test_parser_with_sample_data():
    """Test the parser with sample data to demonstrate functionality"""
    
    print("🧪 Testing USB PD Parser with Sample Data")
    print("=" * 50)
    
    # Sample TOC entries (simulating what would be extracted from a PDF)
    sample_toc_entries = [
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "1",
            "title": "Introduction",
            "page": 1,
            "level": 1,
            "parent_id": None,
            "full_path": "1 Introduction",
            "tags": ["overview"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "2",
            "title": "Overview",
            "page": 15,
            "level": 1,
            "parent_id": None,
            "full_path": "2 Overview",
            "tags": ["overview"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "2.1",
            "title": "Power Delivery Basics",
            "page": 15,
            "level": 2,
            "parent_id": "2",
            "full_path": "2.1 Power Delivery Basics",
            "tags": ["power_management"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "2.1.1",
            "title": "Voltage Levels",
            "page": 16,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.1 Voltage Levels",
            "tags": ["power_management"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "2.1.2",
            "title": "Current Capabilities",
            "page": 18,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.2 Current Capabilities",
            "tags": ["power_management"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "2.2",
            "title": "Communication Protocol",
            "page": 25,
            "level": 2,
            "parent_id": "2",
            "full_path": "2.2 Communication Protocol",
            "tags": ["communication"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "3",
            "title": "State Machines",
            "page": 45,
            "level": 1,
            "parent_id": None,
            "full_path": "3 State Machines",
            "tags": ["state_machine"]
        }
    ]
    
    # Sample section entries with content
    sample_section_entries = []
    for toc_entry in sample_toc_entries:
        section_entry = toc_entry.copy()
        # Add sample content based on section type
        if "voltage" in toc_entry["title"].lower():
            section_entry["content"] = "This section describes the various voltage levels supported by USB Power Delivery, including 5V, 9V, 12V, 15V, and 20V configurations."
        elif "current" in toc_entry["title"].lower():
            section_entry["content"] = "Current capabilities are defined for each voltage level, with maximum current ratings and safety considerations."
        elif "protocol" in toc_entry["title"].lower():
            section_entry["content"] = "The communication protocol uses CC line signaling and message-based communication for power negotiation and status updates."
        elif "state" in toc_entry["title"].lower():
            section_entry["content"] = "State machines define the behavior of USB PD devices during power negotiation, contract establishment, and operational states."
        else:
            section_entry["content"] = f"This is the content for section {toc_entry['section_id']}: {toc_entry['title']}. It contains relevant information about the topic."
        
        sample_section_entries.append(section_entry)
    
    # Test validation functionality
    print("🔍 Testing Validation System...")
    
    # Generate validation report
    report_df = generate_validation_report(sample_toc_entries, sample_section_entries)
    print(f"✅ Generated validation report with {len(report_df)} entries")
    
    # Generate analysis
    analysis = analyze_toc_vs_parsed(sample_toc_entries, sample_section_entries)
    summary = generate_summary_statistics(sample_toc_entries, sample_section_entries)
    
    # Print validation summary
    print_validation_summary(analysis, summary)
    
    # Test output generation
    print("\n📁 Testing Output Generation...")
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save sample data to JSONL files
        from parser.utils import write_jsonl
        
        toc_file = os.path.join(temp_dir, "usb_pd_toc.jsonl")
        spec_file = os.path.join(temp_dir, "usb_pd_spec.jsonl")
        metadata_file = os.path.join(temp_dir, "usb_pd_metadata.jsonl")
        
        write_jsonl(sample_toc_entries, toc_file)
        write_jsonl(sample_section_entries, spec_file)
        
        # Create sample metadata
        sample_metadata = {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "total_pages": 150,
            "toc_pages": [1, 2, 3],
            "sections_count": len(sample_section_entries),
            "tables_count": 5,
            "figures_count": 12
        }
        write_jsonl([sample_metadata], metadata_file)
        
        # Save validation report
        report_file = save_validation_report(report_df, analysis, summary, temp_dir)
        
        print(f"✅ Sample files created in temporary directory:")
        print(f"   • TOC: {toc_file}")
        print(f"   • Sections: {spec_file}")
        print(f"   • Metadata: {metadata_file}")
        print(f"   • Validation Report: {report_file}")
        
        # Display sample JSONL content
        print("\n📊 Sample JSONL Output:")
        print("-" * 30)
        
        with open(toc_file, 'r') as f:
            for i, line in enumerate(f.readlines()[:3]):  # Show first 3 entries
                data = json.loads(line.strip())
                print(f"TOC Entry {i+1}:")
                print(f"  Section: {data['section_id']} - {data['title']}")
                print(f"  Page: {data['page']}, Level: {data['level']}")
                print(f"  Tags: {', '.join(data['tags'])}")
                print()
    
    print("✅ All tests completed successfully!")
    print("\n💡 To use with real PDFs:")
    print("   python scripts/parse_usb_pd.py path/to/your/document.pdf")

def main():
    """Main test function"""
    try:
        test_parser_with_sample_data()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
