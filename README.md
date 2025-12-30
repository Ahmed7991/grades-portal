# 🎓 Secure Student Grade Portal & Distribution Bot
# بوابة درجات الطلاب الآمنة وبوت التوزيع

<p align="center">
  <a href="#-english"><strong>🇺🇸 English</strong></a> |
  <a href="#-العربية"><strong>🇮🇶 العربية</strong></a>
</p>

---

<div id="english"></div>

## 🇺🇸 English

This project is a complete system for securely distributing student grades. It streamlines the process by combining a cloud-hosted dashboard for results and a secure Telegram bot for access management.

### 📂 Project Structure

| File | Description |
| :--- | :--- |
| `app.py` | The code for the **Website** (Streamlit). |
| `bot.py` | The code for the **Telegram Bot** (Runs locally). |
| `grades.csv` | The database containing names, grades, and secret Access Keys. |
| `requirements.txt` | List of libraries needed for the website deployment. |

### 🚀 Part 1: The Website (Streamlit)
The interface students see to check their results. It is designed to be hosted on the cloud.

#### ✨ Features
* **Visual Gauge:** A speedometer visualization showing the total score.
* **Class Stats:** Displays the student's rank and the class average anonymously.
* **Final Exam Calculator:** Calculates the exact score required to pass or excel.
* **Secure Login:** Uses a unique 5-digit PIN (Key) for access.

#### ☁️ Installation & Deployment
1. Upload `app.py`, `grades.csv`, and `requirements.txt` to this GitHub repository.
2. Go to **Streamlit Cloud**.
3. Connect your GitHub account and select this repository.
4. Click **Deploy**.

> **⚠️ Important:** If you update the grades in `grades.csv`, you must upload the new file to GitHub for the changes to appear on the live website.

### 🤖 Part 2: The Admin Bot (Telegram)
This tool hands out access keys to students so you don't have to message them individually. This script runs locally on your computer.

#### ✨ Features
* **One-Shot Security:** Students can only claim *one* key per Telegram account.
* **Smart Recovery:** If a student loses their key, the bot resends the existing key (instead of blocking them).
* **Smart Typos:** Detects spelling mistakes (e.g., "Ahmd" → "Did you mean Ahmed?").
* **Admin Tools:** View logs, stats, and export data to Excel.

#### 💻 Setup (On your Computer)
1. Install **Python**.
2. Install the required libraries:
   ```bash
   pip install python-telegram-bot pandas openpyxl
