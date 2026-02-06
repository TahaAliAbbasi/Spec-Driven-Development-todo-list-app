/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f5f5f5',
          100: '#e5e5e5',
          200: '#d4d4d4',
          300: '#a3a3a3',
          400: '#737373',
          500: '#525252',
          600: '#404040',
          700: '#262626',
          800: '#171717',
          900: '#0a0a0a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
  safelist: [
    // Safelist classes that might be dynamically generated
    'bg-primary-50', 'bg-primary-100', 'bg-primary-200', 'bg-primary-300', 'bg-primary-400',
    'bg-primary-500', 'bg-primary-600', 'bg-primary-700', 'bg-primary-800', 'bg-primary-900',
    'bg-gray-50', 'bg-gray-100', 'bg-gray-200', 'bg-gray-300', 'bg-gray-400',
    'bg-gray-500', 'bg-gray-600', 'bg-gray-700', 'bg-gray-800', 'bg-gray-900',
    'border-primary-500', 'border-gray-300', 'border-gray-200',
    'text-primary-700', 'text-gray-800', 'text-gray-700', 'text-gray-600', 'text-gray-500', 'text-gray-400',
    'focus:ring-primary-500', 'focus:ring-gray-500', 'focus:ring-red-500',
    'hover:bg-primary-200', 'hover:bg-primary-700', 'hover:bg-gray-100', 'hover:bg-gray-300',
    'min-h-11', 'min-w-11',
    'px-4', 'py-2', 'px-3', 'py-1.5', 'px-6', 'py-3',
    'text-sm', 'text-base', 'text-lg',
  ],
}