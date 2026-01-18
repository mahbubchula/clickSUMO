# 🚀 Streamlit Cloud Deployment Guide

**ClickSUMO v8.0 (NEBULA AI)**

---

## ✅ Pre-Deployment Checklist

Before deploying to Streamlit Cloud, verify:

- [x] Repository is pushed to GitHub
- [x] API keys are in `.gitignore` (not in repository)
- [x] `requirements.txt` is complete
- [x] `packages.txt` is present (for system dependencies)
- [x] `.streamlit/config.toml` is configured

---

## 📦 Step 1: Push to GitHub

**Your repository is ready!** Just run this in PowerShell:

```powershell
cd "D:\03_Education_&_Courses\Daily_AI_Tool\sumo-forge"
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 1274, done.
Counting objects: 100% (1274/1274), done.
Delta compression using up to X threads
Compressing objects: 100% (1268/1268), done.
Writing objects: 100% (1274/1274), X.XX MiB | X.XX MiB/s, done.
Total 1274 (delta 123), done.
To https://github.com/mahbubchula/clickSUMO.git
 * [new branch]      main -> main
```

**Verify on GitHub:**
1. Go to: https://github.com/mahbubchula/clickSUMO
2. Check files are there
3. Search for "gsk_" - should find ZERO actual keys (only examples)

---

## ☁️ Step 2: Deploy to Streamlit Cloud

### 2.1 Login to Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Sign in with GitHub account (mahbubchula)
3. Click "New app" button

### 2.2 Configure Deployment

**Repository Settings:**
- **Repository:** `mahbubchula/clickSUMO`
- **Branch:** `main`
- **Main file path:** `app.py`

**App Settings:**
- **App URL:** Choose: `clicksumo.streamlit.app` (or your preference)
- **Python version:** 3.9 (or 3.10)

### 2.3 Advanced Settings (Important!)

Click "Advanced settings" and configure:

**Secrets:** (Click "Secrets" tab)
```toml
# Paste this in the Secrets section (use YOUR actual API key from .env file):
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

**Important:** Replace with YOUR actual API key. It's stored securely in Streamlit Cloud and never exposed publicly.

### 2.4 Deploy!

1. Click "Deploy" button
2. Wait 3-5 minutes for initial deployment
3. Watch the deployment logs
4. ✅ Your app will be live at: `https://clicksumo.streamlit.app`

---

## 🔧 Step 3: Post-Deployment Configuration

### 3.1 Build Vector Database

**Problem:** The vector database (`vector_db/`) is NOT included in the repository (too large, in `.gitignore`).

**Solution Options:**

#### Option A: Build on First Use (Recommended)
Your app will detect if `vector_db/` is missing and show instructions to users. Users can:
1. Clone your repository
2. Run `python build_vector_db.py` locally
3. Use the app locally

**For Streamlit Cloud:** RAG features won't work until you include the database.

#### Option B: Include Pre-built Database (Quick Fix)
If you want RAG to work on Streamlit Cloud:

1. **Remove from .gitignore:**
   ```bash
   # Edit .gitignore - comment out this line:
   # vector_db/
   ```

2. **Add to repository:**
   ```bash
   cd "D:\03_Education_&_Courses\Daily_AI_Tool\sumo-forge"
   git add vector_db/
   git commit -m "Add pre-built vector database for RAG"
   git push origin main
   ```

3. **Streamlit Cloud will auto-redeploy** with the database

**Size:** ~15-20 MB (acceptable for GitHub)

#### Option C: Use Hugging Face Datasets (Advanced)
Upload vector database to Hugging Face and download on app startup:
```python
# In app.py startup
if not os.path.exists('vector_db/'):
    download_from_huggingface()
```

### 3.2 SUMO Documentation

**Problem:** `sumo_docs/` folder is 79MB and excluded from repository.

