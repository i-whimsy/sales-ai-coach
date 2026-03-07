<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          执行日志
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          查看所有分析任务的执行记录和调用日志
        </p>
      </div>
      <div class="flex gap-2">
        <button @click="refreshLogs" class="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors">
          刷新
        </button>
        <button @click="clearLogs" class="px-4 py-2 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/50 font-medium transition-colors">
          清空日志
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-4">
      <div class="flex flex-wrap gap-4">
        <div class="flex-1 min-w-[200px]">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">搜索</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="搜索日志内容..."
            class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
          />
        </div>
        <div class="w-40">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">类型</label>
          <select
            v-model="filters.type"
            class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
          >
            <option value="">全部</option>
            <option value="api_call">API调用</option>
            <option value="model_call">模型调用</option>
            <option value="analysis">分析</option>
            <option value="error">错误</option>
          </select>
        </div>
        <div class="w-40">
          <label class="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1 block">日期</label>
          <select
            v-model="filters.date"
            class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
          >
            <option value="">全部</option>
            <option value="today">今天</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Log List -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white">
            日志列表 ({{ filteredLogs.length }})
          </h2>
          <label class="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
            <input type="checkbox" v-model="autoRefresh" class="rounded" />
            自动刷新
          </label>
        </div>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="animate-spin text-4xl mb-4">⏳</div>
        <p class="text-slate-600 dark:text-slate-400">加载中...</p>
      </div>
      
      <div v-else-if="filteredLogs.length === 0" class="p-8 text-center">
        <p class="text-slate-600 dark:text-slate-400">暂无日志记录</p>
      </div>
      
      <div v-else class="divide-y divide-slate-200 dark:divide-slate-700">
        <div
          v-for="(log, index) in filteredLogs"
          :key="index"
          class="p-4 hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors"
        >
          <div class="flex items-start gap-4">
            <div 
              class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center"
              :class="getLogIconClass(log.type)"
            >
              <span class="text-lg">{{ getLogIcon(log.type) }}</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1">
                <div class="flex items-center gap-2">
                  <span 
                    class="px-2 py-0.5 rounded text-xs font-medium"
                    :class="getLogTypeClass(log.type)"
                  >
                    {{ getLogTypeName(log.type) }}
                  </span>
                  <span class="font-medium text-slate-900 dark:text-white">
                    {{ log.title }}
                  </span>
                </div>
                <span class="text-xs text-slate-500">
                  {{ formatTime(log.timestamp) }}
                </span>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-400 mb-2">
                {{ log.message }}
              </p>
              <div v-if="log.details" class="mt-2 p-3 bg-slate-100 dark:bg-slate-900 rounded-lg">
                <pre class="text-xs text-slate-600 dark:text-slate-400 whitespace-pre-wrap overflow-x-auto">{{ log.details }}</pre>
              </div>
              <div v-if="log.model_info" class="mt-2 flex flex-wrap gap-2">
                <span 
                  v-for="(info, key) in log.model_info"
                  :key="key"
                  class="px-2 py-1 bg-slate-200 dark:bg-slate-700 rounded text-xs text-slate-700 dark:text-slate-300"
                >
                  {{ key }}: {{ info }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Button -->
    <div class="flex justify-end">
      <button @click="exportLogs" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors">
        导出日志
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const autoRefresh = ref(false)
const logs = ref([])

const filters = ref({
  search: '',
  type: '',
  date: ''
})

// Sample log data (in real app, this would come from backend)
const sampleLogs = ref([
  {
    id: 1,
    type: 'model_call',
    title: '调用语音识别模型',
    message: '使用 OpenAI Whisper API 进行语音转文字',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    details: 'API URL: https://api.openai.com/v1/audio/transcriptions\nModel: whisper-1\nLanguage: zh',
    model_info: {
      '模型': 'OpenAI Whisper API',
      '类型': 'API',
      '耗时': '1.2s'
    }
  },
  {
    id: 2,
    type: 'analysis',
    title: '执行内容分析',
    message: '分析转录文本的内容完整性和逻辑结构',
    timestamp: new Date(Date.now() - 1000 * 60 * 10).toISOString(),
    details: 'Prompt: 请分析以下销售对话的内容完整性和逻辑结构\n转录长度: 1250字符',
    model_info: {
      '模型': 'OpenAI GPT-4o',
      '类型': 'API',
      '耗时': '2.5s'
    }
  },
  {
    id: 3,
    type: 'model_call',
    title: '调用情感分析模型',
    message: '使用本地模型识别语音情感倾向',
    timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    details: 'Model: 本地情感分析模型\nCommand: python -m transformers_pipeline --task sentiment-analysis',
    model_info: {
      '模型': '本地情感分析模型',
      '类型': '本地程序',
      '耗时': '3.8s'
    }
  },
  {
    id: 4,
    type: 'api_call',
    title: '调用评分API',
    message: '调用自定义评分模型进行综合评分',
    timestamp: new Date(Date.now() - 1000 * 60 * 20).toISOString(),
    details: 'Endpoint: http://localhost:8001/api/v1/scoring\nMethod: POST',
    model_info: {
      '模型': '自定义评分模型API',
      '类型': 'API',
      '耗时': '0.8s'
    }
  },
  {
    id: 5,
    type: 'error',
    title: '模型调用失败',
    message: '调用百度情感分析API时发生错误',
    timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    details: 'Error: 401 Unauthorized\nAPI Key无效或已过期',
    model_info: {
      '模型': '百度情感分析API',
      '类型': 'API'
    }
  }
])

const filteredLogs = computed(() => {
  let result = logs.value
  
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(log => 
      log.title.toLowerCase().includes(search) || 
      log.message.toLowerCase().includes(search)
    )
  }
  
  if (filters.value.type) {
    result = result.filter(log => log.type === filters.value.type)
  }
  
  if (filters.value.date) {
    const now = new Date()
    result = result.filter(log => {
      const logDate = new Date(log.timestamp)
      if (filters.value.date === 'today') {
        return logDate.toDateString() === now.toDateString()
      } else if (filters.value.date === 'week') {
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
        return logDate >= weekAgo
      } else if (filters.value.date === 'month') {
        const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
        return logDate >= monthAgo
      }
      return true
    })
  }
  
  return result
})

