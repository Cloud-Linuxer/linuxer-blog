# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo-based technical blog (linuxer.name) migrated from WordPress. Korean/English bilingual content focusing on AWS, Kubernetes, and Linux systems engineering.

- **Platform**: Hugo v0.146.0 Extended
- **Theme**: PaperMod (customized with Matrix terminal aesthetic)
- **Posts**: 198 migrated articles (2019-2025)
- **Images**: 689 optimized images (58MB)
- **Deployment**: AWS S3 + CloudFront via GitHub Actions

## Development Commands

### Build and Test
```bash
# Clean rebuild
rm -rf public resources && hugo --minify

# Development server
hugo server --bind 0.0.0.0 --port 1313 --disableFastRender

# Production build
hugo --gc --minify --baseURL "https://www.linuxer.name/"
```

### Content Management
```bash
# Create new post
hugo new posts/YYYY-MM-DD-title.md

# Find posts with code blocks
grep -l "^\`\`\`" content/posts/*.md

# Add language to code blocks
sed -i 's/^```$/```bash/g' content/posts/*.md
```

## Architecture

### Custom Design System

**Terminal Theme** (`assets/css/extended/terminal-theme.css`):
- **Dark Mode**: Matrix-inspired with rainbow gradient prompt
- **Light Mode**: Clean terminal aesthetic
- **Critical**: Uses `[data-theme="dark"]` and `[data-theme="light"]` selectors (NOT `.dark` class)
- **Fonts**: IBM Plex Mono (code/headings), IBM Plex Sans KR (body)

**Key CSS Features:**
- Rainbow gradient logo prompt: `linuxer# cd /blog ▊`
- Terminal window decorations: `● ● ●` on post cards and code blocks
- Clickability fix: `pointer-events: none` on pseudo-elements, `z-index: 10` on `.entry-link`
- Code blocks hidden in previews: `.entry-content code { display: none !important; }`

### Theme Customization

**Override PaperMod defaults:**
- `assets/css/extended/terminal-theme.css`: Main styling
- `layouts/partials/post_meta.html`: Add categories/tags to listings
- **DO NOT** create `assets/css/core/theme-vars.css` (causes conflicts)

**CSS Selector Priority:**
```
[data-theme="dark"] > .dark  ← Use data-theme attribute
:root[data-theme="dark"]     ← For CSS variables
```

### Deployment Pipeline

**GitHub Actions** (`.github/workflows/hugo.yml`):
1. Build with Hugo v0.146.0
2. Deploy to S3: `s3://linuxer-blog`
3. Invalidate CloudFront: `E2F55V6TWIFX8B`

**CloudFront Setup:**
- Function required for `/posts/slug/` → `/posts/slug/index.html` rewrite
- See `CLOUDFRONT_SETUP.md` and `cloudfront-function-index.js`

## Content Guidelines

### Code Blocks

**MUST specify language:**
```markdown
✅ ```bash
❌ ```
```

**Common issues:**
- Line numbers disabled (`lineNos = false` in hugo.toml) to prevent preview contamination
- Previews hide code blocks to avoid clutter

### Front Matter
```yaml
---
title: "Post Title"
date: 2025-11-20T15:00:00+09:00
draft: false
categories: ["AWS", "Kubernetes"]
tags: ["eks", "karpenter"]
slug: "post-slug"
---
```

### Images
- Path: `/images/YYYY/MM/filename.jpg`
- Stored in: `static/images/YYYY/MM/`
- WordPress images migrated: 689 files, unused removed

## Common Issues

### CSS Not Applying
1. Check selector: Use `[data-theme="dark"]` NOT `.dark`
2. Clean rebuild: `rm -rf public resources && hugo --minify`
3. Clear browser cache or use incognito
4. CloudFront cache: Wait 5-10min or invalidate manually

### Post Cards Not Clickable
- Ensure `pointer-events: none` on `::before` and `::after`
- Ensure `.entry-link` has `z-index: 10 !important`

### Code Blocks Broken
- Check language specifier present
- Verify closing backticks match
- Line numbers disabled to prevent summary pollution

## Design Philosophy

**Matrix Terminal Aesthetic:**
- Retro terminal meets modern brutalism
- Colors: Rainbow gradient prompt, matrix green accents, cyan/purple/orange highlights
- Typography: IBM Plex (technical heritage)
- Effects: Scan line animation, noise texture, neon glows

**Both themes supported:**
- Dark: Matrix green (#00ff41), deep black backgrounds
- Light: Clean white, blue accents, subtle terminal windows
- Consistent: Same fonts, same terminal decorations (● ● ●)

## Site Configuration

- **Domain**: www.linuxer.name
- **Base URL**: https://www.linuxer.name/
- **Default Theme**: Dark
- **Language**: Korean (ko-kr)
- **Syntax Highlighting**: Dracula
