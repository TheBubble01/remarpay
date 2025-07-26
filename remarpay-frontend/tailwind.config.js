// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        forest: "#041c05ff",
        gold: "#e6be8a",
      },
    },
  },
  darkMode: "class", // Keep dark mode support
  plugins: [],
};
