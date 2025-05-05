from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Define 10 questions with options and associated humor types
questions = [
    {"q": "1. What meme is funnier to you?", "options": [("Cat in space", "meme"), ("Joke about death", "dark"), ("Dancing banana", "absurd"), ("Life sarcasm", "intellectual")]},
    {"q": "2. What kind of joke makes you laugh?", "options": [("Stupid pun", "absurd"), ("Dry sarcasm", "intellectual"), ("TikTok sound joke", "meme"), ("Very dark joke", "dark")]},
    {"q": "3. What do you think of dark humor?", "options": [("Love it", "dark"), ("Only sometimes", "intellectual"), ("Not for me", "meme"), ("I laugh awkwardly", "absurd")]},
    {"q": "4. Favorite reaction to a joke?", "options": [("Laugh inside", "dry"), ("Laugh loud", "meme"), ("Say hmm", "intellectual"), ("Weird face", "absurd")]},
    {"q": "5. Pick a movie genre:", "options": [("Comedy", "meme"), ("Satire", "intellectual"), ("Horror-comedy", "dark"), ("Experimental", "absurd")]},
    {"q": "6. Your humor style is closer to:", "options": [("Random chaos", "absurd"), ("Cold sarcasm", "dry"), ("Silly TikTok", "meme"), ("Complex irony", "intellectual")]},
    {"q": "7. You see someone trip. Your reaction:", "options": [("Laugh", "meme"), ("Ask if they're okay", "intellectual"), ("Film it", "dark"), ("Make a weird sound", "absurd")]},
    {"q": "8. Choose a word:", "options": [("Banana", "absurd"), ("Irony", "intellectual"), ("Boomer", "meme"), ("Grave", "dark")]},
    {"q": "9. Favorite meme format:", "options": [("Drake", "meme"), ("Doomer Wojak", "dark"), ("Surreal memes", "absurd"), ("Mocking SpongeBob", "intellectual")]},
    {"q": "10. Which comedian do you prefer?", "options": [("Mr. Bean", "absurd"), ("George Carlin", "intellectual"), ("Dark TikTok guy", "dark"), ("Kevin Hart", "meme")]} 
]

humor_descriptions = {
    "meme": "😂 *Meme Humor* – You enjoy relatable, viral content and laugh at everyday absurdities.",
    "dark": "🖤 *Dark Humor* – You find humor in the taboo, irony, and life’s uncomfortable truths.",
    "absurd": "🤪 *Absurd Humor* – You love nonsense, randomness, and unpredictable silliness.",
    "intellectual": "🧠 *Intellectual Humor* – You enjoy clever wordplay, irony, and sarcasm with meaning.",
    "dry": "🤓 *Dry Humor* – You prefer wit delivered with a straight face, often misunderstood by others."
}

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"index": 0, "scores": {"meme": 0, "dark": 0, "absurd": 0, "intellectual": 0, "dry": 0}}
    await send_question(update, context, user_id)

async def send_question(update, context, user_id):
    data = user_data[user_id]
    index = data["index"]
    if index >= len(questions):
        await show_result(context, user_id)
        return

    q_data = questions[index]
    keyboard = [[InlineKeyboardButton(opt[0], callback_data=opt[1])] for opt in q_data["options"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text=q_data["q"], reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    selected = query.data
    user_data[user_id]["scores"][selected] += 1
    user_data[user_id]["index"] += 1
    await send_question(update, context, user_id)

async def show_result(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    scores = user_data[user_id]["scores"]
    total = sum(scores.values())
    result = "🎯 *Your Humor Type Breakdown:*\n"
    for k, v in scores.items():
        percent = (v / total) * 100
        result += f"{k.capitalize()} Humor: {percent:.0f}%\n"

    await context.bot.send_message(chat_id=user_id, text=result, parse_mode="Markdown")

    # Send detailed descriptions for each type
    for k in scores:
        await context.bot.send_message(chat_id=user_id, text=humor_descriptions[k], parse_mode="Markdown")

    del user_data[user_id]

app = ApplicationBuilder().token("8116827270:AAHit4ns9zNfuR-XZsxzNFBWrCxA0hKpcMs").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_answer))
app.run_polling()
