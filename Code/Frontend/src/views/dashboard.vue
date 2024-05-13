<template>
  <div >
    <section class="dashboard-container">
      

      <div v-if="user && role==='creator'" class="container">
    <h1 class="dashboard-heading text-white mb-4">Music Studio Dashboard</h1>

    <!-- Add New Album Button -->
    <router-link to="/add-album" class="btn btn-success">Add New Album</router-link>
    <br>

    <!-- Dashboard Box -->
    <div class="dashboard-box mt-4">
      
      <div v-for="album in user.albums" :key="album.album_id" class="card mb-4 bg-dark text-white">
        <div class="card-body">
          <h3 class="card-title">{{ album.album_name }}</h3>

          
          <div class="album-buttons mt-3">
            <!-- Edit Album Button -->
            <router-link :to="{ name: 'Edit_album', params: { id: album.album_id }}" class="btn btn-secondary mr-2">Edit</router-link>
            <!-- Delete Album Button -->
            <button @click="deleteAlbum(album.album_id)" class="btn btn-danger mr-2">Delete</button>
            <!-- Add New Song Button -->
            <router-link :to="{ name: 'Song_add', params: { id: album.album_id }}" class="btn btn-success mr-2">Add New Song</router-link>
            </div>

          <hr class="dashboard-divider mt-3"/>

          <!-- Song List -->
          <div class="song-list mt-3">
            
            <div v-for="song in album.songs" :key="song.song_id" class="card bg-secondary text-white">
              <div class="card-body">
                <h4 class="card-title">{{ song.song_name }}</h4>
                
                <router-link :to="{ name: 'Song_action', params: { id: song.song_id }}" class="btn btn-primary">Edit/Delete</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
            
      <div v-else-if="user && role==='admin'" class="container">
        <h1 class="text-white">Admin Management</h1>
        <div class="container mt-5">
    <div class="row">
        <div class="col-md-3 mb-4">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Creators</h5>
                    <h1 class="display-4">{{ metrics[0].total_creator_user }}</h1>
                    <p class="card-text">Creators</p>
                </div>
            </div>
        </div>
    
        <div class="col-md-3 mb-4">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Playlist</h5>
                    <h1 class="display-4">{{ metrics[0].total_playlist }}</h1>
                    <p class="card-text">Number of playlist created</p>
                </div>
            </div>
        </div>
    
        <div class="col-md-3 mb-4">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Rating</h5>
                    <h1 class="display-4">{{ metrics[0].total_rating }}</h1>
                    <p class="card-text">Rating of songs</p>
                </div>
            </div>
        </div>
    
        <div class="col-md-3 mb-4">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Total Songs</h5>
                    <h1 class="display-4">{{ metrics[0].total_songs }}</h1>
                    <p class="card-text">Songs uploaded</p>
                </div>
            </div>
        </div>
    </div>
</div>


        <div class="dashboard-box mt-4">
      <!-- Album Cards -->
      
      <div v-for="album in user.albums" :key="album.album_id" class="card mb-4 bg-dark text-white">
    <div class="card-body">
        <h3 class="card-title">{{ album.album_name }}</h3>

        <!-- Album Buttons -->
        <div class="album-buttons mt-3">
            <button @click="deleteAlbum(album.album_id)" class="btn btn-danger mr-2">Delete Album</button>
        </div>

        <hr class="dashboard-divider mt-3"/>

        <!-- Song List -->
        <div class="song-list mt-3">
           
            <div v-for="song in album.songs" :key="song.song_id" class="card bg-secondary text-white mb-2">
                <div class="card-body">
                    <h4 class="card-title">
                        {{ song.song_name }} 
                        <span v-if="song.is_flagged" class="btn btn-info text-white">Flagged</span>
                    </h4>
                    <p class="card-text">
                        Total Ratings Received: {{ totalRatingsPer[song.song_id] || 0 }}
                    </p>
                    
                    <button @click="deleteSong(song.song_id)" class="btn btn-danger mr-2">Delete Song</button>
                </div>
            </div>
        </div>
    </div>
