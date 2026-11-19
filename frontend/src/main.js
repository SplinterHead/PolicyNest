import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'

import '@mdi/font/css/materialdesignicons.css'

const app = createApp(App)
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'system',
    themes: {
      light: {
        colors: {
          primary: '#1565C0',
          'on-primary': '#FFFFFF',
          info: '#01579B',
          'on-info': '#FFFFFF',
        },
      },
      dark: {
        colors: {
          primary: '#64B5F6',
          'on-primary': '#0D1B2A',
          info: '#4FC3F7',
          'on-info': '#0D1B2A',
        },
      },
    },
  },
})

app.use(router)
app.use(vuetify)
app.mount('#app')
