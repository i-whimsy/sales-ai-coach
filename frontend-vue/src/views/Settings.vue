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
      <div class="flex gap-3">
        <router-link to="/models" class="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors">
          模型管理
        </router-link>
      </div>
    </div>

    <!-- Scoring Weights -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">评分权重配置</h2>
      </div>
      <div class="p-6 space-y-6">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-900 dark:text-white">
              表达质量权重
            </label>
            <span class="text-sm text-slate-600 dark:text-slate-400">{{ Math.round(form.expression_weight * 100) }}%</span>
          </div>
          <input
            v-model.number="form.expression_weight"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">
            评估语速、停顿、流畅度等表达技巧
          </p>
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-900 dark:text-white">
              内容质量权重
            </label>
            <span class="text-sm text-slate-600 dark:text-slate-400">{{ Math.round(form.content_weight * 100) }}%</span>
          </div>
          <input
            v-model.number="form.content_weight"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">
            评估内容完整性，专业性、价值传递
          </p>
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-900 dark:text-white">
              逻辑结构权重
            </label>
            <span class="text-sm text-slate-600 dark:text-slate-400">{{ Math.round(form.logic_weight * 100) }}%</span>
          </div>
          <input
            v-model.number="form.logic_weight"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">
            评估讲解逻辑、层次结构、说服力
          </p>
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-900 dark:text-white">
              客户理解权重
            </label>
            <span class="text-sm text-slate-600 dark:text-slate-400">{{ Math.round(form.customer_weight * 100) }}%</span>
          </div>
          <input
            v-model.number="form.customer_weight"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">
            评估对客户需求的理解程度
          </p>
        </div>

        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-900 dark:text-white">
              说服力权重
            </label>
            <span class="text-sm text-slate-600 dark:text-slate-400">{{ Math.round(form.persuasion_weight * 100) }}%</span>
          </div>
          <input
            v-model.number="form.persuasion_weight"
            type="range"
            min="0"
            max="1"
            step="0.05"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
          />
          <p class="text-xs text-slate-500 dark:text-slate-400">
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

    <!-- Prompt Configuration -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Prompt配置</h2>
        <p class="mt-1 text-sm text-slate-600 dark:text-slate-400">
          为每个分析任务配置自定义Prompt。使用{transcript}占位符表示转录文本。
        </p>
      </div>
      <div class="p-6 space-y-4">
        <div v-for="task in workflowTasks" :key="task.name" class="space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="font-medium text-slate-900 dark:text-white">{{ task.name }}</h3>
              <p class="text-xs text-slate-500">{{ task.description }}</p>
            </div>
            <button 
              @click="togglePromptEditor(task.name)"
              class="px-3 py-1.5 text-sm bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
            >
              {{ task.showPromptEditor ? '隐藏' : '编辑Prompt' }}
            </button>
          </div>
          
          <div v-if="task.showPromptEditor" class="mt-2">
            <textarea
              v-model="task.prompt"
              rows="4"
              class="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              placeholder="输入自定义Prompt，使用{transcript}表示转录文本..."
            ></textarea>
            <div class="mt-2 flex justify-between items-center">
              <span class="text-xs text-slate-500">
                长度: {{ task.prompt?.length || 0 }} 字符
              </span>
              <button 
                @click="resetPrompt(task.name)"
                class="px-3 py-1 text-sm bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
              >
                恢复默认
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Workflow -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">分析工作流</h2>
      </div>
      <div class="p-6 space-y-4">
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
              class="w-48 px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-sm"
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

    <!-- Save Button -->
    <div class="flex justify-end gap-3">
      <button @click="resetDefaults" class="px-6 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors">
        恢复默认
      </button>
      <button @click="saveSettings" :disabled="totalWeight !== 100" 
        class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
        保存设置
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  expression_weight: 0.20,
  content_weight: 0.30,
  logic_weight: 0.20,
  customer_weight: 0.20,
  persuasion_weight: 0.10
})

