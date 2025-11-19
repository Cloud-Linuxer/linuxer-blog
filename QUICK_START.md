# Quick Start Guide

## For GitHub Deployment

```bash
# 1. Navigate to repository
cd /home/linuxer-hugo

# 2. Rename branch to main
git branch -M main

# 3. Add GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/linuxer-hugo.git

# 4. Push to GitHub
git push -u origin main
```

## Then on GitHub

1. Go to repository Settings → Pages
2. Set Source to: **GitHub Actions**
3. Wait 2-3 minutes for deployment
4. Visit: `https://USERNAME.github.io/linuxer-hugo/`

## For Custom Domain (linuxer.name)

### DNS Records (at your domain registrar):
```
Type: A, Name: @, Value: 185.199.108.153
Type: A, Name: @, Value: 185.199.109.153
Type: A, Name: @, Value: 185.199.110.153
Type: A, Name: @, Value: 185.199.111.153
Type: CNAME, Name: www, Value: USERNAME.github.io
```

### In hugo.toml:
```toml
baseURL = 'https://linuxer.name/'
```

### In GitHub:
- Settings → Pages → Custom domain: `linuxer.name`

## Local Development

```bash
# Start dev server
hugo server -D

# Build for production
hugo --minify

# Check for errors
hugo --buildDrafts --buildFuture
```

## Adding New Posts

1. Create file: `content/posts/YYYY-MM-DD-title.md`
2. Add front matter:
   ```yaml
   ---
   title: "Post Title"
   date: 2025-11-19T12:00:00+09:00
   draft: false
   categories: ["Category"]
   tags: ["tag1", "tag2"]
   ---
   ```
3. Commit and push: `git add . && git commit -m "New post" && git push`

## Troubleshooting

**Build fails?**
- Check GitHub Actions logs
- Verify Hugo version matches (v0.146.0)

**Custom domain not working?**
- Wait 24-48 hours for DNS propagation
- Check DNS with: `dig linuxer.name`

**Need help?**
- See DEPLOYMENT_INSTRUCTIONS.md for details
- Check MIGRATION_REPORT.md for technical info

---

**Current Status**: Ready for deployment
**Posts**: 198 (100% migrated)
**Build Time**: ~626ms
**Repository**: /home/linuxer-hugo/
