<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          系统设置
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          配置API密钥和评分参数
        </p>
      </div>
      <RouterLink to="/models" class="btn btn-secondary">
        前往模型管理
      </RouterLink>
    </div>

    <!-- API Keys -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">API密钥配置</h2>
      </div>
      <div class="card-content">
        <div class="space-y-6">
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                OpenAI API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                <a href="https://platform.openai.com" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline">官方网站</a>
              </span>
            </div>
            <input
              v-model="form.openai_api_key"
              type="password"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              用于GPT-4o等OpenAI模型
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                Claude API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                <a href="https://www.anthropic.com" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline">官方网站</a>
              </span>
            </div>
            <input
              v-model="form.claude_api_key"
              type="password"
              placeholder="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              用于Claude模型，长文本处理能力强
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                DeepSeek API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                <a href="https://www.deepseek.com" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline">官方网站</a>
              </span>
            </div>
            <input
              v-model="form.deepseek_api_key"
              type="password"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              用于DeepSeek模型，中文支持好，性价比高
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                Whisper API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                <a href="https://openai.com/research/whisper" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline">官方网站</a>
              </span>
            </div>
            <input
              v-model="form.whisper_api_key"
              type="password"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              用于Whisper语音识别模型
            </p>
          </div>

          <div class="mt-4 p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
            <h3 class="text-sm font-medium text-green-800 dark:text-green-300 mb-2">📡 配置说明</h3>
            <div class="space-y-2 text-xs text-slate-600 dark:text-slate-300">
              <p>• <strong>模型管理：</strong>请前往 <RouterLink to="/models" class="text-blue-600 hover:underline">模型管理页面</RouterLink> 激活和管理AI模型</p>
              <p>• <strong>API密钥：</strong>配置在对应模型的详情页中，输入密钥后模型会自动激活</p>
              <p>• <strong>本地模式：</strong>也可使用本地模型（无需API密钥），在模型管理中下载安装</p>
              <p>• <strong>安全提示：</strong>所有API密钥仅存储在本地数据库，不会上传到任何第三方</p>
            </div>
          </div>
        </div>
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
              评估内容完整性、专业性、价值传递
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
  openai_api_key: '',
  claude_api_key: '',
  deepseek_api_key: '',
  whisper_api_key: '',
  expression_weight: 0.20,
  content_weight: 0.30,
  logic_weight: 0.20,
  customer_weight: 0.20,
  persuasion_weight: 0.10
})

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
    const [apiConfig, scoringConfig] = await Promise.all([
      axios.get('/api/v1/api-config'),
      axios.get('/api/v1/scoring-config')
    ])
    
    if (apiConfig.data) {
      form.value.openai_api_key = apiConfig.data.openai_api_key || ''
      form.value.claude_api_key = apiConfig.data.claude_api_key || ''
      form.value.deepseek_api_key = apiConfig.data.deepseek_api_key || ''
      form.value.whisper_api_key = apiConfig.data.whisper_api_key || ''
    }
    
    if (scoringConfig.data) {
      form.value.expression_weight = scoringConfig.data.expression_weight || 0.20
      form.value.content_weight = scoringConfig.data.content_weight || 0.30
      form.value.logic_weight = scoringConfig.data.logic_weight || 0.20
      form.value.customer_weight = scoringConfig.data.customer_weight || 0.20
      form.value.persuasion_weight = scoringConfig.data.persuasion_weight || 0.10
    }
  } catch (error) {
    console.error('Failed to fetch settings:', error)
  }
}

const saveSettings = async () => {
  if (totalWeight.value !== 100) {
    alert('权重总和必须等于100%')
    return
  }
  
  try {
    await axios.put('/api/v1/api-config', {
      openai_api_key: form.value.openai_api_key,
      claude_api_key: form.value.claude_api_key,
      deepseek_api_key: form.value.deepseek_api_key,
      whisper_api_key: form.value.whisper_api_key
    })
    
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
