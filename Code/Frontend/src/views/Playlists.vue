<template>
  <section class="playlist-background">
    <div class="container">
    <h1 class="text-white">Playlists</h1>

    <!-- Display Playlists -->
    <div class="music-app-container">
    <ul v-if="playlists.length" class="list-group">
      <li v-for="playlist in playlists" :key="playlist.id" class="list-group-item playlist-item">
        <router-link :to="{ name: 'PlaylistSong', params: { playlistId: playlist.id } }" class="playlist-link">
          {{ playlist.playlist_name }}
        </router-link>
        <button v-show="songId>0" @click="handleSongAdd(playlist.id)" class="btn btn-secondary btn-sm">Add</button>
        <button @click="handleDeletePlaylist(playlist.id)" class="btn btn-danger btn-sm">Delete</button>
      </li>
    </ul>
    <p v-else>No playlists found.</p>

    <!-- Create New Playlist Form -->
    <form @submit.prevent="createPlaylist" class="mt-3">
      <div class="form-group">
        <label for="playlistName">Playlist Name</label>
        <input v-model="newPlaylistName" type="text" class="form-control" id="playlistName" required>
      </div>
      <button type="submit" class="btn btn-primary">Create Playlist</button>
    </form>
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
      const playlists = ref([]);
      const newPlaylistName = ref('');
      const route = useRouter();
      const songId = route.currentRoute.value.params.songId;
       

      const handleSongAdd = async (playlistId) => {
        try{
          const response = await axios.post('http://127.0.0.1:5000/playlistsong', { playlist_id : playlistId, song_id: songId});
          console.log(response.data.message)
          route.push('/dashboard');
        } catch (error) {
          console.error("Error adding song to playlist", error);
        }
      };

      const handleDeletePlaylist = async (playlistId) => {
        try{
          const response = await axios.delete(`http://127.0.0.1:5000/playlists?playlist_id=${playlistId}`)
          console.log(response.data.message)
          await loadPlaylists();
        } catch (error) {
          console.error('Error deleting playlist', error)
        }
      }
  
      const loadPlaylists = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:5000/playlists');
          playlists.value = response.data;
          console.log(playlists.value)
        } catch (error) {
          console.error('Error loading playlists', error);
        }
      };
  
      const createPlaylist = async () => {
        try {
          await axios.post('http://127.0.0.1:5000/playlists', { playlist_name: newPlaylistName.value });
          // Refresh the playlists after creating a new one
          await loadPlaylists();
         
          newPlaylistName.value = '';
        } catch (error) {
          console.error('Error creating playlist', error);
        }
      };
  
      onMounted(() => {
        // Load playlists when the component is mounted
        loadPlaylists();
      });
  
      return {
        playlists,
        newPlaylistName,
        createPlaylist,
        handleSongAdd,
        handleDeletePlaylist,
        songId
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
  