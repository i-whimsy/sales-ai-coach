<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          系统设置
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          配置API密钥和分析参数
        </p>
      </div>
      <div>
        <button @click="saveSettings" class="btn btn-primary">
          保存设置
        </button>
      </div>
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
              type="text"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
            <p class="text-xs text-slate-500 dark:text-slate-500">
              用于GPT-3.5/GPT-4模型进行智能分析，分析质量最高，适合对准确度要求高的场景
            </p>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                Claude API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                用于Claude模型分析
              </span>
            </div>
            <input
              v-model="form.claude_api_key"
              type="text"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                DeepSeek API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                用于DeepSeek模型分析
              </span>
            </div>
            <input
              v-model="form.deepseek_api_key"
              type="text"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                Whisper API Key
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                用于Whisper API服务
              </span>
            </div>
            <input
              v-model="form.whisper_api_key"
              type="text"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              class="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-2 text-sm text-slate-900 dark:text-white"
            />
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
                表达质量权重: {{ form.expression_weight }}%
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                当前占比
              </span>
            </div>
            <input
              v-model.number="form.expression_weight"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                内容完整度权重: {{ form.content_weight }}%
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                当前占比
              </span>
            </div>
            <input
              v-model.number="form.content_weight"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                逻辑结构权重: {{ form.logic_weight }}%
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                当前占比
              </span>
            </div>
            <input
              v-model.number="form.logic_weight"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                客户理解度权重: {{ form.customer_weight }}%
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                当前占比
              </span>
            </div>
            <input
              v-model.number="form.customer_weight"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full"
            />
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <label class="text-sm font-medium text-slate-900 dark:text-white">
                说服力权重: {{ form.persuasion_weight }}%
              </label>
              <span class="text-xs text-slate-500 dark:text-slate-500">
                当前占比
              </span>
            </div>
            <input
              v-model.number="form.persuasion_weight"
              type="range"
              min="0"
              max="100"
              step="1"
              class="w-full"
            />
          </div>

          <div class="mt-6 p-3 rounded-lg bg-slate-100 dark:bg-slate-900/50">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-slate-900 dark:text-white">
                总权重合计: {{ totalWeight }}%
              </span>
              <span
                class="text-xs font-medium px-2 py-1 rounded-full"
                :class="{
                  'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': totalWeight === 100,
                  'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300': totalWeight !== 100
                }"
              >
                {{ totalWeight === 100 ? '✅ 比例均衡' : '⚠️ 比例失衡' }}
              </span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-500 mt-1">
              建议总权重保持为100%以确保评分准确
            </p>
          </div>

          <div class="mt-4 p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
            <h3 class="text-sm font-medium text-blue-800 dark:text-blue-300 mb-2">📊 总分计算逻辑</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mb-2">
              系统采用加权平均法计算最终得分，计算公式为：
            </p>
            <p class="text-xs font-mono bg-white dark:bg-slate-800 p-2 rounded mb-2">
              总分 = (表达质量得分 × 表达权重%) + (内容完整度得分 × 内容权重%) + (逻辑结构得分 × 逻辑权重%) + (客户理解度得分 × 客户权重%) + (说服力得分 × 说服力权重%)
            </p>
            <div class="space-y-1 text-xs text-slate-600 dark:text-slate-300 mb-3">
              <p>• 各维度得分范围：0-100分</p>
              <p>• 最终总分范围：0-100分</p>
              <p>• 80分以上为优秀，60-80分为良好，60分以下需要改进</p>
            </div>
            
            <h4 class="text-sm font-medium text-blue-800 dark:text-blue-300 mb-2">📋 各维度评分标准</h4>
            <div class="space-y-3 text-xs text-slate-600 dark:text-slate-300">
              <div>
                <p class="font-medium">1. 表达质量得分（0-100分）</p>
                <p class="mt-1 pl-2">• 语速（30%）：每分钟120-160字为最优，过快/过慢扣分</p>
                <p class="pl-2">• 流畅度（30%）：根据停顿次数、重复次数、卡顿次数扣分</p>
                <p class="pl-2">• 口头禅（20%）："嗯"、"啊"、"然后"等无意义助词出现频率扣分</p>
                <p class="pl-2">• 语气（20%）：是否热情、自信，有无抑扬顿挫</p>
              </div>
              
              <div>
                <p class="font-medium">2. 内容完整度得分（0-100分）</p>
                <p class="mt-1 pl-2">• 产品介绍（25%）：是否清晰说明产品核心功能和优势</p>
                <p class="pl-2">• 需求挖掘（25%）：是否主动询问客户需求和痛点</p>
                <p class="pl-2">• 方案呈现（25%）：是否针对客户需求给出具体解决方案</p>
                <p class="pl-2">• 价值传递（25%）：是否清晰说明产品能为客户带来的价值</p>
              </div>
              
              <div>
                <p class="font-medium">3. 逻辑结构得分（0-100分）</p>
                <p class="mt-1 pl-2">• 沟通逻辑（40%）：是否遵循"开场-需求挖掘-方案介绍-异议处理-收尾"的合理流程</p>
                <p class="pl-2">• 条理清晰度（30%）：表达是否层次分明，重点突出</p>
                <p class="pl-2">• 前后一致性（30%）：表达内容是否前后一致，无矛盾</p>
              </div>
              
              <div>
                <p class="font-medium">4. 客户理解度得分（0-100分）</p>
                <p class="mt-1 pl-2">• 需求倾听（30%）：是否认真倾听客户讲话，不随意打断</p>
                <p class="pl-2">• 痛点挖掘（30%）：是否准确识别客户核心痛点和顾虑</p>
                <p class="pl-2">• 异议处理（40%）：是否能有效回应客户疑问和反对意见</p>
              </div>
              
              <div>
                <p class="font-medium">5. 说服力得分（0-100分）</p>
                <p class="mt-1 pl-2">• 案例使用（30%）：是否使用成功案例或数据增强说服力</p>
                <p class="pl-2">• 价值表达（30%）：是否能将产品特性转化为客户可感知的利益</p>
                <p class="pl-2">• 成交引导（40%）：是否主动引导客户下一步动作，促进成交</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Info -->
    <div class="card">
      <div class="card-header">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">系统信息</h2>
      </div>
      <div class="card-content">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">后端版本</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              v1.0.0
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">前端框架</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              Vue 3 + Tailwind CSS
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">AI模型</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              Whisper Base (本地)
            </p>
          </div>
          <div>
            <p class="text-sm text-slate-600 dark:text-slate-400">最大文件大小</p>
            <p class="text-lg font-medium text-slate-900 dark:text-white">
              200MB
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  openai_api_key: '',
  claude_api_key: '',
  deepseek_api_key: '',
  whisper_api_key: '',
  expression_weight: 20,
  content_weight: 30,
  logic_weight: 20,
  customer_weight: 20,
  persuasion_weight: 10
})

