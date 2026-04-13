<script setup>
import { ref, onMounted } from "vue";

const apiOrigin = (import.meta.env.VITE_API_ORIGIN || "").replace(/\/$/, "");

function apiUrl(path) {
  const p = path.startsWith("/") ? path : `/${path}`;
  return apiOrigin ? `${apiOrigin}${p}` : p;
}

const fetchOpts = {
  credentials: apiOrigin ? "include" : "same-origin",
};

let movies = ref([]);

function posterSrc(posterPath) {
  if (!posterPath) return "";
  return apiUrl(posterPath);
}

function fetchMovies() {
  return fetch(apiUrl("/api/v1/movies"), { credentials: fetchOpts.credentials })
    .then((r) => r.json())
    .then((data) => {
      movies.value = Array.isArray(data.movies) ? data.movies : [];
    })
    .catch(() => {
      movies.value = [];
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<template>
  <div class="container">
    <h1 class="mb-4">Movies</h1>

    <div
      v-for="movie in movies"
      :key="movie.id"
      class="card mb-3 shadow-sm overflow-hidden"
    >
      <div class="row g-0">
        <div class="col-md-4 col-lg-3">
          <img
            v-if="movie.poster"
            :src="posterSrc(movie.poster)"
            class="img-fluid w-100 rounded-start"
            style="min-height: 200px; object-fit: cover"
            :alt="movie.title"
          />
        </div>
        <div class="col-md-8 col-lg-9">
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <p v-if="!movies.length" class="text-muted">No movies yet. Add one from the menu.</p>
  </div>
</template>

<style scoped>
/* Add any component specific styles here */
</style>
