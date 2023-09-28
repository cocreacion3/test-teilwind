/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx}"],
  theme: {
    extend: {
      backgroundImage: {
        'hero_pattern': "url('/src/svg/background3.svg')",
        // 'footer-texture': "url('/img/footer-texture.png')",
      }
    }
  },
  plugins: [],
}