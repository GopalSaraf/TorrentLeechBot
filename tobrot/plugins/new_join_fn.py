from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            f"""<b>Hello there!\nWelcome to our group!</b>\n\nFor further information, press /help""",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Channel', url='https://t.me/torrentgs')
                    ]
                ]
               )
            )
    await message.delete(revoke=True)