**Solution:**
1. RAG won't work without it on Streamlit Cloud
2. Either:
   - Include it in repository (not recommended - too large)
   - Download on app startup from external source
   - **Best:** Use Option B above (include vector_db only)

---

## 🎛️ Step 4: Configure App Settings on Streamlit Cloud

After deployment, go to your app dashboard:

### 4.1 Resource Settings
- **Memory:** 1 GB (default) - should be sufficient
- **CPU:** Default (shared)
- **Timeout:** 10 minutes (for long simulations)

### 4.2 Update Secrets Anytime
1. Go to app dashboard
2. Click "⚙️ Settings"
3. Click "Secrets"
4. Update `GROQ_API_KEY` if needed
5. Click "Save" - app will auto-restart

### 4.3 Custom Domain (Optional)
1. Purchase a domain (e.g., clicksumo.com)
2. Go to app settings → "Custom domain"
3. Follow instructions to configure DNS

---

## 🔍 Step 5: Test Your Deployed App

### 5.1 Basic Functionality Test
1. Open your app URL
2. Navigate to "🏗️ Network Studio"
3. Try creating a simple intersection
4. Verify file generation works

### 5.2 AI Assistant Test
1. Go to "🤖 AI Assistant"
2. Ensure Groq API key is working
3. Ask a question
4. Verify response is generated

### 5.3 RAG Test (if vector_db included)
1. Enable "📚 Use Official SUMO Documentation"
2. Ask a SUMO-specific question
3. Verify sources are shown

### 5.4 Project Manager Test
1. Save a test project
2. Reload page
3. Try loading the project
4. Verify state is restored

---

## ⚠️ Important Limitations on Streamlit Cloud

### Free Tier Limitations
- **Sleep after inactivity:** App sleeps after 7 days without visits
- **Resource limits:** 1 GB RAM, shared CPU
- **Storage:** Temporary (files deleted on restart)
- **Execution time:** 10-minute timeout for long-running processes

### What Won't Work on Streamlit Cloud
1. **Running SUMO simulations:** SUMO software not installed
   - Users need to run SUMO locally
   - ClickSUMO generates files for download

2. **Persistent storage:** Saved projects lost on restart
   - Use export/import feature
   - Or integrate with cloud storage (S3, Google Drive)

3. **Large simulations:** May timeout or run out of memory

### What WILL Work
✅ Network generation
✅ Route file creation
✅ Signal optimization calculations
✅ AI assistant (with Groq API)
✅ RAG documentation search (if vector_db included)
✅ Output file analysis (upload XML files)
✅ File downloads
✅ All UI features

---

## 🔄 Step 6: Update Your App

**After pushing updates to GitHub:**

1. Streamlit Cloud auto-detects changes
2. App automatically redeploys
3. Takes 2-3 minutes
4. No manual intervention needed!

**Manual trigger:**
1. Go to app dashboard
2. Click "Reboot app" if needed

---

## 🎨 Step 7: Customize Your README

Update your GitHub README to mention the live deployment:

```markdown
## ⚡ Try It Online

**🌐 [Launch ClickSUMO on Streamlit Cloud](https://clicksumo.streamlit.app)**

Try ClickSUMO instantly - no installation required!

> Note: For running actual SUMO simulations, you'll need to install SUMO locally.
> ClickSUMO generates all necessary files which you can download and run with SUMO.
```

---

## 🐛 Troubleshooting

### App won't start
**Check:**
1. Deployment logs for errors
2. `requirements.txt` - all packages installable?
3. Python version compatibility
4. Secrets configured correctly?

**Common fixes:**
- Update package versions in `requirements.txt`
- Check for Windows-specific packages
- Verify Python 3.9+ compatibility

