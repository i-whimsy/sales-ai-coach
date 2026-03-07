<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-slate-900 dark:via-slate-950 dark:to-slate-900">
    <!-- Header -->
    <header class="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm border-b border-slate-200 dark:border-slate-800">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
              <span class="text-white font-bold text-xl">AI</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-slate-900 dark:text-white">销售教练</h1>
              <p class="text-xs text-slate-500 dark:text-slate-400">AI驱动的销售能力提升系统</p>
            </div>
          </div>
          
          <!-- Navigation -->
          <nav class="hidden md:flex items-center gap-6">
            <RouterLink 
              to="/" 
              class="nav-link" 
              :class="{ 'text-primary-600 dark:text-primary-400': $route.name === 'Home' }"
            >
              <span class="nav-text">首页</span>
            </RouterLink>
            <RouterLink 
              to="/upload" 
              class="nav-link" 
              :class="{ 'text-primary-600 dark:text-primary-400': $route.name === 'Upload' }"
            >
              <span class="nav-text">上传录音</span>
            </RouterLink>
            <RouterLink 
              to="/history" 
              class="nav-link" 
              :class="{ 'text-primary-600 dark:text-primary-400': $route.name === 'History' }"
            >
              <span class="nav-text">历史记录</span>
            </RouterLink>
            <RouterLink 
              to="/settings" 
              class="nav-link" 
              :class="{ 'text-primary-600 dark:text-primary-400': $route.name === 'Settings' }"
            >
              <span class="nav-text">系统设置</span>
            </RouterLink>
            <RouterLink 
              to="/models" 
              class="nav-link" 
              :class="{ 'text-primary-600 dark:text-primary-400': $route.name === 'ModelManagement' }"
            >
              <span class="nav-text">模型管理</span>
            </RouterLink>
          </nav>
        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <RouterView />
    </main>
    
    <!-- Footer -->
    <footer class="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div class="container mx-auto px-4 py-8">
        <div class="text-center text-sm text-slate-500 dark:text-slate-400">
          <p>AI销售教练系统 © 2026</p>
          <p class="mt-1">由 OpenClaw 自主研发 | 基于 FastAPI + Vue 3 构建</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-2 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors;
}

.nav-text {
  @apply text-sm font-medium;
}
</style>
