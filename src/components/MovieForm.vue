<template>
  <form id="movieForm" @submit.prevent="saveMovie">
    <div v-if="successMessage" class="alert alert-success" role="alert">
      {{ successMessage }}
    </div>
    <div v-if="errorMessages.length" class="alert alert-danger" role="alert">
      <ul class="mb-0 ps-3">
        <li v-for="(msg, index) in errorMessages" :key="index">{{ msg }}</li>
      </ul>
    </div>

    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input
        id="title"
        type="text"
        name="title"
        class="form-control"
      />
    </div>

    <div class="form-group mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea
        id="description"
        name="description"
        class="form-control"
        rows="5"
      ></textarea>
    </div>

    <div class="form-group mb-3">
      <label for="poster" class="form-label">Movie Poster</label>
      <input
        id="poster"
        type="file"
        name="poster"
        class="form-control"
        accept="image/jpeg,image/png,image/gif,.jpg,.jpeg,.png,.gif"
      />
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
const successMessage = ref("");
const errorMessages = ref([]);

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

onMounted(() => {
  getCsrfToken();
});

function saveMovie() {
  successMessage.value = "";
  errorMessages.value = [];

  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(function (response) {
      return response.json().then(function (data) {
        return { ok: response.ok, status: response.status, data };
      });
    })
    .then(function (result) {
      const data = result.data;
      if (!result.ok) {
        if (data.errors && data.errors.length) {
          errorMessages.value = data.errors;
        } else {
          errorMessages.value = [
            (data.message || "Request failed") + " (HTTP " + result.status + ")",
          ];
        }
        return;
      }
      if (data.errors && data.errors.length) {
        errorMessages.value = data.errors;
        return;
      }
      successMessage.value = data.message || "Movie Successfully added";
      errorMessages.value = [];
      console.log(data);
    })
    .catch(function (error) {
      console.log(error);
      errorMessages.value = ["Network error: " + String(error)];
    });
}
</script>

<style scoped>
/* Add any component specific styles here */
</style>
