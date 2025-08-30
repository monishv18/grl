import React, { useState } from 'react';

export const UploadSection = (
  { onProcessComplete }:
  { onProcessComplete: (r: any) => void }
) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');

  const onFile = (f?: File) => {
    if (f) setSelectedFile(f);
  };

  const processFile = async () => {
    if (!selectedFile) return;
    setIsProcessing(true);
    setStatus('Uploading...');
    setProgress(10);

    const body = new FormData();
    body.append('pdf', selectedFile);
    body.append('samplePages', '3');

    try {
      const res = await fetch('http://localhost:4000/api/process', {
        method: 'POST',
        body
      });
      setStatus('Processing...');
      setProgress(60);
      const data = await res.json();
      setStatus('Done');
      setProgress(100);
      onProcessComplete?.(data);
    } catch (e: any) {
      setStatus(e?.message || 'Failed');
      setProgress(0);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <section className="p-4 border rounded-2xl">
      <h2 className="text-xl font-bold mb-2">Process Your PDF</h2>
      <input
        type="file"
        accept="application/pdf"
        onChange={e => onFile(e.target.files?.[0] || undefined)}
      />
      {selectedFile && !isProcessing && (
        <button
          onClick={processFile}
          className="mt-3 px-4 py-2 bg-black text-white rounded"
        >
          Process PDF
        </button>
      )}
      {isProcessing && (
        <div className="mt-3">
          <div className="w-full bg-gray-200 h-2 rounded">
            <div className="h-2 bg-black" style={{ width: progress + '%' }} />
          </div>
          <div className="text-sm mt-2">{status} — {progress}%</div>
        </div>
      )}
    </section>
  );
};