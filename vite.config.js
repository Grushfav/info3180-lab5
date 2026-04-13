import { fileURLToPath, URL } from 'url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  // Align with .env FLASK_RUN_PORT (default 8080 in this project).
  const flaskTarget =
    env.VITE_API_ORIGIN?.replace(/\/$/, '') || 'http://127.0.0.1:8080'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      proxy: {
        // Regex form: Vite treats keys starting with ^ as RegExp (see doesProxyContextMatchUrl).
        '^/api': {
          target: flaskTarget,
          changeOrigin: true
        }
      }
    }
  }
})
