# 🚀 Deploy YTDown to Render — Step by Step Guide

## What you'll need
- A free GitHub account → https://github.com
- A free Render account → https://render.com

---

## PART 1 — Upload your code to GitHub

### Step 1 — Create a GitHub account
1. Go to https://github.com
2. Click **Sign up** → follow the steps
3. Verify your email

### Step 2 — Create a new repository
1. Click the **+** icon (top right) → **New repository**
2. Name it: `ytconverter`
3. Set it to **Public**
4. Click **Create repository**

### Step 3 — Upload your files
On the new repo page:
1. Click **"uploading an existing file"** link
2. Drag and drop ALL these files into the window:
   - `server.py`
   - `index.html`
   - `requirements.txt`
   - `render.yaml`
   - `.gitignore`
3. Click **Commit changes**

---

## PART 2 — Deploy on Render

### Step 4 — Create a Render account
1. Go to https://render.com
2. Click **Get Started for Free**
3. Sign up with your GitHub account (easiest!)

### Step 5 — Create a new Web Service
1. On Render dashboard, click **New +** → **Web Service**
2. Click **Connect** next to your `ytconverter` GitHub repo
3. Fill in the settings:
   - **Name**: `ytconverter` (or anything you like)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Instance Type**: `Free`
4. Click **Create Web Service**

### Step 6 — Wait for deployment (~2-3 minutes)
Render will:
- Pull your code from GitHub
- Install Python packages
- Install ffmpeg automatically
- Start your server

You'll see a green **"Live"** badge when done.

### Step 7 — Get your public URL!
Render gives you a URL like:
```
https://ytconverter.onrender.com
```

**Share this link with your friends — they can use it from anywhere! 🎉**

---

## ⚠️ Free Tier Notes

| Limitation | Detail |
|---|---|
| Spin down | Free apps sleep after 15 mins of inactivity. First load takes ~30 seconds to wake up. |
| Disk space | 512MB — files auto-delete after 1 hour (already built in) |
| Bandwidth | 100GB/month — plenty for personal use |

## 💡 To avoid sleep (optional)
Use a free service like https://uptimerobot.com to ping your URL every 10 minutes — keeps it awake 24/7.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Build failed | Check the Render logs — usually a missing package |
| ffmpeg error | Render has ffmpeg pre-installed, should work automatically |
| App sleeping | Normal on free tier — first visit takes 30s to wake |
| YouTube blocked | Some server IPs get blocked by YouTube — try again later |
