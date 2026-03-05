import { Upload } from "@/components/Upload";
import { Features } from "@/components/Features";
import { Navbar } from "@/components/Navbar";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center max-w-4xl mx-auto space-y-8">
          <h1 className="text-5xl font-bold tracking-tight text-foreground">
            AI Sales Coaching
          </h1>
          <p className="text-xl text-muted-foreground leading-relaxed">
            上传您的销售讲解录音，AI智能分析您的表达能力、内容完整度、逻辑结构、客户理解度和说服力，
            帮您提升销售讲解技巧，获得更高的转化率。
          </p>
          <div className="pt-8">
            <Upload />
          </div>
        </div>
        
        <div className="mt-32">
          <Features />
        </div>
      </main>
    </div>
  );
}