/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f4788',
        secondary: '#2c5aa0',
        success: '#28a745',
        warning: '#ffc107',
        danger: '#dc3545',
        light: '#f8f9fa',
      },
    },
  },
  plugins: [],
}
