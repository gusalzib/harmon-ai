<template>
    <div class="account-main-container">
        <div class="account-sidebar">
            <div class="account-sidebar-menu">
                <h2>{{ $t('sidebar.menu') }}</h2>
                <a id="sidebar-links" @click.native="setActive('profile')">{{ $t('sidebar.profile') }}</a>
                <a id="sidebar-links" @click.native="setActive('history')">{{ $t('sidebar.history') }}</a>
                <a id="sidebar-links" @click.native="setActive('favorite_songs')">{{ $t('sidebar.favorite_songs') }}</a>
            </div>
        </div>
        <div class="profile-container">
            <div v-if="activeSection === 'profile'">
                <Profile/>
            </div>

            <div v-else-if="activeSection === 'history'">
                <History/>
            </div>

            <div v-else-if="activeSection === 'favorite_songs'">
                <FavoriteSongs/>
            </div>
        </div>
    </div>
</template>

<script>
import FavoriteSongs from '@/components/FavoriteSongs.vue';
import Profile from '@/components/Profile.vue';
import History from '@/components/History.vue';
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'UserAccount',
    components: {
        Profile,
        FavoriteSongs,
        History
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            error: '',
            url: 'http://localhost:8001/api/users',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, 
            activeSection: 'profile', //this controls which section in visible to the user at any time. I set it to the profile page as default


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

    },
    methods: {
        setActive(section) {
            try {
                this.activeSection = section
            } catch (error) {
                this.toast && this.toast.error(this.$t('notification.loadingFailed') || 'Loading failed')
            }
        },
        },
    }
</script>