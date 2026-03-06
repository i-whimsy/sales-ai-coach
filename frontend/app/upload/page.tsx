"use client";

import React, { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, FileText, Music, AlertCircle, CheckCircle } from "lucide-react";

export default function UploadPage() {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleDragOver = (e: React.DragEvent) => {
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
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      validateAndSetFile(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    const validTypes = ["audio/mpeg", "audio/wav", "audio/mp4", "audio/m4a"];
    const validExtensions = ["mp3", "wav", "m4a"];
    
    const fileExtension = file.name.split(".").pop()?.toLowerCase() || "";
    const isValidType = validTypes.includes(file.type) || validExtensions.includes(fileExtension);
    
    if (!isValidType) {
      setError("无效的文件格式。请上传 MP3、WAV 或 M4A 文件。");
      return;
    }

    const maxSize = 20 * 1024 * 1024; // 20MB
    if (file.size > maxSize) {
      setError("文件大小超过限制。请上传小于 20MB 的文件。");
      return;
    }

    setSelectedFile(file);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch("http://localhost:8000/api/v1/recordings", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "上传失败");
      }

      const data = await response.json();
      
      // Navigate to analyze page with recording id
      router.push(`/analyze/${data.id}`);
      
    } catch (err: any) {
      setError(err.message || "上传过程中发生错误");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
          上传录音
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          上传你的销售讲解录音，AI 将为你分析表达质量、内容完整性、逻辑结构和客户理解度
        </p>
      </div>

      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            选择录音文件
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* File Drop Zone */}
            <div
              className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors duration-200
                ${isDragging 
                  ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20" 
                  : "border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-900"}
                ${selectedFile ? "border-green-500 bg-green-50 dark:bg-green-900/20" : ""}
              `}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              {selectedFile ? (
                <div className="space-y-4">
                  <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
                  <div className="space-y-1">
                    <p className="text-lg font-medium text-slate-900 dark:text-white">
                      文件已选择
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {selectedFile.name}
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-500">
                      {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <Upload className="h-16 w-16 text-slate-400 mx-auto" />
                  <div className="space-y-1">
                    <p className="text-lg font-medium text-slate-900 dark:text-white">
                      拖拽文件到此处或点击选择
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      支持 MP3、WAV、M4A 格式，最大 20MB
                    </p>
                  </div>
                </div>
              )}
              
              <input
                ref={fileInputRef}
                type="file"
                accept="audio/mp3,audio/wav,audio/m4a"
                onChange={handleFileSelect}
                className="hidden"
              />
              
              <Button
                onClick={() => fileInputRef.current?.click()}
                variant="outline"
                className="mt-6"
                disabled={selectedFile !== null}
              >
                <FileText className="mr-2 h-4 w-4" />
                选择文件
              </Button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="flex items-center space-x-2 rounded-lg bg-red-50 p-4 text-red-700 dark:bg-red-900/20 dark:text-red-400">
                <AlertCircle className="h-5 w-5" />
                <p>{error}</p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex justify-between pt-4">
              <Button
                variant="ghost"
                onClick={() => setSelectedFile(null)}
                disabled={!selectedFile}
              >
                重新选择
              </Button>
              
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                {uploading ? (
                  <>
                    <Music className="mr-2 h-4 w-4 animate-pulse" />
                    上传中...
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    开始分析
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* File Requirements */}
      <div className="max-w-4xl mx-auto grid gap-6 md:grid-cols-2">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-4">
              <FileText className="h-8 w-8 text-blue-600" />
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                  支持格式
                </h3>
                <p className="text-slate-600 dark:text-slate-400 text-sm">
                  MP3, WAV, M4A
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-4">
              <AlertCircle className="h-8 w-8 text-yellow-600" />
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                  文件大小
                </h3>
                <p className="text-slate-600 dark:text-slate-400 text-sm">
                  最大 20MB
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
