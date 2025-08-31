import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import FileUploader from "@/components/ui/file-uploader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { FileText, Zap, Shield, Clock } from "lucide-react";

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        variant: "destructive",
        title: "No file selected",
        description: "Please select a PDF file to process.",
      });
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      // Mock API call - replace with actual backend endpoint
      const response = await fetch("/api/process-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process PDF");
      }

      const result = await response.json();
      
      // Store results for the results page
      localStorage.setItem("processingResult", JSON.stringify({
        data: result,
        fileName: selectedFile.name,
        timestamp: new Date().toISOString(),
      }));

      toast({
        variant: "default",
        title: "PDF processed successfully",
        description: "Your document has been analyzed. Redirecting to results...",
      });

      // Redirect to results page
      setTimeout(() => {
        navigate("/results");
      }, 1000);

    } catch (error) {
      console.error("Upload error:", error);
      toast({
        variant: "destructive",
        title: "Processing failed",
        description: "There was an error processing your PDF. Please try again.",
      });
    } finally {
      setIsUploading(false);
    }
  };

  const features = [
    {
      icon: <Zap className="w-5 h-5" />,
      title: "Fast Processing",
      description: "Analyze your PDFs in seconds with our optimized algorithms"
    },
    {
      icon: <Shield className="w-5 h-5" />,
      title: "Secure & Private",
      description: "Your documents are processed securely and never stored"
    },
    {
      icon: <Clock className="w-5 h-5" />,
      title: "Real-time Results",
      description: "Get instant feedback and detailed analysis reports"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12 fade-in">
          <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-4">
            PDF Document Processor
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Upload your PDF documents and get instant analysis, validation, and structured data extraction.
          </p>
        </div>

        {/* Upload Section */}
        <Card className="mb-8 slide-up">
          <CardHeader>
            <CardTitle className="text-center">Upload Your PDF</CardTitle>
          </CardHeader>
          <CardContent>
            <FileUploader
              onFileSelect={handleFileSelect}
              onUpload={handleUpload}
              isUploading={isUploading}
            />
          </CardContent>
        </Card>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {features.map((feature, index) => (
            <Card key={index} className="text-center slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
              <CardContent className="pt-6">
                <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4 text-primary">
                  {feature.icon}
                </div>
                <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Sample Results Link */}
        <Card className="slide-up">
          <CardContent className="p-6 text-center">
            <h3 className="font-semibold text-foreground mb-2">Want to see a sample?</h3>
            <p className="text-muted-foreground mb-4">
              Check out sample processing results to understand what our tool can do.
            </p>
            <Button 
              variant="outline" 
              onClick={() => {
                // Mock sample data
                const sampleData = {
                  overview: {
                    totalPages: 5,
                    documentType: "Business Report",
                    language: "English",
                    fileSize: "2.3 MB"
                  },
                  extractedText: {
                    headings: ["Executive Summary", "Market Analysis", "Financial Projections"],
                    keyPoints: [
                      "Revenue increased by 25% year-over-year",
                      "New market opportunities identified in Asia",
                      "Product development costs decreased by 15%"
                    ]
                  },
                  validation: {
                    formatValid: true,
                    contentReadable: true,
                    noCorruption: true,
                    score: 95
                  },
                  metadata: {
                    creator: "Adobe Acrobat",
                    creationDate: "2024-01-15",
                    title: "Q4 Business Report 2023"
                  }
                };

                localStorage.setItem("processingResult", JSON.stringify({
                  data: sampleData,
                  fileName: "sample-business-report.pdf",
                  timestamp: new Date().toISOString(),
                }));

                navigate("/results");
              }}
            >
              View Sample Results
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Upload;