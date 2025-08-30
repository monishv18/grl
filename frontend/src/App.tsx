import React, { useState } from 'react';
import { UploadSection } from './components/UploadSection';

export default function App() {
  const [result, setResult] = useState<any | null>(null);
  return (
    <div className="min-h-screen p-6 bg-gray-50">
      <div className="max-w-3xl mx-auto">
        <UploadSection onProcessComplete={setResult} />
        {result && (
          <pre className="mt-6 bg-white p-4 rounded-lg shadow text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
