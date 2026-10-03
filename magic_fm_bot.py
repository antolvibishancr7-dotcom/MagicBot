import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

stories_db = {
    "avatar": {
        "name": "Avatar / அவதார்",
        "episodes": "2650/2800",
        "platform": "Pocket FM",
        "status": "RUNNING STORY",
    }
}


@bot.message_handler(commands=["start"])
def start_command(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Tap to interrupt", callback_data="interrupt")
    )
    welcome_text = (
        "✨ WELCOME TO MAGIC FM! ✨\n\n"
        "Use /search <name> to find shows and get episode details.\n"
        "Use /mysteries to view unlocked shows.\n"
        "Download Episodes: Type /ep_single <show_name> and reply to the bot message."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)


@bot.message_handler(commands=["search"])
def search_handler(message):
    query = message.text.replace("/search", "").strip().lower()
    if not query:
        bot.reply_to(message, "Please provide a show name. Example: /search avatar")
        return

    found = False
    for key, data in stories_db.items():
        if query in key.lower() or query in data["name"].lower():
            response = (
                f"📖 *{data['name']}*\n"
                f"📊 Episodes: {data['episodes']}\n"
                f"🎧 Platform: {data['platform']}\n"
                f"Status: {data['status']}"
            )
            bot.reply_to(message, response, parse_mode="Markdown")
            found = True
            break

    if not found:
        bot.reply_to(
            message,
            "Sorry, this show isn't available right now. Contact admin for requests.",
        )


@bot.message_handler(commands=["mysteries"])
def mysteries_handler(message):
    response = "⭐ *Available Unlocked Shows* ⭐\n\n"
    for data in stories_db.values():
        response += f"• *{data['name']}* ({data['platform']})\n"
    bot.reply_to(message, response, parse_mode="Markdown")


@bot.message_handler(commands=["ep_single"])
def ep_single_handler(message):
    if not message.reply_to_message:
        bot.reply_to(
            message,
            "Please reply to the message with the show name to download episodes.",
        )
        return
    bot.reply_to(message, "Processing your download request... Please wait.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
    
