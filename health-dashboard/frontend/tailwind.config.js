/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0f172a",
        surface: "#1e293b",
        border: "#334155",
        muted: "#64748b",
        accent: {
          garmin: "#00b3e6",
          strava: "#fc4c02",
          rempho: "#7c3aed",
        },
      },
    },
  },
  plugins: [],
};
