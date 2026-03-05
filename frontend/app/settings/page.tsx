"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/Navbar";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

export default function SettingsPage() {
  const [apiKeys, setApiKeys] = useState({
    openai: "",
    claude: "",
    deepseek: "",
    whisper: "",
  });
  const [saveStatus, setSaveStatus] = useState("");

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await fetch("/api/config");
        const data = await response.json();
        // 我们这里只需要显示配置状态，而不是暴露完整的API Key
        setApiKeys({
          openai: data.api_keys.openai ? "••••••••" : "",
          claude: data.api_keys.claude ? "••••••••" : "",
          deepseek: data.api_keys.deepseek ? "••••••••" : "",
          whisper: data.api_keys.whisper ? "••••••••" : "",
        });
      } catch (error) {
        console.error("加载配置失败:", error);
      }
    };

    loadConfig();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    setSaveStatus("saving");
    
    try {
      const response = await fetch("/api/config", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(apiKeys),
      });

      if (response.ok) {
        setSaveStatus("success");
        setTimeout(() => setSaveStatus(""), 2000);
      } else {
        setSaveStatus("error");
      }
    } catch (error) {
      console.error("保存配置失败:", error);
      setSaveStatus("error");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setApiKeys(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-3xl font-bold text-foreground">
              系统设置
            </h1>
            <p className="text-muted-foreground">
              配置 AI 分析引擎和语音识别 API
            </p>
          </div>

          <div className="bg-card rounded-lg p-8 border">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  OpenAI API Key
                </label>
                <Input
                  type="password"
                  name="openai"
                  value={apiKeys.openai}
                  onChange={handleChange}
                  placeholder="sk-..."
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Claude API Key
                </label>
                <Input
                  type="password"
                  name="claude"
                  value={apiKeys.claude}
                  onChange={handleChange}
                  placeholder="sk-ant-..."
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  DeepSeek API Key
                </label>
                <Input
                  type="password"
                  name="deepseek"
                  value={apiKeys.deepseek}
                  onChange={handleChange}
                  placeholder="sk-..."
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Whisper API Key
                </label>
                <Input
                  type="password"
                  name="whisper"
                  value={apiKeys.whisper}
                  onChange={handleChange}
                  placeholder="sk-..."
                />
              </div>

              <div className="flex items-center space-x-4">
                <Button
                  type="submit"
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  {saveStatus === "saving" ? "保存中..." : "保存设置"}
                </Button>
                {saveStatus === "success" && (
                  <span className="text-green-500">✅ 保存成功</span>
                )}
                {saveStatus === "error" && (
                  <span className="text-red-500">❌ 保存失败</span>
                )}
              </div>
            </form>

            <div className="mt-8 pt-8 border-t">
              <div className="space-y-4">
                <h3 className="text-sm font-medium text-foreground">
                  💡 使用说明
                </h3>
                <ul className="text-sm text-muted-foreground space-y-2">
                  <li>• OpenAI API Key 需要具有 Whisper 语音识别和 GPT 模型访问权限</li>
                  <li>• 配置至少一个 API Key，系统将自动选择可用的引擎</li>
                  <li>• API Key 会加密存储在服务器上，不会暴露给前端</li>
                  <li>• 语音识别优先使用 OpenAI Whisper API，无可用 Key 时使用本地 Whisper 模型</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}