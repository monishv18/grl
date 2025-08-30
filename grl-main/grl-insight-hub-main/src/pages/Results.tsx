import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ResultDisplay from "@/components/ui/result-display";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowLeft, Download, RotateCcw, AlertCircle } from "lucide-react";

interface ProcessingResult {
  data: any;
  fileName: string;
  timestamp: string;
}

const Results = () => {
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Load results from localStorage
    const storedResult = localStorage.getItem("processingResult");
    if (storedResult) {
      try {
        const parsedResult = JSON.parse(storedResult);
        setResult(parsedResult);
      } catch (error) {
        console.error("Error parsing stored result:", error);
      }
    }
  }, []);

  const handleClearResults = () => {
    localStorage.removeItem("processingResult");
    setResult(null);
    navigate("/");
  };

  const handleDownloadResults = () => {
    if (!result) return;

    const dataStr = JSON.stringify(result.data, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement("a");
    link.href = url;
    link.download = `${result.fileName.replace('.pdf', '')}-analysis.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  if (!result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <Card className="text-center">
            <CardContent className="py-12">
              <AlertCircle className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h2 className="text-2xl font-semibold text-foreground mb-2">
                No Results Found
              </h2>
              <p className="text-muted-foreground mb-6">
                It looks like you haven't processed any documents yet. Upload a PDF to get started.
              </p>
              <div className="space-x-4">
                <Button onClick={() => navigate("/")}>
                  Upload New Document
                </Button>
                <Button variant="outline" onClick={() => navigate("/about")}>
                  Learn More
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8 fade-in">
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate("/")}
              className="flex items-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Upload</span>
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Processing Results</h1>
              <p className="text-sm text-muted-foreground">
                Processed on {formatTimestamp(result.timestamp)}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleDownloadResults}
              className="flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Download</span>
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearResults}
              className="flex items-center space-x-2"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Clear Results</span>
            </Button>
          </div>
        </div>

        {/* Results Display */}
        <ResultDisplay 
          data={result.data} 
          fileName={result.fileName}
          className="mb-8"
        />

        {/* Actions */}
        <Card className="slide-up">
          <CardContent className="p-6 text-center">
            <h3 className="font-semibold text-foreground mb-2">Ready to process another document?</h3>
            <p className="text-muted-foreground mb-4">
              Upload a new PDF to analyze more documents or compare results.
            </p>
            <Button onClick={() => navigate("/")}>
              Process New Document
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Results;