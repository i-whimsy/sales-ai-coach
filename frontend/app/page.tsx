"use client";

import { useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, BarChart3, Upload, Clock, CheckCircle2 } from "lucide-react";

export default function Home() {
  const [stats] = useState({
    totalRecordings: 12,
    avgScore: 78,
    topPerformer: 95,
    weeklyImprovement: 12,
  });

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
            AI 销售培训系统
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
            提升销售团队的讲解能力。上传演示录音，获得 AI 分析报告，包括表达质量、内容完整性、逻辑结构和客户理解度评分。
          </p>
        </div>
        <Button size="lg" className="w-full md:w-auto" asChild>
          <Link href="/upload">
            <Upload className="mr-2 h-5 w-5" />
            上传录音
          </Link>
        </Button>
      </div>

      {/* Stats Section */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 dark:text-slate-400">
              总记录数
            </CardTitle>
            <FileText className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {stats.totalRecordings}
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              已分析的录音
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 dark:text-slate-400">
              平均评分
            </CardTitle>
            <BarChart3 className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {stats.avgScore}
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              综合评分
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 dark:text-slate-400">
              最佳成绩
            </CardTitle>
            <CheckCircle2 className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {stats.topPerformer}
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              最高评分
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-500 dark:text-slate-400">
              周进步
            </CardTitle>
            <Clock className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              +{stats.weeklyImprovement}%
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              相比上周
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Features Section */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              语音识别
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              自动将录音转换为文本，支持多种语言识别
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              AI 分析
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              深度分析表达能力、内容完整性、逻辑结构和客户理解度
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              智能评分
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              基于多个维度的自动评分系统，帮助销售人员提升业绩
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              详细报告
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              生成可视化报告，展示优缺点和改进建议
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              历史记录
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              保存并对比历史记录，跟踪销售能力提升
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-slate-900 dark:text-white">
              API 集成
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-600 dark:text-slate-400">
              支持 OpenAI、DeepSeek、Anthropic Claude 等 AI 接口
            </p>
          </CardContent>
        </Card>
      </div>

      {/* CTA Section */}
      <div className="mt-8 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-center text-white">
        <h2 className="text-2xl font-bold mb-4">
          开始提升你的销售讲解能力
        </h2>
        <p className="mb-6 text-blue-100">
          上传你的演示录音，获得专业的 AI 分析和改进建议
        </p>
        <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50" asChild>
          <Link href="/upload">
            <Upload className="mr-2 h-5 w-5" />
            立即上传
          </Link>
        </Button>
      </div>
    </div>
  );
}
