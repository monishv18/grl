import os, argparse
from parser.core import USBPDParser
from parser.utils import write_jsonl
from parser.validation import generate_validation_report, save_validation_report, print_validation_summary

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_path")
    ap.add_argument("--output", default="output")
    ap.add_argument("--doc-title", default="USB PD Specification")
    args = ap.parse_args()

    parser = USBPDParser(args.pdf_path, doc_title=args.doc_title)
    parser.parse()

    os.makedirs(args.output, exist_ok=True)
    toc_path = os.path.join(args.output, "usb_pd_toc.jsonl")
    spec_path = os.path.join(args.output, "usb_pd_spec.jsonl")
    meta_path = os.path.join(args.output, "usb_pd_metadata.jsonl")

    write_jsonl(toc_path, parser.toc_entries)
    write_jsonl(spec_path, parser.section_entries)
    write_jsonl(meta_path, [parser.metadata])

    try:
        df = generate_validation_report(parser.toc_entries, parser.section_entries, output_dir=args.output)
        save_validation_report(df, os.path.join(args.output, "validation_report.xlsx"))
        print_validation_summary(df)
    except Exception as e:
        print('Validation report generation failed:', e)

    print("\n✅ Generated files:")
    print(toc_path, spec_path, meta_path, os.path.join(args.output,"validation_report.xlsx"), sep="\n")
