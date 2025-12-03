<template>
    <div class="profile" id="edit-profile" v-if="activeSection === 'profile'">
        <h3>{{ $t('profile.editProfile') }}</h3>
        
            <label>{{ $t('labels.username') }}</label>
            <input v-model="form.username" type="text" id="name" required/>
            <br>
            <label>{{ $t('labels.email') }}</label>
            <input v-model="form.email" type="email" id="email" required/>
            <br>
            <label>{{ $t('labels.password') }}</label>
            <input v-model="form.password" type="password" id="password" required/>
            <div class="show-password-box">
                <label>{{ $t('labels.ShowPassword') }}</label>
                <input id="checkbox" type="checkbox" v-on:click="toggle()">
            </div>

            <button id="update-button" class="submit-button" v-on:click="updateUserInfo()" type="button">{{ $t('profile.updateInfo') }}</button>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'Profile',
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: '',
            },
            url: 'http://localhost:8000/api/users',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, 
            activeSection: 'profile', //this controls which section in visible to the user at any time. I set it to the profile page as default


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable
        this.getUserInfo() // we get the user info as soon as the page is loaded
    },
    methods: {
        async getUserInfo() {

            try {
                // get token of the logged in user - the token should hold the userid
                const userId = localStorage.getItem('token');

                //get info of the logged in user using their ID
                const response = await axios.get(`${this.url}/${userId}`);

                // if server returns 200, then we populate the form data
                if (response.status === 200) {
                    this.form = response.data.user;

                }
            } catch (error) {
                // if status is 401 then the request was not authorized meaning that it is likely that the user session is expired
                if (error.response?.status === 401) {
                    this.toast && this.toast.error(this.$t('notification.sessionExpired') || 'User session expired')

                    // automatically send the user to login page
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, this.timeout)
                } else {
                    // we show a localized notification and if we fail to get that, we have the fallback english string
                    this.toast && this.toast.error(this.$t('notification.failedToLoadUserInfo') || 'Failed to load user data')

                }

            }

        },
        async updateUserInfo() {
            try {
                // get token of the logged in user - the token should hold the userid
                const userId = localStorage.getItem('token');

                // put request to update the user info if the user makes any changes
                const response = await axios.put(`${this.url}/${userId}`, JSON.stringify(this.form));

                if (response.status === 200) {

                    // refresh the user info displayed 
                    this.getUserInfo()

                    // display notification
                    this.toast && this.toast.success(this.$t('notification.updateSuccessful') || 'Updated successfully');

                }


            } catch (error) {
                // we may detect upon a put request that the session is xpired
                if (error.response?.status === 401) {

                    this.toast && this.toast.error(this.$t('notification.sessionExpired') || 'User session expired')

                    // automatically send the user to login page
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, this.timeout)
                } else {
                    // else we have a server error and we display a generic error message
                    this.toast && this.toast.error(this.$t('notification.somethingWentWrong') || 'Something went wrong')

                }

            }
        },
        toggle() {
            // allow user to show the password in the password filed
            let temp = document.getElementById("password")

            if (temp.type === "password") {
                temp.type = "text";

            } else {
                temp.type = "password";
            }
            }
        },
    }
</script>