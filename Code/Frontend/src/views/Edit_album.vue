<template>
  <section class="dashboard-container">
    <div>
      <form @submit.prevent="updateAlbum" class="container">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2 class="text-left mb-4 text-white">Edit Album</h2>
        <div class="form-group">
          <label class="text-white" for="album_name">Album Name:</label>
          <input type="text" id="album_name" v-model="album_name" class="form-control" required>
        </div>
        <div class="form-group">
          <label class="text-white" for="genre">Genre:</label>
          <input type="text" id="genre" v-model="genre" class="form-control" required>
        </div>
        <div class="form-group">
          <label class="text-white" for="artist">Artist:</label>
          <input type="text" id="artist" v-model="artist" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-dark">Update</button>
      </form>
    </div>
  </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';
  
  const album_name = ref('');
  const genre = ref('');
  const artist = ref('');
  let errorMessage = ref('');

  const route = useRouter();
  const album_id = route.currentRoute.value.params.id;

  
// Fetch the song details from the backend API when the component is mounted
onMounted(async () => {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get('http://127.0.0.1:5000/album', {params : {album_id:album_id}});
        album_name.value = response.data.album_name;
        genre.value = response.data.genre;
        artist.value = response.data.artist;

        console.log(response.data);

      } catch (error) {
        console.error(error);
        
      }
    });
  
async function updateAlbum() {
      try {

        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.patch('http://127.0.0.1:5000/album', {
            album_name: album_name.value,
            genre: genre.value,
            artist: artist.value,
        }, {
          params: {
            album_id: album_id
          }
        });
  
  
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        errorMessage.value = 'An error occurred during album updation. Please try again later.';
        console.error(error);
      }
}

  </script>
  
<style scoped>
.dashboard-container{
  background-color: #395B64;
}

</style>

