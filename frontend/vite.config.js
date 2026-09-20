import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
const proxyErrorHandler = (proxy) => {
  proxy.on('error', (err, _req, res) => {
    if (res && res.writeHead && !res.headersSent) {
      res.writeHead(503, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 503,
        error: "STATWISE FastAPI backend server is not running on http://127.0.0.1:8000.",
        message: "Please start the backend with 'npm run backend' or run 'run_app.bat'."
      }));
    }
  });
};

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        configure: proxyErrorHandler
      },
      '/health': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        configure: proxyErrorHandler
      },
      '/docs': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        configure: proxyErrorHandler
      },
      '/openapi.json': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        configure: proxyErrorHandler
      }
    }
  }
})
