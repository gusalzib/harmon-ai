<!--

Authors of code:
- 

-->
<template>
    <div class="model-training-section" id="training" v-if="activeSection === 'modelTraining'">
        <h3>{{ $t('admin.model.startTrainingCycle') }}</h3>

            

    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'ModelTraining',
    data() {
        return {

            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,
            activeSection: 'modelTraining', //this controls which section in visible to the user at any time.
            
            
        }
    },
    mounted() {
        this.url = `${import.meta.env.VITE_API_URL}/admin/model-training`,
        this.toast = useToast(); // initiate a toast variable


    },
    methods: {

    }
}
</script>