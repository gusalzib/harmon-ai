

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
      form: {
        email: '',
        password: '',
      },
      error: '',
      url: 'http://localhost:8000/api/prediction',
      toast: null, // declare a toast variable to be used with toastification library for notifications


    }
  },
  mounted() {
    this.toast = useToast(); // initiate a toast variable

  },
  methods: {
    async handleFileUpload() {
      // placeholder until we implement the audio upload logic
    },

  }
}
</script>