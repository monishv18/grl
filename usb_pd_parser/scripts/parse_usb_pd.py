import sys
import os
import argparse
from pathlib import Path
from parser.core import USBPDParser
from parser.validation import (generate_validation_report, analyze_toc_vs_parsed, 
                              generate_summary_statistics, save_validation_report, 
                              print_validation_summary)
from parser.config import Config

def main():
    parser = argparse.ArgumentParser(
        description="Parse USB PD Specification PDF and generate structured JSONL output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/parse_usb_pd.py document.pdf
  python scripts/parse_usb_pd.py document.pdf --output custom_output
  python scripts/parse_usb_pd.py document.pdf --doc-title "USB PD Spec v3.0"
        """
    )
    
    parser.add_argument("pdf_path", help="Path to the USB PD specification PDF file")
    parser.add_argument("--output", "-o", default=Config.OUTPUT_DIR, 
                       help=f"Output directory (default: {Config.OUTPUT_DIR})")
    parser.add_argument("--doc-title", "-t", default=Config.DOC_TITLE,
                       help=f"Document title (default: {Config.DOC_TITLE})")
    parser.add_argument("--toc-pages", "-p", type=int, default=Config.TOC_SCAN_PAGES,
                       help=f"Number of pages to scan for TOC (default: {Config.TOC_SCAN_PAGES})")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"❌ Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"❌ Error: File must be a PDF: {pdf_path}")
        sys.exit(1)
    
    # Update config
    Config.OUTPUT_DIR = args.output
    Config.DOC_TITLE = args.doc_title
    Config.TOC_SCAN_PAGES = args.toc_pages
    
    print("🚀 USB PD Specification Parser")
    print("=" * 50)
    print(f"📄 Input: {pdf_path}")
    print(f"📁 Output: {Config.OUTPUT_DIR}")
    print(f"📋 Document Title: {Config.DOC_TITLE}")
    print(f"🔍 TOC Scan Pages: {Config.TOC_SCAN_PAGES}")
    print("=" * 50)
    
    try:
        # Initialize parser
        parser_instance = USBPDParser(str(pdf_path), Config.DOC_TITLE)
        
        # Run complete parsing workflow
        if not parser_instance.parse_complete():
            print("❌ Parsing failed!")
            sys.exit(1)
        
        # Generate validation report
        print("\n🔍 Generating validation report...")
        report_df = generate_validation_report(
            parser_instance.toc_entries, 
            parser_instance.section_entries,
            Config.OUTPUT_DIR
        )
        
        # Generate analysis and summary
        analysis = analyze_toc_vs_parsed(
            parser_instance.toc_entries, 
            parser_instance.section_entries
        )
        summary = generate_summary_statistics(
            parser_instance.toc_entries, 
            parser_instance.section_entries
        )
        
        # Save comprehensive validation report
        report_file = save_validation_report(
            report_df, analysis, summary, Config.OUTPUT_DIR
        )
        
        # Print validation summary
        print_validation_summary(analysis, summary)
        
        # Print file locations
        print(f"\n📁 Output Files:")
        print(f"   • TOC: {os.path.join(Config.OUTPUT_DIR, 'usb_pd_toc.jsonl')}")
        print(f"   • Sections: {os.path.join(Config.OUTPUT_DIR, 'usb_pd_spec.jsonl')}")
        print(f"   • Metadata: {os.path.join(Config.OUTPUT_DIR, 'usb_pd_metadata.jsonl')}")
        print(f"   • Validation Report: {report_file}")
        
        print("\n✅ Parsing completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Parsing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
