/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        statwise: {
          navy: "#0A1931",        // Deep navy for authority and navigation
          navyActive: "#1A3D63",  // Active sidebar / header item state
          blue: "#4A7FA7",        // Medium blue for actions and active buttons
          pale: "#B3CFE5",        // Pale blue for surfaces, progress tracks, soft borders
          canvas: "#F6FAFD",      // Near-white for clean, readable content areas
          slate: "#334155",
          muted: "#64748B",
          border: "#E2E8F0"
        }
      },
      fontFamily: {
        sans: ['Inter', 'Segoe UI', 'Roboto', 'sans-serif']
      }
    },
  },
  plugins: [],
}
