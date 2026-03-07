// Simple Tabs component for Vue
export const Tabs = {
  name: 'Tabs',
  props: {
    defaultValue: String
  },
  setup(props, { slots }) {
    return () => {
      const defaultSlot = slots.default?.()
      const content = defaultSlot?.find(el => el.type?.name === 'TabsList')
      return content
    }
  }
}

export const TabsList = {
  name: 'TabsList',
  setup(props, { slots }) {
    return () => {
      const children = slots.default?.()
      return h('div', { class: 'flex gap-2' }, children)
    }
  }
}

export const TabsTrigger = {
  name: 'TabsTrigger',
  props: {
    value: String
  },
  setup(props, { slots }) {
    return () => {
      return h('button', { 
        class: 'px-4 py-2 rounded-md text-sm font-medium transition-colors data-[state=active]:bg-primary-600 data-[state=active]:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
      }, slots.default?.())
    }
  }
}

export const TabsContent = {
  name: 'TabsContent',
  props: {
    value: String
  },
  setup(props, { slots }) {
    return () => h('div', { class: 'mt-4' }, slots.default?.())
  }
}

import { h } from 'vue'