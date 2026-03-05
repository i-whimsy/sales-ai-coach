export function Features() {
  const features = [
    {
      title: "音频上传",
      description: "支持 MP3、WAV、M4A 格式，拖拽上传简单易用",
      icon: "📁",
    },
    {
      title: "自动语音识别",
      description: "基于 OpenAI Whisper API 的高精度语音识别",
      icon: "🎤",
    },
    {
      title: "AI 讲解分析",
      description: "多维度分析：表达能力、内容完整度、逻辑结构、客户理解度、说服力",
      icon: "🧠",
    },
    {
      title: "自动评分",
      description: "总分 100 分，每个维度权重可配置",
      icon: "📊",
    },
    {
      title: "生成分析报告",
      description: "详细的优缺点分析和改进建议",
      icon: "📄",
    },
    {
      title: "历史记录",
      description: "保存所有分析记录，随时查看和对比",
      icon: "📚",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {features.map((feature, index) => (
        <div
          key={index}
          className="bg-card rounded-lg p-6 border hover:shadow-lg transition-shadow"
        >
          <div className="text-3xl mb-4">{feature.icon}</div>
          <h3 className="text-lg font-bold text-foreground mb-2">
            {feature.title}
          </h3>
          <p className="text-muted-foreground">
            {feature.description}
          </p>
        </div>
      ))}
    </div>
  );
}