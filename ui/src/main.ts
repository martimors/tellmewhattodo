import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import { OhVueIcon, addIcons } from 'oh-vue-icons'

import { BiGithub, RiQuestionnaireLine } from 'oh-vue-icons/icons'
import { client } from '@/client/services.gen'

client.setConfig({
  baseUrl: import.meta.env.VITE_API_URL
})

addIcons(BiGithub, RiQuestionnaireLine)

const app = createApp(App)
app.component('v-icon', OhVueIcon)

app.mount('#app')
