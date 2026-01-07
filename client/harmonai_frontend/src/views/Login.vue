<!--

Authors of code:
- Carl-Johan Erikson

-->
<template>

    <div class="login-form-container">
        <div class="login-form">
            <label for="login_username"> {{ $t('labels.username') }} </label>
            <input v-model="form.username" id="login_username" class="login_input" type="text" placeholder="Username">
            <br>
            <label for="login_password"> {{ $t('labels.password') }} </label>
            <input v-model="form.password" id="login_password" class="login_input" type="password" placeholder="password">
            <div class="show-password-box">
                <label>{{ $t('labels.ShowPassword') }}</label>
                <input id="checkbox" type="checkbox" v-on:click="toggle()">
            </div>
            <button type="submit" @click="login()"> {{ $t('buttons.login') }} </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'
import { getCsrfToken } from "@/utils/csrfTokenUtils";
import { useAuthStore } from "@/stores/auth"

export default {
    name: 'login',
    data() {
        return {
            form: {
                username: '',
                password: ''
            },
            error: '',
            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, // the amount of time to wait before directing the user to home page upon succesful login
            authStore: useAuthStore()
        }
    },
    mounted() {
        this.url = `${import.meta.env.VITE_API_URL}/users/login`,
        this.toast = useToast(); // initiate a toast variable
    },
    methods: {
        async login() {
            try {
                /* we send the login info as json to backend and await response */
                const response = await axios.post(`${this.url}`, JSON.stringify(this.form), {
                    withCredentials: true,
                    headers: {
                        "X-CSRFToken": getCsrfToken()
                    }
                })

                // if the login was successful, we automatically redirect the
                // user to the home page
                // timeout is set to 2 seconds as a default
                if (response.status === 201) {
                    // display notifications
                    this.toast && this.toast.success(this.$t('notification.loginSuccessful') || 'Login successful');

                    // check the user status 
                    this.authStore.checkStatus()

                    // redirect the user to home page
                    setTimeout(() => {
                        this.$router.push('/'); // go to home
                    }, this.timeout);
                }
                        
            } catch (error) {
                    // if password is invalid, display invalid cridentials notification
                if (error.response?.status === 401) {
                        // we show a localized notification and if we fail to get that, we have the fallback english string
                        this.toast && this.toast.error(this.$t('notification.invalidCridentials') || 'Login Failed')

                    // else if email is not found in registry, display user not found notification
                } else if (error.response?.status === 404) {
                        // we show a localized notification and if we fail to get that, we have the fallback english string
                        this.toast && this.toast.error(this.$t('notification.userNotFound') || 'Login Failed')
                    }
                }
        },
        toggle() {
            // allow user to show the password in the password filed
            let temp = document.getElementById("login_password")

            if (temp.type === "password") {
                temp.type = "text";

            } else {
                temp.type = "password";
            }
        }
    }
}
</script>