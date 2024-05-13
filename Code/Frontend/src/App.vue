<script setup>
import { RouterLink, RouterView } from 'vue-router'
import store from './store';
import router from './router';
import { computed } from 'vue';
import axios from "axios";



async function handleLogout() {
  await store.dispatch('logout');
  router.push('/login'); // Redirect to home page after logout
}

const toggleCreator = async () => {
  try {
    // This make a POST request to the toggle user to creator
    const response = await axios.post("http://127.0.0.1:5000/toggle-creator", {}, {
      headers: {
        Authorization: `Bearer ${store.state.token}`
      }
     
    });

    console.log(response.data.message);
    store.commit('setRole', 'creator');
    const role = store.state.role;
    console.log(role);
    router.push('/dashboard');

  } catch (error) {
    errorMessage.value = "Error toggling creator status";
    console.error(error);
  }
};


const isLoggedIn = computed(() => {
  return store.state.token;
});

const isRole = computed(() => {
  return store.state.role;
  
})

const userName = computed(() => {
  if (store.state.user) {
    return store.state.user[1]
  } else {
    return null
  }
})


</script>

<template>
  <head>
    <title>BeatFlow - Your Daily Music Dose</title>
  </head>
  <body>
    <header>
      <nav>
        
        <ul class="nav-links">
          <li><router-link v-if="!isLoggedIn" to="/"><b>BeatFlow</b></router-link></li>
          <li><router-link v-if="!isLoggedIn" to="/login">Login</router-link></li>
          <li><router-link v-if="!isLoggedIn" to="/signup">Signup</router-link></li>
          <li><router-link v-if="!isLoggedIn" to="/admin">Admin Login</router-link></li>
          <li><router-link v-if="isLoggedIn" to="/dashboard">Home</router-link></li>
          <li><router-link v-if="isLoggedIn" to="/" @click="handleLogout">Logout</router-link></li>
          <li><router-link v-if="isLoggedIn && isRole==='user'" to="/playlists/0">Playlists</router-link></li>
          <li><router-link v-show="isLoggedIn && isRole==='user'" to="/dashboard" @click="toggleCreator">Become Creator</router-link></li>
         
          <li class="rightUserName">{{ userName }}</li>
        </ul>
      </nav>
      
      
    </header> 
    <RouterView />
    
    <footer>
      <div class="container">
        <p>Copyright &copy; Music Streaming App</p>
      </div>
    </footer>
  </body>
  
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.rightUserName{
  padding-left: 40%;
  color: #F5F2E7;
  display:inline-block;
}

/* Header Styles */
header {
  background-color: #2C3333;
  color: #fff;
  padding: 20px;
}

/* .logo h1 {
  margin: 0;
} */

.nav-links {
  list-style: none;
  padding: 0;
  display: flex;
}

.nav-links li {
  margin-right: 20px;
}

.nav-links li a {
  color: #fff;
  text-decoration: none;
}





.cta-btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #FF5722;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}

.btn:hover {
  filter: brightness(85%);
}



/* Footer Styles */
footer {
  background-color: #2C3333;
  color: #fff;
  padding: 5px 0;
  text-align: center;
}

</style>