# USB PD Specification Parser

Parses the USB PD specification PDF into structured **JSONL** and an **Excel validation report**.

## Deliverables
- `usb_pd_toc.jsonl` – Table of Contents hierarchy
- `usb_pd_spec.jsonl` – Section content
- `usb_pd_metadata.jsonl` – Document metadata
- `validation_report.xlsx` – Coverage vs mismatches

## Install & Run
```bash
cd usb_pd_parser
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
pip install -r requirements.txt

python scripts/parse_usb_pd.py "D:\path\to\USB_PD.pdf" --output output --doc-title "USB PD Rev 3.2"
```

