"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Navbar } from "@/components/Navbar";
import { Progress } from "@/components/ui/Progress";

export default function ProgressPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const recordingId = searchParams.get("recordingId");
  const [currentStep, setCurrentStep] = useState(0);
  const [steps, setSteps] = useState([
    { label: "上传文件", completed: false },
    { label: "语音识别", completed: false },
    { label: "表达分析", completed: false },
    { label: "逻辑分析", completed: false },
    { label: "客户理解", completed: false },
    { label: "生成报告", completed: false },
  ]);

  useEffect(() => {
    const processAnalysis = async () => {
      for (let i = 0; i < steps.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        setCurrentStep(i);
        
        const updatedSteps = [...steps];
        updatedSteps[i].completed = true;
        setSteps(updatedSteps);
      }

      // 分析完成后跳转
      router.push(`/report?recordingId=${recordingId}`);
    };

    processAnalysis();
  }, [recordingId, router, steps]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-3xl mx-auto px-6 py-24">
        <div className="text-center space-y-12">
          <h1 className="text-3xl font-bold text-foreground">
            AI 分析进度
          </h1>

          <div className="space-y-6">
            {steps.map((step, index) => (
              <div key={index} className="relative">
                <div
                  className={`flex items-center space-x-4 p-4 rounded-lg border transition-all ${
                    index === currentStep ? "bg-primary/5 border-primary" : "bg-card"
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                      step.completed ? "bg-green-500 text-white" : "bg-muted"
                    }`}
                  >
                    {step.completed ? "✓" : index + 1}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-foreground">{step.label}</p>
                    {index === currentStep && (
                      <p className="text-sm text-primary">
                        正在处理...
                      </p>
                    )}
                    {step.completed && index < currentStep && (
                      <p className="text-sm text-muted-foreground">
                        已完成
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-8">
            <div className="space-y-2">
              <Progress value={(currentStep / steps.length) * 100} />
              <p className="text-sm text-muted-foreground text-center">
                {Math.round((currentStep / steps.length) * 100)}% 完成
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}