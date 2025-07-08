# 🔐 BruteWall - Brute Force Simulator + IP Blocker

**BruteWall** is a Django-based security simulation tool that:
- Simulates brute-force login attempts
- Logs IP addresses and failed attempts
- Blocks malicious IPs after a threshold
- Auto-unblocks after a cooldown
- Visualizes data with charts (Doughnut + Attempts over Time)

---

## 🚀 Features

- 🚫 Temporary IP blocking
- 📊 Real-time attempt logging
- ⏱ Countdown timer for blocked IPs
- 📉 ChartJS-based data visualization
- 📁 Export logs to CSV
- 🔒 Realistic brute-force mitigation logic

---

## 📸 Screenshots

> Just setup has been completed

---

## ⚙️ Tech Stack

- Django
- Chart.js
- Bulma CSS
- SQLite (default, can be changed)
- HTML/CSS/JS

---

## 🔧 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/Ataur1502/brutewall.git
   cd brutewall
## ⚙️ Setup Instructions

### 🐍 Create virtual environment

```bash
python -m venv env
env\Scripts\activate  # On Windows
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```
### 🚀 Run the server

```bash
python manage.py migrate
python manage.py runserver
```
---
### 💡 To-Do
- Add user authentication

 - GeoIP-based IP info

 - Admin panel controls

 - Deployment (Render/Railway)
---
# 📄 License
MIT – use freely for learning or internal tools.

