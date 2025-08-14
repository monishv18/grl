import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { 
  FileText, 
  Zap, 
  Shield, 
  Clock, 
  CheckCircle, 
  Code,
  Database,
  Cpu
} from "lucide-react";

const About = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <FileText className="w-6 h-6" />,
      title: "PDF Analysis",
      description: "Extract text, metadata, and structural information from PDF documents with high accuracy."
    },
    {
      icon: <CheckCircle className="w-6 h-6" />,
      title: "Content Validation",
      description: "Verify document integrity, readability, and format compliance automatically."
    },
    {
      icon: <Database className="w-6 h-6" />,
      title: "Data Extraction",
      description: "Intelligently parse and structure data from forms, tables, and text content."
    },
    {
      icon: <Cpu className="w-6 h-6" />,
      title: "Smart Processing",
      description: "Advanced algorithms for document classification and content understanding."
    }
  ];

  const benefits = [
    {
      icon: <Zap className="w-5 h-5" />,
      title: "Lightning Fast",
      description: "Process documents in seconds, not minutes"
    },
    {
      icon: <Shield className="w-5 h-5" />,
      title: "Secure Processing",
      description: "Your documents are processed securely and never stored"
    },
    {
      icon: <Clock className="w-5 h-5" />,
      title: "Real-time Results",
      description: "Get instant feedback and detailed analysis"
    },
    {
      icon: <Code className="w-5 h-5" />,
      title: "API Integration",
      description: "Easy integration with your existing workflow"
    }
  ];

  const useCases = [
    "Document compliance checking",
    "Automated data entry from forms",
    "Content extraction for archival",
    "Document quality assessment",
    "Batch document processing",
    "Legal document analysis"
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
            About PDF Processor
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A powerful tool for analyzing, validating, and extracting data from PDF documents 
            with advanced processing capabilities and real-time results.
          </p>
        </div>

        {/* Main Features */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-foreground mb-6 text-center">Core Features</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
                      {feature.icon}
                    </div>
                    <span>{feature.title}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Benefits */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-foreground mb-6 text-center">Why Choose Our Tool?</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {benefits.map((benefit, index) => (
              <Card key={index} className="slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-accent/10 rounded-lg flex items-center justify-center text-accent">
                      {benefit.icon}
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{benefit.title}</h3>
                      <p className="text-sm text-muted-foreground">{benefit.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Use Cases */}
        <div className="mb-12">
          <Card className="slide-up">
            <CardHeader>
              <CardTitle className="text-center">Common Use Cases</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-3">
                {useCases.map((useCase, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-success flex-shrink-0" />
                    <span className="text-foreground">{useCase}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Technical Info */}
        <div className="mb-12">
          <Card className="slide-up">
            <CardHeader>
              <CardTitle>Technical Specifications</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Supported Formats</h4>
                  <ul className="text-muted-foreground space-y-1">
                    <li>• PDF (all versions)</li>
                    <li>• Password-protected PDFs</li>
                    <li>• Scanned documents (OCR)</li>
                    <li>• Multi-page documents</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Processing Limits</h4>
                  <ul className="text-muted-foreground space-y-1">
                    <li>• Max file size: 10MB</li>
                    <li>• Max pages: 100 pages</li>
                    <li>• Processing time: ~5-30 seconds</li>
                    <li>• Concurrent uploads: 10</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* CTA */}
        <Card className="slide-up">
          <CardContent className="p-8 text-center">
            <h3 className="text-2xl font-bold text-foreground mb-4">Ready to Get Started?</h3>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Upload your first PDF document and experience the power of automated document processing.
            </p>
            <div className="space-x-4">
              <Button 
                size="lg"
                onClick={() => navigate("/")}
              >
                Start Processing
              </Button>
              <Button 
                variant="outline" 
                size="lg"
                onClick={() => navigate("/results")}
              >
                View Sample Results
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default About;