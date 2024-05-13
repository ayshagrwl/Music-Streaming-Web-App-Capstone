<script setup>
</script>

<template>
  <section class="trending-songs dark-background">
    <div class="container">
      <h2 class="text-light">Trending Songs</h2>

      <div class="song-list">
        <div class="song-card">
          <img src="../assets/dunki.jpg" alt="Dunki song cover">
          <h3 class="text-light">O Maahi (From "Dunki")</h3>
          <p class="text-light">Duration: 3:53 </p>
          <router-link to="/Signup" class="btn btn-dark">View Lyrics</router-link>
        </div>
        <div class="song-card">
          <img src="../assets/animal.jpg" alt="animal song cover">
          <h3 class="text-light">Satranga (From "Animal")</h3>
          <p class="text-light">Duration: 4:31</p>
          <router-link to="/Signup" class="btn btn-dark">View Lyrics</router-link>
        </div>
        <div class="song-card">
          <img src="../assets/anuv_jain.jpg" alt="anuv jain cover">
          <h3 class="text-light">Husn (From "Anuv Jain")</h3>
          <p class="text-light">Duration: 3:37</p>
          <router-link to="/Signup" class="btn btn-dark">View Lyrics</router-link>
        </div>
      </div>
      <router-link to="/Signup" class="btn btn-large btn-dark w-100">View More Songs</router-link>
    </div>
  </section>
  <section class="about dark-background">
    <div class="container">
      <h2 class="text-light">Music Application System</h2>
      <p class="text-light">
        BeatFlow is an online platform that brings you a wide range of songs and albums from various genres.
        Whether you're a fan of artists or want to study songs, we have something for everyone.
      </p>
      <p class="text-light">
        With our easy-to-use interface, you can browse through the available songs, check out the albums,
        and add your song to the playlist in just a few clicks.
        We strive to provide you with a seamless music streaming experience and ensure that you have a fantastic time at every song you listen.
      </p>
    </div>
  </section>
</template>

<style scoped>
.dark-background {
  background-color: #395B64; 
}

.text-light {
  color: #5C8374;
}


.song-list {
  display: flex;
  justify-content: space-between;
}

.song-card{
  padding: 20px;
}
.song-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin-bottom: 20px;
}
</style>


