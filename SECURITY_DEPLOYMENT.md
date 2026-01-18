# 🔐 Secure Deployment Guide

This guide ensures your API keys and secrets remain secure when deploying to GitHub and Streamlit Cloud.

---

## ✅ Security Checklist

### Before Pushing to GitHub

- [x] ✅ `.env` file is in `.gitignore`
- [x] ✅ `.streamlit/secrets.toml` is in `.gitignore`
- [x] ✅ No API keys in source code
- [ ] ⚠️ Run security check before first push

---

## 🔒 How Your Secrets Are Protected

### Local Development (Your Computer)

**Secrets are stored in TWO places:**

1. **`.env` file** (for environment variables)
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

2. **`.streamlit/secrets.toml`** (for Streamlit-specific secrets)
   ```toml
   GROQ_API_KEY = "your_actual_key_here"
   ```

**Both files are:**
- ✅ In `.gitignore` (won't be committed to GitHub)
- ✅ Only exist on your local machine
- ✅ Never pushed to remote repository

### GitHub Repository

**What WILL be pushed:**
- ✅ `.env.example` - Template with placeholders
- ✅ `.streamlit/secrets.toml.example` - Template with placeholders
- ✅ Source code with NO hardcoded secrets

**What will NOT be pushed:**
- ❌ `.env` - Your actual API keys (gitignored)
- ❌ `.streamlit/secrets.toml` - Your actual secrets (gitignored)

### Streamlit Cloud Deployment

**Secrets are configured via dashboard:**
1. Go to https://share.streamlit.io
2. Select your app
3. Click "⚙️ Settings" → "Secrets"
4. Paste your secrets in TOML format
5. Click "Save"

**Streamlit Cloud will:**
- ✅ Encrypt your secrets
- ✅ Inject them at runtime
- ✅ Never expose them in logs or UI

---

## 🚀 Deployment Steps

### Step 1: Prepare for GitHub

**Before your first git push, verify secrets won't leak:**

```bash
# Check what will be committed
git status

# Verify .env is NOT listed (should be ignored)
git check-ignore .env
# Should output: .env

# Verify secrets.toml is NOT listed (should be ignored)
git check-ignore .streamlit/secrets.toml
# Should output: .streamlit/secrets.toml

# See what files will be pushed (ensure no secret files)
git ls-files
```

**If `.env` or `secrets.toml` appear in `git status`:**

```bash
# Remove them from git tracking (if accidentally added)
git rm --cached .env
git rm --cached .streamlit/secrets.toml

# Ensure .gitignore is properly configured
cat .gitignore | grep -E "\.env|secrets.toml"
```

### Step 2: Push to GitHub

```bash
# Add all files (secrets are automatically excluded)
git add .

# Commit changes
git commit -m "Initial commit"

# Push to GitHub
git push origin main
```

### Step 3: Deploy to Streamlit Cloud

**A. Connect GitHub Repository**

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `clicksumo`
5. Set main file: `app.py`
6. Click "Deploy"

**B. Add Secrets**

1. Click "⚙️ Settings" on your app dashboard
2. Click "Secrets" in the sidebar
3. Paste this (with your actual key):

```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
```

4. Click "Save"
5. App will restart automatically with secrets

---

## 🛡️ Security Best Practices

### ✅ DO:

- ✅ Keep secrets in `.env` or `.streamlit/secrets.toml`
- ✅ Always check `.gitignore` includes secret files
- ✅ Use `secrets.toml.example` to show format (with placeholders)
- ✅ Add secrets via Streamlit Cloud dashboard
- ✅ Rotate API keys if accidentally exposed

### ❌ DON'T:

- ❌ Hardcode API keys in source code
- ❌ Commit `.env` or `secrets.toml` to git
- ❌ Share your `.env` or `secrets.toml` files
- ❌ Put real secrets in example files
- ❌ Screenshot or share secrets publicly

---

## 🔍 How to Verify Security

### Check Before Push

```bash
# Scan for potential secrets in tracked files
git grep -i "gsk_"  # Should return nothing

# List all tracked files
git ls-files | grep -E "\.env|secrets\.toml"
# Should return nothing (or only .example files)

# Check gitignore is working
git check-ignore .env .streamlit/secrets.toml
# Should output both files
```

### Test on GitHub

After pushing:
1. Go to your GitHub repository
2. Browse all files
3. Verify `.env` and `secrets.toml` are NOT visible
4. Only `.env.example` and `secrets.toml.example` should be there

---

## 🆘 What If I Accidentally Exposed a Secret?

**If you committed a secret to GitHub:**

1. **Revoke the API key immediately**
   - Go to https://console.groq.com
   - Delete the exposed key
   - Generate a new one

2. **Remove from git history**
   ```bash
   # WARNING: This rewrites history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (overwrites remote)
   git push origin --force --all
   ```

3. **Update your local `.env` with new key**

4. **Update Streamlit Cloud secrets** with new key

---

## 📋 Current Security Status

### ✅ Protected Files:

- `.env` - Contains: `GROQ_API_KEY`
- `.streamlit/secrets.toml` - Contains: `GROQ_API_KEY`

### ✅ Gitignore Coverage:

```
Line 42: .env
Line 43: .env.local
Line 44: .env.*.local
Line 47: .streamlit/secrets.toml
```

### ✅ Example Files (Safe to Commit):

- `.env.example` - Template with placeholders
- `.streamlit/secrets.toml.example` - Template with placeholders

---

## 🎯 Quick Reference

**Local Development:**
```bash
# Your secrets are in:
.env
.streamlit/secrets.toml

# These are gitignored and safe
```

**GitHub:**
```bash
# Only these are committed:
.env.example
.streamlit/secrets.toml.example

# Your actual secrets are NOT in the repo
```

**Streamlit Cloud:**
```
Settings → Secrets → Paste TOML format
GROQ_API_KEY = "your_key"
```

---

## ✅ Final Verification

Before deploying, run this checklist:

- [ ] `.env` exists locally with real key
- [ ] `.streamlit/secrets.toml` exists locally with real key
- [ ] Both files are in `.gitignore`
- [ ] Neither file appears in `git status`
- [ ] GitHub repo doesn't show these files
- [ ] Streamlit Cloud secrets configured
- [ ] App works with AI Assistant

---

**Your secrets are now secure!** 🔒

You can safely:
- ✅ Push to GitHub
- ✅ Deploy to Streamlit Cloud
- ✅ Share your repository publicly
- ✅ Collaborate with others

**Your API key will remain private!**
