<template>
<section class="dashboard-container">
  <p v-if="errorMessage" class="prompt-message">{{ errorMessage }}</p>
<div class="container my-1 music-app-container">
    <div class="row">
      <div class="col-md-3">
        <div class="border border-primary album-artwork-container">
          <!-- <img src="../assets/album_artwork.jpg" alt="Album Artwork" class="img-fluid"> -->
          <img src="/lyrics/album_artwork.jpg" alt="Album Artwork" class="img-fluid">
        </div>
        
        <div class="mt-5">
          
          <router-link to="/dashboard"><button class="btn btn-primary">Back to Home</button></router-link>
          <button @click="flagSong()" class="btn btn-warning">Flag this song</button>

          <h3>Rate This Song</h3>
          <div>
          <label for="rating">Rating:</label>
          <input v-model="rating" type="number" min="1" max="5" />
       
      
          <button @click="submitRating">Submit Rating</button>
           </div>
        </div>
      </div>
      <div class="col-md-9">
        <h1 class="mb-4">Now Playing: {{ song.song_name }} by {{ album.artist }}</h1>
        <audio controls class="w-100" :src="songName" type="audio/mp3">
          Your browser does not support the audio element.
        </audio>
        <p><strong>Album:</strong> {{ album.album_name }}</p>
        <p><strong>Genre:</strong> {{ album.genre }}</p>
        <p><strong>Artist:</strong> {{ album.artist }}</p>
        <p><strong>Rating:</strong> {{ song.rating }}/5</p>
        <p><strong>Duration:</strong> {{ song.duration }} seconds</p>
        <p><strong>Publish on:</strong> {{ song.date_created }}</p>
        <div class="mt-4">
          <h2>Lyrics</h2>
          <p>{{ song.lyrics }}</p>
        </div>
      </div>
    </div>
  </div>
</section>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import store from '../store';


const router = useRouter();
const songName = ref('');
const song = ref('');
const album = ref('');
const rating = ref('');
let errorMessage = ref(null);

onMounted(async () => {
  try {
    const song_id = router.currentRoute.value.params.id; // Assuming you're passing the song ID through the URL
    const token = store.state.token;
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    // console.log(axios.defaults)
    const response = await axios.get('http://127.0.0.1:5000/song', {params : {song_id:song_id}});
    //console.log(response.data.song_path)

    songName.value = "/lyrics/"+response.data.song_path;
    song.value = response.data;
    album.value = response.data.album;
    
    
  } catch (error) {
    console.error('Error fetching song details:', error);
  }
});



const submitRating = async () => {
        try{
          
          console.log(rating.value)
          const songId= router.currentRoute.value.params.id;
          const userId = store.state.user[0]
          console.log(songId)
          console.log(userId)
          const response = await axios.post('http://127.0.0.1:5000/rating', { user_id : userId, song_id: songId, rating: rating.value});
          console.log(response.data.message)
          errorMessage.value = response.data.message

        } catch (error) {
          console.error("Error adding song to playlist", error);
        }
      };

const flagSong = async () => {
      try {
        const songId= router.currentRoute.value.params.id;
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.patch('http://127.0.0.1:5000/song', {
          flagged: true,
        }, {
          params: {
            song_id: songId
          }
        });
  
  
        // Handle success and song feedback to the user
        console.log(response.data.message);
        errorMessage.value = response.data.message
        
      } catch (error) {
        console.error("Error flagging song", error);
      }
    }
  
</script>

<style scoped>
.music-app-container {
  background-color: #1f2530; 
  color: #ffffff; 
}

.album-artwork-container {
  background-color: #2c3542; 
  padding: 15px; 
}

.dashboard-container{
  background-color: lightslategrey;
}

.prompt-message {
  color: #F5F2E7;
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  background-color: #2666CF;
  border-radius: 4px;
  text-align: center;
}


</style>