import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";
import { Upload, File, X, CheckCircle } from "lucide-react";
import { Button } from "./button";

interface FileUploaderProps {
  className?: string;
}

const FileUploader: React.FC<FileUploaderProps> = ({ className }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
    } else {
      alert("Only PDF files are allowed.");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
    disabled: isUploading,
  });

  const clearFile = () => {
    setSelectedFile(null);
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    setIsUploading(true);
    setUploadResult(null);

    try {
      const res = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setUploadResult(data);

      if (res.ok) {
        alert("✅ PDF processed successfully!");
      } else {
        alert("❌ Error processing PDF: " + (data.error || data.stderr));
      }
    } catch (err) {
      console.error("❌ Upload failed:", err);
      alert("Upload failed. Check console for details.");
    } finally {
      setIsUploading(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className={cn("w-full space-y-4", className)}>
      {/* Upload Dropzone */}
      <div
        {...getRootProps()}
        className={cn(
          "upload-zone cursor-pointer transition-all duration-300",
          isDragActive && "upload-zone-active",
          isUploading && "opacity-50 cursor-not-allowed"
        )}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center space-y-3">
          <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
            <Upload className="w-6 h-6 text-primary" />
          </div>
          {isDragActive ? (
            <p className="text-primary font-medium">
              Drop your PDF file here...
            </p>
          ) : (
            <div className="text-center">
              <p className="text-foreground font-medium">
                Drag & drop your PDF file here
              </p>
              <p className="text-muted-foreground text-sm mt-1">
                or click to browse files
              </p>
            </div>
          )}
          <p className="text-xs text-muted-foreground">
            Supports: PDF files only (max 10MB)
          </p>
        </div>
      </div>

      {/* Selected File Preview */}
      {selectedFile && (
        <div className="bg-muted/50 rounded-lg p-4 space-y-3 fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <File className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="font-medium text-foreground">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-muted-foreground">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-success" />
              <Button
                variant="ghost"
                size="sm"
                onClick={clearFile}
                disabled={isUploading}
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={isUploading}
            className="w-full"
          >
            {isUploading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                <span>Processing PDF...</span>
              </div>
            ) : (
              "Process PDF"
            )}
          </Button>

          {/* Show Result */}
          {uploadResult && (
            <div className="mt-4 text-sm bg-white p-3 rounded border">
              <p className="font-bold">Parser Output:</p>
              <pre className="whitespace-pre-wrap text-xs overflow-auto max-h-60">
                {JSON.stringify(uploadResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FileUploader;
