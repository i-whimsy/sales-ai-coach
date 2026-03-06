"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export function Upload() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

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
    
    const file = e.dataTransfer.files[0];
    if (file && isSupportedFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && isSupportedFile(file)) {
      setSelectedFile(file);
    }
  };

  const isSupportedFile = (file: File): boolean => {
    const supportedTypes = ["audio/mp3", "audio/wav", "audio/m4a"];
    return supportedTypes.some((type) => file.type.includes(type)) || 
           [".mp3", ".wav", ".m4a"].some((ext) => file.name.toLowerCase().endsWith(ext));
  };

  const handleUpload = () => {
    router.push("/upload");
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-card rounded-lg p-12 border">
        {!selectedFile ? (
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all cursor-pointer ${
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
          <div className="space-y-6">
            <div className="bg-secondary rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="text-2xl">🎵</div>
                  <div>
                    <p className="font-bold text-foreground">{selectedFile.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedFile(null)}
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>
            <Button
              onClick={handleUpload}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
            >
              分析录音
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}