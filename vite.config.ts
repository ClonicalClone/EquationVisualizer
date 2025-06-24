import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5000,
    strictPort: true,
    hmr: false,
    allowedHosts: "all",
  },
  define: {
    global: "globalThis",
  },
  resolve: {
    alias: {
      buffer: "buffer",
    },
  },
  optimizeDeps: {
    include: ["plotly.js-dist", "mathjs", "buffer"],
  },
});
