<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          内容分析配置
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          配置 LLM 分析维度和评估标准
        </p>
      </div>
      <div class="flex gap-3">
        <button @click="resetToDefault" class="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 font-medium transition-colors">
          恢复默认
        </button>
        <button @click="saveConfig" :disabled="!isValid" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors disabled:opacity-50">
          保存配置
        </button>
      </div>
    </div>

    <!-- System Prompt -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700">
        <h2 class="text-xl font-semibold text-slate-900 dark:text-white">系统提示词</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">设定 AI 分析专家的角色和风格</p>
      </div>
      <div class="p-6">
        <textarea
          v-model="systemPrompt"
          rows="3"
          class="w-full px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white font-mono text-sm"
          placeholder="你是一位专业的销售演讲分析专家..."
        ></textarea>
      </div>
    </div>

    <!-- Dimensions -->
    <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700">
      <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
        <div>
          <h2 class="text-xl font-semibold text-slate-900 dark:text-white">分析维度</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">定义分析的不同方面和权重</p>
        </div>
        <button @click="addDimension" class="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 font-medium transition-colors">
          + 添加维度
        </button>
      </div>
      
      <div class="p-6 space-y-6">
        <div v-for="(dim, index) in dimensions" :key="index" class="border border-slate-200 dark:border-slate-700 rounded-lg p-4 space-y-4">
          <!-- Dimension Header -->
          <div class="flex gap-4 items-start">
            <div class="flex-1 grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">维度名称</label>
                <input
                  v-model="dim.name"
                  type="text"
                  class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm"
                  placeholder="如：内容完整性"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">权重 (0-1)</label>
                <input
                  v-model.number="dim.weight"
                  type="number"
                  step="0.05"
                  min="0"
                  max="1"
                  class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm"
                />
              </div>
            </div>
            <button @click="removeDimension(index)" class="mt-6 px-3 py-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors">
              删除
            </button>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">维度描述</label>
            <input
              v-model="dim.description"
              type="text"
              class="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm"
              placeholder="描述这个维度的评估目的"
            />
          </div>

          <!-- Criteria -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">评估标准</label>
              <button @click="addCriteria(index)" class="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors">
                + 添加标准
              </button>
            </div>
            <div class="space-y-2">
              <div v-for="(criteria, cIndex) in dim.criteria" :key="cIndex" class="flex gap-2">
                <span class="text-sm text-slate-500 dark:text-slate-400 py-2">{{ cIndex + 1 }}.</span>
                <input
                  v-model="dim.criteria[cIndex]"
                  type="text"
                  class="flex-1 px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm"
                  placeholder="如：公司介绍：是否介绍了公司背景、业务范围"
                />
                <button @click="removeCriteria(index, cIndex)" class="px-2 py-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors">
                  ×
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Weight Summary -->
        <div class="pt-4 border-t border-slate-200 dark:border-slate-700">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-slate-700 dark:text-slate-300">总权重：</span>
            <span :class="totalWeight === 1 ? 'text-green-600' : 'text-red-600'" class="text-lg font-bold">
              {{ (totalWeight * 100).toFixed(0) }}%
            </span>
          </div>
          <p v-if="totalWeight !== 1" class="text-xs text-red-600 mt-1">
            ⚠️ 总权重必须等于 100%
          </p>
        </div>
      </div>
    </div>

    <!-- API Config Reminder -->
    <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl p-4">
      <div class="flex gap-3">
        <div class="text-amber-600 text-xl">💡</div>
        <div>
          <h3 class="font-medium text-amber-900 dark:text-amber-300">LLM API 配置提示</h3>
          <p class="text-sm text-amber-800 dark:text-amber-400 mt-1">
            要获得最佳分析效果，请在 <router-link to="/settings" class="underline hover:text-amber-900">系统设置</router-link> 中配置 OpenAI/Claude/DeepSeek API 密钥。
            未配置时将使用关键词匹配（效果有限）。
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const systemPrompt = ref('')
const dimensions = ref([])

const totalWeight = computed(() => {
  return dimensions.value.reduce((sum, dim) => sum + (dim.weight || 0), 0)
})

const isValid = computed(() => {
  return Math.abs(totalWeight.value - 1) < 0.01 && dimensions.value.length > 0
})

