# Health Dashboard – Setup Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- npm

---

## 1. Garmin Setup (easiest)

1. Copy the env file:
   ```bash
   cp backend/.env.example backend/.env
   ```
2. Fill in your Garmin credentials in `backend/.env`:
   ```
   GARMIN_EMAIL=your@email.com
   GARMIN_PASSWORD=yourpassword
   ```
   That's it — no API registration needed.

---

## 2. Strava Setup

### Step 1: Create a Strava API Application
1. Go to **https://www.strava.com/settings/api**
2. Fill in:
   - **Application Name:** Health Dashboard (anything works)
   - **Category:** Other
   - **Website:** `http://localhost`
   - **Authorization Callback Domain:** `localhost`
3. Click **Create** and you'll see your **Client ID** and **Client Secret**

### Step 2: Add credentials to `.env`
```
STRAVA_CLIENT_ID=123456
STRAVA_CLIENT_SECRET=abcdef...
```

### Step 3: Connect Strava
1. Start the dashboard (`./start.sh`)
2. Open **http://localhost:5173**
3. Click **Connect →** next to Strava (or go to http://localhost:8000/auth/strava)
4. Authorize in the browser — you'll be redirected back and see a success page
5. Refresh the dashboard — Strava data will now load

---

## 3. Google Fit Setup (for Rempho data)

### Step 1: Make sure Rempho syncs to Google Fit
On your Android phone:
1. Open the **Rempho** app
2. Go to **Settings → Connected Apps**
3. Enable **Google Fit** sync

### Step 2: Create a Google Cloud Project
1. Go to **https://console.cloud.google.com**
2. Click **New Project** → name it "Health Dashboard" → **Create**
3. In the left menu go to **APIs & Services → Library**
4. Search for **Fitness API** → click it → **Enable**

### Step 3: Create OAuth credentials
1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**
3. If prompted, configure the OAuth consent screen first:
   - User type: **External**
   - App name: Health Dashboard
   - Add your email as a test user
   - Scopes: add `fitness.body.read` and `fitness.activity.read`
4. Back in Create Credentials:
   - Application type: **Web application**
   - Name: Health Dashboard
   - Authorized redirect URIs: `http://localhost:8000/auth/google/callback`
5. Click **Create** — copy the **Client ID** and **Client Secret**

### Step 4: Add credentials to `.env`
```
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...
```

### Step 5: Connect Google Fit
1. Start the dashboard (`./start.sh`)
2. Click **Connect →** next to Rempho / Google Fit (or go to http://localhost:8000/auth/google)
3. Sign in with your Google account and grant access
4. Refresh the dashboard — weight and body fat data will appear

---

## Running the Dashboard

```bash
./start.sh
```

- Dashboard: **http://localhost:5173**
- From phone (same WiFi): **http://YOUR_LOCAL_IP:5173**
  - Find your IP: `hostname -I` (Linux/Mac)

The dashboard auto-refreshes data each time you open or reload it.
Use the **Refresh** button in the top-right to re-sync manually.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Garmin login fails | Check email/password in `.env`. If you use 2FA, you may need to disable it temporarily or use the Garmin app to approve the login. |
| Strava shows 401 | Click Connect Strava again to re-authorise. |
| No Rempho data in Google Fit | Open Rempho app → sync manually → wait a few minutes for Google Fit to update. |
| Can't access from phone | Make sure phone and computer are on the same WiFi. Use the IP shown by `start.sh`. |
