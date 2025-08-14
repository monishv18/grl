import pandas as pd
from typing import List, Dict, Tuple
import os

def generate_validation_report(toc_entries: List[Dict], section_entries: List[Dict], 
                             output_dir: str = "output") -> pd.DataFrame:
    """Generate comprehensive validation report comparing TOC and parsed sections"""
    
    # Create detailed analysis
    analysis = analyze_toc_vs_parsed(toc_entries, section_entries)
    
    # Generate summary statistics
    summary_stats = generate_summary_statistics(toc_entries, section_entries)
    
    # Create detailed report
    report_data = []
    
    # TOC vs Parsed comparison
    for toc_entry in toc_entries:
        section_id = toc_entry["section_id"]
        parsed_entry = next((s for s in section_entries if s["section_id"] == section_id), None)
        
        report_data.append({
            "section_id": section_id,
            "title": toc_entry["title"],
            "toc_page": toc_entry["page"],
            "in_toc": "YES",
            "in_parsed": "YES" if parsed_entry else "NO",
            "parsed_page": parsed_entry["page"] if parsed_entry else "N/A",
            "status": "OK" if parsed_entry else "MISSING",
            "level": toc_entry["level"],
            "parent_id": toc_entry["parent_id"],
            "content_length": len(parsed_entry["content"]) if parsed_entry else 0,
            "tags": ", ".join(toc_entry.get("tags", []))
        })
    
    # Extra parsed sections (not in TOC)
    for section_entry in section_entries:
        if not any(t["section_id"] == section_entry["section_id"] for t in toc_entries):
            report_data.append({
                "section_id": section_entry["section_id"],
                "title": section_entry["title"],
                "toc_page": "N/A",
                "in_toc": "NO",
                "in_parsed": "YES",
                "parsed_page": section_entry["page"],
                "status": "EXTRA",
                "level": section_entry["level"],
                "parent_id": section_entry["parent_id"],
                "content_length": len(section_entry.get("content", "")),
                "tags": ", ".join(section_entry.get("tags", []))
            })
    
    # Sort by section_id for logical order
    report_data.sort(key=lambda x: [int(n) for n in x["section_id"].split(".") if n.isdigit()])
    
    return pd.DataFrame(report_data)

def analyze_toc_vs_parsed(toc_entries: List[Dict], section_entries: List[Dict]) -> Dict:
    """Analyze differences between TOC and parsed sections"""
    
    toc_ids = {e["section_id"] for e in toc_entries}
    parsed_ids = {e["section_id"] for e in section_entries}
    
    missing_from_parsed = toc_ids - parsed_ids
    extra_in_parsed = parsed_ids - toc_ids
    common_ids = toc_ids & parsed_ids
    
    # Check for order mismatches
    order_issues = []
    for i, toc_entry in enumerate(toc_entries):
        if toc_entry["section_id"] in common_ids:
            parsed_entry = next(s for s in section_entries if s["section_id"] == toc_entry["section_id"])
            if toc_entry["page"] != parsed_entry["page"]:
                order_issues.append({
                    "section_id": toc_entry["section_id"],
                    "toc_page": toc_entry["page"],
                    "parsed_page": parsed_entry["page"],
                    "difference": abs(toc_entry["page"] - parsed_entry["page"])
                })
    
    # Check for gaps in section numbering
    gaps = find_section_gaps(toc_entries)
    
    return {
        "total_toc_entries": len(toc_entries),
        "total_parsed_entries": len(section_entries),
        "missing_from_parsed": list(missing_from_parsed),
        "extra_in_parsed": list(extra_in_parsed),
        "common_entries": len(common_ids),
        "order_issues": order_issues,
        "gaps": gaps,
        "coverage_percentage": (len(common_ids) / len(toc_ids)) * 100 if toc_ids else 0
    }

def find_section_gaps(toc_entries: List[Dict]) -> List[Dict]:
    """Find gaps in section numbering"""
    gaps = []
    
    # Group by level
    levels = {}
    for entry in toc_entries:
        level = entry["level"]
        if level not in levels:
            levels[level] = []
        levels[level].append(entry)
    
    # Check each level for gaps
    for level, entries in levels.items():
        entries.sort(key=lambda x: [int(n) for n in x["section_id"].split(".")])
        
        for i in range(len(entries) - 1):
            current_id = entries[i]["section_id"]
            next_id = entries[i + 1]["section_id"]
            
            # Check if there's a gap
            if has_gap(current_id, next_id):
                gaps.append({
                    "level": level,
                    "before_section": current_id,
                    "after_section": next_id,
                    "gap_description": f"Missing sections between {current_id} and {next_id}"
                })
    
    return gaps

