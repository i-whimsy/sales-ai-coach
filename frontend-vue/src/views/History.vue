<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          历史分析记录
        </h1>
        <p class="mt-2 text-slate-600 dark:text-slate-400">
          查看所有已上传的录音文件和分析结果
        </p>
      </div>
      <RouterLink to="/upload" class="btn btn-primary">
        上传新录音
      </RouterLink>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold text-slate-900 dark:text-white">记录列表</h2>
          <div class="text-sm text-slate-500 dark:text-slate-500">
            共 {{ recordings.length }} 条记录
          </div>
        </div>
      </div>
      <div class="card-content">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b dark:border-slate-800">
                <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-white">文件名</th>
                <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-white">上传时间</th>
                <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-white">状态</th>
                <th class="text-left py-3 px-4 font-semibold text-slate-900 dark:text-white">评分</th>
                <th class="text-right py-3 px-4 font-semibold text-slate-900 dark:text-white">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="recording in recordings"
                :key="recording.id"
                class="border-b dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900/50"
              >
                <td class="py-3 px-4">
                  <div class="flex items-center gap-3">
                    <span class="text-lg">🎧</span>
                    <div class="min-w-0">
                      <div class="font-medium text-slate-900 dark:text-white truncate">
                        {{ recording.name || recording.file_name }}
                      </div>
                      <div class="text-xs text-slate-500 dark:text-slate-500 truncate">
                        {{ recording.file_name }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="py-3 px-4 text-sm text-slate-600 dark:text-slate-400">
                  {{ formatDate(recording.upload_time) }}
                </td>
                <td class="py-3 px-4">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="{
                      'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300': recording.status === 'uploaded',
                      'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': recording.status === 'analyzed',
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300': recording.status === 'analyzing'
                    }"
                  >
                    {{ statusText(recording.status) }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-bold"
                    :class="{
                      'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300': recording.score === null,
                      'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': recording.score !== null
                    }"
                  >
                    {{ recording.score !== null ? recording.score.toFixed(1) : '--' }}
                  </span>
                </td>
                <td class="py-3 px-4 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button
                      v-if="recording.status === 'uploaded'"
                      @click="startAnalysis(recording)"
                      class="btn btn-primary btn-sm"
                    >
                      分析
                    </button>
                    <RouterLink
                      v-if="recording.status === 'analyzed'"
                      :to="`/report/${recording.id}`"
                      class="btn btn-outline btn-sm"
                    >
                      报告
                    </RouterLink>
                    <RouterLink
                      :to="`/analyze/${recording.id}`"
                      class="btn btn-secondary btn-sm"
                    >
                      详情
                    </RouterLink>
                    <button
                      @click="renameRecording(recording)"
                      class="btn btn-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
                      title="重命名"
                    >
                      ✏️
                    </button>
                    <button
                      @click="deleteRecording(recording.id)"
                      class="btn btn-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                    >
                      🗑️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="recordings.length === 0" class="text-center py-12">
      <div class="text-4xl mb-4">📂</div>
      <h3 class="text-xl font-semibold mb-2 text-slate-900 dark:text-white">暂无记录</h3>
      <p class="text-slate-600 dark:text-slate-400 mb-6">
        还没有上传过录音文件
      </p>
      <RouterLink to="/upload" class="btn btn-primary">
        上传第一个录音
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const recordings = ref([])
const loading = ref(true)

const fetchRecordings = async () => {
  try {
    const response = await axios.get('/api/v1/recordings')
    recordings.value = response.data.recordings
    loading.value = false
  } catch (error) {
    console.error('Failed to fetch recordings:', error)
    loading.value = false
  }
}

const startAnalysis = async (recording) => {
  try {
    recording.status = 'analyzing'
    await axios.post(`/api/v1/recordings/${recording.id}/analyze`)
    await fetchRecordings()
  } catch (error) {
    console.error('Failed to start analysis:', error)
    recording.status = 'uploaded'
  }
}

const deleteRecording = async (id) => {
  if (confirm('确定要删除这条记录吗？')) {
    try {
      await axios.delete(`/api/v1/recordings/${id}`)
      recordings.value = recordings.value.filter(r => r.id !== id)
    } catch (error) {
      console.error('Failed to delete recording:', error)
    }
  }
}

const renameRecording = async (recording) => {
  const newName = prompt('请输入新的名称:', recording.name || recording.file_name)
  if (newName !== null) {
    const trimmedName = newName.trim()
    if (trimmedName) {
      try {
        await axios.post(`/api/v1/recordings/${recording.id}/rename`, {
          name: trimmedName
        })
        recording.name = trimmedName
      } catch (error) {
        console.error('Failed to rename recording:', error)
        alert('重命名失败，请重试。')
      }
    }
  }
}

const statusText = (status) => {
  const statusMap = {
    'uploaded': '已上传',
    'analyzed': '已分析',
    'analyzing': '分析中'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchRecordings()
})
</script>

<style scoped>
table {
  border-collapse: collapse;
}

.btn-sm {
  @apply px-3 py-1 text-xs;
}
</style>