const workflowTasks = ref([
  { name: '语音转写', description: '将音频转换为文字', model_id: null, prompt: '', showPromptEditor: false },
  { name: '内容分析', description: '分析内容完整性和逻辑', model_id: null, prompt: '', showPromptEditor: false },
  { name: '情感识别', description: '识别语音情感倾向', model_id: null, prompt: '', showPromptEditor: false },
  { name: '说话人识别', description: '识别说话人身份', model_id: null, prompt: '', showPromptEditor: false },
  { name: '意图识别', description: '识别客户意图', model_id: null, prompt: '', showPromptEditor: false },
  { name: '质量评分', description: '综合评分', model_id: null, prompt: '', showPromptEditor: false }
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
    try {
      const tasksResponse = await axios.get('/api/v1/tasks')
      if (tasksResponse.data.tasks) {
        tasksResponse.data.tasks.forEach(task => {
          const wfTask = workflowTasks.value.find(t => t.name === task.task_name)
          if (wfTask) {
            if (task.default_model_id) {
              wfTask.model_id = task.default_model_id
            }
            if (task.prompt_config) {
              wfTask.prompt = task.prompt_config
            } else {
              // Set default prompts if not configured
              const defaultPrompts = {
                '语音转写': '请将以下音频转录为文字：{transcript}',
                '内容分析': '请分析以下销售对话的内容完整性和逻辑结构：{transcript}',
                '情感识别': '请识别以下语音的情感倾向：{transcript}',
                '说话人识别': '请识别以下音频中的说话人身份：{transcript}',
                '意图识别': '请识别以下对话中的客户意图：{transcript}',
                '质量评分': '请对以下销售对话进行综合评分：{transcript}'
              }
              wfTask.prompt = defaultPrompts[wfTask.name] || ''
            }
          }
        })
      }
    } catch (e) {
      console.error('Failed to fetch tasks:', e)
    }
    
    // Fetch active models
    try {
      const modelsResponse = await axios.get('/api/v1/models')
      activeModels.value = (modelsResponse.data.models || []).filter(m => m.status === 'active')
    } catch (e) {
      console.error('Failed to fetch models:', e)
    }
  } catch (error) {
    console.error('Failed to fetch settings:', error)
  }
}

const togglePromptEditor = (taskName) => {
  const task = workflowTasks.value.find(t => t.name === taskName)
  if (task) {
    task.showPromptEditor = !task.showPromptEditor
  }
}

const resetPrompt = (taskName) => {
  const task = workflowTasks.value.find(t => t.name === taskName)
  if (task) {
    // 设置默认Prompt
    const defaultPrompts = {
      '语音转写': '请将以下音频转录为文字：{transcript}',
      '内容分析': '请分析以下销售对话的内容完整性和逻辑结构：{transcript}',
      '情感识别': '请识别以下语音的情感倾向：{transcript}',
      '说话人识别': '请识别以下音频中的说话人身份：{transcript}',
      '意图识别': '请识别以下对话中的客户意图：{transcript}',
      '质量评分': '请对以下销售对话进行综合评分：{transcript}'
    }
    task.prompt = defaultPrompts[taskName] || ''
  }
}

const savePromptConfig = async (taskName) => {
  const task = workflowTasks.value.find(t => t.name === taskName)
  if (!task) return
  
  try {
    await axios.put(`/api/v1/tasks/${taskName}`, {
      prompt_config: task.prompt
    })
    alert('Prompt配置已保存')
  } catch (error) {
    console.error('Failed to save prompt:', error)
    alert('保存失败: ' + (error.response?.data?.detail || error.message))
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
    
    // Save prompt configs for each task
    for (const task of workflowTasks.value) {
      if (task.prompt) {
        await axios.put(`/api/v1/tasks/${task.name}`, {
          prompt_config: task.prompt
        }).catch(e => console.error('Failed to save prompt for', task.name, e))
      }
    }
    
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
