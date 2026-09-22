/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        authkit: {
          bg: "#05060f",             // Midnight Canvas
          surface: "rgba(186, 214, 247, 0.03)", // Translucent frosted surface
          surfaceHover: "rgba(186, 214, 247, 0.06)",
          border: "rgba(186, 215, 247, 0.12)",  // Frosted inset border
          borderGlow: "rgba(186, 215, 247, 0.24)",
          violet: "#663af3",         // Void Violet (exclusive CTA)
          violetHover: "#542be3",
          highlight: "#F0F6FF",     // Ice Highlight
          glow: "#C8DCF5",          // Frost Glow
          mist: "#8AA4C4",          // Moon Mist
          veil: "#526884",          // Fog Veil
          darkCard: "#090b17",      // Deep midnight card
        },
        quest: {
          bg: "#05060f",
          card: "rgba(186, 214, 247, 0.03)",
          hover: "rgba(186, 214, 247, 0.06)",
          border: "rgba(186, 215, 247, 0.12)",
          accent: "#663af3",
          primary: "#F0F6FF",
          gold: "#663af3",
          emerald: "#8AA4C4",
          purple: "#663af3",
          rose: "#EF4444",
        }
      },
      fontFamily: {
        heading: ['"Outfit"', '"Inter"', 'sans-serif'],
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
        eyebrow: ['"Space Mono"', 'monospace'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glass-elevation': '0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 1px 1px 0 rgba(255, 255, 255, 0.05)',
        'glass-glow': '0 0 40px -10px rgba(102, 58, 243, 0.3)',
        'violet-glow': '0 0 25px rgba(102, 58, 243, 0.45)',
      },
      borderRadius: {
        'card': '16px',
        'input': '6px',
        'badge': '6px',
        'pill': '999px',
        'circle': '9999px',
      }
    },
  },
  plugins: [],
}
