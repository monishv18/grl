import re

SECTION_HEADER_PATTERNS = [
    r'^(\d+(?:\.\d+)*)\s+([A-Za-z].*?)\s*$',               # "2.1.3 Title"
    r'^(Chapter\s+\d+)\s+(.+)$',                            # "Chapter 2 Overview"
    r'^(Section\s+\d+(?:\.\d+)*)\s+(.+)$'                   # "Section 2.1 Intro"
]

def find_section_headers_in_text(line: str):
    line = line.strip()
    for pat in SECTION_HEADER_PATTERNS:
        m = re.match(pat, line, re.IGNORECASE)
        if m:
            raw = m.group(1)
            title = m.group(2)
            if raw.lower().startswith("chapter") or raw.lower().startswith("section"):
                nums = re.findall(r'\d+(?:\.\d+)*', raw)
                if nums:
                    return nums[0], title
            return raw, title
    return None
