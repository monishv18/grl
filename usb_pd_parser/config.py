class Config:
    MAX_FILE_SIZE_MB = 80            # allow bigger PDFs
    TOC_SCAN_PAGES = 20              # scan more front pages for TOC
    OUTPUT_DIR = "output"
    VALIDATION_REPORT = "validation_report.xlsx"
    DOC_TITLE = "USB Power Delivery Specification"

    # New fallbacks
    FULL_DOC_TOC_FALLBACK = True     # scan entire doc if TOC incomplete
    MIN_TOC_COVERAGE_RATIO = 0.65    # if < 65% sections found, trigger fallback
