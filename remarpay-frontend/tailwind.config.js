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
        forest: "#014421",
        gold: "#D4AF37",
      },
    },
  },
  darkMode: "class", // Keep dark mode support
  plugins: [],
};
