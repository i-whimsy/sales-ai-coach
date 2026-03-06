"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { BarChart3, FileText, ArrowLeft, CheckCircle2, AlertCircle } from "lucide-react";

const sampleReport = {
  totalScore: 85,
  dimensionScores: {
    expression: 82,
    content: 90,
    logic: 85,
    customerUnderstanding: 78,
    persuasion: 88,
  },
  strengths: [
    "表达清晰流畅，语速适中",
    "内容覆盖全面，包含完整的产品介绍",
    "逻辑结构清晰，有明确的开场和总结",
    "使用了客户案例，增强了说服力",
  ],
  improvements: [
    "可以增加一些停顿，增强客户的理解和记忆",
    "产品优势的描述可以更加具体",
    "客户痛点的分析可以更加深入",
    "可以增加一些数据支持，增强可信度",
  ],
};

export default function ReportPage() {
  const params = useParams();
  const router = useRouter();

  const [report, setReport] = useState(sampleReport);

  useEffect(() => {
    // In real implementation, fetch report data from API
    const fetchReport = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/recordings/${params.id}`);
        if (response.ok) {
          const data = await response.json();
          if (data.report) {
            setReport(data.report);
          }
        }
      } catch (error) {
        console.error("Error fetching report:", error);
      }
    };

    fetchReport();
  }, [params.id]);

  const chartData = [
    { subject: "表达能力", A: report.dimensionScores.expression, fullMark: 100 },
    { subject: "内容完整", A: report.dimensionScores.content, fullMark: 100 },
    { subject: "逻辑结构", A: report.dimensionScores.logic, fullMark: 100 },
    { subject: "客户理解", A: report.dimensionScores.customerUnderstanding, fullMark: 100 },
    { subject: "说服力", A: report.dimensionScores.persuasion, fullMark: 100 },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
            分析报告
          </h1>
          <p className="mt-2 text-lg text-slate-600 dark:text-slate-400">
            销售讲解录音分析结果
          </p>
        </div>
        
        <Button
          variant="ghost"
          onClick={() => router.push("/history")}
          className="flex items-center space-x-2"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>返回历史记录</span>
        </Button>
      </div>

      {/* Overall Score */}
      <Card className="max-w-4xl mx-auto">
        <CardContent className="p-8">
          <div className="flex items-center justify-between">
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
                综合评分
              </h2>
              <div className="flex items-end space-x-4">
                <div className="text-7xl font-bold text-blue-600 dark:text-blue-400">
                  {report.totalScore}
                </div>
                <div className="mb-2 text-2xl text-slate-500 dark:text-slate-400">
                  / 100
                </div>
              </div>
            </div>
            
            <Badge variant={report.totalScore >= 80 ? "default" : "destructive"} className="text-lg px-4 py-2">
              {report.totalScore >= 80 ? "优秀" : report.totalScore >= 60 ? "良好" : "需要改进"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Radar Chart */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            各维度评分
          </CardTitle>
          <CardDescription>
            分析报告覆盖五个关键维度的详细评分
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b' }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#94a3b8' }} />
                <Radar
                  name="评分"
                  dataKey="A"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  fill="#3b82f6"
                  fillOpacity={0.6}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e2e8f0', 
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Report Sections */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Strengths */}
        <Card className="col-span-1">
          <CardHeader className="pb-4">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="h-5 w-5 text-green-500" />
              <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
                优点
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {report.strengths.map((strength, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="mt-1.5 h-1.5 w-1.5 rounded-full bg-green-500 flex-shrink-0" />
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {strength}
                  </p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {/* Improvements */}
        <Card className="col-span-1 lg:col-span-2">
          <CardHeader className="pb-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-5 w-5 text-yellow-500" />
              <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
                改进建议
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3">
              {report.improvements.map((improvement, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="mt-1.5 h-1.5 w-1.5 rounded-full bg-yellow-500 flex-shrink-0" />
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {improvement}
                  </p>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analysis */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            详细分析
          </CardTitle>
          <CardDescription>
            各维度的评分详情和改进建议
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            {/* Expression Analysis */}
            <div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
                表达能力
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    总体评分
                  </span>
                  <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {report.dimensionScores.expression}/100
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  表达清晰流畅，语速适中，但可以增加一些停顿以增强客户理解。
                </p>
              </div>
            </div>

            {/* Content Analysis */}
            <div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
                内容完整度
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    总体评分
                  </span>
                  <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {report.dimensionScores.content}/100
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  内容覆盖全面，包含完整的产品介绍，但产品优势的描述可以更加具体。
                </p>
              </div>
            </div>

            {/* Logic Analysis */}
            <div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
                逻辑结构
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    总体评分
                  </span>
                  <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {report.dimensionScores.logic}/100
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  逻辑结构清晰，有明确的开场和总结，但问题引入可以更加直接。
                </p>
              </div>
            </div>

            {/* Customer Understanding */}
            <div>
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
                客户理解度
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    总体评分
                  </span>
                  <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {report.dimensionScores.customerUnderstanding}/100
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  客户可以理解公司和产品价值，但客户痛点的分析可以更加深入。
                </p>
              </div>
            </div>

            {/* Persuasion Analysis */}
            <div className="md:col-span-2">
              <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-3">
                说服力
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600 dark:text-slate-400">
                    总体评分
                  </span>
                  <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {report.dimensionScores.persuasion}/100
                  </span>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  使用了客户案例，增强了说服力，但可以增加一些数据支持，增强可信度。
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="max-w-4xl mx-auto text-center">
        <Button
          className="bg-blue-600 text-white hover:bg-blue-700"
          onClick={() => router.push("/history")}
        >
          <FileText className="mr-2 h-4 w-4" />
          查看更多历史记录
        </Button>
      </div>
    </div>
  );
}
