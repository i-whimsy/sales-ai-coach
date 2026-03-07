<template>
  <div class="max-w-7xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-3xl font-bold text-slate-900 dark:text-white">模型管理</h2>
        <p class="mt-1 text-slate-600 dark:text-slate-400">管理系统中的AI模型配置</p>
      </div>
      <button @click="showAddModal = true" class="btn-primary">
        <span class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          添加模型
        </span>
      </button>
    </div>

    <!-- 筛选器 -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-4 mb-6">
      <div class="flex flex-wrap gap-4">
        <select v-model="filterType" class="form-select w-auto">
          <option value="">全部类型</option>
          <option value="api">API模型</option>
          <option value="local_service">本地服务</option>
          <option value="local_program">本地程序</option>
        </select>
        <select v-model="filterCategory" class="form-select w-auto">
          <option value="">全部类别</option>
          <option value="ASR">语音识别</option>
          <option value="NLP">自然语言处理</option>
          <option value="EMOTION">情感分析</option>
          <option value="VOICEPRINT">声纹识别</option>
          <option value="INTENT">意图识别</option>
          <option value="SCORE">评分模型</option>
        </select>
        <select v-model="filterStatus" class="form-select w-auto">
          <option value="">全部状态</option>
          <option value="active">已激活</option>
          <option value="inactive">未激活</option>
        </select>
      </div>
    </div>

    <!-- 模型列表 -->
    <div class="grid gap-4">
      <div v-for="model in filteredModels" :key="model.id" 
        class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-3">
              <h3 class="text-lg font-semibold text-slate-900 dark:text-white">{{ model.name }}</h3>
              <span :class="getTypeBadgeClass(model.type)" class="badge">{{ getTypeName(model.type) }}</span>
              <span :class="getCategoryBadgeClass(model.category)" class="badge">{{ getCategoryName(model.category) }}</span>
              <span :class="getStatusBadgeClass(model.status)" class="badge">{{ model.status === 'active' ? '已激活' : '未激活' }}</span>
            </div>
            <div class="mt-2 text-sm text-slate-600 dark:text-slate-400">
              <p>供应商: {{ model.provider || '未设置' }}</p>
              <p v-if="model.type === 'api'">API地址: {{ model.api_url || '未设置' }}</p>
              <p v-if="model.type === 'local_service'">服务地址: {{ model.api_url || '未设置' }}</p>
              <p v-if="model.type === 'local_program'">程序路径: {{ model.local_path || '未设置' }}</p>
              <p>模型标识: {{ model.model_name || '未设置' }}</p>
            </div>
            <!-- 标签 -->
            <div class="mt-3 flex flex-wrap gap-2">
              <span v-for="tag in model.tags" :key="tag.id" 
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                :style="{ backgroundColor: tag.color + '20', color: tag.color }">
                {{ tag.name }}
              </span>
            </div>
          </div>
          <div class="flex items-center gap-2 ml-4">
            <button @click="testModel(model)" class="btn-secondary text-sm py-1.5 px-3">
              测试
            </button>
            <button @click="editModel(model)" class="btn-secondary text-sm py-1.5 px-3">
              编辑
            </button>
            <button @click="toggleModelStatus(model)" 
              :class="model.status === 'active' ? 'btn-warning' : 'btn-success'" 
              class="text-sm py-1.5 px-3">
              {{ model.status === 'active' ? '停用' : '激活' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredModels.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-slate-900 dark:text-white">没有找到模型</h3>
      <p class="mt-1 text-sm text-slate-500">尝试添加一个新的模型</p>
    </div>

    <!-- 添加/编辑模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex min-h-screen items-center justify-center p-4">
        <div class="fixed inset-0 bg-black/50" @click="closeModal"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-2xl p-6 max-h-[90vh] overflow-y-auto">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-6">
            {{ showEditModal ? '编辑模型' : '添加模型' }}
          </h3>
          <form @submit.prevent="saveModel" class="space-y-4">
            <!-- 基本信息 -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">模型名称</label>
                <input v-model="modelForm.name" type="text" class="form-input" required />
              </div>
              <div>
                <label class="form-label">模型类型</label>
                <select v-model="modelForm.type" class="form-select" required @change="onTypeChange">
                  <option value="api">API模型 (云服务)</option>
                  <option value="local_service">本地服务 (Ollama等)</option>
                  <option value="local_program">本地程序 (faster-whisper等)</option>
                </select>
              </div>
              <div>
                <label class="form-label">类别</label>
                <select v-model="modelForm.category" class="form-select" required>
                  <option value="ASR">语音识别</option>
                  <option value="NLP">自然语言处理</option>
                  <option value="EMOTION">情感分析</option>
                  <option value="VOICEPRINT">声纹识别</option>
                  <option value="INTENT">意图识别</option>
                  <option value="SCORE">评分模型</option>
                </select>
              </div>
              <div>
                <label class="form-label">供应商</label>
                <input v-model="modelForm.provider" type="text" class="form-input" />
              </div>
              <div>
                <label class="form-label">模型标识</label>
                <input v-model="modelForm.model_name" type="text" class="form-input" :placeholder="modelPlaceholder" />
              </div>
              <div>
                <label class="form-label">设为默认</label>
                <label class="flex items-center gap-2 mt-2">
                  <input v-model="modelForm.is_default" type="checkbox" class="form-checkbox" />
                  <span class="text-sm text-slate-600 dark:text-slate-400">设为系统默认模型</span>
                </label>
              </div>
            </div>

            <!-- API模型配置 -->
            <div v-if="modelForm.type === 'api'" class="space-y-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <h4 class="font-medium text-blue-900 dark:text-blue-300">API模型配置</h4>
              <div>
                <label class="form-label">API地址</label>
                <input v-model="modelForm.api_url" type="text" class="form-input" placeholder="https://api.openai.com/v1/chat/completions" />
              </div>
              <div>
                <label class="form-label">API密钥</label>
                <input v-model="modelForm.api_key" type="password" class="form-input" placeholder="sk-xxxxxxxxxxxxx" />
              </div>
            </div>

            <!-- 本地服务配置 -->
            <div v-if="modelForm.type === 'local_service'" class="space-y-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <h4 class="font-medium text-green-900 dark:text-green-300">本地服务配置</h4>
              <p class="text-xs text-green-700 dark:text-green-400">运行 Ollama、LocalAI 等本地模型服务</p>
              <div>
                <label class="form-label">服务地址</label>
                <input v-model="modelForm.api_url" type="text" class="form-input" placeholder="http://localhost:11434" />
              </div>
              <div>
                <label class="form-label">API密钥 (可选)</label>
                <input v-model="modelForm.api_key" type="password" class="form-input" placeholder="如需认证则填写" />
              </div>
            </div>

            <!-- 本地程序配置 -->
            <div v-if="modelForm.type === 'local_program'" class="space-y-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
              <h4 class="font-medium text-purple-900 dark:text-purple-300">本地程序配置</h4>
              <p class="text-xs text-purple-700 dark:text-purple-400">直接调用本地Python程序或命令行工具</p>
              <div>
                <label class="form-label">程序/命令路径</label>
                <input v-model="modelForm.local_path" type="text" class="form-input" placeholder="D:\models\whisper 或 whisper.exe" />
              </div>
              <div>
                <label class="form-label">运行参数 (可选)</label>
                <input v-model="modelForm.command_args" type="text" class="form-input" placeholder="--model base --language zh" />
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6">
              <button type="button" @click="closeModal" class="btn-secondary">取消</button>
              <button type="submit" class="btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 测试结果弹窗 -->
    <div v-if="showTestModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex min-h-screen items-center justify-center p-4">
        <div class="fixed inset-0 bg-black/50" @click="showTestModal = false"></div>
        <div class="relative bg-white dark:bg-slate-800 rounded-2xl shadow-xl w-full max-w-lg p-6">
          <h3 class="text-xl font-bold text-slate-900 dark:text-white mb-4">模型测试结果</h3>
          <div v-if="testResult.success" class="text-green-600 dark:text-green-400">
            <p class="font-medium">测试成功!</p>
            <pre class="mt-2 bg-slate-100 dark:bg-slate-700 p-4 rounded-lg text-sm overflow-auto">{{ JSON.stringify(testResult.result, null, 2) }}</pre>
          </div>
          <div v-else class="text-red-600 dark:text-red-400">
            <p class="font-medium">测试失败</p>
            <p class="mt-2">{{ testResult.error }}</p>
          </div>
          <div class="flex justify-end mt-6">
            <button @click="showTestModal = false" class="btn-primary">关闭</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = '/api/v1'

const models = ref([])
const filterType = ref('')
const filterCategory = ref('')
const filterStatus = ref('')

const showAddModal = ref(false)
const showEditModal = ref(false)
const showTestModal = ref(false)
const testResult = ref({})

const modelForm = ref({
  id: null,
  name: '',
  type: 'api',
  category: 'ASR',
  provider: '',
  model_name: '',
  api_url: '',
  api_key: '',
  local_path: '',
  command_args: '',
  is_default: false
})

const modelPlaceholders = {
  api: '如: gpt-4o, whisper-1',
  local_service: '如: llama3, mistral',
  local_program: '如: base, small'
}

const modelPlaceholder = computed(() => modelPlaceholders[modelForm.value.type] || '')

const filteredModels = computed(() => {
  return models.value.filter(model => {
    if (filterType.value && model.type !== filterType.value) return false
    if (filterCategory.value && model.category !== filterCategory.value) return false
    if (filterStatus.value && model.status !== filterStatus.value) return false
    return true
  })
})

const onTypeChange = () => {
  // 清空相关字段
  modelForm.value.api_url = ''
  modelForm.value.api_key = ''
  modelForm.value.local_path = ''
  modelForm.value.command_args = ''
}

const getTypeName = (type) => {
  const names = {
    api: 'API模型',
    local_service: '本地服务',
    local_program: '本地程序'
  }
  return names[type] || type
}

const getCategoryName = (category) => {
  const names = {
    ASR: '语音识别',
    NLP: '自然语言处理',
    EMOTION: '情感分析',
    VOICEPRINT: '声纹识别',
    INTENT: '意图识别',
    SCORE: '评分模型'
  }
  return names[category] || category
}

const getTypeBadgeClass = (type) => {
  const classes = {
    api: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    local_service: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    local_program: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

const getCategoryBadgeClass = (category) => {
  const classes = {
    ASR: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    NLP: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    EMOTION: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    VOICEPRINT: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    INTENT: 'bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200',
    SCORE: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200'
  }
  return classes[category] || 'bg-gray-100 text-gray-800'
}

const getStatusBadgeClass = (status) => {
  return status === 'active'
    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const fetchModels = async () => {
  try {
    const response = await axios.get(`${API_BASE}/models`)
    models.value = response.data.models || []
  } catch (error) {
    console.error('Failed to fetch models:', error)
  }
}

const saveModel = async () => {
  try {
    const data = {
      name: modelForm.value.name,
      type: modelForm.value.type,
      category: modelForm.value.category,
      provider: modelForm.value.provider,
      model_name: modelForm.value.model_name,
      api_url: modelForm.value.api_url,
      api_key: modelForm.value.api_key,
      local_path: modelForm.value.local_path,
      command_args: modelForm.value.command_args,
      is_default: modelForm.value.is_default
    }
    
    if (showEditModal.value) {
      await axios.put(`${API_BASE}/models/${modelForm.value.id}`, data)
    } else {
      await axios.post(`${API_BASE}/models`, data)
    }
    
    closeModal()
    fetchModels()
  } catch (error) {
    console.error('Failed to save model:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

const editModel = (model) => {
  modelForm.value = { 
    ...model, 
    is_default: model.is_default || false,
    command_args: model.command_args || ''
  }
  showEditModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  modelForm.value = {
    id: null,
    name: '',
    type: 'api',
    category: 'ASR',
    provider: '',
    model_name: '',
    api_url: '',
    api_key: '',
    local_path: '',
    command_args: '',
    is_default: false
  }
}

const toggleModelStatus = async (model) => {
  try {
    const newStatus = model.status === 'active' ? 'inactive' : 'active'
    await axios.put(`${API_BASE}/models/${model.id}`, { status: newStatus })
    fetchModels()
  } catch (error) {
    console.error('Failed to toggle model status:', error)
  }
}

const testModel = async (model) => {
  try {
    const response = await axios.post(`${API_BASE}/models/test`, { model_id: model.id })
    testResult.value = response.data
    showTestModal.value = true
  } catch (error) {
    testResult.value = { success: false, error: error.response?.data?.detail || error.message }
    showTestModal.value = true
  }
}

onMounted(() => {
  fetchModels()
})
</script>

<style scoped>
.btn-primary {
  @apply bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors;
}
.btn-secondary {
  @apply bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 px-4 py-2 rounded-lg font-medium transition-colors;
}
.btn-success {
  @apply bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors;
}
.btn-warning {
  @apply bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-medium transition-colors;
}
.form-input {
  @apply w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}
.form-select {
  @apply px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent;
}
.form-checkbox {
  @apply h-4 w-4 text-blue-600 border-slate-300 dark:border-slate-600 rounded;
}
.form-label {
  @apply block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1;
}
.badge {
  @apply px-2 py-0.5 rounded-full text-xs font-medium;
}
</style>