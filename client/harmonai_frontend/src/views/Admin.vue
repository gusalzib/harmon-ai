<template>
    <div class="account-main-container">
        <div class="account-sidebar">
            <div class="account-sidebar-menu">
                <h2>{{ $t('sidebar.menu') }}</h2>
                <a id="sidebar-links" @click.native="setActive('adminProfile')">{{ $t('sidebar.profile') }}</a>
                <a id="sidebar-links" @click.native="setActive('modelTraining')">{{ $t('sidebar.modelTraining') }}</a>
                <a id="sidebar-links" @click.native="setActive('dataUpload')">{{ $t('sidebar.dataUpload') }}</a>
            </div>
        </div>
        <div class="profile-container">
            <div v-if="activeSection === 'adminProfile'">
                <AdminProfile />
            </div>

            <div v-else-if="activeSection === 'modelTraining'">
                <ModelTraining />
            </div>

            <div v-else-if="activeSection === 'dataUpload'">
                <UploadData />
            </div>
        </div>
    </div>
</template>

<script>
import AdminProfile from '@/components/AdminProfile.vue';
import ModelTraining from '@/components/ModelTraining.vue';
import UploadData from '@/components/UploadData.vue';
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'Admin',
    components: {
        AdminProfile,
        ModelTraining,
        UploadData
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            error: '',
            url: 'http://localhost:8000/api/admin',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000, 
            activeSection: 'adminProfile', //this controls which section in visible to the user at any time. I set it to the profile page as default


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