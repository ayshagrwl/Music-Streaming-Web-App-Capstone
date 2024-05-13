<template>
  <section class="playlist-background">
  <div class="container">
    <h1 class="text-white">{{ playlistName.playlist_name }}</h1>

    <!-- Display Playlist Songs -->
    <div class="music-app-container">
    <ul v-if="playlistSongs.length" class="list-group">
      <li v-for="playlistSong in playlistSongs" :key="playlistSong.song_id" class="list-group-item playlist-item">
        {{ playlistSong.song.song_name }} | Album: {{ playlistSong.song.album.album_name }}
        
        <router-link :to="{ name: 'ViewLyrics', params: { id: playlistSong.song_id } }">
          <button class="btn btn-primary">View Lyrics</button>
        </router-link>
      </li>
    </ul>
    <p v-else>No songs found in the playlist.</p>
  </div>
  </div>
</section>
</template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

 
  
  export default {
    
    setup() {
      const route = useRouter();
      const playlistSongs = ref([]);
      const playlistName = ref('');
      const newSongId = ref('');
      const playlistId = route.currentRoute.value.params.playlistId;
  
      const loadPlaylistSongs = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/playlistsong?playlist_id=${playlistId}`);
          playlistSongs.value = response.data;
          playlistName.value = response.data[0].playlist
          console.log(playlistName);
        } catch (error) {
          console.error('Error loading playlist songs', error);
        }
      };
  
      
  
      
  
      onMounted(() => {
        // Load playlist songs when the component is mounted
        loadPlaylistSongs();
      });
  
      return {
        playlistSongs,
        playlistName,
        newSongId,
     
    };
  },
};
</script>

<style scoped>
  .music-app-container {
    background-color: #1f2530; 
    color: #ffffff; 
    padding: 20px; 
  }
  
  .playlist-item {
    background-color: white; 
    margin-top: 10px; 
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }
  
  .playlist-link {
    color: #2C3333; 
    text-decoration: none; 
  }
  
  form {
    max-width: 400px; 
  }

  .playlist-background{
    background-color: #395B64;
  }
  </style>
       
  