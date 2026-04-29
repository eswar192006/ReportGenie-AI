# Vercel Deployment Guide

## Overview

ReportGenie AI is a full-stack application with a React frontend and FastAPI backend. This guide covers deploying both to production.

## Frontend Deployment (Vercel)

The React frontend is configured to deploy automatically to Vercel.

### Prerequisites
- Vercel account (free at https://vercel.com)
- GitHub account with this repository

### Steps

1. **Connect to GitHub**
   - Go to https://vercel.com/new
   - Select "Import Project"
   - Choose your GitHub repository

2. **Configure Environment Variables**
   In the Vercel dashboard, set:
   ```
   VITE_API_URL=https://your-backend-domain.com
   ```
   (Replace with your actual backend URL)

3. **Deploy**
   - Vercel automatically deploys on git push to main branch
   - Your frontend will be live at a `.vercel.app` domain

## Backend Deployment

The FastAPI backend needs to be deployed separately. Choose one of these options:

### Option 1: Railway (Recommended)

1. **Create a Railway account** at https://railway.app

2. **Connect GitHub**
   - New Project → Deploy from GitHub
   - Select your repository

3. **Configure Railway**
   - Set Python version: `3.11` or higher
   - Add environment variables if needed
   - Railway auto-detects `requirements.txt`

4. **Deploy**
   ```bash
   git push
   ```

5. **Get your backend URL**
   - Copy the generated domain from Railway dashboard
   - Set `VITE_API_URL` in your Vercel environment variables to this URL

### Option 2: Render

1. **Create a Render account** at https://render.com

2. **Deploy**
   - New Web Service
   - Connect to GitHub
   - Set Build Command: `pip install -r requirements.txt`
   - Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

3. **Get your backend URL**
   - Copy the service URL from Render dashboard
   - Set `VITE_API_URL` in Vercel to this URL

### Option 3: Heroku

1. **Create a Heroku account** at https://heroku.com

2. **Install Heroku CLI** and authenticate

3. **Create Procfile** (if not exists)
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

5. **Get your backend URL**
   - `https://your-app-name.herokuapp.com`
   - Set `VITE_API_URL` in Vercel to this URL

## CORS Configuration

The backend is pre-configured to allow requests from:
- `http://localhost:8000`
- Your Vercel frontend domain

For production, update `app/main.py` if needed:
```python
CORS_ALLOW_ORIGINS=https://your-vercel-domain.vercel.app,https://your-custom-domain.com
```

## Testing

After deployment:

1. **Test frontend**
   - Visit your Vercel domain
   - Verify styling loads correctly

2. **Test API connectivity**
   - Upload a CSV file
   - Verify analysis completes
   - Check browser console for errors

3. **Debug**
   - Check Vercel logs: `vercel logs --follow`
   - Check backend logs (Railway/Render/Heroku dashboard)
   - Verify CORS headers are correct

## Local Development with Backend

To test locally before deploying:

```bash
# Terminal 1: Backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Then visit: `http://localhost:5173`

## Production Checklist

- [ ] Backend deployed to chosen platform
- [ ] Backend URL set as `VITE_API_URL` in Vercel
- [ ] Frontend deployed to Vercel
- [ ] CORS configured for production domains
- [ ] Error logging enabled
- [ ] File upload limits verified (2MB max)
- [ ] Test end-to-end flow with sample CSV

## Troubleshooting

### "Failed to fetch API"
- Check `VITE_API_URL` environment variable in Vercel
- Verify backend is running and accessible
- Check browser console for CORS errors

### "413 Payload Too Large"
- CSV file exceeds 2MB limit
- Reduce file size or update `MAX_UPLOAD_BYTES` in `app/routes/report.py`

### Backend timeout
- Increase timeout in backend deployment settings
- Check if Ollama service is running (if using AI features)

## Custom Domain

To use a custom domain:

1. **Vercel**
   - Settings → Domains
   - Add your domain
   - Update DNS records as shown

2. **Update CORS**
   - Set `CORS_ALLOW_ORIGINS` to include your custom domain

## Support

For issues, check:
- Vercel logs dashboard
- Backend platform logs (Railway/Render/Heroku)
- Browser developer console (F12)
