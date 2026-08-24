// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// The repo is a GitHub Pages *project* site, so it is served from a subpath.
// The repo was renamed MyPortfolio -> portfolio, so the site now lives at
// https://thetilakraj.github.io/portfolio/ and `base` must match the repo name
// exactly — a mismatch 404s every asset and the page renders unstyled.
// Never hardcode root-relative paths; use the `url()` helper in src/lib/url.ts.
export default defineConfig({
  site: 'https://thetilakraj.github.io',
  base: '/portfolio',
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],

  build: {
    // The page CSS gzips to ~7kB. Inlining it removes one render-blocking
    // round trip on the critical path, which is what FCP was waiting on.
    inlineStylesheets: 'always',
  },

  // Merriweather + Source Sans carried over from the original site. Downloaded
  // and self-hosted at build time — no Google Fonts request at runtime.
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Merriweather',
      cssVariable: '--font-merriweather',
      weights: [300, 700],
      styles: ['normal'],
      subsets: ['latin'],
      fallbacks: ['Georgia', 'serif'],
      display: 'swap',
    },
    {
      provider: fontProviders.google(),
      name: 'Source Sans 3',
      cssVariable: '--font-source',
      weights: [600, 900],
      styles: ['normal'],
      subsets: ['latin'],
      fallbacks: ['Helvetica Neue', 'Helvetica', 'sans-serif'],
    },
  ],

  vite: {
    plugins: [tailwindcss()],
  },
});
