import logging
import pandas as pd
import json
import os
import difflib
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CONFIGURATION ---
BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE" 
WEBSITE_URL = "https://grades-app-a.streamlit.app/"
ADMIN_ID = 000000000  # Replace with your Admin ID

# --- DATA LOADING ---
try:
    df = pd.read_csv("students.csv", dtype={'رمز_الدخول': str})
    grades_db = dict(zip(df['اسم الطالب'].str.strip(), df['رمز_الدخول']))
    print("✅ Database loaded successfully.")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    grades_db = {}

# --- FILES ---
CLAIMS_FILE = "claims.json"
LOG_FILE = "log.txt"

def load_claims():
    if os.path.exists(CLAIMS_FILE):
        with open(CLAIMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}, "names": {}}

def save_claims(claims):
    with open(CLAIMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(claims, f, ensure_ascii=False, indent=4)

def append_to_log(user_id, telegram_handle, telegram_name, student_name, action="Claimed"):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"ID: {user_id} | User: {telegram_handle} ({telegram_name}) ===> {action}: {student_name}\n")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- ADMIN COMMANDS ---

async def admin_export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("❌ No logs found.")
        return
    await update.message.reply_text("⏳ Exporting Excel...")
    
    # ... (Export logic omitted for brevity in template, or keep full logic) ...
    # You can keep the full code here, just the TOKEN matters.

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    claims = load_claims()
    total = len(grades_db)
    claimed = len(claims["names"])
    msg = f"📊 **Stats**\n✅ Claimed: {claimed}\n📚 Total: {total}"
    await update.message.reply_text(msg, parse_mode='Markdown')

# ... (Keep the rest of the functions exactly as they are in your local file) ...

# --- USER COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome\nSend your full name to get your key.", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (Logic identical to local file) ...
    pass 

if __name__ == '__main__':
    # Build Application
    if BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("⚠️ Error: Please insert your Token in the code.")
    else:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        # Add handlers here...
        print("🤖 Bot Running...")
        application.run_polling()
