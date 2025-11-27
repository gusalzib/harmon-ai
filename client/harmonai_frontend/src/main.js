import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// importing the locales english and swedish files
import en from './locales/en.json'
import sv from './locales/sv.json'
import { createI18n } from 'vue-i18n'

// getting the user language preference from local storage. 
// if it does not exist we default to english
const savedLocale  = localStorage.getItem('lang') || 'en'

// creating an i18n instance to use the localized values from the files
const i18n = createI18n({
    legacy: true,  // allows us to embedd $t() in html
    locale: savedLocale,
    fallbackLocale: 'en',
    messages: {
        en, 
        sv
    }

})

export { i18n }

const app = createApp(App)

app.use(router)
app.use(i18n)

app.mount('#app')
