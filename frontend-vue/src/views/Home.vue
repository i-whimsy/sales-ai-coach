<template>
  <div class="space-y-12">
    <!-- Hero Section -->
    <div class="text-center space-y-8">
      <div class="inline-block mb-4">
        <div class="h-20 w-20 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg">
          <span class="text-white font-bold text-3xl">AI</span>
        </div>
      </div>
      <h1 class="text-5xl font-bold tracking-tight text-slate-900 dark:text-white">
        AI销售教练系统
      </h1>
      <p class="text-xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed">
        通过AI技术分析你的销售讲解，提供专业的改进建议，帮助你提升销售能力
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <RouterLink to="/upload" class="btn btn-primary px-8 py-4">
          开始上传录音
        </RouterLink>
        <RouterLink to="/history" class="btn btn-outline px-8 py-4">
          查看历史分析
        </RouterLink>
      </div>
    </div>

    <!-- Features Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="card p-6 shadow-md hover:shadow-lg transition-shadow">
        <div class="h-14 w-14 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
          <span class="text-blue-600 dark:text-blue-400 text-2xl">🎤</span>
        </div>
        <h3 class="text-xl font-semibold mb-3 text-slate-900 dark:text-white">语音转文本</h3>
        <p class="text-slate-600 dark:text-slate-400">
          使用先进的Whisper模型将语音转换为文本，支持多种音频格式
        </p>
      </div>

      <div class="card p-6 shadow-md hover:shadow-lg transition-shadow">
        <div class="h-14 w-14 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center mb-4">
          <span class="text-green-600 dark:text-green-400 text-2xl">📊</span>
        </div>
        <h3 class="text-xl font-semibold mb-3 text-slate-900 dark:text-white">智能分析</h3>
        <p class="text-slate-600 dark:text-slate-400">
          从表达质量、内容完整性、逻辑结构等多个维度进行全面分析
        </p>
      </div>

      <div class="card p-6 shadow-md hover:shadow-lg transition-shadow">
        <div class="h-14 w-14 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-4">
          <span class="text-purple-600 dark:text-purple-400 text-2xl">💡</span>
        </div>
        <h3 class="text-xl font-semibold mb-3 text-slate-900 dark:text-white">改进建议</h3>
        <p class="text-slate-600 dark:text-slate-400">
          基于分析结果提供个性化的改进建议，帮助你提升销售技巧
        </p>
      </div>
    </div>

    <!-- How It Works -->
    <div class="card shadow-lg">
      <div class="card-header">
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">工作流程</h2>
      </div>
      <div class="card-content">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="h-16 w-16 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mx-auto mb-4">
              <span class="text-blue-600 dark:text-blue-400 text-xl font-bold">1</span>
            </div>
            <h4 class="text-lg font-semibold mb-2">上传录音</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              上传MP3、WAV或M4A格式的录音文件，最大支持200MB
            </p>
          </div>
          <div class="text-center">
            <div class="h-16 w-16 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mx-auto mb-4">
              <span class="text-green-600 dark:text-green-400 text-xl font-bold">2</span>
            </div>
            <h4 class="text-lg font-semibold mb-2">AI分析</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              AI自动将语音转换为文本，并从多个维度进行分析
            </p>
          </div>
          <div class="text-center">
            <div class="h-16 w-16 rounded-full bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center mx-auto mb-4">
              <span class="text-yellow-600 dark:text-yellow-400 text-xl font-bold">3</span>
            </div>
            <h4 class="text-lg font-semibold mb-2">生成报告</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              生成详细的分析报告和个性化的改进建议
            </p>
          </div>
          <div class="text-center">
            <div class="h-16 w-16 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mx-auto mb-4">
              <span class="text-purple-600 dark:text-purple-400 text-xl font-bold">4</span>
            </div>
            <h4 class="text-lg font-semibold mb-2">持续改进</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              查看历史分析记录，跟踪你的销售能力提升过程
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- System Info -->
    <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-8">
      <div class="text-center">
        <h3 class="text-xl font-semibold mb-4 text-slate-900 dark:text-white">技术架构</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl mx-auto">
          <div class="flex items-center justify-center gap-3">
            <span class="text-2xl">⚙️</span>
            <div>
              <p class="font-medium">后端</p>
              <p class="text-sm text-slate-600 dark:text-slate-400">FastAPI + Python</p>
            </div>
          </div>
          <div class="flex items-center justify-center gap-3">
            <span class="text-2xl">🎨</span>
            <div>
              <p class="font-medium">前端</p>
              <p class="text-sm text-slate-600 dark:text-slate-400">Vue 3 + Tailwind CSS</p>
            </div>
          </div>
          <div class="flex items-center justify-center gap-3">
            <span class="text-2xl">🧠</span>
            <div>
              <p class="font-medium">AI模型</p>
              <p class="text-sm text-slate-600 dark:text-slate-400">OpenAI Whisper</p>
            </div>
          </div>
          <div class="flex items-center justify-center gap-3">
            <span class="text-2xl">💾</span>
            <div>
              <p class="font-medium">数据库</p>
              <p class="text-sm text-slate-600 dark:text-slate-400">SQLite</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>
