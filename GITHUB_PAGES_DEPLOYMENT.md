# GitHub Pages Deployment Guide

## Prerequisites
- A GitHub account
- Git installed on your local machine
- The website files in `results/website/` directory

## Step-by-Step Deployment

### Option 1: Deploy from `results/website` directory (Recommended)

1. **Initialize Git repository** (if not already initialized):
   ```bash
   cd results/website
   git init
   ```

2. **Create a `.gitignore` file** (optional but recommended):
   ```bash
   cat > .gitignore << 'EOF'
   # Python
   __pycache__/
   *.pyc
   .python-version
   
   # OS
   .DS_Store
   Thumbs.db
   EOF
   ```

3. **Add all files to Git**:
   ```bash
   git add .
   git commit -m "Initial commit: Alzheimer's Disease Clinical Trials Explorer"
   ```

4. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `ad-clinical-trials-explorer`)
   - **Do NOT** initialize with README, .gitignore, or license
   - Copy the repository URL (e.g., `https://github.com/yourusername/ad-clinical-trials-explorer.git`)

5. **Add GitHub remote and push**:
   ```bash
   git remote add origin https://github.com/yourusername/ad-clinical-trials-explorer.git
   git branch -M main
   git push -u origin main
   ```

6. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** tab
   - Scroll down to **Pages** section (left sidebar)
   - Under **Source**, select:
     - Branch: `main`
     - Folder: `/ (root)`
   - Click **Save**

7. **Access your website**:
   - Your site will be available at: `https://yourusername.github.io/ad-clinical-trials-explorer/`
   - It may take a few minutes for the first deployment

### Option 2: Deploy from root directory with subdirectory

If you want to keep the website as part of a larger repository:

1. **Create a `gh-pages` branch**:
   ```bash
   cd /Users/zocean/Work/AD_project/Clinical_AI
   git checkout -b gh-pages
   ```

2. **Copy website files to root** (or keep in subdirectory):
   ```bash
   # Option A: Copy to root
   cp -r results/website/* .
   
   # Option B: Keep in subdirectory (update paths in index.html)
   # No copying needed, but update all paths in index.html
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Deploy website to GitHub Pages"
   git push origin gh-pages
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Select `gh-pages` branch
   - Select folder (root or subdirectory)
   - Save

## Updating the Website

### When you update trial data:

1. **Regenerate trials_data.js**:
   ```bash
   cd results/website
   python3 build_data.py
   ```

2. **Commit and push changes**:
   ```bash
   git add trials_data.js
   git commit -m "Update trial data"
   git push origin main  # or gh-pages
   ```

3. **GitHub Pages will automatically rebuild** (usually within 1-2 minutes)

## Important Notes

### File Size Considerations
- `trials_data.js` is 11MB - GitHub Pages can handle this, but consider:
  - Using GitHub LFS for very large files
  - Or splitting data into multiple files
  - Or using a CDN for large assets

### Path References
- All paths in `index.html` are relative (e.g., `data/networks.js`)
- Make sure all file references work correctly
- Test locally before deploying

### Custom Domain (Optional)
- In repository Settings → Pages
- Add your custom domain
- Update DNS records as instructed

## Troubleshooting

### Site not loading?
- Check repository Settings → Pages for errors
- Verify branch and folder settings
- Check Actions tab for build errors

### Files not updating?
- Clear browser cache
- Wait 1-2 minutes for GitHub Pages to rebuild
- Check file paths are correct

### Large file issues?
- Consider using Git LFS for files > 100MB
- Or optimize/compress large files

## Quick Deploy Script

Save this as `deploy.sh` in `results/website/`:

```bash
#!/bin/bash
# Quick deployment script for GitHub Pages

echo "Building trial data..."
python3 build_data.py

echo "Adding files to git..."
git add .

echo "Committing changes..."
git commit -m "Update website: $(date +%Y-%m-%d)"

echo "Pushing to GitHub..."
git push origin main

echo "Deployment complete! Check GitHub Pages in 1-2 minutes."
```

Make it executable:
```bash
chmod +x deploy.sh
```

Then run:
```bash
./deploy.sh
```


