<template>
  <form id="movieForm" @submit.prevent="saveMovie">
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

    <button type="submit" class="btn btn-primary" :disabled="!csrfReady">
      {{ csrfReady ? "Submit" : "Loading…" }}
    </button>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

/** Empty = use same-origin /api/... (Vite proxy). Set VITE_API_ORIGIN in .env.development to call Flask directly. */
const apiOrigin = (import.meta.env.VITE_API_ORIGIN || "").replace(/\/$/, "");

function apiUrl(path) {
  return apiOrigin ? `${apiOrigin}${path}` : path;
}

const fetchOpts = {
  credentials: apiOrigin ? "include" : "same-origin",
};

let csrf_token = ref("");
const csrfReady = ref(false);
const errorMessages = ref([]);

function parseJsonOrExplain(response, text) {
  const trimmed = (text || "").trim();
  if (!trimmed) {
    return {
      error: [
        "Empty response from server (HTTP " +
          response.status +
          "). Start Flask with: flask --app app run --debug",
      ],
    };
  }
  if (trimmed.startsWith("<!") || trimmed.toLowerCase().startsWith("<!doctype")) {
    return {
      error: [
        "Received HTML instead of JSON. Run Flask (flask --app app run --debug) on the port in .env.development " +
          "(VITE_API_ORIGIN, default 127.0.0.1:5000), restart npm run dev, or clear VITE_API_ORIGIN to use only the Vite proxy.",
      ],
    };
  }
  try {
    return { data: JSON.parse(trimmed) };
  } catch (e) {
    return {
      error: ["Invalid JSON from server (HTTP " + response.status + "): " + trimmed.slice(0, 120)],
    };
  }
}

function getCsrfToken() {
  csrfReady.value = false;
  return fetch(apiUrl("/api/v1/csrf-token"), { credentials: fetchOpts.credentials })
    .then((response) => response.text().then((text) => ({ response, text })))
    .then(({ response, text }) => {
      const parsed = parseJsonOrExplain(response, text);
      if (parsed.error) {
        console.error(parsed.error);
        errorMessages.value = parsed.error;
        return;
      }
      const data = parsed.data;
      csrf_token.value = data.csrf_token;
      csrfReady.value = Boolean(data.csrf_token);
    });
}

onMounted(() => {
  getCsrfToken();
});

function saveMovie() {
  errorMessages.value = [];

  if (!csrf_token.value) {
    errorMessages.value = [
      "Security token not ready yet. Wait a moment, or refresh the page.",
    ];
    getCsrfToken();
    return;
  }

  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);
  form_data.append("csrf_token", csrf_token.value);

  fetch(apiUrl("/api/v1/movies"), {
    method: "POST",
    body: form_data,
    credentials: fetchOpts.credentials,
    headers: {
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then(function (response) {
      return response.text().then(function (text) {
        const parsed = parseJsonOrExplain(response, text);
        if (parsed.error) {
          return { ok: false, status: response.status, data: {}, parseError: parsed.error };
        }
        return { ok: response.ok, status: response.status, data: parsed.data };
      });
    })
    .then(function (result) {
      if (result.parseError) {
        errorMessages.value = result.parseError;
        return;
      }
      const data = result.data;
      if (!result.ok) {
        const isCsrf =
          result.status === 400 &&
          Array.isArray(data.errors) &&
          data.errors.some((e) => String(e).toLowerCase().includes("csrf"));
        if (isCsrf) {
          return getCsrfToken().then(() => {
            errorMessages.value = [
              "Session or security token was out of date. Token refreshed — try Submit again.",
            ];
          });
        }
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
      errorMessages.value = [];
      sessionStorage.setItem(
        "flashMessage",
        data.message || "Movie Successfully added"
      );
      router.push({ name: "movies" });
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
