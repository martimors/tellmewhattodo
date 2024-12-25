import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import './assets/main.css'

import { createBootstrap } from 'bootstrap-vue-next'
import { createApp } from 'vue'
import App from './App.vue'

import { OhVueIcon, addIcons } from 'oh-vue-icons'

import { BiGithub, ViFileTypeHelm, RiQuestionnaireLine } from 'oh-vue-icons/icons'
import { client } from '@/client/services.gen'

client.setConfig({
  baseUrl: import.meta.env.VITE_API_URL,
})

addIcons(BiGithub, ViFileTypeHelm, RiQuestionnaireLine)

const app = createApp(App)
app.use(createBootstrap())
app.component('v-icon', OhVueIcon)

app.mount('#app')
