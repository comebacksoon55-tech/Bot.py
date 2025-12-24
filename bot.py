import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔴 YAHAN APNA BOT TOKEN DALO
TOKEN = "8306418938:AAEA4LRUY-FWGHIWMpktCs5pVBk5h4UnUyk"

# ⏱️ DELETE DELAY (seconds)
DELETE_DELAY = 40


def contains_bot_or_mention(message) -> bool:
    # Combine text + caption
    text = (message.text or "") + (message.caption or "")
    text_lower = text.lower()

    # 🔹 Normal text check (@ or bot)
    if "@" in text_lower or "bot" in text_lower:
        return True

    # 🔹 Entity & Hidden link check
    entities = (message.entities or []) + (message.caption_entities or [])
    for ent in entities:
        # Hidden link: [Click here](https://t.me/abc_bot)
        if ent.type == "text_link":
            if ent.url and "bot" in ent.url.lower():
                return True

        # Normal URL: https://t.me/abc_bot
        elif ent.type == "url":
            extracted = text[ent.offset: ent.offset + ent.length]
            if "bot" in extracted.lower():
                return True

    return False


async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if contains_bot_or_mention(message):
        await asyncio.sleep(DELETE_DELAY)
        try:
            await context.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            print("Deleted message:", message.message_id)
        except Exception as e:
            print("Delete failed:", e)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.ChatType.CHANNEL, channel_post_handler)
    )

    print("Bot running & watching channel...")
    app.run_polling()


if __name__ == "__main__":
    main()