

<template>
  <div class="home-container">

    <div class="banner-image">
      <!-- <img src="@\assets\images\harmonai.png" alt="banner"> -->
      <!-- <img src="@\assets\images\9.jpeg" alt="banner"> -->
       <div class="banner-text">
        <h1>{{ $t('home.title') }}</h1>
       </div>
    </div>

    <div class="explanation-box">
      <h2>{{ $t('home.purposeOfTheApp') }}</h2>
      <p class="explanation">{{ $t('home.purposeOfTheAppExplanation1') }} <a href="/profile"><em>{{ $t('nav.profile') }}</em></a></p>
      <!-- <p>{{ $t('home.purposeOfTheAppExplanation2') }}</p> -->
    </div>

    <hr>

    <div class="search-upload-section">
      <h2>{{ $t('home.findChordsHeading') }}</h2>

      <div class="search-form">
        <label for="song-search">{{ $t('home.searchLabel') }}</label>
        <input type="text" id="song-search" :placeholder="$t('home.searchPlaceholder')">
        <button class="btn search-btn">{{ $t('buttons.searchButton') }}</button>
      </div>

      <hr>

      <div class="upload-form">
        <label for="mp3-upload">{{ $t('home.uploadLabel') }}</label>
        <input type="file" accept="audio/mp3" @change="handleFileUpload">
        <p class="disclaimer">{{ $t('home.warning') }}</p>
        <button class="btn upload-btn" @click="submitUpload">{{ $t('buttons.uploadButton') }}</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
  name: 'home',
  data() {
    return {
      audioFile: null, // holds the selecte audio file
      error: '',
      url: 'http://localhost:8000/api/create-song/',
      toast: null, // declare a toast variable to be used with toastification library for notifications


    }
  },
  mounted() {
    this.toast = useToast(); // initiate a toast variable

  },
  methods: {
    handleFileUpload() {
      this.audioFile = event.target.files[0];
      this.toast.info('File selected: ' + this.audioFile.name)
    },

    async submitUpload() {
      // check if the user selected a file first
      if (!this.audioFile) {
        this.toast.error(this.$t('notification.pleaseSelectFile') || 'Please select a file first');
        return;
      }

      const formData = new FormData();
      // the audio file must match the key Django expects: request.files['audio']
      formData.append('audio', this.audioFile);

      // displaying a permanent toat notification here until the file upload is done
      this.toast.info('Processing started...', { timeout: false });

      try {
        const response = await axios.post(this.url, formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          }
        })

        if (response.status === 200) {
          this.toast.clear(); // removes the permanenet loading notification we had created earlier
          this.toast.success(('notification.uploadSuccessful') || 'File uploaded successfully');
        }

      } catch (error) {

        this.toast.clear(); // clearing any hanging loading notification
        this.toast && this.toast.error(this.$t('notification.processFailed') || 'Processing failed');

        console.error(error); // debug
      }
    }

  }
}
</script>