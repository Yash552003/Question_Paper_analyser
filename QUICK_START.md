# Quick Start - Online Setup (30 Minutes)

## 1. BACKEND - Make it Online

### Step 1: Update Backend Code
✅ **DONE** - We've already updated:
- `backend/main.py` - Now uses environment variables
- `backend/.env` - Has all configuration
- `Dockerfile` - Ready for cloud deployment
- `requirements.txt` - All dependencies listed

### Step 2: Test Backend Locally
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Make sure .env has your Google API key:
# GOOGLE_API_KEY=AIzaSyBLshUPjEHU-QOX9VcpurOZAszQ100I15E

# Run backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
Uvicorn running on http://0.0.0.0:8000
```

**Test it works:**
```bash
# In another terminal
curl http://localhost:8000/
# Should return: {"status":"Bramha Universal Server Online","version":"2.0-Flash"}
```

---

## 2. FRONTEND - Connect to Backend

### Step 1: Update Frontend Libraries
✅ **DONE** - Already updated `pubspec.yaml` to include:
- `connectivity_plus` - Check internet connection
- Better error handling in `main.dart`
- New `config/app_config.dart` for URL management

### Step 2: Get Flutter Dependencies
```bash
cd frontend
flutter pub get
flutter pub upgrade
```

### Step 3: Test on Local Machine

#### For Desktop Testing:
```bash
flutter run -d windows  # or macos / linux
```

#### For Android Emulator:
```bash
flutter run -d emulator-5554
```

#### For iOS Simulator:
```bash
flutter run -d ios
```

#### For Web:
```bash
flutter run -d chrome
```

---

## 3. DEPLOY BACKEND (Pick One - Takes 5 Minutes)

### FREE Option 1: Google Cloud Run (Recommended)

**Why:** Most free requests (2M/month), auto-scaling, simple setup

```bash
# 1. Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Deploy (from backend folder)
cd backend
gcloud run deploy bramha-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="AIzaSyBLshUPjEHU-QOX9VcpurOZAszQ100I15E"
```

**You'll get:** `https://bramha-api-xxxxx.run.app`

### FREE Option 2: Render.com

**Why:** Even simpler, just connect GitHub

1. Push backend to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect GitHub repo
4. Set environment variables
5. Deploy!

### FREE Option 3: Railway.app

Similar to Render, with free credits.

---

## 4. UPDATE FRONTEND FOR ONLINE

### Step 1: Update Backend URL
Edit `frontend/lib/config/app_config.dart`:

```dart
// Change this:
static const String _devBackendUrl = 'http://192.168.56.1:8000';

// To this (your deployed URL):
static const String _prodBackendUrl = 'https://bramha-api-xxxxx.run.app';

// And change the getter to use production:
static String get backendUrl {
  return _prodBackendUrl;  // Changed from _devBackendUrl
}
```

### Step 2: Rebuild for All Platforms

```bash
cd frontend
flutter clean
flutter pub get

# Android
flutter build apk --split-per-abi

# iOS
flutter build ios

# Web
flutter build web
```

---

## 5. PLATFORM-SPECIFIC FIXES (Optional but Recommended)

### Android
Edit `android/app/src/main/AndroidManifest.xml` - Add these inside `<manifest>`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### iOS
Edit `ios/Runner/Info.plist` - Add these inside root `<dict>`:
```xml
<key>NSBonjourServices</key>
<array>
  <string>_http._tcp</string>
  <string>_https._tcp</string>
</array>
```

### Web
Already works! No extra configuration needed.

---

## 6. TESTING CHECKLIST

- [ ] Backend running locally and responding
- [ ] Google API key is working (test with a PDF)
- [ ] Firebase deploy successful (if using)
- [ ] Flutter app points to correct backend URL
- [ ] Tested on Android with internet
- [ ] Tested on iOS with internet
- [ ] Tested on Web
- [ ] Can upload PDFs and get analysis

---

## 7. QUICK TROUBLESHOOTING

### "Connection refused"
```
✓ Check backend is running
✓ Check URL in app_config.dart matches deployed URL
✓ Check internet is working
```

### "CORS error"
```
✓ Update ALLOWED_ORIGINS in backend .env
✓ Restart backend
```

### "No internet detected"
```
✓ App has connectivity_plus checking before upload
✓ Check WiFi/Mobile data is on
```

### "Timeout after 3 minutes"
```
✓ File might be too large
✓ Backend might be slow (cold start)
✓ Network might be unstable
```

---

## 8. WHAT'S CHANGED

| Component | Old | New |
|-----------|-----|-----|
| Backend URL | Hardcoded `192.168.56.1` | Dynamic via `app_config.dart` |
| API Key | Hardcoded in code | Environment variable |
| CORS | Allow all `["*"]` | Restricted origins |
| Error Handling | Basic catch | Detailed network errors |
| Connectivity Check | None | Added before upload |
| File Validation | None | Size checking |
| Request Timeout | None | 3 minute timeout |

---

## Next Steps

1. **Test locally first** - Backend + Frontend on same machine
2. **Deploy backend** - Pick Google Cloud Run or Render
3. **Update frontend URL** - Point to deployed backend
4. **Build for all platforms** - APK, iOS, Web
5. **Install on devices** - Test on real phones

**Total Time: 30-45 minutes**
