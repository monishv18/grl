# USB Power Delivery (USB PD) Specification Parser

A comprehensive Python system for parsing USB PD specification PDFs and converting them into structured, machine-readable JSONL formats. This system preserves the logical hierarchy, metadata, and content of technical specifications while providing robust validation and error reporting.

## 🚀 Features

- **Intelligent TOC Extraction**: Multi-pattern regex matching for various Table of Contents formats
- **Hierarchical Section Parsing**: Maintains section relationships and parent-child hierarchies
- **Content Extraction**: Extracts full section content with proper page boundaries
- **Comprehensive Validation**: Detailed comparison between TOC and parsed sections
- **Multiple Output Formats**: JSONL files for TOC, sections, and metadata
- **Excel Validation Reports**: Detailed analysis with multiple worksheets
- **Robust Error Handling**: Graceful handling of malformed PDFs and edge cases
- **Semantic Tagging**: Automatic generation of relevant tags for sections

## 📋 Requirements

- Python 3.7+
- PDF files (USB PD specifications or similar technical documents)

## 🛠️ Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd usb_pd_parser
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage

```bash
python scripts/parse_usb_pd.py path/to/your/document.pdf
```

### Advanced Usage

```bash
# Custom output directory
python scripts/parse_usb_pd.py document.pdf --output custom_output

# Custom document title
python scripts/parse_usb_pd.py document.pdf --doc-title "USB PD Spec v3.0"

# Adjust TOC scan pages
python scripts/parse_usb_pd.py document.pdf --toc-pages 15

# Verbose output for debugging
python scripts/parse_usb_pd.py document.pdf --verbose
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output directory | `output` |
| `--doc-title` | `-t` | Document title | `USB Power Delivery Specification` |
| `--toc-pages` | `-p` | Pages to scan for TOC | `12` |
| `--verbose` | `-v` | Verbose output | `False` |

## 📁 Output Files

The parser generates three main JSONL files and a validation report:

### 1. `usb_pd_toc.jsonl` - Table of Contents
Contains the hierarchical structure of the document:
```json
{"doc_title": "USB Power Delivery Specification", "section_id": "2.1.2", "title": "Power Delivery Contract Negotiation", "page": 53, "level": 3, "parent_id": "2.1", "full_path": "2.1.2 Power Delivery Contract Negotiation", "tags": ["contracts", "negotiation"]}
```

### 2. `usb_pd_spec.jsonl` - Full Sections
Contains all sections with their complete content:
```json
{"doc_title": "USB Power Delivery Specification", "section_id": "2.1.2", "title": "Power Delivery Contract Negotiation", "page": 53, "level": 3, "parent_id": "2.1", "full_path": "2.1.2 Power Delivery Contract Negotiation", "content": "Full section content here...", "tags": ["contracts", "negotiation"]}
```

### 3. `usb_pd_metadata.jsonl` - Document Metadata
Contains document-level information:
```json
{"doc_title": "USB Power Delivery Specification", "total_pages": 150, "toc_pages": [3, 4, 5], "sections_count": 45, "tables_count": 12, "figures_count": 8}
```

### 4. `validation_report.xlsx` - Validation Report
Multi-sheet Excel report with:
- **Validation_Report**: Detailed TOC vs parsed comparison
- **Summary_Statistics**: Overall statistics and metrics
- **Analysis_Details**: Gap analysis and order issues
- **Level_Distribution**: Section hierarchy distribution

## 🔧 How It Works

### 1. TOC Extraction
The parser scans the first few pages (configurable) looking for Table of Contents entries using multiple regex patterns:

- Standard format: `2.1.2 Power Delivery Contract Negotiation .......... 53`
- Format without dots: `2.1.2 Power Delivery Contract Negotiation 53`
- Chapter format: `Chapter 2 Overview 53`
- Section format: `Section 2.1 Introduction 53`

### 2. Section Content Extraction
For each TOC entry, the parser:
- Identifies the start page from the TOC
- Finds the end page by looking for the next section at the same or higher level
- Extracts all text content between these boundaries
- Maintains proper section hierarchy

### 3. Validation and Analysis
The system performs comprehensive validation:
- **Coverage Analysis**: TOC entries vs parsed sections
- **Order Validation**: Page number consistency
- **Gap Detection**: Missing section numbers
- **Content Analysis**: Text length and quality metrics

### 4. Semantic Tagging
Automatic tag generation based on section titles:
- `power_management`: Power, voltage, current-related
- `negotiation`: Contract, agreement, negotiation-related
- `communication`: Protocol, message, communication-related
- `state_machine`: State, machine, transition-related
- `hardware`: Cable, connector, plug-related
- `compatibility`: Revision, version, compatibility-related

## 🏗️ Architecture

```
usb_pd_parser/
├── parser/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Main parser logic
│   ├── schemas.py           # JSON schema definitions
│   ├── utils.py             # Utility functions and regex patterns
│   ├── validation.py        # Validation and reporting
│   └── config.py            # Configuration constants
├── scripts/
│   └── parse_usb_pd.py     # Main command-line interface
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
└── README.md                # This file
```

## 🔍 Configuration

Key configuration options in `parser/config.py`:

```python
class Config:
    MAX_FILE_SIZE_MB = 50          # Maximum PDF file size
    TOC_SCAN_PAGES = 12            # Pages to scan for TOC
    OUTPUT_DIR = "output"          # Default output directory
    VALIDATION_REPORT = "validation_report.xlsx"  # Report filename
    DOC_TITLE = "USB Power Delivery Specification"  # Default title
