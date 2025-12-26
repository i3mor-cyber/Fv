import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ========= إعدادات =========
ADMIN_ID = 6791241030
DATA_FILE = "data.json"

waiting_for = None

# ========= تحميل / حفظ البيانات =========
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"sources": [], "targets": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# ========= تحقق أدمن =========
def is_admin(update: Update):
    user = update.effective_user
    return user and user.id == ADMIN_ID

# ========= /start =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text(
            f"📩 رسالة من شخص غير أدمن\n"
            f"👤 الاسم: {update.effective_user.full_name}\n"
            f"🆔 ID: {update.effective_user.id}\n"
            f"🔗 @{update.effective_user.username}"
        )
        return

    keyboard = [
        [InlineKeyboardButton("➕ إضافة مصدر", callback_data="add_source")],
        [InlineKeyboardButton("➕ إضافة هدف", callback_data="add_target")],
        [InlineKeyboardButton("🗑️ مسح الأهداف", callback_data="clear_targets")]
    ]

    await update.message.reply_text(
        "🎛️ لوحة التحكم",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========= الأزرار =========
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for
    query = update.callback_query
    await query.answer()

    if not is_admin(update):
        return

    if query.data == "add_source":
        waiting_for = "source"
        await query.edit_message_text("📥 أرسل معرف القناة المصدر")

    elif query.data == "add_target":
        waiting_for = "target"
        await query.edit_message_text("📤 أرسل معرف القناة الهدف")

    elif query.data == "clear_targets":
        data["targets"] = []
        save_data()
        await query.edit_message_text("🗑️ تم مسح جميع القنوات الهدف")

# ========= استقبال النص =========
async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for

    if not is_admin(update):
        return

    text = update.message.text.strip()

    if waiting_for == "source":
        data["sources"].append(text)
        save_data()
        waiting_for = None
        await update.message.reply_text("✅ تم إضافة المصدر")

    elif waiting_for == "target":
        data["targets"].append(text)
        save_data()
        waiting_for = None
        await update.message.reply_text("✅ تم إضافة الهدف")

# ========= تحويل الرسائل =========
async def forward_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if chat_id in data["sources"]:
        for target in data["targets"]:
            try:
                await update.message.forward(chat_id=target)
            except:
                pass

# ========= تشغيل البوت =========
async def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("TOKEN غير موجود في Variables")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))
    app.add_handler(MessageHandler(filters.ALL, forward_messages))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())        await update.message.reply_text(
            f"📩 رسالة من شخص غير أدمن\n"
            f"👤 الاسم: {update.effective_user.full_name}\n"
            f"🆔 ID: {update.effective_user.id}\n"
            f"🔗 @{update.effective_user.username}"
        )
        return

    keyboard = [
        [InlineKeyboardButton("➕ إضافة مصدر", callback_data="add_source")],
        [InlineKeyboardButton("➕ إضافة هدف", callback_data="add_target")],
        [InlineKeyboardButton("🗑️ مسح الأهداف", callback_data="clear_targets")],
    ]

    await update.message.reply_text(
        "🎛️ لوحة التحكم",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========= أزرار =========
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for
    query = update.callback_query
    await query.answer()

    if not is_admin(update):
        return

    if query.data == "add_source":
        waiting_for = "source"
        await query.edit_message_text("📥 أرسل معرف القناة المصدر")

    elif query.data == "add_target":
        waiting_for = "target"
        await query.edit_message_text("📤 أرسل معرف القناة الهدف")

    elif query.data == "clear_targets":
        data["targets"] = []
        save_data()
        await query.edit_message_text("🗑️ تم مسح جميع القنوات الهدف")

# ========= استقبال النص =========
async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for

    if not is_admin(update):
        return

    text = update.message.text.strip()

    if waiting_for == "source":
        data["sources"].append(text)
        save_data()
        waiting_for = None
        await update.message.reply_text("✅ تم إضافة المصدر")

    elif waiting_for == "target":
        data["targets"].append(text)
        save_data()
        waiting_for = None
        await update.message.reply_text("✅ تم إضافة الهدف")

# ========= تحويل الرسائل =========
async def forward_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    if chat_id in data["sources"]:
        for target in data["targets"]:
            try:
                await update.message.forward(chat_id=target)
            except:
                pass

# ========= تشغيل البوت =========
async def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))
    app.add_handler(MessageHandler(filters.ALL, forward_messages))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