</div>

    
    </div>

      </div>

      <!-- Song the user dashboard if the user is a normal user -->
      <div v-else-if="user && role==='user'" class="container">
    <!-- User Dashboard Heading -->
    <h1 class="dashboard-heading text-white">Music Dashboard</h1>

    <!-- Search Container -->
    <div class="search-container mt-4">

      <input v-model="searchQuery" @input="performSearch(searchQuery)" type="text" placeholder="Search songs by artist, genre, or song name" class="form-control search-input" />

      <!-- Search Results -->
      <div v-if="searchQuery !== ''" class="search-results mt-3">
        <p class="text-left font-weight-bold h5 text-white">Search Results:</p>
        <div v-for="result in searchResults" :key="result.song_id" class="search-result card mb-3 bg-dark text-white">
          <div class="card-body">
            
            <h3>{{ result.song_name }}</h3>
            <p class="music-info">Rating: {{ result.rating }}/5</p> 
            <router-link :to="{ name: 'ViewLyrics', params: { id: result.song_id }}" class="btn btn-info ">View Lyrics</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Album List -->
    <div class="album-list mt-4">
      <div v-for="album in user.albums" :key="album.album_id" class="album-box card mb-3 bg-dark text-white">
        <div class="card-body">
          <ul class="list-links">
          <li><h2>{{ album.album_name }}</h2></li>
          <li><p class="album-location"><b>Artist -</b> {{ album.artist }}</p></li>
          <li><p class="album-location"><b>Genre -</b> {{ album.genre }}</p></li>
          </ul>

          <!-- Song List -->
          <div class="music-list mt-3">
            <div v-for="song in album.songs" :key="song.song_id" class="music-card card mb-3 bg-secondary text-white">
              
              <div class="card-body">
                <ul class="list-links">
                <li><h3>{{ song.song_name }}</h3></li>
                <li><p class="price"><b>Rating:</b> {{ song.rating }}/5</p></li>
                <li><p class="rating"><b>Duration:</b> {{ song.duration }} sec</p></li>
                </ul>

                
                <router-link :to="{ name: 'playlists', params: { songId: song.song_id}}" class="btn btn-primary mr-2">Add to Playlist</router-link>
                <router-link :to="{ name: 'ViewLyrics', params: { id: song.song_id }}" class="btn btn-info ">View Lyrics</router-link>
              </div>
               
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    </section>
  </div>
</template>

  
<script setup>
import axios from "axios";
import store from "../store";

import { ref, onMounted } from "vue";



const errorMessage = ref("");
const searchQuery = ref("");
const searchResults = ref("");


const user = ref("");
let role = ref("");

const totalRatingsPer = ref('')
const metrics = ref('')

const fetchData = async () => {
  try{

    const token = store.state.token;
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    const response = await axios.get("http://127.0.0.1:5000/home");

    user.value = response.data;
    console.log(user._rawValue);
    metrics.value = response.data.metrics;
    console.log(metrics);
    role = store.state.role;




    const totalRatingsPerSong = user._rawValue.albums.reduce((acc, albums) => {


        
          albums.songs.forEach(song => {
            const songId = song.song_id;
            const songRating = song.ratings.reduce((total, rating) => total + 1, 0);

            if (!acc[songId]) {
              acc[songId] = songRating;
            } else {
              acc[songId] += songRating;
            }
          });
        
      

      return acc;
    }, {});

    totalRatingsPer.value = totalRatingsPerSong


  }
  catch (error) {
    errorMessage.value = "An error occurred during user fetch. Please try again later.";
    console.error(error);
  }
};

onMounted(() => {
  // Call the function to fetch the user data when the component is mounted
  fetchData();
  
});



async function deleteAlbum(album_id) {

      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.delete(`http://127.0.0.1:5000/album`, {params: {album_id: album_id}});
  
        // Handle success and song feedback to the user
        console.log(response.data.message);
        fetchData();
      } 
      catch (error) {
        // Handle error and song feedback to the user (e.g., toast message)
        errorMessage.value = 'An error occurred during album deletion. Please try again later.';
        console.error(error);
      }
    }
async function deleteSong(song_id) {
try {
  const token = store.state.token;
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  const response = await axios.delete(`http://127.0.0.1:5000/song`, {params: {song_id: song_id}});

  // Handle success and song feedback to the user
  console.log(response.data.message);
  fetchData();
} 
catch (error) {
  // Handle error and song feedback to the user (e.g., toast message)
  errorMessage.value = 'An error occurred during song deletion. Please try again later.';
  console.error(error);
}
}

async function performSearch(searchQuery){
  
    try {
      const token = store.state.token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await axios.get(`http://127.0.0.1:5000/search`, {params: {searchQuery: searchQuery}});
      
      searchResults.value = response.data.songs;
      console.log(searchResults);

    } catch (error) {
      errorMessage.value = 'An error occurred during search. Please try again later.';
      console.error("Error performing search:", error);
      
      
    }
};
</script>


<style scoped>


.list-links{
  list-style: none;
  padding: 0;
  display: flex;
}

.list-links li{
  margin-right: 20px;
}

.list-links p {
  margin-top: 10px;
}


.dashboard-container{
  background-color: #395B64;
}
.dashboard-heading {
  font-size: 2.5rem;
  font-weight: bold;
}


.album-buttons button,
.song-list .card {
  border-radius: 10px;
  margin-bottom: 0.5rem;
}

.dashboard-divider {
  background-color: #fff;
}

</style>


