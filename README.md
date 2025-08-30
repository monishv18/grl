# GRL PDF Processor — Working Build

This package includes a minimal **backend (Express + TypeScript)** and a
**frontend (React + Vite)** that together process **very large PDFs** and
produce assignment deliverables.

## What it does

- Accepts a PDF upload and parses metadata and text with `pdf-parse`.
- Returns total pages, size, and a small text sample.
- Writes one **JSONL** record per processed document to `backend/outputs`.
- Writes a detailed JSON report with stats and detected sections.
- Frontend shows a simple upload UI and progress.

## Deliverables produced

- `*.jsonl` — lines of `{ "doc_title": ..., "total_pages": ... }`
- `*-report.json` — structured results including `sections[]` and `stats`.

## Install & run

### Backend
```bash
cd backend
npm i
cp .env.example .env # optional
npm run dev          # starts http://localhost:4000
```

### Frontend
```bash
cd frontend
npm i
npm run dev          # starts Vite dev server
```

## API

`POST /api/process` — multipart form with field **pdf** and optional
**samplePages** (default 3). Returns:
```json
{
  "ok": true,
  "jsonl": "usb_pd-1700000000000.jsonl",
  "report": "usb_pd-1700000000000-report.json",
  "meta": { "totalPages": 123, "durationMs": 456, "samplePages": 3 }
}
```

## JSON Schemas

Basic schema for a Table-of-Contents section is in
`backend/schemas/toc_section.schema.json`.

## Notes

- Lines are wrapped to ~79 chars to satisfy linters.
- Keep string concatenation out of loops; use array joins when needed.
- Add more tests in `backend/tests` as you extend functionality.