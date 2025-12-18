<template>
    <div class="history-section" id="history" v-if="activeSection === 'history'">
        <h3>{{ $t('history.yourSongsHistory') }}</h3>

        <ul class="history-list-container">
            <!-- displaying the dummy_songs temporarily as a placeholder until we get the song service up and running
                once the song service is running, we delete the dummy_songs and replace it with 'songs' -->
            <li class="song-card" v-for="song in dummy_history" :key="song.name">
                <div class="song-details-header">
                    <h4 class="song-name">{{ song.name }}</h4>
                    <p class="song-artist">{{ song.artist }}</p>
                </div>

                <div class="chord-display-box">
                    <label class="chord-label" for="chord-list">{{ $t('song.chords') }}</label>
                    <pre class="chord-list">{{ song.chord_list }}</pre>
                </div>
            </li>

            <li v-if="songs.length === 0" class="empty-list-message">
                <p>{{ $t('history.noHistory') }} <a href="/">{{ $t('nav.home') }}</a></p>
            </li>
        </ul>
            

    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification'

export default {
    name: 'History',
    data() {
        return {
            // dummy_history is a temporary list of songs as a placeholder to test how the UI looks
            dummy_history: [
                {
                    artist: "The chillware collective",
                    name: "sunset echoes",
                    chord_list: "Cm - Gm - Eb - Bb\n(Verse repeats 4x) \n Cm - Gm - Eb - Bb\n(Verse repeats 4x) \n Cm - Gm - Eb - Bb\n(Verse repeats 4x)"

                },
                {
                    artist: "Arnao & Yhe GU Band",
                    name: "The blues",
                    chord_list: "E7 - A7 - D7 - G7\n(12-bar progression)"

                },
                {
                    artist: "Classical composer AI",
                    name: "Sonata for Timed-out Connections",
                    chord_list: "Am(9) | E7/G# | Cmaj7 | F#dim | B7"

                }
            ],
            songs: [], // holds the list of songs
            baseURL: '',
            url: '',
            toast: null, // declare a toast variable to be used with toastification library for notifications
            timeout: 2000,
            activeSection: 'history', //this controls which section in visible to the user at any time.


        }
    },
    mounted() {
        this.baseURL = import.meta.env.VITE_API_URL || "http://34.51.250.115"
        this.url = `${this.baseURL}/api/users`
        this.toast = useToast(); // initiate a toast variable

        // since the users service is not online yet, we do not want to fetch the songs on page load because that just causes errors
        // this.getUserSongsHistory() // we get the user favorite songs as soon as the page is loaded
    },
    methods: {
        async getUserSongsHistory() {

            try {
                // get token of the logged in user - the token should hold the userid
                const userId = localStorage.getItem('token');

                //get info of the logged in user using their ID
                const response = await axios.get(`${this.url}/history/${userId}`);

                // if server returns 200, then we populate the song list
                if (response.status === 200) {
                    this.songs = response.data.songs;

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
                    this.toast && this.toast.error(this.$t('notification.loadingFailed') || 'Loading failed')

                }

            }

        }
    }
}
</script>