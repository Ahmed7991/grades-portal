# 🎓 Secure Student Grade Portal & Distribution Bot

[![Language](https://img.shields.io/badge/Language-English-blue)](#english) [![Language](https://img.shields.io/badge/Language-Arabic-green)](#arabic)

This project is a complete system for securely distributing student grades. It streamlines the process by combining a cloud-hosted dashboard for results and a secure Telegram bot for access management.

هذا المشروع عبارة عن نظام متكامل لتوزيع درجات الطلاب بشكل آمن. يجمع بين لوحة تحكم سحابية لعرض النتائج وبوت تيليجرام لإدارة وتوزيع مفاتيح الدخول.

---

<a name="english"></a>
## 🇬🇧 English Description

### 📂 Project Structure

| File | Description |
| :--- | :--- |
| `app.py` | The code for the **Website** (Streamlit). |
| `bot.py` | The code for the **Telegram Bot** (Runs locally). |
| `grades.csv` | The database containing names, grades, and secret Access Keys. |
| `requirements.txt` | List of libraries needed for the website deployment. |

### 🚀 Part 1: The Website (Streamlit)
The interface students see to check their results. It is designed to be hosted on the cloud.

**✨ Features**
* **Visual Gauge:** A speedometer visualization showing the total score.
* **Class Stats:** Displays the student's rank and the class average anonymously.
* **Final Exam Calculator:** Calculates the exact score required to pass or excel based on current grades.
* **Secure Login:** Uses a unique 5-digit PIN (Key) for access.

**☁️ Installation & Deployment**
1.  Upload `app.py`, `grades.csv`, and `requirements.txt` to this GitHub repository.
2.  Go to **Streamlit Cloud**.
3.  Connect your GitHub account and select this repository.
4.  Click **Deploy**.

> **⚠️ Important:** If you update the grades in `grades.csv`, you must upload the new file to GitHub for the changes to appear on the live website.

### 🤖 Part 2: The Admin Bot (Telegram)
This tool automatically hands out access keys to students so you don't have to message them individually. This script runs locally on your computer.

**✨ Features**
* **One-Shot Security:** Students can only claim *one* key per Telegram account.
* **Smart Recovery:** If a student loses their key, the bot resends the existing key (instead of blocking them).
* **Smart Typos:** Detects spelling mistakes (e.g., "Ahmd" → "Did you mean Ahmed?").
* **Admin Tools:** View logs, stats, and export data to Excel.

**💻 Setup (On your Computer)**
1.  Install **Python**.
2.  Install the required libraries:
    ```bash
    pip install python-telegram-bot pandas openpyxl
    ```
3.  Place `bot.py` and `grades.csv` in the same folder.
4.  Run the bot:
    ```bash
    python bot.py
    ```

**🛠️ Admin Commands (For You Only)**
* `/stats` - View how many students have collected their keys.
* `/log` - Receive the raw text log file of all transactions.
* `/export` - **(New)** Download an Excel file of all registered students (Names + Telegram Usernames).
* `/reset [Full Name]` - Delete a student's claim so they can try again.

### ⚠️ Crucial Security Note
1.  **Synchronization:** Ensure the `grades.csv` file on your **Laptop** (for the Bot) is the exact same version as the one on **GitHub** (for the Website).
2.  **Bot Token:** **Never** upload `bot.py` containing your secret API Token to a public GitHub repository.

---

<a name="arabic"></a>
## 🇮🇶 الشرح بالعربي (Arabic)

### 📂 هيكلية المشروع

| الملف | الوصف |
| :--- | :--- |
| `app.py` | كود **الموقع الإلكتروني** (مبني بـ Streamlit). |
| `bot.py` | كود **بوت التيليجرام** (يعمل على لابتوبك). |
| `grades.csv` | قاعدة البيانات التي تحتوي على الأسماء، الدرجات، والمفاتيح السرية (Keys). |
| `requirements.txt` | قائمة المكتبات البرمجية المطلوبة لتشغيل الموقع. |

### 🚀 الجزء الأول: الموقع الإلكتروني (Streamlit)
هذه هي الواجهة التي يراها الطلاب. يتم استضافتها على السحابة (Cloud).

**✨ المميزات**
* **عداد مرئي:** عداد سرعة يظهر المجموع الكلي للطالب بشكل جميل.
* **إحصائيات الصف:** تظهر ترتيب الطالب ومعدل الصف العام (دون كشف أسماء الآخرين).
* **حاسبة الامتحان النهائي:** تحسب الدرجة المطلوبة منك في "الفاينل" للنجاح أو التفوق.
* **تسجيل دخول آمن:** يستخدم رمز سري مكون من 5 أرقام (Key).

**☁️ التنصيب والرفع**
1.  ارفع الملفات `app.py`, `grades.csv`, و `requirements.txt` إلى مستودع GitHub هذا.
2.  اذهب إلى موقع **Streamlit Cloud**.
3.  اربط حساب GitHub الخاص بك واختر هذا المستودع (Repository).
4.  اضغط على **Deploy**.

> **⚠️ مهم جداً:** إذا قمت بتحديث الدرجات في ملف `grades.csv`، يجب عليك رفع الملف الجديد إلى GitHub لتظهر التغييرات للطلاب على الموقع.

### 🤖 الجزء الثاني: بوت الأدمن (Telegram)
هذه الأداة توزع المفاتيح للطلاب تلقائياً لكي لا تضطر لمراسلتهم واحداً تلو الآخر. يعمل هذا الملف محلياً على حاسوبك.

**✨ المميزات**
* **أمان المرة الواحدة:** يمكن للطالب استلام مفتاح واحد فقط لكل حساب تيليجرام.
* **استرجاع ذكي:** إذا أضاع الطالب مفتاحه، يعيد البوت إرسال نفس المفتاح (بدلاً من حظره).
* **تصحيح الأخطاء:** يكتشف الأخطاء الإملائية في الأسماء (مثلاً "أحممد" ← "هل تقصد أحمد؟").
* **أدوات الأدمن:** عرض السجلات، الإحصائيات، وتصدير البيانات إلى Excel.

**💻 الإعداد (على حاسوبك)**
1.  قم بتنصيب **Python**.
2.  نصّب المكتبات المطلوبة عبر التيرمنال:
    ```bash
    pip install python-telegram-bot pandas openpyxl
    ```
3.  ضع ملف `bot.py` وملف `grades.csv` في نفس المجلد.
4.  شغل البوت:
    ```bash
    python bot.py
    ```

**🛠️ أوامر الأدمن (لك أنت فقط)**
* `/stats` - عرض عدد الطلاب الذين استلموا مفاتيحهم حتى الآن.
* `/log` - استلام ملف السجل النصي (Log) لجميع العمليات التي تمت.
* `/export` - **(جديد)** تحميل ملف Excel يحتوي على جميع الطلاب المسجلين (الأسماء + معرفات التيليجرام).
* `/reset [الاسم الكامل]` - حذف مطالبة طالب معين ليتمكن من المحاولة مرة أخرى (مفيد إذا أخطأ الطالب في كتابة اسمه).

### ⚠️ ملاحظة أمنية هامة
1.  **التزامن (Synchronization):** تأكد من أن ملف `grades.csv` الموجود على **لابتوبك** (للبوت) هو نسخة طبق الأصل للملف الموجود على **GitHub** (للموقع). إذا اختلفت الملفات، لن تعمل المفاتيح.
2.  **توكن البوت:** لا تقم أبداً برفع ملف `bot.py` الذي يحتوي على التوكن السري (Token) إلى مستودع عام (Public Repo). ابقه خاصاً على جهازك.

---

## 📝 Credits
Built with [Streamlit](https://streamlit.io/) and [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot).
