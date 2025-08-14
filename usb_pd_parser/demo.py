#!/usr/bin/env python3
"""
USB PD Parser Demo
This script demonstrates the parser functionality with sample data
"""

import json
import tempfile
import os
from pathlib import Path

def create_sample_data():
    """Create sample data to demonstrate the parser"""
    
    # Sample TOC entries (simulating what would be extracted from a USB PD PDF)
    sample_toc = [
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
            "section_id": "2.2.1",
            "title": "CC Line Signaling",
            "page": 26,
            "level": 3,
            "parent_id": "2.2",
            "full_path": "2.2.1 CC Line Signaling",
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
        },
        {
            "doc_title": "USB Power Delivery Specification Rev 3.0",
            "section_id": "3.1",
            "title": "Power Negotiation States",
            "page": 45,
            "level": 2,
            "parent_id": "3",
            "full_path": "3.1 Power Negotiation States",
            "tags": ["state_machine", "negotiation"]
        }
    ]
    
    # Create section entries with content
    sample_sections = []
    for toc_entry in sample_toc:
        section_entry = toc_entry.copy()
        
        # Generate realistic content based on section type
        if "voltage" in toc_entry["title"].lower():
            section_entry["content"] = """This section describes the various voltage levels supported by USB Power Delivery. The specification defines multiple voltage levels including 5V, 9V, 12V, 15V, and 20V configurations. Each voltage level is designed to provide optimal power delivery for different device requirements and use cases."""
        elif "current" in toc_entry["title"].lower():
            section_entry["content"] = """Current capabilities are defined for each voltage level, with maximum current ratings and safety considerations. The specification includes detailed current limits, protection mechanisms, and thermal management requirements to ensure safe operation across all supported voltage levels."""
        elif "protocol" in toc_entry["title"].lower():
            section_entry["content"] = """The communication protocol uses CC line signaling and message-based communication for power negotiation and status updates. This includes structured message formats, timing requirements, and error handling mechanisms to ensure reliable power delivery communication."""
        elif "cc line" in toc_entry["title"].lower():
            section_entry["content"] = """CC line signaling is the primary communication method for USB Power Delivery. It uses specific voltage levels and timing patterns to establish communication channels, negotiate power contracts, and maintain operational status."""
        elif "state" in toc_entry["title"].lower():
            section_entry["content"] = """State machines define the behavior of USB PD devices during power negotiation, contract establishment, and operational states. Each state has specific entry conditions, exit conditions, and timeout behaviors to ensure predictable device operation."""
        elif "negotiation" in toc_entry["title"].lower():
            section_entry["content"] = """Power negotiation states handle the process of establishing power contracts between source and sink devices. This includes capability exchange, contract negotiation, and contract establishment phases with proper error handling and recovery mechanisms."""
        else:
            section_entry["content"] = f"This section provides comprehensive information about {toc_entry['title'].lower()}. It covers the fundamental concepts, requirements, and implementation details necessary for understanding and implementing USB Power Delivery functionality."
        
        sample_sections.append(section_entry)
    
    return sample_toc, sample_sections

def demonstrate_jsonl_output():
    """Demonstrate the JSONL output format"""
    
    print("📄 JSONL Output Format Demonstration")
    print("=" * 50)
    
    # Create sample data
    toc_entries, section_entries = create_sample_data()
    
    # Show TOC JSONL format
    print("\n📋 Table of Contents (usb_pd_toc.jsonl):")
    print("-" * 40)
    for i, entry in enumerate(toc_entries[:3]):  # Show first 3 entries
        json_line = json.dumps(entry, indent=2)
        print(f"Entry {i+1}:")
        print(json_line)
        print()
    
    # Show section JSONL format
    print("📄 Full Sections (usb_pd_spec.jsonl):")
    print("-" * 40)
    for i, entry in enumerate(section_entries[:2]):  # Show first 2 entries
        # Truncate content for display
        display_entry = entry.copy()
        if len(display_entry["content"]) > 100:
            display_entry["content"] = display_entry["content"][:100] + "..."
        
        json_line = json.dumps(display_entry, indent=2)
        print(f"Entry {i+1}:")
        print(json_line)
        print()
    
    # Show metadata format
    metadata = {
        "doc_title": "USB Power Delivery Specification Rev 3.0",
        "total_pages": 150,
        "toc_pages": [1, 2, 3],
        "sections_count": len(section_entries),
        "tables_count": 8,
        "figures_count": 15
    }
    
    print("📊 Metadata (usb_pd_metadata.jsonl):")
    print("-" * 40)
    print(json.dumps(metadata, indent=2))
    print()

