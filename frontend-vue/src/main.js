import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './assets/css/main.css'

// Import components
import Home from './views/Home.vue'
import Upload from './views/Upload.vue'
import History from './views/History.vue'
import Analyze from './views/Analyze.vue'
import Report from './views/Report.vue'
import Settings from './views/Settings.vue'
import ModelManagement from './views/ModelManagement.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/upload', name: 'Upload', component: Upload },
  { path: '/history', name: 'History', component: History },
  { path: '/analyze/:id', name: 'Analyze', component: Analyze },
  { path: '/report/:id', name: 'Report', component: Report },
  { path: '/settings', name: 'Settings', component: Settings },
  { path: '/models', name: 'ModelManagement', component: ModelManagement },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
