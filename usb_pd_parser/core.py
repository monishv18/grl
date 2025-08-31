# core.py - modified USBPDParser additions (merge into your existing parser if needed)
from .utils import extract_toc_entry, write_jsonl, extract_section_content, find_section_headers_in_text
from .config import Config

class USBPDParser:
    def __init__(self, pdf_path, doc_title=None):
        self.pdf_path = pdf_path
        self.doc_title = doc_title or Config.DOC_TITLE
        self.toc_entries = []
        self.section_entries = []
        self.metadata = {}

    def _compute_parent_id(self, section_id: str):
        return ".".join(section_id.split(".")[:-1]) or None

    def _level_from_id(self, section_id: str) -> int:
        return len(section_id.split("."))

    def _toc_is_incomplete(self) -> bool:
        return (not self.toc_entries) or len(self.toc_entries) < 10

    def _scan_front_matter_for_toc(self, pdf):
        entries = []
        for i in range(min(Config.TOC_SCAN_PAGES, len(pdf.pages))):
            text = (pdf.pages[i].extract_text() or "")
            for line in text.splitlines():
                try:
                    e = extract_toc_entry(line, self.doc_title)
                except Exception:
                    e = None
                if e:
                    entries.append(e)
        return entries

    def _fallback_scan_full_doc_for_toc(self, pdf):
        seen, entries = set(), []
        for pageno in range(len(pdf.pages)):
            text = (pdf.pages[pageno].extract_text() or "")
            for line in text.splitlines():
                res = find_section_headers_in_text(line)
                if not res: continue
                sid, title = res
                if sid in seen: continue
                seen.add(sid)
                entries.append({
                    "doc_title": self.doc_title,
                    "section_id": sid,
                    "title": title.strip().rstrip("."),
                    "page": pageno + 1,
                    "level": self._level_from_id(sid),
                    "parent_id": self._compute_parent_id(sid),
                    "full_path": f"{sid} {title}".strip(),
                    "tags": []
                })
        # sort by numeric dotted key
        def dotted_key(s):
            parts = s.split(".")
            out = []
            for p in parts:
                try:
                    out.append(int(p))
                except:
                    out.append(p)
            return out
        entries.sort(key=lambda e: dotted_key(e["section_id"]))
        return entries

    def _build_toc(self, pdf):
        entries = self._scan_front_matter_for_toc(pdf)
        if Config.FULL_DOC_TOC_FALLBACK and self._toc_is_incomplete():
            fb = self._fallback_scan_full_doc_for_toc(pdf)
            if len(fb) > len(entries):
                entries = fb
        return entries

    def _find_section_end_page(self, pdf, current_section):
        curr_id, curr_level, curr_page = current_section["section_id"], current_section["level"], current_section["page"]
        def dotted_key(s): return [int(x) for x in s.split(".") if x.isdigit()]
        ordered = sorted(self.toc_entries, key=lambda e: dotted_key(e["section_id"]))
        next_page = None
        hit = False
        for e in ordered:
            if e["section_id"] == curr_id:
                hit = True
                continue
            if not hit:
                continue
            if e["level"] <= curr_level:
                next_page = e["page"]
                break
        return len(pdf.pages) if next_page is None else max(curr_page, next_page - 1)

    def parse(self):
        import pdfplumber, os
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(self.pdf_path)
        with pdfplumber.open(self.pdf_path) as pdf:
            self.toc_entries = self._build_toc(pdf)
            self.section_entries = []
            for e in self.toc_entries:
                start, end = e["page"], self._find_section_end_page(pdf, e)
                content = ""
                try:
                    content = extract_section_content(pdf, start, end, e["title"])
                except Exception:
                    content = ""
                self.section_entries.append({**e, "content": content or ""})
            # minimal metadata
            self.metadata = {
                "doc_title": self.doc_title,
                "total_pages": len(pdf.pages),
                "toc_count": len(self.toc_entries),
                "parsed_count": len(self.section_entries)
            }
