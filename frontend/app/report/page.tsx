"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Navbar } from "@/components/Navbar";
import { RadarChart } from "@/components/ui/RadarChart";
import { Button } from "@/components/ui/button";

function ReportContent() {
  const searchParams = useSearchParams();
  const recordingId = searchParams.get("recordingId");
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await fetch(`/api/report/${recordingId}`);
        const data = await response.json();
        setReport(data);
      } catch (error) {
        console.error("获取报告失败:", error);
      } finally {
        setLoading(false);
      }
    };

    if (recordingId) {
      fetchReport();
    }
  }, [recordingId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="max-w-5xl mx-auto px-6 py-24 text-center">
          <div className="space-y-4">
            <div className="text-4xl animate-spin">🔄</div>
            <h1 className="text-2xl font-bold text-foreground">
              正在加载分析报告...
            </h1>
          </div>
        </main>
      </div>
    );
  }

  const dimensions = [
    { label: "表达能力", value: report.expression_score },
    { label: "内容完整度", value: report.content_score },
    { label: "逻辑结构", value: report.logic_score },
    { label: "客户理解度", value: report.customer_score },
    { label: "说服力", value: report.persuasion_score },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-24">
        <div className="space-y-12">
          {/* 标题和总评分 */}
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold text-foreground">
              {report.file_name}
            </h1>
            <div className="inline-block bg-card rounded-full px-8 py-4 border">
              <div className="text-6xl font-bold text-primary mb-2">
                {report.total_score}
              </div>
              <div className="text-sm text-muted-foreground">
                总分 100 分
              </div>
            </div>
          </div>

          {/* 评分雷达图 */}
          <div className="bg-card rounded-lg p-8 border">
            <h2 className="text-2xl font-bold text-foreground mb-8 text-center">
              评分分析
            </h2>
            <RadarChart data={dimensions} />
          </div>

          {/* 优点 */}
          {report.strengths.length > 0 && (
            <div className="bg-card rounded-lg p-8 border">
              <h3 className="text-xl font-bold text-foreground mb-4">
                ✅ 优点
              </h3>
              <ul className="space-y-2">
                {report.strengths.map((strength: string, index: number) => (
                  <li key={index} className="text-foreground">
                    • {strength}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 问题 */}
          {report.weaknesses.length > 0 && (
            <div className="bg-card rounded-lg p-8 border">
              <h3 className="text-xl font-bold text-foreground mb-4">
                ❌ 问题
              </h3>
              <ul className="space-y-2">
                {report.weaknesses.map((weakness: string, index: number) => (
                  <li key={index} className="text-foreground">
                    • {weakness}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 改进建议 */}
          {report.suggestions.length > 0 && (
            <div className="bg-card rounded-lg p-8 border">
              <h3 className="text-xl font-bold text-foreground mb-4">
                💡 改进建议
              </h3>
              <ul className="space-y-2">
                {report.suggestions.map((suggestion: string, index: number) => (
                  <li key={index} className="text-foreground">
                    • {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 操作按钮 */}
          <div className="flex justify-center space-x-4 pt-8">
            <Button
              onClick={() => window.print()}
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              🖨️ 打印报告
            </Button>
            <Button
              onClick={() => window.location.href = "/history"}
              className="bg-secondary text-secondary-foreground hover:bg-secondary/90"
            >
              📄 查看历史
            </Button>
            <Button
              onClick={() => window.location.href = "/"}
              className="bg-accent text-accent-foreground hover:bg-accent/90"
            >
              🏠 回到首页
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function ReportPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="max-w-5xl mx-auto px-6 py-24 text-center">
          <div className="space-y-4">
            <div className="text-4xl animate-spin">🔄</div>
            <h1 className="text-2xl font-bold text-foreground">
              正在加载报告...
            </h1>
          </div>
        </main>
      </div>
    }>
      <ReportContent />
    </Suspense>
  );
}