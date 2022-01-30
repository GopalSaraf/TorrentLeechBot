from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tobrot import AUTH_CHANNEL


async def start_fn(client, message):
    if message.chat.type == "private":
        name = message.from_user.first_name
        msg = f"Hey {name}!\n"
        msg += "I am a leecher bot..\n"
        msg += "If you want to use me you have to join <a href='https://t.me/torrentleechgs'>TorrentLeech</a>!"
        msg += "\n\nThank You😊"
        await message.reply_text(
            msg,
            parse_mode="html",
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "TorrentLeech", url="https://t.me/torrentleechgs"
                        )
                    ]
                ]
            ),
        )
    elif message.from_user.id in AUTH_CHANNEL:
        await message.reply_text(f"Hey {message.from_user.first_name}!\nI'm alive.")
