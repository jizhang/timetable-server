import { defineConfig, UserConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteMockServe } from 'vite-plugin-mock'
import { fileURLToPath, URL } from 'url'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const mockEnabled = command === 'serve' && process.env.MOCK !== 'none'

  const config: UserConfig = {
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    plugins: [
      vue(),
      viteMockServe({
        localEnabled: mockEnabled,
        prodEnabled: false,
      }),
    ],
  }

  if (!mockEnabled) {
    config.server = {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:5001',
        },
      },
    }
  }

  return config
})
