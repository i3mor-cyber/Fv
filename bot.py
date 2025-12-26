import os
import json
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 6791241030

DATA_FILE = "data.json"

# ===== تحميل / حفظ البيانات =====
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "sources": [],
            "targets": [],
            "active": False
        }
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()
waiting_for = None

# ===== أدوات مساعدة =====
def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID

def dashboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ إضافة قروب مصدر", callback_data="add_source")],
        [InlineKeyboardButton("➕ إضافة قروب هدف", callback_data="add_target")],
        [InlineKeyboardButton("🗑️ مسح القروبات الهدف", callback_data="clear_targets")],
        [
            InlineKeyboardButton("▶️ تشغيل", callback_data="on"),
            InlineKeyboardButton("⏹️ إيقاف", callback_data="off")
        ],
        [InlineKeyboardButton("📊 الحالة", callback_data="status")]
    ])

# ===== أوامر =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return
    await update.message.reply_text(
        "🎛️ **لوحة التحكم**\nاختر ما تريد:",
        reply_markup=dashboard(),
        parse_mode="Markdown"
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for
    query = update.callback_query
    await query.answer()

    if not is_admin(update):
        return

    if query.data == "add_source":
        waiting_for = "source"
        await query.edit_message_text("📥 رد على رسالة من قروب المصدر")

    elif query.data == "add_target":
        waiting_for = "target"
        await query.edit_message_text("📤 رد على رسالة من قروب الهدف")

    elif query.data == "clear_targets":
        data["targets"] = []
        save_data()
        await query.edit_message_text("🗑️ تم مسح القروبات الهدف")


    elif query.data == "add_source":
    await query.edit_message_text("أرسل معرف القناة المصدر")
