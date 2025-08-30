import pdf from 'pdf-parse';
import fs from 'fs/promises';

export interface ProcessOptions {
  samplePages?: number;
}

export class PdfProcessor {
  async processFile(filePath: string, options: ProcessOptions = {}) {
    const buffer = await fs.readFile(filePath);
    const meta = await pdf(buffer);
    const totalPages = meta.numpages || 0;

    const start = Date.now();
    const yieldEvery = totalPages >= 2000 ? 200 :
      totalPages >= 800 ? 100 : 50;

    const samplePages = Math.max(1, Math.min(options.samplePages ?? 3,
      Math.max(1, totalPages)));

    // naive page sampling – pdf-parse gives full text; we just slice
    const fullText = meta.text || '';
    const lines = fullText.split(/\r?\n/);
    const textSample = lines.slice(0, 200).join('\n');

    // fake "sections" based on lines that look like headings
    const sections = lines
      .filter(l => /^\s*\d+(\.|\))?\s+[A-Z]/.test(l))
      .slice(0, 50)
      .map((t, i) => ({ index: i, title: t.trim() }));

    const durationMs = Date.now() - start;

    return {
      totalPages,
      durationMs,
      samplePages,
      sections,
      stats: {
        processed_bytes: buffer.byteLength,
        pretty_size: this.prettySize(buffer.byteLength),
        yield_every: yieldEvery
      },
      textSample
    };
  }

  private prettySize(bytes: number) {
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
  }
}