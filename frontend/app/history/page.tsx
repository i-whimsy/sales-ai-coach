"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/Button";

export default function HistoryPage() {
  const [recordings, setRecordings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("/api/recordings");
        const data = await response.json();
        setRecordings(data.recordings);
      } catch (error) {
        console.error("获取历史记录失败:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="max-w-5xl mx-auto px-6 py-24 text-center">
          <div className="space-y-4">
            <div className="text-4xl animate-spin">🔄</div>
            <h1 className="text-2xl font-bold text-foreground">
              正在加载历史记录...
            </h1>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold text-foreground">
              历史记录
            </h1>
            <p className="text-muted-foreground">
              查看所有分析过的录音和报告
            </p>
          </div>

          {/* 记录列表 */}
          <div className="space-y-4">
            {recordings.length === 0 ? (
              <div className="text-center py-24">
                <div className="text-6xl mb-4">📄</div>
                <h2 className="text-2xl font-bold text-foreground mb-2">
                  暂无分析记录
                </h2>
                <p className="text-muted-foreground mb-8">
                  上传您的第一份录音，开始提升销售技巧
                </p>
                <Button
                  onClick={() => window.location.href = "/"}
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  🚀 上传录音
                </Button>
              </div>
            ) : (
              recordings.map((recording) => (
                <div
                  key={recording.id}
                  className="bg-card rounded-lg p-6 border hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      <div className="text-2xl">🎵</div>
                      <div className="flex-1">
                        <h3 className="font-bold text-foreground">{recording.file_name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {new Date(recording.upload_time).toLocaleString()}
                        </p>
                      </div>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-primary">
                          {recording.score}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          总分
                        </div>
                      </div>
                    </div>
                    <Button
                      onClick={() => window.location.href = `/report?recordingId=${recording.id}`}
                      className="ml-4 bg-primary text-primary-foreground hover:bg-primary/90"
                    >
                      查看报告
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}