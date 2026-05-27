import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://toolbreakdown.com',
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
