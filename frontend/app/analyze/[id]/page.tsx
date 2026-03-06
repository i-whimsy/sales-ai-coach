"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Music, FileText, BarChart3, CheckCircle2, ArrowRight } from "lucide-react";

type AnalysisStep = "uploading" | "transcribing" | "analyzing" | "generating" | "complete";

const steps = [
  { id: "uploading", name: "文件上传", icon: FileText },
  { id: "transcribing", name: "语音识别", icon: Music },
  { id: "analyzing", name: "内容分析", icon: BarChart3 },
  { id: "generating", name: "报告生成", icon: CheckCircle2 },
];

export default function AnalyzePage() {
  const params = useParams();
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<AnalysisStep>("uploading");
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("正在上传文件...");
  const [isAnalyzing, setIsAnalyzing] = useState(true);

  useEffect(() => {
    // Simulate analysis process
    const simulateAnalysis = async () => {
      // Step 1: Uploading
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCurrentStep("transcribing");
      setProgress(25);
      setStatus("正在进行语音识别...");

      // Step 2: Transcribing
      await new Promise(resolve => setTimeout(resolve, 1500));
      setCurrentStep("analyzing");
      setProgress(50);
      setStatus("正在分析表达质量...");

      // Step 3: Analyzing
      await new Promise(resolve => setTimeout(resolve, 2000));
      setCurrentStep("generating");
      setProgress(75);
      setStatus("正在生成报告...");

      // Step 4: Generating
      await new Promise(resolve => setTimeout(resolve, 1500));
      setCurrentStep("complete");
      setProgress(100);
      setStatus("分析完成！");

      // Stop loading and show completion
      setIsAnalyzing(false);
    };

    simulateAnalysis();
  }, []);

  // In real implementation, you would call the backend API
  // to get actual progress updates

  const handleViewReport = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/recordings/${params.id}`);
      const data = await response.json();
      
      if (data.report) {
        router.push(`/report/${params.id}`);
      }
    } catch (error) {
      console.error("Error fetching report:", error);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
          分析中
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          AI 正在分析你的销售讲解录音
        </p>
      </div>

      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            分析进度
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-8">
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-600 dark:text-slate-400">分析进度</span>
                <span className="font-medium text-slate-900 dark:text-white">{progress}%</span>
              </div>
              <Progress value={progress} className="h-3" />
            </div>

            {/* Step Indicators */}
            <div className="space-y-4">
              {steps.map((step, index) => {
                const StepIcon = step.icon;
                const isActive = step.id === currentStep;
                const isCompleted = index < steps.findIndex(s => s.id === currentStep);
                
                return (
                  <div key={step.id} className="flex items-center space-x-4">
                    <div className="relative flex items-center justify-center">
                      <div className={`h-8 w-8 rounded-full border-2 flex items-center justify-center
                        ${isCompleted 
                          ? "bg-green-500 border-green-500 text-white" 
                          : isActive 
                          ? "bg-blue-500 border-blue-500 text-white"
                          : "bg-slate-100 border-slate-300 dark:bg-slate-800 dark:border-slate-600"}
                      `}>
                        {isCompleted ? (
                          <CheckCircle2 className="h-4 w-4" />
                        ) : (
                          <StepIcon className="h-4 w-4" />
                        )}
                      </div>
                      {index < steps.length - 1 && (
                        <div className={`absolute left-8 right-[-20px] top-4 h-0.5 
                          ${isCompleted ? "bg-green-500" : "bg-slate-300 dark:bg-slate-600"}
                        `} />
                      )}
                    </div>
                    
                    <div className="flex-1">
                      <p className={`text-sm font-medium
                        ${isCompleted ? "text-green-600 dark:text-green-400" : 
                          isActive ? "text-blue-600 dark:text-blue-400" : 
                          "text-slate-600 dark:text-slate-400"}
                      `}>
                        {step.name}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Current Status */}
            <div className="rounded-lg bg-blue-50 p-4 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400">
              <div className="flex items-center space-x-2">
                <ArrowRight className="h-5 w-5" />
                <p>{status}</p>
              </div>
            </div>

            {/* Completion Button */}
            {!isAnalyzing && (
              <div className="pt-8 text-center">
                <Button
                  onClick={handleViewReport}
                  className="bg-green-600 text-white hover:bg-green-700"
                >
                  <CheckCircle2 className="mr-2 h-4 w-4" />
                  查看报告
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Analysis Details */}
      {currentStep === "complete" && (
        <div className="max-w-4xl mx-auto grid gap-6 md:grid-cols-2">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <CheckCircle2 className="h-8 w-8 text-green-600" />
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                    语音识别完成
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm">
                    录音已成功转换为文本
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <BarChart3 className="h-8 w-8 text-blue-600" />
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                    分析结果
                  </h3>
                  <p className="text-slate-600 dark:text-slate-400 text-sm">
                    报告已生成，包含评分和优化建议
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
