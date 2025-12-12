<template>
    <div class="profile" id="edit-profile" v-if="activeSection === 'profile'">
        <h3>{{ $t('profile.editProfile') }}</h3>
            <br>
            <label>{{ $t('labels.email') }}</label>
            <input v-model="form.email" type="email" id="email" required/>
            <br>
            <button id="update-button" class="submit-button" v-on:click="updateUserEmail()" type="button">{{ $t('profile.updateInfo') }}</button>
    </div>
    <hr>
    <div class="change-password-section" v-if="activeSection === 'profile'">
        <h3>{{ $t('profile.editPassword') }}</h3>
            <label>{{ $t('labels.changePassword') }}</label>
            <input v-model="passwordForm.oldPassword" type="password" id="old_password" class="password" :placeholder="$t('profile.yourOldPasswordPlaceholder')" required/>
            <input v-model="passwordForm.newPassword" type="password" id="new_password" class="password"  :placeholder="$t('profile.yourNewPasswordPlaceholder')" required/>
            <div class="show-password-box">
                <label>{{ $t('labels.ShowPassword') }}</label>
                <input id="checkbox" type="checkbox" v-on:click="toggle()">
            </div>

            <button id="update-button" class="submit-button" v-on:click="updatePassword()" type="button">{{ $t('profile.updateInfo') }}</button>
    </div>
</template>

<script>
import { getCsrfToken } from '@/utils/csrfTokenUtils';
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'Profile',
    data() {
        return {
            form: {
                email: '',
            },
            baseURL: import.meta.env.VITE_API_URL,
            url: `${baseURL}users/profile`,
            emailURL: `${baseURL}/users/edit-profile`,
            passwordURL: `${baseURL}/users/change-password`,
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, 
            activeSection: 'profile', //this controls which section in visible to the user at any time. I set it to the profile page as default
            passwordForm: {
                oldPassword: '',
                newPassword: ''
            }


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable
        this.getUserInfo() // we get the user info as soon as the page is loaded
    },
    methods: {
        async getUserInfo() {

            try {

                //get info of the logged in user using their ID
                const response = await axios.get(`${this.url}`, {
                    withCredentials: true,
                    headers: {
                        "X-CSRFToken": getCsrfToken()
                    }
                });

                // if server returns 200, then we populate the form data
                if (response.status === 200) {
                    this.form = response.data;

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
        async updateUserEmail() {
            try {

                // put request to update the user info if the user makes any changes
                const response = await axios.put(`${this.emailURL}`, JSON.stringify(this.form), {
                    withCredentials: true,
                    headers: {
                        "X-CSRFToken": getCsrfToken()
                    }
                });

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
        async updatePassword() {
            try {
                console.log('token ', getCsrfToken());
                
                // put request to update the user info if the user makes any changes
                const response = await axios.put(`${this.passwordURL}`, JSON.stringify(this.passwordForm), {
                    withCredentials: true,
                    headers: {
                        "X-CSRFToken": getCsrfToken()
                    }
                });

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
            let temp1 = document.getElementById("old_password")
            let temp2 = document.getElementById("new_password")

            if (temp1.type === "password" && temp2.type === "password") {
                temp1.type = "text";
                temp2.type = "text";

            } else {
                temp1.type = "password";
                temp2.type = "password";
            }
            }
        },
    }
</script>