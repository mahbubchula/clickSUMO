# ClickSUMO Deployment Guide

Complete guide for deploying ClickSUMO to GitHub and Streamlit Cloud.

**Author:** Mahbub Hassan
**Date:** January 18, 2026

---

## 🔐 IMPORTANT: Your API Key

⚠️ **Your API key is stored in `.env` file locally** ⚠️

**For Streamlit Cloud deployment:**
- You'll add your API key in Streamlit Cloud settings
- Never commit API keys to GitHub
- Use `.env` file locally (already in `.gitignore`)

---

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository

```bash
cd "D:\03_Education_&_Courses\Daily_AI_Tool\sumo-forge"

# Initialize git (if not already done)
git init

# Set your identity
git config user.name "Mahbub Hassan"
git config user.email "your-email@example.com"
```

### Step 2: Create Repository on GitHub

1. Go to https://github.com
2. Click "+" → "New repository"
3. Repository name: `clicksumo` or `sumo-forge`
4. Description: "ClickSUMO - AI-Powered Traffic Simulation Tool"
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

### Step 3: Add Files and Commit

```bash
# Check what will be committed (verify .env is NOT listed)
git status

# Add all files
git add .

# Verify .env is ignored
git status
# You should NOT see .env in the list!

# Create first commit
git commit -m "Initial commit: ClickSUMO v8.0 (NEBULA AI)

Features:
- Network Studio with templates
- Traffic demand generator
- Signal designer with Webster's optimization
- Output analyzer with visualizations
- RAG-powered AI assistant (497 SUMO docs indexed)
- Documentation browser
- Project manager (save/load)

Author: Mahbub Hassan
Institution: Chulalongkorn University"
```

### Step 4: Push to GitHub

```bash
# Add GitHub as remote (replace YOUR-USERNAME and REPO-NAME)
git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### ✅ Verification

After pushing, check GitHub to ensure:
- ✅ All files are there
- ✅ `.env` is NOT visible (secrets safe!)
- ✅ `.env.example` IS visible (template for others)
- ✅ README.md displays nicely

---

## Part 2: Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud

1. Visit https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"

### Step 2: Configure Deployment

**Main settings:**
- **Repository:** YOUR-USERNAME/REPO-NAME
- **Branch:** main
- **Main file path:** `app.py`
- **App URL:** (choose a custom URL like `clicksumo`)

### Step 3: Configure Secrets ⭐ CRITICAL

Click "Advanced settings" → "Secrets"

**Copy and paste this EXACTLY:**

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Important:**
- Format is: `VARIABLE_NAME = "value"`
- Use TOML format (not .env format)
- Keep the quotes around the API key
- No spaces around `=` except what's shown

### Step 4: Deploy!

1. Click "Deploy"
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors

### Step 5: Test Your Deployed App

Once deployed, test these features:
- ✅ Home page loads
- ✅ Network Studio works
- ✅ AI Assistant has API key (check for "✅ Documentation database loaded")
- ✅ Documentation Browser works
- ✅ Project Manager can save/load

---

## 🔧 Troubleshooting

### Problem: "streamlit.errors.StreamlitSecretNotFoundError"

**Solution:** Verify secrets configuration:
1. Go to Streamlit Cloud dashboard
2. Click on your app → Settings
3. Click "Secrets"
4. Verify this exact format:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
5. Click "Save"
6. App will auto-restart

### Problem: RAG System "Documentation database not found"

**Expected on first deployment!** The vector database is not in git (too large).

**Two options:**

**Option A: Build on first run (users wait 1-2 minutes)**
- App will show instructions to run `python build_vector_db.py`
- This is normal for first-time setup

**Option B: Pre-build and commit (faster for users)**
```bash
# On your local machine
cd "D:\03_Education_&_Courses\Daily_AI_Tool\sumo-forge"

# Remove vector_db from .gitignore temporarily
# (Edit .gitignore, comment out the vector_db line)

# Add and commit vector database
git add vector_db/
git commit -m "Add pre-built vector database for faster deployment"
git push

