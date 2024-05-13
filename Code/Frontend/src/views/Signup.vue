<!-- views/Signup.vue -->
<template>
  <div>
    <form @submit.prevent="handleSignup" class="container mt-5">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <h2 class="text-left mb-4">SignUp</h2>
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="name" id="name" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" class="form-control" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn btn-dark">SignUp</button>
    </form>
  </div>
</template>
    
<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import store from "../store";

const name = ref("");
const email = ref("");
const password = ref("");
let errorMessage = ref("");

const router = useRouter();

async function handleSignup() {
  try {
    const response = await axios.post("http://127.0.0.1:5000/signup", {
      name: name.value,
      email: email.value,
      password: password.value,
    });
    console.log(response.data.token);
    store.commit("setToken", response.data.token);
    store.commit('setUser', [response.data.user_id, email.value]);
    store.commit('setRole', response.data.role);

    router.push("/dashboard");
  } catch (error) {
    if (error.response && error.response.status === 403) {
      errorMessage.value = error.response.data.message;
    } else {
      // Handle other types of errors (network errors, server errors, etc.)
      errorMessage.value =
        "An error occurred during signup. Please try again later.";
      console.error(error);
    }
  }
}
</script>
