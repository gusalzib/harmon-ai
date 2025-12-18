import axios from 'axios'
import { getCsrfToken } from '@/utils/csrfTokenUtils';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    isSuperUser: false
  }),
  actions: {
    async checkStatus() {
      // Ask for session validity from server
      const baseUrl = import.meta.env.VITE_API_URL || "http://34.51.250.115"

      const statusUrl = `${baseUrl}/users/check-status`
      await axios.get(statusUrl, {
        withCredentials: true,
        headers: {
          "X-CSRFToken": getCsrfToken()
        }
      }).then(response => {
        // Update state
        this.$state.isLoggedIn = response.data.logged_in
        this.$state.isSuperUser = response.data.is_superuser
      }).catch(reason => {
        // Something went wrong when it really shouldn't have, but we digress
        console.error(reason)
      })
    }
  }
})