const defaultConfig = {
  system_prompt: '你是一位专业的销售演讲分析专家。请根据提供的演讲内容，客观、公正地评估各个维度的表现。',
  dimensions: [
    {
      name: '内容完整性',
      key: 'content',
      weight: 0.30,
      description: '评估演讲内容是否覆盖了所有关键部分',
      criteria: [
        '公司介绍：是否介绍了公司背景、业务范围',
        '行业问题：是否说明了目标行业面临的痛点',
        '技术方案：是否清晰描述了技术解决方案',
        '核心优势：是否说明了与竞争对手的差异化优势',
        '客户案例：是否提供了成功的客户案例',
        '商业价值：是否说明了能带来的商业价值'
      ]
    },
    {
      name: '逻辑结构',
      key: 'logic',
      weight: 0.20,
      description: '评估演讲的逻辑结构是否清晰',
      criteria: [
        '开场：是否有清晰的开场白和主题引入',
        '问题引入：是否先说明问题再给出方案',
        '递进逻辑：是否层层递进、环环相扣',
        '总结：是否有清晰的总结和行动号召'
      ]
    },
    {
      name: '客户理解度',
      key: 'customer',
      weight: 0.20,
      description: '评估客户听完后的理解程度',
      criteria: [
        '公司定位：客户能清楚知道公司是做什么的',
        '问题认知：客户能理解所要解决的问题',
        '价值认知：客户能理解产品/服务的价值',
        '合作意愿：客户是否表现出继续了解的意愿'
      ]
    },
    {
      name: '说服力',
      key: 'persuasion',
      weight: 0.10,
      description: '评估演讲的说服力',
      criteria: [
        '案例说服：是否有具体案例增强说服力',
        '价值表达：是否清晰表达了商业价值',
        '兴趣激发：是否成功激发客户兴趣'
      ]
    }
  ]
}

const loadConfig = async () => {
  try {
    const response = await axios.get('/api/v1/tasks/content_analysis')
    const config = response.data
    
    if (config.prompt_config) {
      const parsed = typeof config.prompt_config === 'string' 
        ? JSON.parse(config.prompt_config) 
        : config.prompt_config
      
      systemPrompt.value = parsed.system_prompt || defaultConfig.system_prompt
      dimensions.value = parsed.dimensions || defaultConfig.dimensions
    } else {
      resetToDefault()
    }
  } catch (error) {
    console.error('Failed to load config:', error)
    resetToDefault()
  }
}

const saveConfig = async () => {
  if (!isValid.value) {
    alert('请确保总权重等于 100%')
    return
  }

  try {
    // Generate keys for dimensions
    const configToSave = {
      system_prompt: systemPrompt.value,
      dimensions: dimensions.value.map((dim, index) => ({
        ...dim,
        key: dim.key || ['content', 'logic', 'customer', 'persuasion', 'custom_' + index][index] || `dim_${index}`
      }))
    }

    await axios.put('/api/v1/tasks/content_analysis', {
      prompt_config: configToSave
    })

    alert('✅ 配置已保存！')
  } catch (error) {
    console.error('Failed to save config:', error)
    alert('❌ 保存失败：' + (error.response?.data?.detail || error.message))
  }
}

const resetToDefault = () => {
  systemPrompt.value = defaultConfig.system_prompt
  dimensions.value = JSON.parse(JSON.stringify(defaultConfig.dimensions))
}

const addDimension = () => {
  dimensions.value.push({
    name: '新维度',
    key: `dim_${dimensions.value.length}`,
    weight: 0.10,
    description: '描述这个维度',
    criteria: ['评估标准 1', '评估标准 2']
  })
}

const removeDimension = (index) => {
  if (dimensions.value.length <= 1) {
    alert('至少需要保留一个维度')
    return
  }
  dimensions.value.splice(index, 1)
}

const addCriteria = (dimIndex) => {
  dimensions.value[dimIndex].criteria.push('新的评估标准')
}

const removeCriteria = (dimIndex, criteriaIndex) => {
  if (dimensions.value[dimIndex].criteria.length <= 1) {
    alert('至少需要保留一个评估标准')
    return
  }
  dimensions.value[dimIndex].criteria.splice(criteriaIndex, 1)
}

onMounted(() => {
  loadConfig()
})
</script>
