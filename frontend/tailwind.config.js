/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0066cc",
        danger: "#dc2626",
        warning: "#f97316",
        success: "#16a34a",
      },
    },
  },
  plugins: [],
};
