<template>

    <div class="signup-form-container">
        <div class="signup-form">
            <label for="signup_email">  {{ $t('labels.username') }}  </label>
            <input v-model="form.username" id="signup_username" class="signup_input" type="text" placeholder="username">
            <label for="signup_email">  {{ $t('labels.email') }}  </label>
            <input v-model="form.email" id="signup_email" class="signup_input" type="email" placeholder="email">
            <label for="signup_password">  {{ $t('labels.password') }}  </label>
            <input v-model="form.password" id="signup_password" class="signup_input" type="password" placeholder="password">
            <div class="show-password-box">
                <label style="font-size: small; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;">{{ $t('labels.ShowPassword') }}</label>
                <input id="checkbox" type="checkbox" v-on:click="toggle()">
            </div>
            
            <button type="submit" @click="signup()"> {{ $t('buttons.signupBtn') }} </button>
        </div>
    </div>
</template>

<script>
import { getCsrfToken } from '@/utils/csrfTokenUtils';
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'signup',
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: '',
            },
            error: '',
            url: 'http://localhost:8001/users/register',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, // the amount of time to wait before directing the user to LOGIN page upon succesful SIGNUP
                
            }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

    },
    methods: {
        toggle() {
            // allow user to show the password in the password filed
            let temp = document.getElementById("signup_password")

            if (temp.type === "password") {
                temp.type = "text";

            } else {
                temp.type = "password";
            }
        },
        async signup() {
            try {
                        
                /* we send the user info as json to backend and await response */
                const response = await axios.post(this.url, JSON.stringify(this.form), {
                    withCredentials: true,
                    headers: {
                         "X-CSRFToken": getCsrfToken()
                    }
                });

                if (response.status === 201) {
                    // display notifications
                    this.toast && this.toast.success(this.$t('notification.signupSuccessful') || 'Signup successful');

                    // redirect the user to login page
                        setTimeout(() => {
                            window.location.replace('/login')
                        }, timeout);
                }
            } catch (error) {
                    // if email is invalid, display invalid cridentials notification
                if (error.response?.status === 400) {
                    // we show a localized notification and if we fail to get that, we have the fallback english string
                    this.toast && this.toast.error(this.$t('notification.invalidCridentials') || 'Sign up Failed')

                    // else if email or username already exists in registry, display duplicate information notification
                } else if (error.response?.status === 409) {
                    // we show a localized notification and if we fail to get that, we have the fallback english string
                    this.toast && this.toast.error(this.$t('notification.duplicateInformation') || 'There is already an account with this email or username')
                }
            }
        }
    }
}
</script>