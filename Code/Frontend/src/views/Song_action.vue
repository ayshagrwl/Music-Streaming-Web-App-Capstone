<template>
  <section class="dashboard-container">
    <div>
        <form @submit.prevent="updateSong" class="container">
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  
          <h2 class="text-left mb-4 text-white">Edit/Delete Song</h2>
            <div class="form-group">
              <label class="text-white" for="song_name">Song Name:</label>
              <input type="text" id="song_name" v-model="song_name" required>
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
          <button type="submit" class="btn btn-dark">Update</button>
          <button @click="deleteSong" class="btn btn-danger">Delete</button>

        </form>

      </div>
    </section>
</template>
  
<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';
    import store from '../store';
  
    const route = useRouter();
    const song_id = route.currentRoute.value.params.id;
  
    
    const song_name = ref('');
    const rating = ref('');
    const lyrics = ref('');
    const duration = ref('');
    const date_created = ref('');
   

    
    const errorMessage = ref('');

    // Fetch the song details from the backend API when the component is mounted
    onMounted(async () => {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get('http://127.0.0.1:5000/song', {params : {song_id:song_id}});
        song_name.value = response.data.song_name;
        rating.value = response.data.rating;
        lyrics.value = response.data.lyrics;
        duration.value = response.data.duration;
        date_created.value = response.data.date_created;
        

      } catch (error) {
        console.error(error);
        
      }
    });
  
    async function updateSong() {
      try {

        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.patch('http://127.0.0.1:5000/song', {
          song_name: song_name.value,
          rating: rating.value,
          lyrics: lyrics.value,
          duration: duration.value,
          date_created: date_created.value,
        }, {
          params: {
            song_id: song_id
          }
        });
  
  
        // Handle success and song feedback to the user
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        errorMessage.value = 'An error occurred during song updation. Please try again later.';
        console.error(error);
      }
    }
  
    async function deleteSong() {
        // Prevent the form submission
        event.preventDefault(); 

      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.delete(`http://127.0.0.1:5000/song`, {
          params: {
            song_id: song_id
          }
        });
  
        // Handle success and song feedback to the user
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        // Handle error and song feedback to the user (e.g., toast message)
        errorMessage.value = 'An error occurred during song deletion. Please try again later.';
        console.error(error);
      }
    }
</script>
  

<style scoped>

.dashboard-container{
  background-color: #395B64;
}

</style>
