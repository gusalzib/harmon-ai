import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from "pinia"
import App from './App.vue'
import router from './router'

import Toast, { POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css' // getting the required styles from the toast css

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

const pinia = createPinia() // Used for holding global state (isLoggedIn)
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.use(Toast, {
    position: POSITION.BOTTOM_CENTER,
    timeout: 3000,
    closeOnClick: true, // close the notification when the user click
    pauseonHover: true // pasue the timeout timer when the user hovers on it
});
readGCSTokenFromURL()
app.mount('#app')




// get the access token returned by google before mounting the app
function readGCSTokenFromURL() {
    if (!window.location.hash) {
        return;
    }

    const hash = window.location.hash.startsWith('#') ? window.location.hash.substring(1) : window.location.hash;
    
    console.log('GLOBAL HASH: ', hash);

    const params = new URLSearchParams(hash);
    const token = params.get('access_token');

    if (token) {
        console.log('GLOBAL GCS TOKEN: ', token);
        localStorage.setItem('gcsAccessToken', token);
    }
    

    //  we cleat the url so that the token is not visible in the address bar of the broswer
    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
}