import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  plugins: [sveltekit()],

  build: {
    assetsDir: 'static'
  },

  server: {
    port: 5000,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        secure: false
      },
      '/feed': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        secure: false
      },
      '/media': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        secure: false
      }
    }
  },

  test: {
    include: ['src/**/*.{test,spec}.{js,ts}']
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@use "src/variables.scss" as *;'
      }
    }
  }
});
// TODO: development & production versions of this file?  For non devserver front-end serving.
