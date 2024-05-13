<template>
  <section class="dashboard-container">
    <div>
      <form @submit.prevent="handleSubmit" class="container">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2 class="text-left mb-4 text-white">Add New Album</h2>
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
        <button type="submit" class="btn btn-dark">Add Album</button>
      </form>
    </div>
  </section>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const album_name = ref('');
  const genre = ref('');
  const artist = ref('');
  let errorMessage = ref('');

  const router = useRouter();
  
  async function handleSubmit() {
    try {
      const response = await axios.post('http://127.0.0.1:5000/album', {
        album_name: album_name.value,
        genre: genre.value,
        artist: artist.value,
        
      });
      
      console.log('Album created:', response.data);
      router.push('/dashboard'); // Redirect to admin dashboard after successful creation
    } catch (error) {
      // Handle error and song feedback to the user (e.g., toast message)
      errorMessage.value = 'An error occurred during album creation. Please try again later.';
      console.error(error);
    }
  }
  </script>
  
<style scoped>
.dashboard-container{
  background-color: #395B64;
}

</style>
