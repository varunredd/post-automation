# Daily Quote Automation System - Technical Documentation

## Overview
This document outlines the architecture, setup, execution flow, and troubleshooting guide for the **Instagram Quote Automation Bot**. The system is designed to generate daily motivational quotes using Google Gemini, render them over a stylized background fetched from Unsplash, and post them automatically to Instagram using a scheduled GitHub Actions pipeline.

---

## Components

### 1. Quote Generator (Google Gemini)
- **API Used:** `gemini-1.5-flash`
- **Integration:** via `google.generativeai` Python SDK
- **Entropy Logic:** Random topic + seed injection to avoid duplicate responses

### 2. Background Image (Unsplash API)
- **API Endpoint:** `https://api.unsplash.com/photos/random`
- **Topic Query:** E.g. `motivation`, `inspiration`, etc.
- **Post-processing:** Image is resized to 1080x1080 and blurred using Pillow's `ImageFilter.GaussianBlur`.

### 3. Image Composer (Pillow)
- **Canvas Size:** 1080x1080 pixels
- **Text Styling:**
  - Font: Poppins-Regular.ttf (fallback to default)
  - Adaptive color (white/black) based on background brightness
  - Centered text with line wrapping

### 4. Instagram Uploader (Instabot)
- **Library:** `instabot`
- **Config Storage:** Creates local `config/secret.txt` to store IG credentials
- **Upload Format:** `.jpg` with `.REMOVE_ME` appended automatically by the bot

### 5. Scheduler (GitHub Actions)
- **Trigger Types:**
  - `workflow_dispatch` (manual run)
  - `cron: '0 9 * * *'` (daily at 9 AM UTC)
- **File:** `.github/workflows/post-instagram.yml`

---

## Environment Variables
Set via `.env` file (locally) or GitHub Secrets (for Actions).

```env
GEMINI_API_KEY=<your-gemini-api-key>
UNSPLASH_ACCESS_KEY=<your-unsplash-access-key>
IG_USERNAME=<instagram-username>
IG_PASSWORD=<instagram-password>

## Installation

git clone https://github.com/<your-username>/daily-quote-bot.git
cd daily-quote-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

