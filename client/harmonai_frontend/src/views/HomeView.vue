

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

      <div class="search-field-switcher">
        <button :class="['view-tab standard-btn', {active: this.activeView === 'title'}]" @click="this.activeView = 'title'">{{ $t('buttons.searchBoxTitle') }}</button>
        <button :class="['view-tab standard-btn', {active: this.activeView === 'artist'}]" @click="this.activeView = 'artist'">{{ $t('buttons.searchBoxArtist') }}</button>
        <button :class="['view-tab standard-btn', {active: this.activeView === 'genre'}]" @click="this.activeView = 'genre'">{{ $t('buttons.searchBoxGenre') }}</button>
      </div>

      <div class="search-form" v-if="this.activeView === 'title'">
        <label for="song-search">{{ $t('home.searchLabelTitle') }}</label>
        <input type="text" id="song-search" v-model="this.searchTitle" :placeholder="$t('home.searchPlaceholderTitle')">
        <button class="btn search-btn" @click="searchQuery(this.activeView)">{{ $t('buttons.searchButton') }}</button>
      </div>
      <div class="search-form" v-if="this.activeView === 'artist'">
        <label for="song-search">{{ $t('home.searchLabelArtist') }}</label>
        <input type="text" id="song-search" v-model="this.searchArtist" :placeholder="$t('home.searchPlaceholderArtist')">
        <button class="btn search-btn" @click="searchQuery(this.activeView)">{{ $t('buttons.searchButton') }}</button>
      </div>
      <div class="search-form" v-if="this.activeView === 'genre'">
        <label for="song-search">{{ $t('home.searchLabelGenre') }}</label>
        <input type="text" id="song-search" v-model="this.searchGenre" :placeholder="$t('home.searchPlaceholderGenre')">
        <button class="btn search-btn" @click="searchQuery(this.activeView)">{{ $t('buttons.searchButton') }}</button>
      </div>
      <div class="search-result-display">
        <div class="song-details-header" v-for="song in this.songs" :key="song.title">
          <h4 class="song-name">{{ song.title }}</h4>
          <h4 class="song-artist">{{ song.artist }}</h4>
          <h4 class="song-genre">{{ song.genre }}</h4>
          <p class="chord-list">{{ song.prediction }}</p>
        </div>
      </div>
      <hr>

      <div class="upload-form">
        <label for="mp3-upload">{{ $t('home.uploadLabel') }}</label>
        <br>
        <label class="input-label" for="song-title">{{ $t('home.songTitle') }}</label>
        <input v-model="this.title" type="text" id="song-title" :placeholder="$t('home.songTitlePlaceholder')" required>

        <label class="input-label" for="song-artist">{{ $t('home.songArtist') }}</label>
        <input v-model="this.artist" type="text" id="song-artist" :placeholder="$t('home.songArtistPlaceholder')" required>

        <label class="input-label" for="song-genre">{{ $t('home.songGenre') }}</label>
        <input v-model="this.genre" type="text" id="song-genre" :placeholder="$t('home.songGenrePlaceholder')" required>

        <input type="file" accept="audio/mp3" @change="handleFileUpload">
        <p class="disclaimer">{{ $t('home.warning') }}</p>
        <button class="btn upload-btn" @click="submitUpload">{{ $t('buttons.uploadButton') }}</button>
      </div>
    </div>
  </div>
  
  <div class="favorite-songs-section" id="favorite-songs" v-if="this.predictionsIsMade">

        <h3>{{ $t('song.predictedChords') }}</h3>

        <ul class="song-list-container">
          
            <li class="song-card" >
                <div class="song-details-header">
                    <h4 class="song-name">{{ $t('home.songTitle') }} : {{ this.song.title }}</h4>
                    <p class="song-artist">{{ $t('home.songArtist') }} : {{ this.song.artist }}</p>
                    <p class="song-genre">{{ $t('home.songGenre') }} : {{ this.song.genre}}</p>
                    <p class="song-BPM">{{ $t('home.songBPM') }} : {{ this.song.BPM}}</p>
                    <p class="song-duration">{{ $t('home.songDuration') }} : {{ this.song.duration}}</p>
                </div>

                <div class="chord-display-box">
                    <label class="chord-label" for="chord-list">{{ $t('song.chords') }}</label>
                    <pre class="chord-list">{{ this.song.chord_list }}</pre>
                </div>
            </li>

            
        </ul>
            

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
      searchTitle: '',
      searchArtist: '',
      searchGenre: '',
      title: '',
      artist: '',
      genre: '',
      error: '',
      url: '',
      toast: null, // declare a toast variable to be used with toastification library for notifications,
      predictionsIsMade: false,
      activeView: 'title', // default search field is title
      songs: [], // stores result of searchQuery
      song:{
        title: "",
        artist: "",
        genre: "",
        prediction: [],
        BPM: "",
        duration:""
      }
    }
  },
  mounted() {
    this.url = `${import.meta.env.VITE_API_URL}/api/create-song/`|| "http://34.51.250.115.nip.io/api/create-song/",
    this.toast = useToast(); // initiate a toast variable
  },
  methods: {
    async searchQuery(queryType) {
      var search = "";
      var kind = "";
      if (queryType === 'title') {
        search = this.searchTitle;
        kind = 'title';
      }
      if (queryType === 'artist'){
        search = this.searchArtist;
        kind = 'artist';
      }
      if (queryType === 'genre') {
        search = this.searchGenre;
        kind = 'genre';
        
      }
      try{
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/get_songs/?${kind}=${search}`);

        if (response.status === 200) {
          this.songs = response.data.songs; 

          console.log('Retrieved songs', this.songs);
          
        } 
      }catch(error){
        if (error.response?.status === 404) {
          this.toast.warning(this.$t('home.noResultsFound'));
        }else{
          this.toast.error(this.$t('notification.somethingWentWrong'))
        }
      }  
    },
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

      // check if all fields are filled
      if (!this.title || !this.genre || !this.artist) {

        this.toast.error(this.$t('notification.pleaseFillIntheFields') || 'Please fill in the missing fields');
        return; 
      }

      // add the input to formData in preparation for sending it to server
      formData.append('title', this.title);
      formData.append('artist', this.artist);
      formData.append('genre', this.genre);

      // debug prints 
      // console.log(this.title);
      // console.log(this.artist);
      // console.log(this.genre);
        
      // displaying a permanent toat notification here until the file upload is done
      this.toast.info(this.$t('notification.processingStarted'), { timeout: false });

      try {
        // THE FIRST POST REQUEST
        const response = await axios.post(this.url, formData, {
          headers: {
            'Content-Type': 'multipart/form-data', 
          }
        })


        console.log('response ', response);
        
        console.log('status', response.status);
        
        if (response.status === 200) {
          this.toast.clear(); // removes the permanenet loading notification we had created earlier
          this.toast.success(this.$t('notification.uploadSuccessful') || 'File uploaded successfully');

          this.predictionsIsMade= true;
          console.log("testing:", response.data.title);
          this.song.title = response.data.title;
          this.song.artist = response.data.artist;
          this.song.genre = response.data.genre;
          this.song.BPM = response.data.tempo;
          this.song.duration = response.data.duration;
          this.song.chord_list = response.data.chords;
          console.log("Chords:", this.song.chord_list);
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