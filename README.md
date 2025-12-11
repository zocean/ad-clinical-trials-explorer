# Alzheimer's Disease Clinical Trials Explorer

A web-based explorer for Alzheimer's Disease clinical trials with interactive network visualization.

## Features

- 📊 **Clinical Trials Database**: Browse and search through clinical trials
- 💊 **Drug Analysis**: View top 25 drugs and their associations
- 🧬 **Gene Targets**: Explore target genes in clinical trials
- 🕸️ **Network Visualization**: Interactive drug-cell type network
- 🔍 **Advanced Filtering**: Search and filter trials dynamically

## Quick Start

### Local Development

1. **Install Python 3** (if not already installed)

2. **Generate trial data**:
   ```bash
   python3 build_data.py
   ```

3. **Open in browser**:
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     # Python 3
     python3 -m http.server 8000
     
     # Then visit: http://localhost:8000
     ```

## Deployment

See [GITHUB_PAGES_DEPLOYMENT.md](./GITHUB_PAGES_DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to GitHub Pages

```bash
# Initialize git repository
cd results/website
git init
git add .
git commit -m "Initial commit"

# Add your GitHub repository
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main

# Then enable GitHub Pages in repository settings
```

## File Structure

```
results/website/
├── index.html              # Main website file
├── trials_data.js          # Generated trial data (run build_data.py)
├── build_data.py           # Data aggregation script
├── data/
│   ├── networks.js         # Network visualization data
│   ├── network_styles.js   # Network styles
│   └── *.json             # Individual trial data files
├── README.md              # This file
├── GITHUB_PAGES_DEPLOYMENT.md  # Deployment guide
└── PRODUCTION_CHECKLIST.md     # Production checklist
```

## Updating Data

When you have new trial data:

1. Update JSON files in `data/` directory
2. Run `python3 build_data.py` to regenerate `trials_data.js`
3. Commit and push changes

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

[Add your license here]

## Contact

[Add contact information here]

