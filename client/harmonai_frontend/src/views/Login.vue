<template>

    <div class="login-form-container">
        <div class="login-form">
            <label for="login_email"> {{ $t('labels.email') }} </label>
            <input id="login_email" class="login_input" type="email" placeholder="email">
            <br>
            <label for="login_password"> {{ $t('labels.password') }} </label>
            <input id="login_password" class="login_input" type="password" placeholder="password">
            <button type="submit"> {{ $t('buttons.login') }} </button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            error: '',
            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications

                
            }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

    },
    methods: {
        async login() {
                try {
                    const response = await axios.get(`${this.url}`, {
                        
                    })
                } catch (error) {
                    
                }
            }
        }
    }
</script>