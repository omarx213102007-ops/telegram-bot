import telebot
import time

TOKEN = "7839188694:AAHco14GPuUcl1m7haP4sXecpZrMiR-HWTk"
GROUP_ID = -1003771318957

bot = telebot.TeleBot(TOKEN)

# منع السبام
last_message_time = {}

# ربط رسالة الجروب بالمستخدم
message_map = {}

WELCOME_TEXT = (
    "👋 أهلاً بيك!\n\n"
    "📩 ابعت رسالتك هنا، وهتوصل للإدارة مباشرة.\n"
    "⏳ سيتم الرد عليك في أقرب وقت ممكن.\n\n"
    "شكراً لتواصلك 💙"
)

# /start → ترحيب فقط
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, WELCOME_TEXT)

# استقبال رسائل المستخدمين
@bot.message_handler(func=lambda message: message.chat.type == "private")
def handle_user_message(message):
    user_id = message.from_user.id
    now = time.time()

    # Anti-spam (رسالة كل دقيقة)
    if user_id in last_message_time and now - last_message_time[user_id] < 60:
        bot.send_message(message.chat.id, "⛔ من فضلك استنى شوية قبل ما تبعت رسالة تانية")
        return

    last_message_time[user_id] = now

    text = (
        "📩 رسالة جديدة\n\n"
        f"👤 الاسم: {message.from_user.first_name}\n"
        f"🔗 اليوزر: @{message.from_user.username}\n"
        f"🆔 ID: {user_id}\n\n"
        "💬 الرسالة:\n"
        f"{message.text}"
    )

    sent = bot.send_message(GROUP_ID, text)

    # نخزن الربط
    message_map[sent.message_id] = user_id

    # تطمين للمستخدم فقط
    bot.send_message(
        message.chat.id,
        "✅ رسالتك وصلت، برجاء الانتظار لحين الرد."
    )

# الرد من الجروب
@bot.message_handler(func=lambda message: message.chat.id == GROUP_ID and message.reply_to_message)
def handle_admin_reply(message):
    replied_id = message.reply_to_message.message_id

    if replied_id in message_map:
        user_id = message_map[replied_id]
        bot.send_message(user_id, message.text)        # مفيش أي رسالة تطمين هنا 👌

bot.infinity_polling()
