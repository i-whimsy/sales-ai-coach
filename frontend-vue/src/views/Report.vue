<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          详细分析报告
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          {{ recording?.file_name }}
        </p>
      </div>
      <div class="flex gap-2">
        <button @click="printReport" class="btn btn-outline gap-2">
          <span class="text-lg">🖨️</span>
          打印报告
        </button>
        <RouterLink to="/history" class="btn btn-secondary">
          返回历史
        </RouterLink>
      </div>
    </div>

    <!-- Summary Card -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">报告摘要</h2>
      </div>
      <div class="card-content">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">上传时间</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ formatDate(recording?.upload_time) }}
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">分析时间</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ new Date().toLocaleString('zh-CN') }}
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">使用模型</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              Whisper Base (本地)
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">评分结果</p>
            <div class="flex items-center gap-3">
              <span class="text-3xl font-bold text-primary-600 dark:text-primary-400">
                {{ recording?.score?.toFixed(1) }}
              </span>
              <span
                class="px-3 py-1 rounded-full text-sm font-medium"
                :class="{
                  'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300': recording?.score < 60,
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300': recording?.score < 80,
                  'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': recording?.score >= 80
                }"
              >
                {{ getScoreLevel(recording?.score) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dimension Scores -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">各维度评分</h2>
      </div>
      <div class="card-content">
        <div class="space-y-4">
          <div
            v-for="(score, dimension) in recording?.report?.dimension_scores"
            :key="dimension"
            class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50"
          >
            <div class="flex justify-between items-center mb-2">
              <span class="font-medium text-slate-900 dark:text-white">
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
            <div class="flex justify-between mt-1 text-xs text-slate-500">
              <span>0</span>
              <span>50</span>
              <span>100</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Strengths -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">优势分析</h2>
      </div>
      <div class="card-content">
        <div class="space-y-3">
          <div
            v-for="(strength, index) in recording?.report?.strengths"
            :key="index"
            class="p-3 rounded-lg border border-green-200 dark:border-green-900/30 bg-green-50 dark:bg-green-900/10"
          >
            <div class="flex items-start gap-3">
              <span class="text-green-600 dark:text-green-400 mt-0.5">✅</span>
              <p class="text-slate-800 dark:text-slate-200 leading-relaxed">
                {{ strength }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Improvement Suggestions -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">改进建议</h2>
      </div>
      <div class="card-content">
        <div class="space-y-3">
          <div
            v-for="(suggestion, index) in recording?.report?.improvement_suggestions"
            :key="index"
            class="p-3 rounded-lg border border-blue-200 dark:border-blue-900/30 bg-blue-50 dark:bg-blue-900/10"
          >
            <div class="flex items-start gap-3">
              <span class="text-blue-600 dark:text-blue-400 mt-0.5">💡</span>
              <p class="text-slate-800 dark:text-slate-200 leading-relaxed">
                {{ suggestion }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Analysis -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">详细分析</h2>
      </div>
      <div class="card-content">
        <!-- Tab Buttons -->
        <div class="flex gap-2 mb-4">
          <button 
            @click="activeTab = 'speech'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="activeTab === 'speech' ? 'bg-primary-600 text-white' : 'bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700'"
          >
            表达质量分析
          </button>
          <button 
            @click="activeTab = 'content'"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="activeTab === 'content' ? 'bg-primary-600 text-white' : 'bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700'"
          >
            内容结构分析
          </button>
        </div>

        <!-- Speech Tab -->
        <div v-if="activeTab === 'speech'" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-1">语速</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.speech_analysis?.speech_rate || '--' }} 词/分钟
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-1">停顿比例</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.speech_analysis?.pause_ratio || '--' }} %
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-1">流畅度</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.speech_analysis?.fluency || '--' }} %
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-1">口头禅</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.speech_analysis?.mantras || '--' }} %
            </p>
          </div>
        </div>

        <!-- Content Tab -->
        <div v-if="activeTab === 'content'" class="space-y-4">
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">内容完整性</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.content_analysis?.total_score || '--' }} / 100
            </p>
            <p class="text-xs text-slate-500 mt-1">
              覆盖了 {{ recording?.report?.content_analysis?.covered_sections || 0 }} / {{ recording?.report?.content_analysis?.total_sections || 0 }} 个部分
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">逻辑结构</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.logic_analysis?.total_score || '--' }} / 100
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">客户理解度</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.customer_analysis?.total_score || '--' }} / 100
            </p>
          </div>
          <div class="p-3 rounded-lg border bg-slate-50 dark:bg-slate-900/50">
            <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">说服力</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              {{ recording?.report?.persuasion_analysis?.total_score || '--' }} / 100
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const activeTab = ref('speech')
const recording = ref(null)

const fetchRecording = async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`/api/v1/recordings/${id}`)
    recording.value = response.data
    
    if (!recording.value.report) {
      router.push(`/analyze/${id}`)
    }
  } catch (error) {
    console.error('Failed to fetch recording:', error)
    router.push('/history')
  }
}

const printReport = () => {
  window.print()
}

const getDimensionName = (dimension) => {
  const names = {
    expression: '表达质量',
    content: '内容完整度',
    logic: '逻辑结构',
    customer_understanding: '客户理解度',
    persuasion: '说服力'
  }
  return names[dimension] || dimension
}

const getScoreLevel = (score) => {
  if (score >= 80) return '优秀'
  if (score >= 60) return '合格'
  return '需要改进'
}

const getScoreColor = (score) => {
  if (score >= 80) return '#10b981' // green
  if (score >= 60) return '#f59e0b' // yellow
  return '#ef4444' // red
}

const formatDate = (dateString) => {
  if (!dateString) return '--'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchRecording()
})
</script>

<style scoped>
@media print {
  .no-print {
    display: none;
  }
}
</style>
