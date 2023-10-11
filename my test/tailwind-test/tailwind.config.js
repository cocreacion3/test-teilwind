/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx}", "./node_modules/tailwind-datepicker-react/dist/**/*.js"],
  theme: {
    extend: {
      backgroundImage: {
        'hero_pattern': "url('/src/svg/background.svg')",
      }
    }
  },
  plugins: [
    require('flowbite/plugin')
  ],
} 