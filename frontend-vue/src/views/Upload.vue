<template>
  <div class="space-y-8">
    <div class="text-center">
      <h1 class="text-4xl font-bold tracking-tight text-slate-900 dark:text-white">
        上传录音文件
      </h1>
      <p class="mt-4 text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
        上传你的销售讲解录音，AI 将为你分析表达质量、内容完整性、逻辑结构和客户理解度
      </p>
    </div>

    <!-- File Upload Area -->
    <div class="max-w-3xl mx-auto">
      <div
        class="border-2 border-dashed rounded-xl p-8 text-center transition-colors duration-200"
        :class="{
          'border-blue-500 bg-blue-50 dark:bg-blue-900/20': isDragging,
          'border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-900': !isDragging
        }"
        @dragover.prevent="handleDragOver"
        @dragleave="handleDragLeave"
        @drop.prevent="handleDrop"
      >
        <div v-if="selectedFile" class="space-y-6">
          <div class="text-green-600 dark:text-green-400">
            <span class="text-4xl">✅</span>
          </div>
          <div class="space-y-2">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-white">文件已选择</h3>
            <p class="text-lg text-slate-700 dark:text-slate-300 truncate">{{ selectedFile.name }}</p>
            <p class="text-sm text-slate-500 dark:text-slate-500">
              大小: {{ formatFileSize(selectedFile.size) }}
            </p>
          </div>
          <div class="flex gap-3 justify-center">
            <button @click="clearFile" class="btn btn-secondary">重新选择</button>
            <button @click="uploadFile" class="btn btn-primary" :disabled="uploading">
              {{ uploading ? '上传中...' : '开始上传' }}
            </button>
          </div>
        </div>
        
        <div v-else class="space-y-6">
          <div class="text-slate-400">
            <span class="text-4xl">📁</span>
          </div>
          <div class="space-y-3">
            <h3 class="text-xl font-semibold text-slate-900 dark:text-white">选择录音文件</h3>
            <p class="text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto">
              支持 MP3、WAV、M4A 格式，最大 200MB
            </p>
          </div>
          
          <!-- Custom Name Input -->
          <div class="max-w-md mx-auto w-full space-y-4">
            <input
              v-model="customName"
              type="text"
              placeholder="自定义文件名（可选）"
              class="w-full px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
            />
            
            <!-- Model Selection -->
            <div class="flex items-center gap-2 justify-center">
              <label class="text-sm text-slate-600 dark:text-slate-400">选择模型:</label>
              <select
                v-model="selectedModelId"
                class="px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm"
              >
                <option :value="null">默认模型</option>
                <option v-for="model in availableModels" :key="model.id" :value="model.id">
                  {{ model.name }} ({{ model.type === 'online' ? '在线' : '本地' }})
                </option>
              </select>
            </div>
          </div>
          
          <div class="flex flex-col gap-3 items-center">
            <button @click="triggerFileInput" class="btn btn-primary px-8">
              浏览文件
            </button>
            <p class="text-xs text-slate-500 dark:text-slate-500">
              或拖拽文件到此处
            </p>
          </div>
        </div>

        <input
          ref="fileInput"
          type="file"
          accept=".mp3,.wav,.m4a"
          @change="handleFileSelect"
          class="hidden"
        />
      </div>
    </div>

    <!-- Upload Progress -->
    <div v-if="uploading" class="max-w-3xl mx-auto">
      <div class="card">
        <div class="card-header">
          <h4 class="text-lg font-semibold text-slate-900 dark:text-white">上传进度</h4>
        </div>
        <div class="card-content">
          <div class="space-y-4">
            <div class="w-full bg-slate-200 rounded-full dark:bg-slate-800 h-2.5">
              <div class="bg-primary-600 h-2.5 rounded-full" :style="{ width: `${uploadProgress}%` }"></div>
            </div>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              已上传: {{ uploadProgress.toFixed(1) }}%
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="max-w-3xl mx-auto">
      <div class="rounded-lg bg-red-50 p-4 text-red-700 dark:bg-red-900/20 dark:text-red-400">
        <div class="flex items-center gap-2">
          <span class="text-lg">❌</span>
          <p>{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="successData" class="max-w-3xl mx-auto">
      <div class="rounded-lg bg-green-50 p-4 text-green-700 dark:bg-green-900/20 dark:text-green-400">
        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-2">
            <span class="text-lg">✅</span>
            <div>
              <p class="font-medium">文件上传成功！</p>
              <p class="text-sm">文件ID: {{ successData.id }}</p>
            </div>
          </div>
          <div class="flex justify-end gap-3">
            <button
              @click="router.push('/history')"
              class="btn btn-secondary"
            >
              返回历史
            </button>
            <button
              @click="router.push(`/analyze/${successData.id}`)"
              class="btn btn-primary"
            >
              开始分析
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- File Requirements -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
      <div class="card p-5">
        <div class="flex items-center gap-3">
          <span class="text-xl">🎧</span>
          <div>
            <h4 class="font-semibold text-slate-900 dark:text-white">支持格式</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              MP3、WAV、M4A
            </p>
          </div>
        </div>
      </div>
      <div class="card p-5">
        <div class="flex items-center gap-3">
          <span class="text-xl">📏</span>
          <div>
            <h4 class="font-semibold text-slate-900 dark:text-white">文件大小</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400">
              最大 200MB
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const fileInput = ref(null)
const selectedFile = ref(null)
const customName = ref('')
const selectedModelId = ref(null)
const availableModels = ref([])

const fetchAvailableModels = async () => {
  try {
    const response = await axios.get('/api/v1/models')
    availableModels.value = (response.data.models || []).filter(m => m.status === 'active')
  } catch (error) {
    console.error('Failed to fetch models:', error)
  }
}

onMounted(() => {
  fetchAvailableModels()
})
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const error = ref(null)
const successData = ref(null)

const allowedExtensions = ['mp3', 'wav', 'm4a']
const maxFileSize = 200 * 1024 * 1024 // 200MB

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = Array.from(event.dataTransfer.files)
  if (files.length > 0) {
    validateFile(files[0])
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateFile(file)
  }
}

const validateFile = (file) => {
  const fileExtension = file.name.split('.').pop()?.toLowerCase() || ''
  
  // Validate file extension
  if (!allowedExtensions.includes(fileExtension)) {
    error.value = `无效的文件格式。请上传 ${allowedExtensions.join('、')} 文件。`
    return
  }

  // Validate file size
  if (file.size > maxFileSize) {
    error.value = `文件大小超过限制。请上传小于 200MB 的文件。`
    return
  }

  selectedFile.value = file
  error.value = null
}

const clearFile = () => {
  selectedFile.value = null
  error.value = null
  successData.value = null
}

const uploadFile = async () => {
  if (!selectedFile.value) return

  uploading.value = true
  error.value = null
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    if (customName.value.trim()) {
      formData.append('name', customName.value.trim())
    }
    if (selectedModelId.value) {
      formData.append('model_id', selectedModelId.value)
    }

    const response = await axios.post('/api/v1/recordings', formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          uploadProgress.value = (progressEvent.loaded / progressEvent.total) * 100
        }
      }
    })

    successData.value = response.data
    uploading.value = false
    selectedFile.value = null
  } catch (err) {
    error.value = err.response?.data?.detail || '上传失败，请重试。'
    uploading.value = false
  }
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB'
  else return (bytes / 1048576).toFixed(2) + ' MB'
}
</script>

<style scoped>
</style>