const getLogIcon = (type) => {
  const icons = {
    'api_call': '🌐',
    'model_call': '🤖',
    'analysis': '📊',
    'error': '❌'
  }
  return icons[type] || '📝'
}

const getLogIconClass = (type) => {
  const classes = {
    'api_call': 'bg-blue-100 dark:bg-blue-900/30',
    'model_call': 'bg-purple-100 dark:bg-purple-900/30',
    'analysis': 'bg-green-100 dark:bg-green-900/30',
    'error': 'bg-red-100 dark:bg-red-900/30'
  }
  return classes[type] || 'bg-slate-100 dark:bg-slate-900/30'
}

const getLogTypeName = (type) => {
  const names = {
    'api_call': 'API调用',
    'model_call': '模型调用',
    'analysis': '分析',
    'error': '错误'
  }
  return names[type] || type
}

const getLogTypeClass = (type) => {
  const classes = {
    'api_call': 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
    'model_call': 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
    'analysis': 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
    'error': 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300'
  }
  return classes[type] || 'bg-slate-100 text-slate-800 dark:bg-slate-900/50 dark:text-slate-300'
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchLogs = async () => {
  loading.value = true
  try {
    // In a real app, this would fetch from backend API
    // const response = await axios.get('/api/v1/logs')
    // logs.value = response.data
    
    // Using sample data for now
    logs.value = sampleLogs.value
  } catch (error) {
    console.error('Failed to fetch logs:', error)
  } finally {
    loading.value = false
  }
}

const refreshLogs = () => {
  fetchLogs()
}

const clearLogs = () => {
  if (confirm('确定要清空所有日志吗？此操作不可恢复。')) {
    logs.value = []
  }
}

const exportLogs = () => {
  const data = JSON.stringify(filteredLogs.value, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `logs_${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}

let autoRefreshInterval = null

onMounted(() => {
  fetchLogs()
  
  if (autoRefresh.value) {
    autoRefreshInterval = setInterval(refreshLogs, 30000)
  }
})

onUnmounted(() => {
  if (autoRefreshInterval) {
    clearInterval(autoRefreshInterval)
  }
})
</script>
