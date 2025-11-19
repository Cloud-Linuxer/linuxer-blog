# Linuxer Blog - Hugo Migration

This repository contains the migrated WordPress blog to Hugo static site generator.

## Migration Details

- **Original Platform**: WordPress
- **New Platform**: Hugo v0.146.0
- **Theme**: PaperMod
- **Total Posts Migrated**: 198
- **Migration Success Rate**: 100%
- **Date Range**: 2019-08-21 to 2025-09-13

## Features

- Clean, modern PaperMod theme
- Full-text search enabled
- SEO optimized with meta tags
- Code syntax highlighting
- Categories and tags preserved
- URL aliases for backward compatibility
- Automatic deployment via GitHub Actions

## Structure

```
linuxer-hugo/
├── content/posts/     # All blog posts (198 posts)
├── themes/PaperMod/   # PaperMod theme (git submodule)
├── hugo.toml          # Hugo configuration
└── .github/workflows/ # GitHub Actions for deployment
```

## Local Development

```bash
# Build the site
hugo --minify

# Run development server
hugo server -D

# Build for production
hugo --minify --gc
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

Custom domain: **linuxer.name**

## Migration Statistics

- Posts processed: 198
- Successfully migrated: 198 (100%)
- Failed: 0
- Images found: 0 (preserved original WordPress image URLs)
- Generated pages: 967 (including archives, categories, tags)
- Build time: ~626ms

## Content Categories

- AWS (Cloud Computing)
- Kubernetes
- Linux
- Certification Reviews
- Cloud Platforms (AWS, GCP, Azure, NCP)
- DevOps and Infrastructure

## License

Content: All rights reserved by the original author
Theme: MIT License (PaperMod)
