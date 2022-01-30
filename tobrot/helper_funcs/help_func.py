from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class HelpCommands:
    help_msg = """**
📖 Help

Choose section you want help in..
**
1. Basic Commands
2. Torrent & Links Leech
3. YouTube Leech
4. Telegram file Leech
5. GDrive Commands
6. Thumbnail Commands 
7. Admin Commands
8. All Commands at once

This should cover everything..
But if you want more, ask admin..!
"""

    help_msg_1 = """**
Basic commands here..
**
/status - downloading status
/stats - bot stats
/list - short search in GDrive
/completelist - full search in gdrive
/uploadvid - to upload files streamable
/uploaddoc - to upload files as a document
/cancel - to cancel process

This is it for basic ones..
"""

    help_msg_2 = """**
Commands for leeching Torrents, links and stuff..
**
/leech - leech to telegram
/gleech - leech to GDrive
/leechunzip - unarchive to telegram
/leechzip - archive to telegram
/gleechunzip - unarchive to GDrive
/gleechzip - archive to GDrive

This commands should either be reply to Torrents and links
--OR-- 
Use them in format like `/leech your_link`

To upload file with custom filename use '|' to seperate link and filename.
eg. download_link | new_filename
"""

    help_msg_3 = """**
YouTube link leeching commands..
**
/ytdl - youtube video to telegram
/gytdl - youtube video to GDrive
/pytdl - youtube playlist to telegram
/gpytdl - youtube playlist to GDrive

Note: /ytdl command can be used for any streamable video.

This commands should either be reply to YouTube links
--OR-- 
Use them in format like `/ytdl youtube_link`
"""

    help_msg_4 = """**
Telegram file leeching commands here..
**
/tleech - leech from telegram to GDrive
/tleechunzip - unarchive from telegram to GDrive
/rename - to rename telegram files
/uploadvid - to upload files streamable
/uploaddoc - to upload files as a document

Note: You can use `/tleech new_name` to rename and GDrive upload.

This commands should be as a reply to Telegram file..
"""

    help_msg_5 = """**
Google Drive related commands here..
**
/clone - to clone GDrive files or folder
/clonezip - to create zip of GDrive folder
/clonetar - to create tar of GDrive folder
/list - short search in GDrive
/completelist - full search in gdrive
/getsize - get GDrive size filled

That's all in here..
"""

    help_msg_6 = """**
Commands related to thumnails here..    
**
/savethumbnail - to save a photo as thumbnail
/clearthumbnail - to clear thumbnail

Use these commands as a reply to Telegram image..
"""

    help_msg_7 = """**
Admin commands here..
**
/rclone
/restart
/purge
/renewme
/upload
/log
/exec
/eval

This are for admins though..
"""

    help_msg_8 = """**
List of all commands..
**
/status
/stats
/list
/leech
/gleech
/clone
/clonezip
/clonetar
/leechunzip
/leechzip
/gleechunzip
/gleechzip
/ytdl
/gytdl
/pytdl
/gpytdl
/tleech
/tleechunzip
/rename
/completelist
/savethumbnail
/clearthumbnail
/uploadvid
/uploaddoc

That's all..
"""


async def help_message_f(client, message, is_cb=False):
    buttons = []
    first_row = [
        InlineKeyboardButton("1", callback_data="help_msg_1"),
        InlineKeyboardButton("2", callback_data="help_msg_2"),
        InlineKeyboardButton("3", callback_data="help_msg_3"),
        InlineKeyboardButton("4", callback_data="help_msg_4"),
    ]
    second_row = [
        InlineKeyboardButton("5", callback_data="help_msg_5"),
        InlineKeyboardButton("6", callback_data="help_msg_6"),
        InlineKeyboardButton("7", callback_data="help_msg_7"),
        InlineKeyboardButton("8", callback_data="help_msg_8"),
    ]
    buttons.append(first_row)
    buttons.append(second_row)
    buttons.append([InlineKeyboardButton("✖️Close", callback_data="close_help")])

    if is_cb:
        await message.edit_text(
            text=HelpCommands.help_msg,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    else:
        await message.reply_text(
            text=HelpCommands.help_msg,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True,
        )
