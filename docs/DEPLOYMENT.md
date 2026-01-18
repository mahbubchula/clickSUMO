# Deployment Guide for ClickSUMO

This guide covers deploying ClickSUMO to Streamlit Community Cloud and other platforms.

## 🚀 Deploy to Streamlit Community Cloud

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

#### 1. Push to GitHub
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: ClickSUMO ready for deployment"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/clicksumo.git

# Push to GitHub
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `YOUR_USERNAME/clicksumo`
4. Set main file path: `app.py`
5. Click "Deploy"

Your app will be live at: `https://YOUR_USERNAME-clicksumo.streamlit.app`

#### 3. Configure Secrets (Optional)

For AI Assistant features with Groq API:

1. In Streamlit Cloud dashboard, go to your app
2. Click "⚙️ Settings" → "Secrets"
3. Add your secrets:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

---

## 🐳 Deploy with Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
# Build image
docker build -t clicksumo .

# Run container
docker run -p 8501:8501 clicksumo
```

---

## ☁️ Deploy to Other Platforms

### Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Railway

1. Connect your GitHub repository
2. Railway auto-detects Streamlit
3. Set start command: `streamlit run app.py`

### Google Cloud Run

```bash
gcloud run deploy clicksumo \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔧 Post-Deployment Checklist

- [ ] Test all features in production
- [ ] Verify file generation works
- [ ] Check download functionality
- [ ] Test on mobile devices
- [ ] Monitor resource usage
- [ ] Set up error tracking (optional: Sentry)
- [ ] Add Google Analytics (optional)

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Module not found" error
**Solution**: Verify `requirements.txt` has all dependencies and versions are compatible

**Issue**: File upload fails
**Solution**: Check `maxUploadSize` in `.streamlit/config.toml`

**Issue**: App crashes on startup
**Solution**: Check logs in Streamlit Cloud dashboard or use `streamlit run app.py --logger.level=debug`

**Issue**: Slow performance
**Solution**: Optimize session state usage and add caching with `@st.cache_data`

---

## 📊 Performance Tips

1. **Use caching**: Add `@st.cache_data` to expensive functions
2. **Minimize reruns**: Use `st.session_state` efficiently
3. **Lazy loading**: Load large templates only when needed
4. **Compress outputs**: Use ZIP for multiple files

---

## 🔒 Security Best Practices

1. Never commit `.env` file with API keys
2. Use Streamlit secrets for sensitive data
3. Validate all user inputs
4. Sanitize file names before saving
5. Set appropriate file size limits

---

## 📈 Monitoring

Monitor your app with:
- Streamlit Cloud analytics (built-in)
- Google Analytics (add tracking code)
- Sentry for error tracking
- UptimeRobot for availability monitoring

---

## 🆘 Support

- **Issues**: Report on [GitHub Issues](https://github.com/YOUR_USERNAME/clicksumo/issues)
- **Email**: 6870376421@student.chula.ac.th
- **Docs**: See [README.md](README.md)

---

**Happy Deploying! 🚀**
