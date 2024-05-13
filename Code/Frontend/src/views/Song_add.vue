<template>
  <section class="dashboard-container">
    <div>
      <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="container">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2 class="text-left mb-4 text-white">Add New Song</h2>
          <div class="form-group">
            <label class="text-white" for="song_name">Song Name:</label>
            <input type="text" id="song_name" v-model="song_name" required>
          </div>
          <div class="form-group">
            <label class="text-white" for="file">Song File:</label>
           <input class="text-white" type="file" id="file" @change="handleFileChange" accept=".mp3" required>
          </div>
          <div class="form-group">
            <label class="text-white" for="rating">Rating:</label>
            <input type="number" id="rating" v-model="rating" min="1" max="5" required>
          </div>
          <div class="form-group">
            <label class="text-white" for="lyrics">Lyrics:</label>
            <input type="text" id="lyrics" v-model="lyrics" required>
          </div>
          <div class="form-group">
            <label class="text-white" for="duration">Duration:</label>
            <input type="number" id="duration" v-model="duration" required>
          </div>
          <div class="form-group">
            <label class="text-white" for="date_created">Date Created:</label>
            <input type="date" id="date_created" v-model="date_created" required>
          </div>
          
        <button type="submit" class="btn btn-dark">Add Song</button>
      </form>
    </div>
  </section>
</template>

<script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';
  
  const route = useRouter();

  const song_name = ref('');
  const rating = ref('');
  const lyrics = ref('');
  const duration = ref('');
  const date_created = ref('');


  const album_id = route.currentRoute.value.params.id;
  
  let errorMessage = ref(null);
  const fileInput = ref('');
  
  function handleFileChange(event) {

    fileInput.value = event.target.files[0];
    
}

  async function handleSubmit(event) {
    try {

      
      const formData = new FormData();
      formData.append('file', fileInput.value);

      // Add your other form data to the FormData object
      formData.append('song_name', song_name.value);
      formData.append('rating', rating.value);
      formData.append('lyrics', lyrics.value);
      formData.append('duration', duration.value);
      formData.append('date_created', date_created.value);
      formData.append('album_id', album_id);
      for (const entry of formData.entries()) {
        console.log(entry);
      }

      const token = store.state.token;
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;


      const response = await axios.post('http://127.0.0.1:5000/song', formData, { headers: {'Content-Type': 'multipart/form-data'}});

      
      // Handle success and song feedback to the user

      console.log(response.data.message);
      route.push('/dashboard');

    } catch (error) {
      // Handle error and song feedback to the user (e.g., toast message)
      errorMessage.value = 'An error occurred during song creation. Please try again later.';
      console.error(error);
    }
  }
</script>
  

<style scoped>

.dashboard-container{
  background-color: #395B64;
}

</style>