```

## 📊 Sample Output

### TOC Entry
```json
{
  "doc_title": "USB Power Delivery Specification Rev X",
  "section_id": "2.1.2",
  "title": "Power Delivery Contract Negotiation",
  "page": 53,
  "level": 3,
  "parent_id": "2.1",
  "full_path": "2.1.2 Power Delivery Contract Negotiation",
  "tags": ["contracts", "negotiation"]
}
```

### Section Entry
```json
{
  "doc_title": "USB Power Delivery Specification Rev X",
  "section_id": "2.1.2",
  "title": "Power Delivery Contract Negotiation",
  "page": 53,
  "level": 3,
  "parent_id": "2.1",
  "full_path": "2.1.2 Power Delivery Contract Negotiation",
  "content": "This section describes the Power Delivery contract negotiation process...",
  "tags": ["contracts", "negotiation"]
}
```

## 🚨 Troubleshooting

### Common Issues

1. **No TOC entries found**:
   - Increase `--toc-pages` parameter
   - Check if PDF has a standard Table of Contents format
   - Verify PDF is not image-based (use `--verbose` for debugging)

2. **Missing sections**:
   - Check PDF quality and text extraction
   - Verify section numbering is consistent
   - Review validation report for specific issues

3. **Content extraction issues**:
   - Ensure PDF has selectable text (not just images)
   - Check for password protection or restrictions

### Debug Mode

Use the `--verbose` flag for detailed error information:
```bash
python scripts/parse_usb_pd.py document.pdf --verbose
```

## 🤝 Contributing

This parser is designed to be extensible. Key areas for enhancement:

- **New TOC Formats**: Add regex patterns in `utils.py`
- **Content Processing**: Enhance text cleaning in `utils.py`
- **Validation Rules**: Add new checks in `validation.py`
- **Output Formats**: Support additional export formats

## 📝 License

This project is provided as-is for educational and development purposes.

## 📞 Support

For technical questions or issues:
- Review the validation report for specific problems
- Use `--verbose` mode for detailed debugging
- Check the generated JSONL files for data quality issues

---

**Note**: This parser is specifically designed for USB PD specifications but can be adapted for other technical documents with similar hierarchical structures.