### API key not working
**Check:**
1. Secrets section has `GROQ_API_KEY`
2. No extra spaces or quotes
3. Key is valid (test at https://console.groq.com)

**Fix:**
1. Update secret in dashboard
2. Reboot app

### RAG not working
**Check:**
1. Is `vector_db/` in repository?
2. Are files corrupted?
3. Check deployment logs

**Fix:**
1. Include `vector_db/` in repository (see Step 3.1 Option B)
2. Or build locally and use locally

### Out of memory errors
**Solutions:**
1. Reduce batch sizes in code
2. Upgrade to paid Streamlit plan
3. Optimize memory usage
4. Use external services for heavy processing

### Files not persisting
**This is normal!** Streamlit Cloud storage is temporary.

**Solutions:**
1. Use export/import features
2. Integrate cloud storage (S3, Drive)
3. Store in database (MongoDB, PostgreSQL)

---

## 💡 Pro Tips

### 1. GitHub Actions for CI/CD
Create `.github/workflows/streamlit.yml`:
```yaml
name: Streamlit Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: streamlit run app.py --server.headless true
```

### 2. Add App Badge to README
```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://clicksumo.streamlit.app)
```

### 3. Monitor App Usage
Streamlit Cloud provides:
- Visitor analytics
- Error logs
- Performance metrics

Access from app dashboard.

### 4. Add Google Analytics (Optional)
In `.streamlit/config.toml`:
```toml
[theme]
# Your theme settings

[browser]
gatherUsageStats = true
```

Then add GA code to your app.

---

## 📊 Expected Deployment Results

### Build Time
- **First deployment:** 5-10 minutes (installing packages)
- **Subsequent deploys:** 2-3 minutes (cached dependencies)

### App Size
- **Repository:** ~20-30 MB (without sumo_docs)
- **With vector_db:** ~45-50 MB
- **With sumo_docs:** ~110 MB (not recommended for GitHub)

### Performance
- **Load time:** 2-5 seconds
- **AI response:** 2-4 seconds
- **RAG query:** 3-6 seconds
- **File generation:** <1 second

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] App is live and accessible
- [ ] No errors in deployment logs
- [ ] API key is working
- [ ] Can create networks
- [ ] Can generate files
- [ ] Can download outputs
- [ ] AI assistant responds
- [ ] RAG works (if vector_db included)
- [ ] Updated README with live link
- [ ] Shared with colleagues/community

---

## 🌟 Share Your Work!

**Promote your app:**
1. Add to SUMO community forums
2. Share on LinkedIn/Twitter
3. Submit to Streamlit gallery
4. Write a blog post
5. Create demo video

**Example posts:**
```
🚀 Just deployed ClickSUMO v8.0 - an AI-powered web platform for SUMO
traffic simulation!

✨ Features:
- One-click network creation
- AI-powered demand generation
- RAG-enhanced assistant with 497 SUMO docs
- Real-time analysis & visualization

Try it free: https://clicksumo.streamlit.app
Code: https://github.com/mahbubchula/clickSUMO

#SUMO #TrafficSimulation #AI #OpenSource
```

---

## 🎓 Next Steps After Deployment

1. **Gather user feedback**
2. **Implement new features** (see FUTURE_FEATURES_ROADMAP.md)
3. **Fix bugs** reported by users
4. **Improve performance**
5. **Add documentation/tutorials**
6. **Build community**

---

## 📞 Need Help?

**Streamlit Resources:**
- Docs: https://docs.streamlit.io/streamlit-cloud
- Community: https://discuss.streamlit.io
- Status: https://streamlit.statuspage.io

**ClickSUMO Issues:**
- GitHub Issues: https://github.com/mahbubchula/clickSUMO/issues
- Email: 6870376421@student.chula.ac.th

---

## 🎉 Congratulations!

You're deploying a production-ready AI-powered traffic simulation platform!

**ClickSUMO v8.0 (NEBULA AI)** - Making SUMO accessible to everyone!

---

**Author:** Mahbub Hassan
**Institution:** Chulalongkorn University
**Last Updated:** January 18, 2026
**Deployment Status:** Ready for Streamlit Cloud! 🚀