const loadConfig = async () => {
  try {
    // Load API config
    const apiResponse = await axios.get('/api/v1/api-config')
    form.value.openai_api_key = apiResponse.data.openai_api_key || ''
    form.value.claude_api_key = apiResponse.data.claude_api_key || ''
    form.value.deepseek_api_key = apiResponse.data.deepseek_api_key || ''
    form.value.whisper_api_key = apiResponse.data.whisper_api_key || ''
    
    // Load scoring config
    const scoringResponse = await axios.get('/api/v1/scoring-config')
    form.value.expression_weight = Math.round(scoringResponse.data.expression_weight * 100)
    form.value.content_weight = Math.round(scoringResponse.data.content_weight * 100)
    form.value.logic_weight = Math.round(scoringResponse.data.logic_weight * 100)
    form.value.customer_weight = Math.round(scoringResponse.data.customer_weight * 100)
    form.value.persuasion_weight = Math.round(scoringResponse.data.persuasion_weight * 100)
  } catch (error) {
    console.error('Failed to load config:', error)
  }
}

const saveSettings = async () => {
  try {
    // Save API config
    await axios.post('/api/v1/api-config', {
      openai_api_key: form.value.openai_api_key,
      claude_api_key: form.value.claude_api_key,
      deepseek_api_key: form.value.deepseek_api_key,
      whisper_api_key: form.value.whisper_api_key
    })
    
    // Save scoring config (convert to decimal weights)
    await axios.post('/api/v1/scoring-config', {
      expression_weight: form.value.expression_weight / 100,
      content_weight: form.value.content_weight / 100,
      logic_weight: form.value.logic_weight / 100,
      customer_weight: form.value.customer_weight / 100,
      persuasion_weight: form.value.persuasion_weight / 100
    })
    
    alert('设置已保存！')
  } catch (error) {
    console.error('Failed to save settings:', error)
    alert('保存失败，请重试。')
  }
}

const totalWeight = computed(() => {
  return (
    form.value.expression_weight +
    form.value.content_weight +
    form.value.logic_weight +
    form.value.customer_weight +
    form.value.persuasion_weight
  )
})

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
input[type="range"] {
  accent-color: #3b82f6;
}
</style>
