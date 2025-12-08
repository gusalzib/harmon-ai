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

            url: 'http://localhost:8000/admin/model-training',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,
            activeSection: 'modelTraining', //this controls which section in visible to the user at any time.


        }
    },
    mounted() {
        this.toast = useToast(); // initiate a toast variable

        // since the users service is not online yet, we do not want to fetch the songs on page load because that just causes errors
        // this.getUserSongsHistory() // we get the user favorite songs as soon as the page is loaded
    },
    methods: {

    }
}
</script>