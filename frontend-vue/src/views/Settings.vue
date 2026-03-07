<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          系统设置
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          配置评分权重和分析工作流
        </p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/models" class="btn btn-secondary">
          模型管理
        </RouterLink>
        <RouterLink to="/workflow" class="btn btn-secondary">
          工作流配置
        </RouterLink>
      </div>
    </div>

    <!-- Scoring Weights -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">评分权重配置</h2>
      </div>
      <div class="card-content">
        <div class="space-y-6">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                表达质量权重
              </label>
              <span class="text-sm text-slate-600 dark:text-slate-400">{{ form.expression_weight * 100 }}%</span>
            </div>
            <input
              v-model.number="form.expression_weight"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              评估语速、停顿、流畅度等表达技巧
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                内容质量权重
              </label>
              <span class="text-sm text-slate-600 dark:text-slate-400">{{ form.content_weight * 100 }}%</span>
            </div>
            <input
              v-model.number="form.content_weight"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              评估内容完整性，专业性、价值传递
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                逻辑结构权重
              </label>
              <span class="text-sm text-slate-600 dark:text-slate-400">{{ form.logic_weight * 100 }}%</span>
            </div>
            <input
              v-model.number="form.logic_weight"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              评估讲解逻辑、层次结构、说服力
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                客户理解权重
              </label>
              <span class="text-sm text-slate-600 dark:text-slate-400">{{ form.customer_weight * 100 }}%</span>
            </div>
            <input
              v-model.number="form.customer_weight"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              评估对客户需求的理解程度
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                说服力权重
              </label>
              <span class="text-sm text-slate-600 dark:text-slate-400">{{ form.persuasion_weight * 100 }}%</span>
            </div>
            <input
              v-model.number="form.persuasion_weight"
              type="range"
              min="0"
              max="1"
              step="0.05"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              评估销售说服技巧、价值表达
            </p>
          </div>

          <div class="pt-4 border-t border-slate-200 dark:border-slate-700">
            <div class="flex items-center justify-between mb-4">
              <span class="text-sm font-medium text-slate-900 dark:text-white">
                总权重
              </span>
              <span 
                :class="totalWeight === 100 ? 'text-green-600' : 'text-red-600'"
                class="text-sm font-bold"
              >
                {{ totalWeight }}%
              </span>
            </div>
            <div v-if="totalWeight !== 100" class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-sm">
              权重总和必须等于100%，当前为 {{ totalWeight }}%
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Workflow -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">分析工作流</h2>
      </div>
      <div class="card-content">
        <div class="space-y-4">
          <div v-for="task in workflowTasks" :key="task.name" 
            class="p-4 rounded-lg border border-slate-200 dark:border-slate-700">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-medium text-slate-900 dark:text-white">{{ task.name }}</h3>
                <p class="text-xs text-slate-500">{{ task.description }}</p>
              </div>
              <select
                v-model="task.model_id"
                @change="updateTaskModel(task.name, task.model_id)"
                class="w-48 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm"
              >
                <option :value="null">默认模型</option>
                <option v-for="model in activeModels" :key="model.id" :value="model.id">
                  {{ model.name }}
                </option>
              </select>
            </div>
            <div v-if="task.model_id" class="text-xs text-green-600">
              ✓ 将使用 {{ getModelName(task.model_id) }} 进行分析
            </div>
            <div v-else class="text-xs text-slate-500">
              将使用系统默认模型
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="flex justify-end gap-3">
      <button @click="resetDefaults" class="btn btn-secondary">
        恢复默认
      </button>
      <button @click="saveSettings" class="btn btn-primary" :disabled="totalWeight !== 100">
        保存设置
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  expression_weight: 0.20,
  content_weight: 0.30,
  logic_weight: 0.20,
  customer_weight: 0.20,
  persuasion_weight: 0.10
})

const workflowTasks = ref([
  { name: '语音转写', description: '将音频转换为文字', model_id: null },
  { name: '内容分析', description: '分析内容完整性和逻辑', model_id: null },
  { name: '情感识别', description: '识别语音情感倾向', model_id: null },
  { name: '说话人识别', description: '识别说话人身份', model_id: null },
  { name: '意图识别', description: '识别客户意图', model_id: null },
  { name: '质量评分', description: '综合评分', model_id: null }
])

const activeModels = ref([])

const totalWeight = computed(() => {
  return Math.round(
    (form.value.expression_weight + 
    form.value.content_weight + 
    form.value.logic_weight + 
    form.value.customer_weight + 
    form.value.persuasion_weight) * 100
  )
})

const fetchSettings = async () => {
  try {
    const scoringConfig = await axios.get('/api/v1/scoring-config')
    
    if (scoringConfig.data) {
      form.value.expression_weight = scoringConfig.data.expression_weight || 0.20
      form.value.content_weight = scoringConfig.data.content_weight || 0.30
      form.value.logic_weight = scoringConfig.data.logic_weight || 0.20
      form.value.customer_weight = scoringConfig.data.customer_weight || 0.20
      form.value.persuasion_weight = scoringConfig.data.persuasion_weight || 0.10
    }
    
    // Fetch task configurations
    const tasksResponse = await axios.get('/api/v1/tasks')
    if (tasksResponse.data.tasks) {
      tasksResponse.data.tasks.forEach(task => {
        const wfTask = workflowTasks.value.find(t => t.name === task.task_name)
        if (wfTask && task.default_model_id) {
          wfTask.model_id = task.default_model_id
        }
      })
    }
    
    // Fetch active models
    const modelsResponse = await axios.get('/api/v1/models')
    activeModels.value = (modelsResponse.data.models || []).filter(m => m.status === 'active')
  } catch (error) {
    console.error('Failed to fetch settings:', error)
  }
}

const getModelName = (modelId) => {
  const model = activeModels.value.find(m => m.id === modelId)
  return model ? model.name : '未知模型'
}

const updateTaskModel = async (taskName, modelId) => {
  try {
    await axios.put(`/api/v1/tasks/${taskName}`, {
      default_model_id: modelId
    })
  } catch (error) {
    console.error('Failed to update task model:', error)
  }
}

const saveSettings = async () => {
  if (totalWeight.value !== 100) {
    alert('权重总和必须等于100%')
    return
  }
  
  try {
    await axios.put('/api/v1/scoring-config', {
      expression_weight: form.value.expression_weight,
      content_weight: form.value.content_weight,
      logic_weight: form.value.logic_weight,
      customer_weight: form.value.customer_weight,
      persuasion_weight: form.value.persuasion_weight
    })
    
    alert('设置已保存')
  } catch (error) {
    console.error('Failed to save settings:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
  }
}

const resetDefaults = () => {
  form.value.expression_weight = 0.20
  form.value.content_weight = 0.30
  form.value.logic_weight = 0.20
  form.value.customer_weight = 0.20
  form.value.persuasion_weight = 0.10
}

onMounted(() => {
  fetchSettings()
})
</script>
