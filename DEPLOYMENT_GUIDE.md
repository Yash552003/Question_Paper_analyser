# Bramha Paper Analyzer - Deployment Guide
## Going Online: iOS, Android & Web (FREE)

---

## Quick Start - Local Development

### 1. Backend Setup (Python)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be available at:** `http://localhost:8000`

### 2. Frontend Setup (Flutter)

```bash
cd frontend

# Get dependencies
flutter pub get

# Run on your device/emulator
flutter run
```

---

## FREE Deployment Options (Choose One)

### Option A: Google Cloud Run (RECOMMENDED - Most Free Tier)

**Why:** 2 million requests/month FREE, auto-scaling, minimal configuration

#### Step 1: Create Google Cloud Account
- Go to [https://cloud.google.com/free](https://cloud.google.com/free)
- Create account (free tier, no credit card charged for free tier)
- Create new project

#### Step 2: Install Google Cloud CLI
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Then initialize:
gcloud init
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Step 3: Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### Step 4: Get Google Gemini API Key
- Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Click "Get API Key" → "Create API Key in new Google Cloud project"
- Copy the key

#### Step 5: Deploy Backend
```bash
cd backend

# Set environment variables
# Windows:
$Env:GOOGLE_API_KEY="your-api-key-here"

# macOS/Linux:
export GOOGLE_API_KEY="your-api-key-here"

# Deploy to Cloud Run
gcloud run deploy bramha-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,ALLOWED_ORIGINS="*"
```

**Output:** You'll get a URL like `https://bramha-api-xxxxx.run.app`

#### Step 6: Update Flutter Config
Edit `frontend/lib/config/app_config.dart`:

```dart
static String get backendUrl {
  // Change to your Cloud Run URL
  return 'https://bramha-api-xxxxx.run.app';
}
```

#### Step 7: Rebuild Flutter
```bash
cd frontend
flutter clean
flutter pub get
flutter build apk    # Android
flutter build ios    # iOS
flutter build web    # Web
```

**Cost:** ~$0-5/month depending on usage (most likely free with free tier)

---

### Option B: Render.com (Simple Alternative)

**Why:** Free tier, easy GitHub integration, simple deployment

#### Step 1: Create Render Account
- Go to [https://render.com](https://render.com)
- Sign up with GitHub account

#### Step 2: Push Backend to GitHub
```bash
# Initialize git in backend folder
cd backend
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git push origin main
```

#### Step 3: Deploy on Render
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Set environment variables:
   - `GOOGLE_API_KEY`: Your API key
   - `ALLOWED_ORIGINS`: Your frontend URL
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`

**Cost:** $0 (free tier, service sleeps after 15 min inactivity)

---

### Option C: Railway.app (Best Free Credits)

**Why:** Generous free credits, simple interface

#### Step 1: Create Account
- Go to [https://railway.app](https://railway.app)
- Sign up with GitHub

#### Step 2: Create New Project
1. Click "New Project" → "Deploy from GitHub repo"
2. Connect your repo
3. Add environment variables
4. Deploy

**Cost:** ~$0-10 first month with free credits

---

## Production Checklist

- [ ] Backend deployed to cloud
- [ ] `GOOGLE_API_KEY` set as environment variable
- [ ] `ALLOWED_ORIGINS` updated to your domain
- [ ] Frontend URL updated in `app_config.dart`
- [ ] Flutter dependencies updated (`flutter pub get`)
- [ ] Tested on all platforms (iOS, Android, Web)
- [ ] Platform-specific configs updated (PLATFORM_CONFIG.md)
- [ ] Rate limiting handled in backend
- [ ] Error messages display correctly

---

## Testing the Deployment

### Test Backend Health
```bash
# Should return status message
curl https://your-backend-url.app/

# If working, you'll see:
# {"status":"Bramha Universal Server Online","version":"2.0-Flash"}
```

### Test on Flutter
1. Update `app_config.dart` with your backend URL
2. Run app: `flutter run`
3. Upload a test PDF
4. Check if analysis appears

---

## Troubleshooting

### "Connection refused" error
- Check backend is running/deployed
- Verify URL in `app_config.dart` is correct
- Check internet connectivity

### "CORS error"
- Ensure frontend URL is in `ALLOWED_ORIGINS` in backend
- Check backend logs for error

### "Timeout" error
- Backend might be slow (cold start on free tier)
- Try again in 30 seconds
- Check file size (max 50MB)

### Google API Quota Error
- Free tier has limits (~15 requests/minute for Gemini)
- Implement caching or use paid tier
- See [https://makersuite.google.com/app/apikeys](https://makersuite.google.com/app/apikeys)

---

## Next Steps

1. **Enable HTTPS** - All cloud platforms provide free HTTPS
2. **Add Authentication** - Implement user login (Firebase recommended - free)
3. **Set up Monitoring** - Cloud Run provides free basic monitoring
4. **Custom Domain** - Link your own domain (~$10-15/year)

---

## Cost Summary (Monthly)

| Component | Free Tier Cost | Notes |
|-----------|---|---|
| Backend (Cloud Run) | $0-5 | 2M requests/month free |
| Google Gemini API | $0-50+ | 60 requests/min for free trial |
| Database (if added) | $0-10 | Hive (local) is free |
| Domain (if custom) | ~$1 | .com domains ~$12/year |
| **Total** | **$0-65** | **Most likely $5-10** |

---

## Quick Commands Reference

```bash
# Local Development
python -m uvicorn main:app --reload

# Deployment
gcloud run deploy bramha-api --source . --allow-unauthenticated

# Flutter Build
flutter build apk --split-per-abi    # Android
flutter build ios                     # iOS
flutter build web                     # Web

# Clean & Rebuild
flutter clean && flutter pub get
```
