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

### **CRITICAL: Pre-Push Testing Rule**

**NEVER push to main without passing local tests:**

```bash
# 1. Clean rebuild
pkill hugo && rm -rf public resources
hugo --minify

# 2. Start local server
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender > /tmp/hugo.log 2>&1 &
sleep 4

# 3. Verify build success
curl -s http://localhost:1313/ | head -50

# 4. Take screenshots for verification
chromium-browser --headless --disable-gpu --no-sandbox \
  --screenshot=/tmp/test_dark.png --window-size=1920,1080 \
  "http://localhost:1313/"

# 5. Manual verification checklist:
# - Does the design look correct in screenshot?
# - Are all visual elements (prompt, colors, fonts) working?
# - Can you see post cards with ● ● ● decorations?
# - Is rainbow gradient visible on prompt?

# 6. Only if ALL tests pass:
git add -A && git commit -m "..." && git push origin main
```

**If ANY test fails, fix issues before pushing.**

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

### Post Cards Not Clickable (CRITICAL ISSUE)

**Root Cause**: Complex CSS stacking and pointer-events inheritance issues

**Symptoms**:
- Click animation works (`.post-entry:active` scales to 0.96)
- But navigation doesn't trigger (`.entry-link` not receiving clicks)

**Complete Fix Required**:
```css
/* 1. Disable ALL clicks on post-entry children */
[data-theme="dark"] .post-entry * {
    pointer-events: none !important;
}

/* 2. Re-enable ONLY on entry-link */
[data-theme="dark"] .entry-link {
    pointer-events: auto !important;
    z-index: 10 !important;
}
```

**Why This Happens**:
- `.post-entry` has multiple children: header, content, footer, and entry-link
- `.entry-link` is absolute positioned but still a child element
- Without explicit `pointer-events: auto` on `.entry-link`, it inherits `none`
- The `*` selector ensures ALL children are disabled, then we selectively re-enable

**Testing**:
1. Check if `.post-entry:active` animation triggers (scale effect)
2. Check if clicking navigates to the post
3. Both should work - if not, CSS specificity issue exists

**Common Mistakes to Avoid**:
- ❌ Setting `pointer-events: none` only on specific children (header, content, footer)
- ❌ Not setting `pointer-events: auto` explicitly on `.entry-link`
- ❌ Assuming z-index alone will fix click issues
- ❌ Setting `pointer-events: auto` on h2, p elements (blocks navigation)

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
