"use client";

import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { CheckCircle2, Save, AlertCircle } from "lucide-react";

type ApiKeyConfig = {
  openaiApiKey: string;
  deepseekApiKey: string;
  claudeApiKey: string;
  whisperApiKey: string;
};

export default function SettingsPage() {
  const [apiKeys, setApiKeys] = useState<ApiKeyConfig>({
    openaiApiKey: "",
    deepseekApiKey: "",
    claudeApiKey: "",
    whisperApiKey: "",
  });

  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    // In real implementation, fetch API keys from backend
    const fetchConfig = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/api-config");
        if (response.ok) {
          const data = await response.json();
          setApiKeys({
            openaiApiKey: data.openai_api_key || "",
            deepseekApiKey: data.deepseek_api_key || "",
            claudeApiKey: data.claude_api_key || "",
            whisperApiKey: data.whisper_api_key || "",
          });
        }
      } catch (error) {
        console.error("Error fetching API config:", error);
      }
    };

    fetchConfig();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setApiKeys(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSaveSuccess(false);
    setSaveError(null);

    try {
      const response = await fetch("http://localhost:8000/api/v1/api-config", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          openai_api_key: apiKeys.openaiApiKey,
          deepseek_api_key: apiKeys.deepseekApiKey,
          claude_api_key: apiKeys.claudeApiKey,
          whisper_api_key: apiKeys.whisperApiKey,
        }),
      });

      if (response.ok) {
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 3000);
      } else {
        setSaveError("保存失败，请重试");
      }
    } catch (error) {
      setSaveError("网络错误，请检查连接");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-5xl">
          设置
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          配置 AI 接口和系统参数
        </p>
      </div>

      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900 dark:text-white">
            API 配置
          </CardTitle>
          <CardDescription>
            配置用于分析的 AI 接口 API 密钥
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* OpenAI API Key */}
            <div className="space-y-2">
              <Label htmlFor="openaiApiKey" className="text-sm font-medium">
                OpenAI API Key
              </Label>
              <Input
                id="openaiApiKey"
                name="openaiApiKey"
                type="password"
                value={apiKeys.openaiApiKey}
                onChange={handleChange}
                placeholder="sk-..."
                className="font-mono text-sm"
              />
              <p className="text-xs text-slate-500 dark:text-slate-400">
                用于访问 OpenAI API，包括 GPT 模型和 Whisper 语音识别
              </p>
            </div>

            <Separator />

            {/* DeepSeek API Key */}
            <div className="space-y-2">
              <Label htmlFor="deepseekApiKey" className="text-sm font-medium">
                DeepSeek API Key
              </Label>
              <Input
                id="deepseekApiKey"
                name="deepseekApiKey"
                type="password"
                value={apiKeys.deepseekApiKey}
                onChange={handleChange}
                placeholder="sk-..."
                className="font-mono text-sm"
              />
              <p className="text-xs text-slate-500 dark:text-slate-400">
                用于访问 DeepSeek API，提供强大的代码和文本分析能力
              </p>
            </div>

            <Separator />

            {/* Claude API Key */}
            <div className="space-y-2">
              <Label htmlFor="claudeApiKey" className="text-sm font-medium">
                Claude API Key
              </Label>
              <Input
                id="claudeApiKey"
                name="claudeApiKey"
                type="password"
                value={apiKeys.claudeApiKey}
                onChange={handleChange}
                placeholder="sk-ant-..."
                className="font-mono text-sm"
              />
              <p className="text-xs text-slate-500 dark:text-slate-400">
                用于访问 Anthropic Claude API，提供专业的自然语言处理能力
              </p>
            </div>

            <Separator />

            {/* Whisper API Key */}
            <div className="space-y-2">
              <Label htmlFor="whisperApiKey" className="text-sm font-medium">
                Whisper API Key
              </Label>
              <Input
                id="whisperApiKey"
                name="whisperApiKey"
                type="password"
                value={apiKeys.whisperApiKey}
                onChange={handleChange}
                placeholder="sk-..."
                className="font-mono text-sm"
              />
              <p className="text-xs text-slate-500 dark:text-slate-400">
                用于访问 OpenAI Whisper API，提供高质量的语音识别服务
              </p>
            </div>

            {/* Status Messages */}
            {saveSuccess && (
              <div className="flex items-center space-x-2 rounded-lg bg-green-50 p-4 text-green-700 dark:bg-green-900/20 dark:text-green-400">
                <CheckCircle2 className="h-5 w-5" />
                <p>API 配置保存成功！</p>
              </div>
            )}

            {saveError && (
              <div className="flex items-center space-x-2 rounded-lg bg-red-50 p-4 text-red-700 dark:bg-red-900/20 dark:text-red-400">
                <AlertCircle className="h-5 w-5" />
                <p>{saveError}</p>
              </div>
            )}

            {/* Save Button */}
            <Button
              onClick={handleSave}
              disabled={isSaving}
              className="w-full bg-blue-600 text-white hover:bg-blue-700"
            >
              {isSaving ? (
                <>
                  <Save className="mr-2 h-4 w-4 animate-pulse" />
                  保存中...
                </>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  保存配置
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Info Cards */}
      <div className="max-w-2xl mx-auto grid gap-6 md:grid-cols-2">
        <Card className="bg-blue-50 dark:bg-blue-900/20">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">
              系统信息
            </h3>
            <div className="space-y-2 text-sm text-blue-700 dark:text-blue-300">
              <p>版本: 1.0.0</p>
              <p>语言: 中文 (简体)</p>
              <p>数据库: SQLite</p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-yellow-50 dark:bg-yellow-900/20">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-3">
              安全提示
            </h3>
            <div className="space-y-2 text-sm text-yellow-700 dark:text-yellow-300">
              <p>API 密钥将安全存储</p>
              <p>使用 HTTPS 保护传输</p>
              <p>定期更换密钥以提高安全性</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