def demonstrate_validation():
    """Demonstrate validation functionality"""
    
    print("🔍 Validation and Analysis Demonstration")
    print("=" * 50)
    
    # Create sample data
    toc_entries, section_entries = create_sample_data()
    
    # Import validation functions
    try:
        from parser.validation import (generate_validation_report, analyze_toc_vs_parsed, 
                                      generate_summary_statistics, print_validation_summary)
        
        # Generate validation report
        print("📊 Generating validation report...")
        report_df = generate_validation_report(toc_entries, section_entries)
        print(f"✅ Generated validation report with {len(report_df)} entries")
        
        # Analyze TOC vs parsed
        print("\n📈 Analysis results:")
        analysis = analyze_toc_vs_parsed(toc_entries, section_entries)
        print(f"   Coverage: {analysis['coverage_percentage']:.1f}%")
        print(f"   Missing: {len(analysis['missing_from_parsed'])}")
        print(f"   Extra: {len(analysis['extra_in_parsed'])}")
        print(f"   Order issues: {len(analysis['order_issues'])}")
        print(f"   Gaps: {len(analysis['gaps'])}")
        
        # Generate summary statistics
        summary = generate_summary_statistics(toc_entries, section_entries)
        print(f"\n📊 Summary statistics:")
        print(f"   Total content length: {summary['total_content_length']:,} characters")
        print(f"   Average content length: {summary['avg_content_length']:.1f} characters")
        print(f"   Sections with content: {summary['sections_with_content']}")
        
        # Show level distribution
        if 'level_distribution' in summary:
            print(f"\n📋 Level distribution:")
            for level, count in summary['level_distribution'].items():
                print(f"   Level {level}: {count} sections")
        
        # Print validation summary
        print_validation_summary(analysis, summary)
        
    except ImportError as e:
        print(f"⚠️  Validation module not available: {e}")
        print("   This is expected if running the demo standalone")

def demonstrate_file_generation():
    """Demonstrate file generation functionality"""
    
    print("📁 File Generation Demonstration")
    print("=" * 50)
    
    # Create sample data
    toc_entries, section_entries = create_sample_data()
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📂 Using temporary directory: {temp_dir}")
        
        try:
            # Import utility functions
            from parser.utils import write_jsonl
            
            # Generate TOC file
            toc_file = os.path.join(temp_dir, "usb_pd_toc.jsonl")
            write_jsonl(toc_entries, toc_file)
            print(f"✅ Generated TOC file: {toc_file}")
            
            # Generate sections file
            sections_file = os.path.join(temp_dir, "usb_pd_spec.jsonl")
            write_jsonl(section_entries, sections_file)
            print(f"✅ Generated sections file: {sections_file}")
            
            # Generate metadata file
            metadata = {
                "doc_title": "USB Power Delivery Specification Rev 3.0",
                "total_pages": 150,
                "toc_pages": [1, 2, 3],
                "sections_count": len(section_entries),
                "tables_count": 8,
                "figures_count": 15
            }
            metadata_file = os.path.join(temp_dir, "usb_pd_metadata.jsonl")
            write_jsonl([metadata], metadata_file)
            print(f"✅ Generated metadata file: {metadata_file}")
            
            # Show file sizes
            print(f"\n📊 File sizes:")
            for filename in [toc_file, sections_file, metadata_file]:
                size = os.path.getsize(filename)
                print(f"   {os.path.basename(filename)}: {size:,} bytes")
            
            # Show sample content from generated files
            print(f"\n📄 Sample content from generated files:")
            print("-" * 40)
            
            with open(toc_file, 'r') as f:
                first_line = f.readline().strip()
                data = json.loads(first_line)
                print(f"First TOC entry: {data['section_id']} - {data['title']}")
            
            with open(sections_file, 'r') as f:
                first_line = f.readline().strip()
                data = json.loads(first_line)
                content_preview = data['content'][:80] + "..." if len(data['content']) > 80 else data['content']
                print(f"First section: {data['section_id']} - {data['title']}")
                print(f"Content preview: {content_preview}")
            
        except ImportError as e:
            print(f"⚠️  Utility module not available: {e}")
            print("   This is expected if running the demo standalone")

def main():
    """Run the complete demo"""
    
    print("🚀 USB PD Parser - Interactive Demo")
    print("=" * 60)
    print("This demo showcases the parser functionality with sample data")
    print("No actual PDF files are required to run this demonstration")
    print("=" * 60)
    
    try:
        # Demonstrate JSONL output format
        demonstrate_jsonl_output()
        
        # Demonstrate validation functionality
        demonstrate_validation()
        
        # Demonstrate file generation
        demonstrate_file_generation()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("\n💡 To use with real PDFs:")
        print("   python scripts/parse_usb_pd.py path/to/your/document.pdf")
        print("\n💡 To run the test script:")
        print("   python scripts/test_parser.py")
        print("\n💡 To see usage examples:")
        print("   python examples/example_usage.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
