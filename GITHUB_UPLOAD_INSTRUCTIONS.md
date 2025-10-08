# 📤 Instructions for Uploading to GitHub

## ✅ Pre-upload Checklist

Before uploading to GitHub, verify the following:

### 1. Protected Files (Will NOT be uploaded)

✅ **Data files are protected:**
- `panel/data/GIFT_database_prepared.csv` - EXCLUDED
- All `*.csv`, `*.xlsx`, `*.xls` files - EXCLUDED

✅ **Large images are protected:**
- `panel/app/assets/img/*.jpg` - EXCLUDED (except logo.png)
- `panel/app/assets/img/*.jpeg` - EXCLUDED
- `panel/app/assets/img/*.png` - EXCLUDED (except logo.png)

✅ **Environment files are protected:**
- `venv/` directories - EXCLUDED
- `.env` files - EXCLUDED
- `.streamlit/secrets.toml` - EXCLUDED

### 2. Files That WILL Be Uploaded

✅ **Code files:**
- All Python files (`.py`)
- `requirements.txt`
- Configuration files

✅ **Documentation:**
- `README.md` (main)
- `panel/data/README.md` (instructions for data file)
- `panel/app/assets/img/README.md` (instructions for images)

✅ **Essential files:**
- `.gitignore`
- `logo.png` (only this image)

## 🚀 Upload Steps

### Step 1: Verify What Will Be Committed

```bash
cd "/Users/susanaflecha/Library/CloudStorage/Dropbox/Mac (2)/Documents/GitHub/GIFT_EDA"
git status
```

**Expected output:** Should NOT show:
- `panel/data/GIFT_database_prepared.csv`
- Image files (except logo.png)
- venv directories

### Step 2: Add All Changes

```bash
git add .
```

### Step 3: Verify Again (Important!)

```bash
git status
```

Check that sensitive files are NOT in "Changes to be committed"

### Step 4: Double-Check Ignored Files

```bash
# Check that data file is ignored
git check-ignore -v panel/data/GIFT_database_prepared.csv

# Check that images are ignored
git check-ignore -v panel/app/assets/img/panel.jpg
git check-ignore -v panel/app/assets/img/Emma.jpeg
```

**Expected:** Each command should show the file is ignored

### Step 5: Create Commit

```bash
git commit -m "Update GIFT Oceanographic Intelligence Platform

- Updated water mass classification criteria
- Enhanced dashboard visualizations
- Added professional README
- Improved data security (excluded sensitive files)
- Added documentation for data and image requirements

🤖 Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 6: Push to GitHub

```bash
git push origin main
```

## 🔒 Security Verification

After pushing, verify on GitHub that:

1. ❌ Data file `GIFT_database_prepared.csv` is NOT visible
2. ❌ Large image files are NOT visible (only logo.png should be there)
3. ✅ Code files ARE visible
4. ✅ README files ARE visible in data/ and img/ directories

## 📝 Post-Upload Tasks

### 1. Update README with Streamlit URL

Once you deploy to Streamlit Cloud:

1. Get your Streamlit app URL (e.g., `https://your-app.streamlit.app`)
2. Update `README.md` replacing all instances of `YOUR_STREAMLIT_APP_URL_HERE`
3. Commit and push the update:

```bash
git add README.md
git commit -m "Add Streamlit app URL"
git push origin main
```

### 2. Set Up Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Set main file path: `panel/app/main.py`
4. **Important:** Upload `GIFT_database_prepared.csv` to Streamlit Cloud secrets or use Streamlit file storage
5. Deploy!

### 3. Configure Streamlit Secrets (if needed)

If using Streamlit secrets for data:

1. In Streamlit Cloud dashboard → Settings → Secrets
2. Add data path or other sensitive configurations
3. Update code to read from secrets

## 🆘 Troubleshooting

### Problem: Data file appears in git status

**Solution:**
```bash
git rm --cached panel/data/GIFT_database_prepared.csv
git commit -m "Remove data file from tracking"
```

### Problem: Images appear in git status

**Solution:**
```bash
git rm --cached panel/app/assets/img/*.jpg
git rm --cached panel/app/assets/img/*.jpeg
git rm --cached panel/app/assets/img/*.png
git add panel/app/assets/img/logo.png
git commit -m "Remove large images from tracking"
```

### Problem: Need to check what's ignored

**Solution:**
```bash
git ls-files --ignored --exclude-standard
```

## 📧 Support

If you encounter issues:
- Review `.gitignore` file
- Check GitHub repository to verify no sensitive files are visible
- Contact: susana.flecha@csic.es

---

**Last Updated:** October 2025
**Status:** Ready for GitHub upload
