"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Calendar, ArrowRight, Download } from "lucide-react";

type Recording = {
  id: number;
  fileName: string;
  uploadTime: string;
  score: number;
};

const sampleRecordings: Recording[] = [
  { id: 1, fileName: "产品介绍录音.mp3", uploadTime: "2024-01-15 10:30", score: 85 },
  { id: 2, fileName: "销售演示.wav", uploadTime: "2024-01-14 14:20", score: 92 },
  { id: 3, fileName: "客户需求分析.mp3", uploadTime: "2024-01-13 09:15", score: 78 },
  { id: 4, fileName: "竞争产品对比.wav", uploadTime: "2024-01-12 16:45", score: 88 },
  { id: 5, fileName: "解决方案演示.mp3", uploadTime: "2024-01-11 11:00", score: 95 },
];

export default function HistoryPage() {
  const router = useRouter();
  const [recordings, setRecordings] = useState<Recording[]>([]);

  useEffect(() => {
    // In real implementation, fetch recordings from API
    const fetchRecordings = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/recordings");
        if (response.ok) {
          const data = await response.json();
          setRecordings(data.recordings);
        } else {
          // Fallback to sample data
          setRecordings(sampleRecordings);
        }
      } catch (error) {
        console.error("Error fetching recordings:", error);
        setRecordings(sampleRecordings);
      }
    };

    fetchRecordings();
  }, []);

  const getScoreBadge = (score: number) => {
    if (score >= 90) {
      return <Badge className="bg-green-500 hover:bg-green-600">优秀</Badge>;
    } else if (score >= 80) {
      return <Badge className="bg-blue-500 hover:bg-blue-600">良好</Badge>;
    } else if (score >= 70) {
      return <Badge className="bg-yellow-500 hover:bg-yellow-600">一般</Badge>;
    } else {
      return <Badge className="bg-red-500 hover:bg-red-600">需要改进</Badge>;
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
          历史记录
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          查看你的销售讲解录音分析历史，跟踪学习和成长
        </p>
      </div>

      {/* Recordings List */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            分析记录
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800">
                  <th className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                    文件名
                  </th>
                  <th className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                    上传时间
                  </th>
                  <th className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                    评分
                  </th>
                  <th className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody>
                {recordings.map((recording) => (
                  <tr
                    key={recording.id}
                    className="border-b border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-900"
                  >
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-4 w-4 text-slate-500" />
                        <span className="text-sm font-medium text-slate-900 dark:text-white">
                          {recording.fileName}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <Calendar className="h-4 w-4 text-slate-500" />
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          {recording.uploadTime}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        {getScoreBadge(recording.score)}
                        <span className="text-sm font-medium text-slate-900 dark:text-white">
                          {recording.score}/100
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <Button
                          size="sm"
                          onClick={() => router.push(`/report/${recording.id}`)}
                          className="bg-blue-600 text-white hover:bg-blue-700"
                        >
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="ghost">
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Empty State */}
          {recordings.length === 0 && (
            <div className="text-center py-12">
              <FileText className="h-12 w-12 text-slate-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-slate-900 dark:text-white mb-2">
                暂无分析记录
              </p>
              <p className="text-slate-600 dark:text-slate-400 mb-6">
                上传你的第一个销售讲解录音开始分析
              </p>
              <Button
                onClick={() => router.push("/upload")}
                className="bg-blue-600 text-white hover:bg-blue-700"
              >
                <FileText className="mr-2 h-4 w-4" />
                上传第一个录音
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Statistics */}
      {recordings.length > 0 && (
        <div className="max-w-4xl mx-auto grid gap-6 md:grid-cols-3">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white">
                  {recordings.length}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                    总记录数
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm">
                    已完成分析
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <div className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center text-white">
                  {Math.round(recordings.reduce((sum, rec) => sum + rec.score, 0) / recordings.length)}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                    平均评分
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm">
                    综合表现
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <div className="h-8 w-8 rounded-full bg-purple-500 flex items-center justify-center text-white">
                  {recordings.reduce((count, rec) => count + (rec.score >= 90 ? 1 : 0), 0)}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                    优秀记录
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm">
                    评分 ≥ 90分
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Action Button */}
      <div className="max-w-4xl mx-auto text-center">
        <Button
          onClick={() => router.push("/upload")}
          className="bg-blue-600 text-white hover:bg-blue-700"
        >
          <FileText className="mr-2 h-4 w-4" />
          上传新的录音
        </Button>
      </div>
    </div>
  );
}
