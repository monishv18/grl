#!/usr/bin/env python3
"""
Enhanced script to find the Table of Contents in a PDF
"""

import pdfplumber
import sys
import re

def find_toc_pages(pdf_path, max_pages_to_scan=1500):
    """Scan PDF to find potential TOC pages with better detection"""
    
    print(f"🔍 Scanning PDF: {pdf_path}")
    print("=" * 60)
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"📄 Total pages: {total_pages}")
        print(f"🔍 Scanning first {max_pages_to_scan} pages for TOC...")
        print()
        
        # Look for actual TOC content, not just revision history
        toc_indicators = [
            "table of contents", "contents", "toc", "index"
        ]
        
        # Look for chapter/section patterns
        chapter_patterns = [
            r'\b\d+\s+\w+',  # "1 Introduction", "2 Overview"
            r'\b\d+\.\d+\s+\w+',  # "2.1 Basics", "3.2 Advanced"
            r'\b\d+\.\d+\.\d+\s+\w+',  # "2.1.1 Details"
            r'chapter\s+\d+',  # "Chapter 1", "Chapter 2"
            r'section\s+\d+',  # "Section 1", "Section 2"
        ]
        
        potential_toc_pages = []
        chapter_pages = []
        
        for page_num in range(min(max_pages_to_scan, total_pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if not text:
                continue
                
            text_lower = text.lower()
            
            # Check for TOC indicators
            toc_score = 0
            for indicator in toc_indicators:
                if indicator in text_lower:
                    toc_score += 3  # High weight for TOC indicators
            
            # Check for chapter/section patterns
            chapter_score = 0
            for pattern in chapter_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    chapter_score += len(matches) * 0.5
            
            # Check for page numbers in TOC format (like ".......... 53")
            page_number_pattern = r'\.+\s*\d+$'
            page_numbers = re.findall(page_number_pattern, text, re.MULTILINE)
            if page_numbers:
                chapter_score += len(page_numbers) * 0.3
            
            # Check for numbered lists that look like TOC
            numbered_lines = re.findall(r'^\s*\d+(?:\.\d+)*\s+', text, re.MULTILINE)
            if numbered_lines:
                chapter_score += len(numbered_lines) * 0.2
            
            # Calculate total score
            total_score = toc_score + chapter_score
            
            # Show detailed analysis for pages with content
            if total_score > 0:
                print(f"📄 Page {page_num + 1}: Score {total_score:.1f} (TOC: {toc_score}, Chapters: {chapter_score:.1f})")
                print(f"   Preview: {text[:150]}...")
                
                if total_score > 3:  # High likelihood of TOC
                    potential_toc_pages.append((page_num + 1, total_score, text[:300]))
                    print(f"   ✅ HIGH TOC PROBABILITY")
                elif total_score > 1.5:  # Medium likelihood
                    chapter_pages.append((page_num + 1, total_score, text[:200]))
                    print(f"   🔍 Potential chapter/section content")
                print()
        
        print("=" * 60)
        
        # Show results
        if potential_toc_pages:
            print(f"✅ Found {len(potential_toc_pages)} high-probability TOC pages:")
            for page_num, score, preview in potential_toc_pages:
                print(f"   📋 Page {page_num} (score: {score:.1f})")
            print()
        
        if chapter_pages:
            print(f"🔍 Found {len(chapter_pages)} pages with chapter/section content:")
            for page_num, score, preview in chapter_pages[:10]:  # Show first 10
                print(f"   📄 Page {page_num} (score: {score:.1f})")
            if len(chapter_pages) > 10:
                print(f"   ... and {len(chapter_pages) - 10} more")
            print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        if potential_toc_pages:
            best_page = max(potential_toc_pages, key=lambda x: x[1])
            print(f"   • Use --toc-pages {best_page[0]} for best TOC extraction")
        else:
            print("   • Try scanning more pages with --toc-pages 1500")
            print("   • The TOC might be scattered across multiple pages")
        
        print("   • Run: py scripts/parse_usb_pd.py \"your_pdf.pdf\" --toc-pages <page_number>")

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_toc.py <path_to_pdf> [max_pages_to_scan]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    
    try:
        find_toc_pages(pdf_path, max_pages)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
