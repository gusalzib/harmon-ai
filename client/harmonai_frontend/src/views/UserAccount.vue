<template>
    <div class="account-main-container">
        <div class="account-sidebar">
            <div class="account-sidebar-menu">
                <h3>{{ $t('sidebar.menu') }}</h3>
                <a id="sidebar-links" @click.native="setActive('profile')">{{ $t('sidebar.profile') }}</a>
                <a id="sidebar-links" @click.native="setActive('history')">{{ $t('sidebar.history') }}</a>
                <a id="sidebar-links" @click.native="setActive('favorite_songs')">{{ $t('sidebar.favorite_songs') }}</a>
            </div>
        </div>
        <div class="profile-container">
            <div class="profile" v-if="activeSection === 'profile'">

            </div>

            <div v-else-if="activeSection === 'history'">

            </div>

            <div v-else-if="activeSection === 'favorite_songs'">

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'UserAccount',
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            error: '',
            url: 'http://localhost:8000/api/users',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, 
            activeSection: 'profile', //this controls which section in visible to the user at any time. I set it to the profile page as default


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

    },
    methods: {
        async getUserInfo() {

        },
        setActive(section) {
            try {
                this.activeSection = section
            } catch (error) {
                this.toast && this.toast.error(this.$t('notification.loadingFailed') || 'Loading failed')
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