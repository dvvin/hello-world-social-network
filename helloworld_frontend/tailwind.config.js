/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
        'm-plus-1p': ['"M PLUS 1p"', 'sans-serif'],
        'm-plus-rounded-1c': ['"M PLUS Rounded 1c"', 'sans-serif']
      },
    },
  },
  plugins: [],
}

