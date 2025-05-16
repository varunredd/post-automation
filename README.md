# Daily Quote Automation Bot - README

Automate your Instagram with a beautifully designed daily quote system. This project uses Google Gemini AI for quote generation, Pillow for image creation, and Instabot to publish directly to Instagram — all orchestrated via GitHub Actions.

---

## 🚀 Features

* 🔮 Daily quote generation using Gemini API
* 🖼️ HD Unsplash backgrounds with blur
* 🧠 Auto-detect text color for readability
* 🤖 Scheduled Instagram posting with Instabot
* 🛠️ GitHub Actions support for daily scheduling

---

## 🧩 Components

### Quote Generation

* Uses `gemini-1.5-flash` via `google.generativeai`
* Adds randomness using a topic + seed

### Image Rendering

* Pulls backgrounds from Unsplash (`orientation=squarish`)
* Resizes to 1080x1080 and applies Gaussian blur
* Adds center-aligned wrapped quote using Pillow

### Instagram Upload

* Uses Instabot
* Stores credentials in `config/secret.txt` after first login

### GitHub Actions

* Daily at 9 AM UTC (`cron`)
* Also supports manual triggering

---

## 🔐 Environment Variables

Create a `.env` file (or set these as GitHub secrets):

```env
GEMINI_API_KEY=<your-gemini-api-key>
UNSPLASH_ACCESS_KEY=<your-unsplash-access-key>
IG_USERNAME=<your-instagram-username>
IG_PASSWORD=<your-instagram-password>
```

---

## 🛠️ Installation

```bash
git clone https://github.com/<your-username>/daily-quote-bot.git
cd daily-quote-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 💻 Running Locally

```bash
python main.py
```

* First-time use will prompt for IG login
* Stores login session in `config/secret.txt`

---

## 🔄 GitHub Actions Setup

### Secrets Required

* `GEMINI_API_KEY`
* `UNSPLASH_ACCESS_KEY`
* `IG_USERNAME`
* `IG_PASSWORD`

### Notes

* Billing must be enabled for Actions in **private repos**
* Always delete `config/` before upload to ensure fresh session

### Sample Workflow File

```yaml
name: Daily Gemini Instagram Poster

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
  post-daily-quote:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Clean config dir
        run: rm -rf config

      - name: Run bot
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          UNSPLASH_ACCESS_KEY: ${{ secrets.UNSPLASH_ACCESS_KEY }}
          IG_USERNAME: ${{ secrets.IG_USERNAME }}
          IG_PASSWORD: ${{ secrets.IG_PASSWORD }}
        run: python main.py
```

---

## 🧪 Troubleshooting

| Issue                         | Cause                         | Fix                                   |
| ----------------------------- | ----------------------------- | ------------------------------------- |
| `403 Upload Failed`           | Session/cookie invalid        | Re-login locally and delete `config/` |
| `challenge_required`          | Instagram flagged session     | Manual login required                 |
| GitHub Actions not triggering | Billing issue in private repo | Enable billing or make repo public    |
| Duplicate quotes              | Gemini may cache              | Add `seed` and random `topic`         |

---

## 💡 Tips & Best Practices

* Keep your repo **public** to avoid Actions billing
* Post max once/day to avoid Instagram soft blocks
* Add Telegram/Discord webhook for preview delivery
* Log each post to a file or GSheet for reference

---

## 📄 License

MIT License. Free and open to use.

---

## 👤 Maintainer

**Varun Reddy Gutha**
Contact: [GitHub Profile](https://github.com/varunredd)

---

> 🎯 Want daily content on autopilot? Fork this repo, add your keys, and let automation do the rest!
