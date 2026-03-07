<template>
  <div v-if="loading" class="text-center py-12">
    <div class="animate-spin text-4xl mb-4">⏳</div>
    <p class="text-slate-600 dark:text-slate-400">加载中...</p>
  </div>
  
  <div v-else-if="!recording" class="text-center py-12">
    <p class="text-slate-600 dark:text-slate-400">未找到录音记录</p>
  </div>
  
  <div v-else class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">分析报告</h1>
        <p class="mt-1 text-slate-600 dark:text-slate-400">{{ recording.name || recording.file_name }}</p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/history" class="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors">
          返回历史
        </RouterLink>
      </div>
    </div>

    <!-- Score Overview -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6">
      <h2 class="text-xl font-semibold text-slate-900 dark:text-white mb-4">总体评分</h2>
      
      <div class="flex items-center justify-center mb-6">
        <div class="relative w-40 h-40">
          <svg class="w-full h-full transform -rotate-90">
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              stroke-width="12"
              fill="none"
              class="text-slate-200 dark:text-slate-700"
            />
            <circle
              cx="80"
              cy="80"
              r="70"
              stroke="currentColor"
              stroke-width="12"
              fill="none"
              :stroke-dasharray="`${(recording.report?.total_score || 0) * 4.4} 440`"
              class="text-blue-600 dark:text-blue-400"
              stroke-linecap="round"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-4xl font-bold text-slate-900 dark:text-white">
              {{ (recording.report?.total_score || 0).toFixed(1) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Dimension Scores -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div v-for="(score, dimension) in recording?.report?.dimension_scores" :key="dimension" 
          class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium text-slate-900 dark:text-white text-sm">
              {{ getDimensionName(dimension) }}
            </span>
            <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
              {{ score.toFixed(1) }}
            </span>
          </div>
          <div class="w-full bg-slate-200 rounded-full dark:bg-slate-800 h-2">
            <div
              class="h-2 rounded-full"
              :style="{
                width: `${score}%`,
                backgroundColor: getScoreColor(score)
              }"
            ></div>
          </div>
          <div class="mt-1 text-xs text-slate-500">
            权重: {{ getWeight(dimension) }}%
          </div>
          <div class="mt-1 text-xs font-medium" :class="getWeightedScore(score, dimension) > 0 ? 'text-green-600' : 'text-slate-400'">
            贡献: +{{ getWeightedScore(score, dimension).toFixed(1) }}
          </div>
        </div>
      </div>
      
      <p class="mt-4 text-xs text-slate-500 text-center">
        * 总分 = 各维度分数 × 权重之和。单项分数不会直接相加等于总分。
      </p>
    </div>

    <!-- Transcript -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">转录文本</h2>
      </div>
      <div class="p-6">
        <p class="text-slate-700 dark:text-slate-300 whitespace-pre-wrap">{{ recording.transcript || '暂无转录文本' }}</p>
      </div>
    </div>

    <!-- Detailed Analysis -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Content Analysis -->
      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
        <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">内容分析</h3>
        </div>
        <div class="p-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-slate-600 dark:text-slate-400">得分</span>
            <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
              {{ recording?.report?.content_analysis?.total_score || '--' }} / 100
            </span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 text-sm">
            {{ recording?.report?.content_analysis?.analysis || '暂无分析' }}
          </p>
        </div>
      </div>

      <!-- Logic Analysis -->
      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
        <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">逻辑结构分析</h3>
        </div>
        <div class="p-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-slate-600 dark:text-slate-400">得分</span>
            <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
              {{ recording?.report?.logic_analysis?.total_score || '--' }} / 100
            </span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 text-sm">
            {{ recording?.report?.logic_analysis?.analysis || '暂无分析' }}
          </p>
        </div>
      </div>

      <!-- Customer Understanding -->
      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
        <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">客户理解分析</h3>
        </div>
        <div class="p-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-slate-600 dark:text-slate-400">得分</span>
            <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
              {{ recording?.report?.customer_analysis?.total_score || '--' }} / 100
            </span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 text-sm">
            {{ recording?.report?.customer_analysis?.analysis || '暂无分析' }}
          </p>
        </div>
      </div>

      <!-- Persuasion -->
      <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
        <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
          <h3 class="text-lg font-semibold text-slate-900 dark:text-white">说服力分析</h3>
        </div>
        <div class="p-6">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-slate-600 dark:text-slate-400">得分</span>
            <span class="text-lg font-bold text-primary-600 dark:text-primary-400">
              {{ recording?.report?.persuasion_analysis?.total_score || '--' }} / 100
            </span>
          </div>
          <p class="text-slate-700 dark:text-slate-300 text-sm">
            {{ recording?.report?.persuasion_analysis?.analysis || '暂无分析' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Strengths -->
    <div v-if="recording?.report?.strengths?.length" class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-green-600 dark:text-green-400">✓ 优势</h3>
      </div>
      <div class="p-6">
        <ul class="space-y-2">
          <li v-for="(strength, index) in recording.report.strengths" :key="index" class="flex items-start gap-2">
            <span class="text-green-500 mt-0.5">✓</span>
            <span class="text-slate-700 dark:text-slate-300">{{ strength }}</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Improvements -->
    <div v-if="recording?.report?.improvement_suggestions?.length" class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h3 class="text-lg font-semibold text-yellow-600 dark:text-yellow-400">改进建议</h3>
      </div>
      <div class="p-6">
        <ul class="space-y-2">
          <li v-for="(suggestion, index) in recording.report.improvement_suggestions" :key="index" class="flex items-start gap-2">
            <span class="text-yellow-500 mt-0.5">!</span>
            <span class="text-slate-700 dark:text-slate-300">{{ suggestion }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const recording = ref(null)
const loading = ref(true)

const getDimensionName = (dimension) => {
  const names = {
    expression: '表达质量',
    content: '内容质量',
    logic: '逻辑结构',
    customer_understanding: '客户理解',
    persuasion: '说服力'
  }
  return names[dimension] || dimension
}

const getWeight = (dimension) => {
  const weights = {
    expression: 20,
    content: 30,
    logic: 20,
    customer_understanding: 20,
    persuasion: 10
  }
  return weights[dimension] || 0
}

const getWeightedScore = (score, dimension) => {
  return score * getWeight(dimension) / 100
}

const getScoreColor = (score) => {
  if (score >= 80) return '#22c55e' // green
  if (score >= 60) return '#3b82f6' // blue
  if (score >= 40) return '#f59e0b' // yellow
  return '#ef4444' // red
}

const fetchReport = async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`/api/v1/recordings/${id}`)
    recording.value = response.data
    
    // Parse report_json if it's a string
    if (recording.value.report && typeof recording.value.report === 'string') {
      try {
        recording.value.report = JSON.parse(recording.value.report)
      } catch (e) {
        console.error('Failed to parse report:', e)
      }
    }
  } catch (error) {
    console.error('Failed to fetch report:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchReport()
})
</script>
