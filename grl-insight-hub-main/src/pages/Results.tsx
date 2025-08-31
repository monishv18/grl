import React, { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';

type Summary = {
  coveragePercent: number;
  tocCount: number;
  parsedCount: number;
  missingCount: number;
};

export default function ResultsPage() {
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("processingSummary");
    if (saved) setSummary(JSON.parse(saved));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Processing Results</h1>
      {summary ? (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card><CardContent className="p-4"><div className="text-sm">Coverage</div><div className="text-2xl font-bold">{summary.coveragePercent.toFixed(1)}%</div></CardContent></Card>
          <Card><CardContent className="p-4"><div className="text-sm">TOC Sections</div><div className="text-2xl font-bold">{summary.tocCount}</div></CardContent></Card>
          <Card><CardContent className="p-4"><div className="text-sm">Parsed Sections</div><div className="text-2xl font-bold">{summary.parsedCount}</div></CardContent></Card>
          <Card><CardContent className="p-4"><div className="text-sm">Missing</div><div className="text-2xl font-bold">{summary.missingCount}</div></CardContent></Card>
        </div>
      ) : (
        <div className="text-muted-foreground">No summary found.</div>
      )}
    </div>
  );
}
