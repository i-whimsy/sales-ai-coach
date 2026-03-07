<template>
  <div class="space-y-8">
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin text-4xl mb-4">⏳</div>
      <p class="text-slate-600 dark:text-slate-400">加载中...</p>
    </div>
    <template v-else>
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          录音分析
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          {{ recording?.file_name }}
        </p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/history" class="btn btn-secondary">
          返回历史
        </RouterLink>
        <button
          v-if="recording?.status !== 'analyzed'"
          @click="startAnalysis"
          :disabled="analyzing"
          class="btn btn-primary"
        >
          {{ analyzing ? '分析中...' : '开始分析' }}
        </button>
      </div>
    </div>

    <!-- Status Card -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">处理状态</h2>
      </div>
      <div class="card-content">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="font-medium text-slate-900 dark:text-white">当前状态</span>
            <span
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="{
                'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300': recording?.status === 'uploaded',
                'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': recording?.status === 'analyzed',
                'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300': analyzing
              }"
            >
              {{ getStatusText() }}
            </span>
          </div>

          <div v-if="analyzing">
            <div class="space-y-2">
              <div class="w-full bg-slate-200 rounded-full dark:bg-slate-800 h-2">
                <div class="bg-primary-600 h-2 rounded-full" :style="{ width: `${progress}%` }"></div>
              </div>
              <p class="text-sm text-slate-500 text-right">
                {{ progress.toFixed(1) }}% 完成
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Processing Logs -->
    <div v-if="logs.length > 0" class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">处理日志</h2>
      </div>
      <div class="card-content">
        <div class="space-y-3">
          <div
            v-for="log in logs"
            :key="log.timestamp"
            class="p-3 rounded-lg border"
            :class="{
              'border-blue-200 bg-blue-50 dark:border-blue-900/30 dark:bg-blue-900/10': log.status === 'in_progress',
              'border-green-200 bg-green-50 dark:border-green-900/30 dark:bg-green-900/10': log.status === 'completed',
              'border-red-200 bg-red-50 dark:border-red-900/30 dark:bg-red-900/10': log.status === 'failed'
            }"
          >
            <div class="flex items-start gap-3">
              <div class="mt-0.5">
                <span v-if="log.status === 'in_progress'" class="text-yellow-600">⏳</span>
                <span v-else-if="log.status === 'completed'" class="text-green-600">✅</span>
                <span v-else class="text-red-600">❌</span>
              </div>
              <div class="flex-1">
                <div class="flex justify-between">
                  <h3 class="font-medium text-slate-900 dark:text-white">{{ log.step }}</h3>
                  <span class="text-xs text-slate-500 dark:text-slate-500">
                    {{ formatTime(log.timestamp) }}
                  </span>
                </div>
                <p class="text-sm text-slate-700 dark:text-slate-300 mt-1">{{ log.details }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Transcript -->
    <div v-if="recording?.transcript" class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">语音转文本结果</h2>
      </div>
      <div class="card-content">
        <div class="flex items-center justify-between mb-4">
          <span class="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
            使用模型: Whisper Base (本地)
          </span>
          <button
            @click="downloadTranscript"
            class="btn btn-outline gap-2"
          >
            <span class="text-lg">📥</span>
            下载文本
          </button>
        </div>

        <div class="border rounded-lg p-4 bg-slate-50 dark:bg-slate-900/50 max-h-96 overflow-y-auto">
          <pre class="text-sm text-slate-800 dark:text-slate-200 whitespace-pre-wrap leading-relaxed">
{{ recording?.transcript || '暂无转录文本' }}
          </pre>
        </div>
      </div>
    </div>

    <!-- Score Summary -->
    <div v-if="recording?.score !== null" class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">评分结果</h2>
      </div>
      <div class="card-content">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20">
            <p class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">总分</p>
            <p class="text-3xl font-bold text-blue-700 dark:text-blue-300">
              {{ recording?.score?.toFixed(1) || '--' }}
            </p>
          </div>
          <div class="text-center p-4 rounded-lg bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20">
            <p class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">表达得分</p>
            <p class="text-2xl font-bold text-purple-700 dark:text-purple-300">
              {{ recording?.report?.dimension_scores?.expression || '--' }}
            </p>
          </div>
          <div class="text-center p-4 rounded-lg bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20">
            <p class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">内容得分</p>
            <p class="text-2xl font-bold text-green-700 dark:text-green-300">
              {{ recording?.report?.dimension_scores?.content || '--' }}
            </p>
          </div>
          <div class="text-center p-4 rounded-lg bg-gradient-to-br from-amber-50 to-amber-100 dark:from-amber-900/20 dark:to-amber-800/20">
            <p class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">逻辑得分</p>
            <p class="text-2xl font-bold text-amber-700 dark:text-amber-300">
              {{ recording?.report?.dimension_scores?.logic || '--' }}
            </p>
          </div>
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const recording = ref(null)
const analyzing = ref(false)
const progress = ref(0)
const logs = ref([])
const loading = ref(true)

const fetchRecording = async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`/api/v1/recordings/${id}`)
    recording.value = response.data
  } catch (error) {
    console.error('Failed to fetch recording:', error)
  } finally {
    loading.value = false
  }
}

const fetchLogs = async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`/api/v1/recordings/${id}/logs`)
    logs.value = response.data.logs
    
    // Update progress
    const completed = response.data.logs.filter(l => l.status === 'completed').length
    const total = response.data.logs.length
    if (total > 0) {
      progress.value = (completed / total) * 100
    }
  } catch (error) {
    console.error('Failed to fetch logs:', error)
  }
}

const startAnalysis = async () => {
  analyzing.value = true
  progress.value = 0

  try {
    const id = route.params.id
    const response = await axios.post(`/api/v1/recordings/${id}/analyze`)
    recording.value = response.data
    analyzing.value = false
    
    // Refresh logs one final time
    await fetchLogs()
  } catch (error) {
    console.error('Failed to analyze recording:', error)
    analyzing.value = false
  }
}

const downloadTranscript = async () => {
  try {
    const id = route.params.id
    const response = await axios.get(`/api/v1/recordings/${id}/transcript`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `transcript_${id}.txt`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Failed to download transcript:', error)
  }
}

const getStatusText = () => {
  if (analyzing.value) return '分析中...'
  if (recording?.value?.status === 'uploaded') return '已上传'
  if (recording?.value?.status === 'analyzed') return '已分析'
  return '未知'
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN')
}

onMounted(() => {
  fetchRecording()
  
  // Poll logs every second if analyzing
  const interval = setInterval(() => {
    if (analyzing.value || recording.value?.status !== 'analyzed') {
      fetchLogs()
    }
  }, 1000)

  return () => clearInterval(interval)
})
</script>

<style scoped>
p {
  margin: 0;
}
</style>
