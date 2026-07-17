import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Aku brand palette — bold, African-inspired
        brand: {
          50: '#fef3e8',
          100: '#fde3c5',
          200: '#fac48d',
          300: '#f79d4d',
          400: '#f47a1a',
          500: '#e85f00',  // primary orange
          600: '#c44d00',
          700: '#9a3d00',
          800: '#6e2d00',
          900: '#451c00',
        },
        accent: {
          50: '#e6f0ff',
          100: '#cce0ff',
          200: '#99c2ff',
          300: '#66a3ff',
          400: '#3385ff',
          500: '#0066ff',  // accent blue
          600: '#0052cc',
          700: '#003d99',
          800: '#002966',
          900: '#001433',
        },
        dark: {
          50: '#f5f5f5',
          100: '#ebebeb',
          200: '#d6d6d6',
          300: '#b8b8b8',
          400: '#8f8f8f',
          500: '#666666',
          600: '#4d4d4d',
          700: '#333333',
          800: '#1a1a1a',
          900: '#0d0d0d',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Cal Sans', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-brand': 'linear-gradient(135deg, #e85f00 0%, #f79d4d 50%, #fac48d 100%)',
        'gradient-dark': 'linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%)',
        'fabric-pattern': "url('/images/fabric-pattern.svg')",
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
        'typing': 'typing 1.5s steps(3, end) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
        typing: {
          '0%': { content: '"."' },
          '33%': { content: '".."' },
          '66%': { content: '"..."' },
        },
      },
    },
  },
  plugins: [],
}

export default config
