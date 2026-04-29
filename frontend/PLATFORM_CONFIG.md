# Platform Configuration Updates

## iOS Configuration

### 1. Update `ios/Runner/Info.plist`

Add the following keys to enable network access:

```xml
<key>NSBonjourServices</key>
<array>
  <string>_http._tcp</string>
  <string>_https._tcp</string>
</array>
<key>NSLocalNetworkUsageDescription</key>
<string>Bramha needs access to your local network</string>
<key>NSBonjourServiceTypes</key>
<array>
  <string>_http._tcp</string>
  <string>_https._tcp</string>
</array>
```

### 2. Enable HTTP Connections (if still using HTTP for development)

For Google Cloud Run, HTTPS is enabled by default, but for local development:

```xml
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <false/>
  <key>NSExceptionDomains</key>
  <dict>
    <key>localhost</key>
    <dict>
      <key>NSIncludesSubdomains</key>
      <true/>
      <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
      <true/>
    </dict>
    <key>192.168.56.1</key>
    <dict>
      <key>NSIncludesSubdomains</key>
      <true/>
      <key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
      <true/>
    </dict>
  </dict>
</dict>
```

---

## Android Configuration

### 1. Update `android/app/src/main/AndroidManifest.xml`

Add internet permissions:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

### 2. Create Network Security Config

Create `android/app/src/main/res/xml/network_security_config.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- For development with local backend -->
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.56.1</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
    </domain-config>
    
    <!-- Production - HTTPS only -->
    <domain-config>
        <domain includeSubdomains="true">bramha-api.onrender.com</domain>
    </domain-config>
</network-security-config>
```

### 3. Update AndroidManifest.xml to use network security config:

```xml
<application
    ...
    android:networkSecurityConfig="@xml/network_security_config"
    ...
>
```

---

## Web Configuration

### 1. Update `web/index.html`

Ensure CORS headers are properly handled by adding meta tags:

```html
<meta http-equiv="Permissions-Policy" content="geolocation=(), microphone=(), camera=()">
```

### 2. Backend CORS settings

Make sure your backend allows your web domain:

```python
# In backend main.py
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
# Example: "http://localhost:3000,https://yourdomain.com"
```

---

## Running on Different Platforms

### Development (Local Backend)

**Android Emulator:**
```bash
flutter run -d emulator-5554 --dart-define=BACKEND_URL=http://10.0.2.2:8000
```

**Physical Android Device (same WiFi):**
```bash
flutter run --dart-define=BACKEND_URL=http://192.168.x.x:8000
```

**iOS Simulator:**
```bash
flutter run -d ios --dart-define=BACKEND_URL=http://localhost:8000
```

**Web:**
```bash
flutter run -d chrome
```

### Production (Cloud Backend)

Update `lib/config/app_config.dart` to use production URL:

```dart
static String get backendUrl {
  return _prodBackendUrl; // "https://bramha-api.onrender.com"
}
```

Then rebuild:
```bash
flutter clean
flutter pub get
flutter build apk    # Android
flutter build ios    # iOS
flutter build web    # Web
```