# Deploy will now include the database
```

**Recommendation:** Use Option A initially, switch to Option B if needed.

### Problem: App is slow on first load

**Normal!** Streamlit Cloud cold starts take 30-60 seconds.

**Solutions:**
- Keep app active by visiting regularly
- Upgrade to Streamlit Cloud paid tier (faster instances)

### Problem: "This app has exceeded its resource limits"

**Causes:**
- Too many users simultaneously
- Large vector database operations
- Heavy computations

**Solutions:**
1. Optimize code for memory usage
2. Add caching with `@st.cache_data` and `@st.cache_resource`
3. Upgrade Streamlit Cloud tier
4. Deploy to your own server

---

## 📊 Resource Limits (Streamlit Cloud Free Tier)

| Resource | Limit |
|----------|-------|
| Memory | 1 GB |
| CPU | Shared |
| Storage | Unlimited (but affects performance) |
| Bandwidth | Fair use |
| Apps | 1 public app |

**ClickSUMO Requirements:**
- Memory: ~500-800 MB (with vector DB loaded)
- Storage: ~100 MB
- **Status:** Should work on free tier ✅

---

## 🔄 Updating Your Deployed App

When you make changes:

```bash
# Make your changes locally
# Test thoroughly

# Commit changes
git add .
git commit -m "Description of changes"
git push

# Streamlit Cloud auto-deploys!
# Changes live in 2-3 minutes
```

---

## 🌐 Share Your App

After deployment, you'll get a URL like:
```
https://clicksumo.streamlit.app
```

**Share it:**
- 📧 Email colleagues
- 🎓 Include in research papers
- 💼 Add to CV/portfolio
- 🐦 Share on social media
- 📚 Link from documentation

**Example sharing text:**
```
Check out ClickSUMO - AI-Powered Traffic Simulation Tool!

🚀 One-click SUMO simulations
🤖 AI assistant with 497 docs indexed
📊 Beautiful visualizations
💾 Save/load projects

Try it: https://clicksumo.streamlit.app

Created by Mahbub Hassan at Chulalongkorn University
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use Streamlit secrets for API keys
- Keep `.env` in `.gitignore`
- Provide `.env.example` template
- Use environment variables for all secrets
- Regularly rotate API keys

### ❌ DON'T:
- Never commit `.env` file
- Never hardcode API keys in code
- Never share secrets in public repos
- Never commit database credentials
- Never expose API keys in frontend

---

## 📈 Monitoring Your App

### Streamlit Cloud Dashboard

Monitor:
- **Viewer count:** How many users
- **Logs:** Error messages, warnings
- **Resource usage:** Memory, CPU
- **Uptime:** Availability

### Analytics

Consider adding:
- Google Analytics
- Custom usage tracking
- Error monitoring (Sentry)
- User feedback forms

---

## 🎯 Post-Deployment Checklist

After deployment, verify:

- [ ] App loads successfully
- [ ] All pages accessible
- [ ] AI Assistant works (API key configured)
- [ ] Documentation Browser works
- [ ] Project Manager save/load works
- [ ] Visualizations render correctly
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Share URL works

---

## 🚀 Next Steps After Deployment

1. **Share with users**
   - Collect feedback
   - Track usage
   - Iterate

2. **Monitor performance**
   - Watch logs
   - Fix errors
   - Optimize

3. **Enhance features**
   - Based on user requests
   - Add analytics
   - Improve UX

4. **Build community**
   - GitHub stars
   - User testimonials
   - Research citations

---

## 📞 Support

**Issues during deployment?**
- Check Streamlit Cloud logs
- Review this guide
- Check Streamlit documentation: https://docs.streamlit.io

**App-specific issues?**
- Check app logs in Streamlit Cloud
- Test locally first
- Verify secrets configuration

---

## 🎓 Additional Resources

**Streamlit Deployment:**
- https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- https://docs.streamlit.io/streamlit-community-cloud/manage-your-app/app-settings

**GitHub:**
- https://docs.github.com/en/get-started

**Environment Variables:**
- https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

---

**Good luck with your deployment! 🚀**

*Questions? Issues? Feel free to open an issue on GitHub!*

---

**© 2026 Mahbub Hassan | Chulalongkorn University**
