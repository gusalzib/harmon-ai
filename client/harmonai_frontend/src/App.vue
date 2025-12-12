<template>
  <div class="nav-bar">
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        <div class="nav-links">
          <RouterLink to="/">{{ $t('nav.home') }}</RouterLink>
          <RouterLink v-show="this.authStore.isLoggedIn" to="/profile">{{ $t('nav.profile') }}</RouterLink>
          <RouterLink to="/about">{{ $t('nav.about') }}</RouterLink>
          <RouterLink v-show="!this.authStore.isLoggedIn" to="/login">{{ $t('nav.login') }}</RouterLink>
          <RouterLink v-show="!this.authStore.isLoggedIn" to="/signup">{{ $t('nav.signup') }}</RouterLink>
          <button v-show="this.authStore.isLoggedIn" class="standard-btn" @click="logout">{{ $t('nav.logout') }}</button>
          <ThemeToggle />
        </div>
        <LanguageSwitcher />
    </header>
  </div>


  <RouterView />
</template>
<script>
import { RouterLink, RouterView } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue';
import { getCsrfToken } from './utils/csrfTokenUtils';
import axios from 'axios';
import { useToast } from 'vue-toastification'
import { useAuthStore } from "@/stores/auth"

export default {
  name: 'App',
  components: {
    LanguageSwitcher,
    ThemeToggle,
  },

  data() {
    return {
      url: 'http://localhost:8000/users/logout',
      statusURL: 'http://localhost:8000/users/check-status',
      prefsURL: "http://localhost:8000/users/get-preferences",
      timeout: 1000,
      toast: null,
      authStore: useAuthStore()
    }
  },
  async mounted() {
    this.toast = useToast(); // initiate a toast variable
    this.get_csrf() // Get CSRF token

    // Check session validity
    await this.authStore.checkStatus()
    await this.loadPrefs()
  },
  methods: {
    async loadPrefs() {
      console.log(`Is logged in? ${this.authStore.isLoggedIn}. Is superuser? ${this.authStore.isSuperUser}`)
      if(this.authStore.isLoggedIn == true) {
        const response = await axios.get(this.prefsURL, {
          withCredentials: true,
          headers: {
            "X-CSRFToken": getCsrfToken()
          }
        });
        console.log(`Prefs: ${JSON.stringify(response.data)}`)
      }
      else {
        console.log("Not logged in")
      }
    },
    get_csrf() {
      try {
        // Get CSRF token from server. If cookie != X-CSRFToken value, bad news
        axios.get("http://localhost:8000/users/set-csrf-cookie", {withCredentials: true})
          .then(response => {
            if(response.status == 200)
              console.log("XSRF cookie set")
            else
              console.log("Failed setting XSRF cookie")
          })
      }
      catch(e) {
        console.log("sorry lmao")
      }
    },
    async logout() {      
      try {
        const response = await axios.post(`${this.url}`, 'logout',{
          withCredentials: true,
          headers: {  
            "X-CSRFToken": getCsrfToken()
          }
        })

        this.authStore.checkStatus()

        // if the logout was successful, we automatically redirect the
        // user to the login page
        // timeout is set to 2 seconds as a default
        if (response.status === 200) {

          // display notifications
          this.toast && this.toast.success(this.$t('notification.logoutSuccessful') || 'Logout successful');
          // redirect the user to home page
          setTimeout(() => {
            this.$router.push('/login'); // go to login
          }, this.timeout);
        }

      } catch (error) {
        // we show a localized notification and if we fail to get that, we have the fallback english string
        this.toast && this.toast.error(this.$t('notification.logoutFailed') || 'Logout Failed')

      }
    }
  }
}
</script>
<style src="@/assets/main.css"></style>
