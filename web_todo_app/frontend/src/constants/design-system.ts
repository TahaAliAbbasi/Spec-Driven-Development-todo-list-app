// Design System Constants
// Color Palette
export const COLORS = {
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
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#e5e5e5',
    300: '#d4d4d4',
    400: '#a3a3a3',
    500: '#737373',
    600: '#525252',
    700: '#404040',
    800: '#262626',
    900: '#171717',
  },
  success: {
    500: '#10b981',
  },
  warning: {
    500: '#f59e0b',
  },
  error: {
    500: '#ef4444',
  },
  background: {
    light: '#f9fafb',
    dark: '#111827',
  },
  text: {
    primary: '#1f2937',
    secondary: '#6b7280',
    inverted: '#ffffff',
  },
};

// Typography Scale
export const TYPOGRAPHY = {
  h1: 'text-4xl font-bold leading-tight',
  h2: 'text-3xl font-bold leading-snug',
  h3: 'text-2xl font-bold leading-relaxed',
  h4: 'text-xl font-semibold',
  body: 'text-base font-normal leading-normal',
  small: 'text-sm font-normal leading-tight',
  caption: 'text-xs font-normal leading-tight',
};

// Spacing System (Tailwind default spacing)
export const SPACING = {
  xs: 'space-y-1 space-x-1', // 4px
  sm: 'space-y-2 space-x-2', // 8px
  md: 'space-y-3 space-x-3', // 12px
  lg: 'space-y-4 space-x-4', // 16px
  xl: 'space-y-6 space-x-6', // 24px
  '2xl': 'space-y-8 space-x-8', // 32px
};

// Breakpoints
export const BREAKPOINTS = {
  sm: '640px',  // Mobile
  md: '768px',  // Tablet
  lg: '1024px', // Desktop
  xl: '1280px', // Large Desktop
  '2xl': '1536px', // Extra Large Desktop
};

// Component Sizing
export const SIZING = {
  touchTarget: 'h-11 w-11', // 44px for accessibility
  button: {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  },
  input: {
    height: 'h-10',
    fontSize: 'text-base',
  },
};

// Border Radius
export const BORDER_RADIUS = {
  sm: 'rounded',
  md: 'rounded-md',
  lg: 'rounded-lg',
  xl: 'rounded-xl',
  full: 'rounded-full',
};

// Shadows
export const SHADOWS = {
  sm: 'shadow-sm',
  md: 'shadow',
  lg: 'shadow-md',
  xl: 'shadow-lg',
  '2xl': 'shadow-xl',
  inner: 'shadow-inner',
};