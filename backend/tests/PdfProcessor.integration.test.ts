import fs from 'fs';
import path from 'path';
import { PdfProcessor } from '../src/services/PdfProcessor';

const dataDir = path.resolve(__dirname, './data');

describe('PdfProcessor Integration Tests (real PDFs)', () => {
  const datasets = [
    {
      name: 'USB PD R3.2 V1.1 (2024)',
      file: path.join(dataDir, 'USB_PD_R3_2 V1.1 2024-10.pdf'),
      expectedText: 'Revision 3.2, Version 1.1',
      minPages: 200,
    },
    {
      name: 'USB PD R2.0 V1.3 (2017)',
      file: path.join(dataDir, 'USB_PD_R2_0 V1.3 - 20170112.pdf'),
      expectedText: 'Revision 2.0, Version 1.3',
      minPages: 50,
    },
  ];

  datasets.forEach((dataset) => {
    const exists = fs.existsSync(dataset.file);
    const testFn = exists ? it : it.skip;

    testFn(`should process ${dataset.name} and detect expected revision`, async () => {
      const processor = new PdfProcessor();
      const report = await processor.processFile(dataset.file, { samplePages: 20 });

      expect(report.totalPages).toBeGreaterThan(dataset.minPages);
      expect(report.validationStatus).toBe('success');
      expect(report.fileSize).toMatch(/MB$/);
      expect(report.textSample).toBeDefined();
      expect(report.textSample).toContain(dataset.expectedText);
    });
  });
});
