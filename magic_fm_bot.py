import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

Bot Token
TOKEN = "8606028877:AAGQNkFiDLPzWJiIFXQTypU5AbF7YmkydQc"
bot = telebot.TeleBot(TOKEN)

Admin Contact
ADMIN_CONTACT = "@MagicFmHelpDesk or @SilentKingKiller"

stories_db = {
"avatar": {
"name": "Avatar / அவதார்",
"episodes": "2650/2800",
"platform": "Pocket FM",
"status": "RUNNING STORY",
}
}

@bot.message_handler(commands=['start'])
def start_command(message):
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("How To Use ❓", callback_data="help"))
welcome_text = (
"🎧 WELCOME TO MAGIC FM!\n\n"
"⭐ STREAM AND LISTEN TO YOUR FAVORITE AUDIO SHOWS FROM POCKET FM & KUKU FM IN 9PER HD QUALITY!\n\n"
"🔍 Start exploring now:\n"
"• Use /search <name> to find your show!\n"
"• Use /mystories to view your unlocked shows!"
)
bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_command(message):
help_text = (
"📖 How To Use MAGIC FM DOWNLOADER BOT\n\n"
"1️⃣ START THE BOT\nOpen the bot chat and tap /start.\n\n"
"2️⃣ SEARCH FOR YOUR SHOW\nType /search followed by the name of your show.\n\n"
"3️⃣ VIEW YOUR SHOWS\nUse /mystories to view your unlocked shows.\n\n"
"4️⃣ DOWNLOAD EPISODES\nEnter episode number or range.\n\n"
f"🔑 Need full access?\nContact: {ADMIN_CONTACT}"
)
bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['search'])
def search_command(message):
query = message.text.replace('/search', '').strip().lower()
if not query:
bot.reply_to(message, "Please provide a show name. Example: /search Avatar", parse_mode="Markdown")
return
if query in stories_db:
story = stories_db[query]
text = (
f"🎬 Show Status Details:\n\n🏷️ Name: {story['name']}\n"
f"📺 Episodes: {story['episodes']}\n🌐 Platform: {story['platform']}\n"
f"🟢 Status: {story['status']}\n\n🔑 How To Get Access:\n"
f"1️⃣ Use /search name to find your favorite show.\n2️⃣ Follow the guidance on the screen.\n"
f"3️⃣ Contact the admin to purchase your access.\n\n💰 To Buy & Get Access Contact:\n"
f"👉 {ADMIN_CONTACT}"
)
bot.send_message(message.chat.id, text, parse_mode="Markdown")
else:
bot.send_message(message.chat.id, "❌ Show not found. Please check the name or contact admin.")

@bot.message_handler(commands=['mystories'])
def mystories_command(message):
markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("Avatar", callback_data="select_avatar"))
text = "📚 Your Stories\n\n✨ Click any story below to start listening."
bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["select_avatar", "help"])
def callback_query(call):
if call.data == "help":
help_command(call.message)
elif call.data == "select_avatar":
text = (
"🏷️ Name: Avatar / அவதார்\n📺 Episodes: 2650/2800\n"
"🌐 Platform: Pocket FM\n🟢 Status: RUNNING STORY\n\n"
"📥 Enter Episode Number:\n🔹 Single: 1\n🔸 Range: 1 10"
)
bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and message.text.replace(' ', '').isdigit())
def handle_episodes(message):
parts = message.text.split()
if len(parts) == 1:
ep = parts[0]
bot.send_message(message.chat.id, f"🎵 Avatar Ep {ep}\n👤 @SilentKingKiller\n\n*(Audio File/Voice Note would be sent here)", parse_mode="Markdown")
elif len(parts) == 2:
start_ep, end_ep = int(parts[0]), int(parts[1])
for ep in range(start_ep, end_ep + 1):
bot.send_message(message.chat.id, f"🎵 Avatar Ep {ep:03d}\n👤 @SilentKingKiller\n\n(Audio File/Voice Note would be sent here)*", parse_mode="Markdown")
bot.send_message(message.chat.id, f"✅ Sent {end_ep - start_ep + 1} episode(s).", parse_mode="Markdown")

if name == 'main':
print("Bot is running...")
bot.infinity_polling()