
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8306418938:AAEA4LRUY-FWGHIWMpktCs5pVBk5h4UnUyk"
DELETE_DELAY = 40


def contains_bot_or_mention(message) -> bool:
    # 1️⃣ Text + Caption
    text = (message.text or "") + (message.caption or "")
    text_lower = text.lower()

    if "@" in text_lower or "bot" in text_lower:
        return True

    # 2️⃣ Entities (hidden / normal links)
    entities = (message.entities or []) + (message.caption_entities or [])
    for ent in entities:
        if ent.type == "text_link":
            if ent.url and "bot" in ent.url.lower():
                return True
        elif ent.type == "url":
            extracted = text[ent.offset: ent.offset + ent.length]
            if "bot" in extracted.lower():
                return True

    # 3️⃣ INLINE BUTTONS (MAIN FIX 🔥)
    if message.reply_markup and message.reply_markup.inline_keyboard:
        for row in message.reply_markup.inline_keyboard:
            for button in row:
                if button.url and "bot" in button.url.lower():
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
            print("Deleted FULL post:", message.message_id)
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
