import express from 'express';
import cors from 'cors';
import multer from 'multer';
import fs from 'fs/promises';
import path from 'path';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { PdfProcessor } from './services/PdfProcessor.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: path.join(__dirname, '../../uploads') });

const processor = new PdfProcessor();

app.post('/api/process', upload.single('pdf'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }
    const opts = {
      samplePages: Number(req.body?.samplePages || 3)
    };
    const result = await processor.processFile(req.file.path, opts);

    const outDir = path.join(__dirname, '../../outputs');
    await fs.mkdir(outDir, { recursive: true });
    const stamp = Date.now();
    const base = path.parse(req.file.originalname).name;
    const jsonlPath = path.join(outDir, `${base}-${stamp}.jsonl`);
    const reportPath = path.join(outDir, `${base}-${stamp}-report.json`);

    // Write JSONL with one record for the document
    const record = {
      doc_title: base,
      total_pages: result.totalPages,
      sample_text_len: result.textSample.length,
      sample_pages: result.samplePages,
      sections_detected: result.sections.length
    };
    await fs.writeFile(jsonlPath, JSON.stringify(record) + '\n', 'utf8');
    await fs.writeFile(reportPath, JSON.stringify(result, null, 2), 'utf8');

    // Clean temp upload
    await fs.unlink(req.file.path).catch(() => {});

    return res.json({
      ok: true,
      jsonl: path.basename(jsonlPath),
      report: path.basename(reportPath),
      meta: result
    });
  } catch (err: any) {
    if (req.file?.path) await fs.unlink(req.file.path).catch(() => {});
    console.error(err);
    return res.status(500).json({
      error: err?.message || 'Processing failed'
    });
  }
});

app.get('/health', (_req, res) => {
  res.json({ ok: true });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend listening on http://localhost:${PORT}`);
});