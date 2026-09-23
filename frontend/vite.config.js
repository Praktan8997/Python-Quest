import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  // Load env vars for the current mode (development / production)
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    // In production, VITE_API_BASE_URL points to the Render backend URL.
    // In development, proxy /api to local backend to avoid CORS issues.
    server: {
      port: 5173,
      proxy: mode === 'development' ? {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false,
        },
      } : undefined,
    },
    build: {
      outDir: 'dist',
      sourcemap: false,
    },
  };
});
