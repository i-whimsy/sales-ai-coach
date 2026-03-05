"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/Button";
import { Progress } from "@/components/ui/Progress";

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && isSupportedFile(droppedFile)) {
      setFile(droppedFile);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && isSupportedFile(selectedFile)) {
      setFile(selectedFile);
    }
  };

  const isSupportedFile = (file: File): boolean => {
    const supportedTypes = ["audio/mp3", "audio/wav", "audio/m4a"];
    return supportedTypes.some((type) => file.type.includes(type)) || 
           [".mp3", ".wav", ".m4a"].some((ext) => file.name.toLowerCase().endsWith(ext));
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    
    // 模拟上传进度
    let progress = 0;
    const progressInterval = setInterval(() => {
      progress += 2;
      if (progress <= 100) {
        setUploadProgress(progress);
      } else {
        clearInterval(progressInterval);
      }
    }, 50);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      
      if (data.success) {
        router.push(`/progress?recordingId=${data.recordingId}`);
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      clearInterval(progressInterval);
      setIsUploading(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-4xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold text-foreground">
              上传销售讲解录音
            </h1>
            <p className="text-muted-foreground">
              支持 MP3、WAV、M4A 格式
            </p>
          </div>

          <div className="bg-card rounded-lg p-8 border">
            {!file ? (
              <div
                className={`border-2 border-dashed rounded-lg p-12 text-center transition-all cursor-pointer ${
                  isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25"
                }`}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  accept="audio/mp3,audio/wav,audio/m4a"
                  onChange={handleFileSelect}
                />
                <div className="space-y-4">
                  <div className="text-4xl mb-4">📁</div>
                  <p className="text-lg font-medium text-foreground">
                    拖拽文件到此处或点击选择
                  </p>
                  <p className="text-sm text-muted-foreground">
                    支持 MP3、WAV、M4A 格式，文件大小不超过 200MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-secondary rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl">🎵</div>
                    <div>
                      <p className="font-medium text-foreground">{file.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={removeFile}
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    ✕
                  </button>
                </div>

                {isUploading && (
                  <div className="space-y-2">
                    <Progress value={uploadProgress} />
                    <p className="text-sm text-muted-foreground text-center">
                      正在上传... {uploadProgress}%
                    </p>
                  </div>
                )}

                <Button
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="w-full"
                >
                  {isUploading ? "上传中..." : "分析录音"}
                </Button>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}