def has_gap(current_id: str, next_id: str) -> bool:
    """Check if there's a gap between two section IDs"""
    current_parts = [int(n) for n in current_id.split(".")]
    next_parts = [int(n) for n in next_id.split(".")]
    
    # Find common prefix
    common_len = 0
    for i in range(min(len(current_parts), len(next_parts))):
        if current_parts[i] == next_parts[i]:
            common_len += 1
        else:
            break
    
    # If same level, check for gaps
    if len(current_parts) == len(next_parts):
        if common_len == len(current_parts) - 1:
            # Check if next number is consecutive
            if next_parts[-1] != current_parts[-1] + 1:
                return True
    
    return False

def generate_summary_statistics(toc_entries: List[Dict], section_entries: List[Dict]) -> Dict:
    """Generate summary statistics for the validation report"""
    
    # Level distribution
    level_distribution = {}
    for entry in toc_entries:
        level = entry["level"]
        level_distribution[level] = level_distribution.get(level, 0) + 1
    
    # Page range analysis
    toc_pages = [e["page"] for e in toc_entries]
    parsed_pages = [e["page"] for e in section_entries]
    
    # Content analysis
    content_lengths = [len(e.get("content", "")) for e in section_entries]
    
    return {
        "level_distribution": level_distribution,
        "toc_page_range": (min(toc_pages), max(toc_pages)) if toc_pages else (0, 0),
        "parsed_page_range": (min(parsed_pages), max(parsed_pages)) if parsed_pages else (0, 0),
        "avg_content_length": sum(content_lengths) / len(content_lengths) if content_lengths else 0,
        "total_content_length": sum(content_lengths),
        "sections_with_content": len([e for e in section_entries if e.get("content")])
    }

def save_validation_report(report_df: pd.DataFrame, analysis: Dict, summary: Dict, 
                          output_dir: str = "output") -> str:
    """Save comprehensive validation report to Excel with multiple sheets"""
    
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, "validation_report.xlsx")
    
    with pd.ExcelWriter(report_file, engine='openpyxl') as writer:
        # Main validation report
        report_df.to_excel(writer, sheet_name='Validation_Report', index=False)
        
        # Summary statistics
        summary_df = pd.DataFrame([summary])
        summary_df.to_excel(writer, sheet_name='Summary_Statistics', index=False)
        
        # Analysis details
        analysis_df = pd.DataFrame([analysis])
        analysis_df.to_excel(writer, sheet_name='Analysis_Details', index=False)
        
        # Level distribution
        if 'level_distribution' in summary:
            level_df = pd.DataFrame(list(summary['level_distribution'].items()), 
                                  columns=['Level', 'Count'])
            level_df.to_excel(writer, sheet_name='Level_Distribution', index=False)
    
    print(f"✅ Validation report saved to: {report_file}")
    return report_file

def print_validation_summary(analysis: Dict, summary: Dict):
    """Print a summary of validation results to console"""
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    print(f"📊 Coverage: {analysis['coverage_percentage']:.1f}%")
    print(f"📋 TOC Entries: {analysis['total_toc_entries']}")
    print(f"📄 Parsed Entries: {analysis['total_parsed_entries']}")
    print(f"❌ Missing: {len(analysis['missing_from_parsed'])}")
    print(f"➕ Extra: {len(analysis['extra_in_parsed'])}")
    print(f"⚠️  Order Issues: {len(analysis['order_issues'])}")
    print(f"🕳️  Gaps: {len(analysis['gaps'])}")
    
    if analysis['missing_from_parsed']:
        print(f"\n❌ Missing sections: {', '.join(sorted(analysis['missing_from_parsed']))}")
    
    if analysis['order_issues']:
        print(f"\n⚠️  Page order issues found in {len(analysis['order_issues'])} sections")
    
    print("="*60)
