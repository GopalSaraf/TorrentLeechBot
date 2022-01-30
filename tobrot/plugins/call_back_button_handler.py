import os
import shutil

from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from tobrot import AUTH_CHANNEL, LOGGER, gDict
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.help_func import HelpCommands, help_message_f
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.plugins.choose_rclone_config import rclone_button_callback


async def button(bot, update: CallbackQuery):
    cb_data = update.data

    try:
        g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
    except Exception as ee:
        LOGGER.info(ee)

    if cb_data.startswith("gUPcancel"):
        cmf = cb_data.split("/")
        chat_id, mes_id, from_usr = cmf[1], cmf[2], cmf[3]
        if (int(update.from_user.id) == int(from_usr)) or g:
            await bot.answer_callback_query(
                update.id, text="trying to cancel...", show_alert=False
            )
            gDict[int(chat_id)].append(int(mes_id))
        else:
            await bot.answer_callback_query(
                callback_query_id=update.id,
                text="who are you? 🤪🤔🤔🤔",
                show_alert=True,
                cache_time=0,
            )
        return

    if "|" in cb_data:
        await bot.answer_callback_query(
            update.id, text="trying to download...", show_alert=False
        )
        await youtube_dl_call_back(bot, update)
        return

    if cb_data.startswith("rclone"):
        await bot.answer_callback_query(
            update.id, text="choose rclone config...", show_alert=False
        )
        await rclone_button_callback(bot, update)
        return

    if cb_data.startswith("cancel"):
        if (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
            await bot.answer_callback_query(
                update.id, text="trying to cancel...", show_alert=False
            )
            if len(cb_data) > 1:
                i_m_s_e_g = await update.message.reply_to_message.reply_text(
                    "checking..?", quote=True
                )
                aria_i_p = await aria_start()
                g_id = cb_data.split()[-1]
                LOGGER.info(g_id)
                try:
                    downloads = aria_i_p.get_download(g_id)
                    file_name = downloads.name
                    LOGGER.info(
                        aria_i_p.remove(
                            downloads=[downloads], force=True, files=True, clean=True
                        )
                    )
                    if os.path.exists(file_name):
                        if os.path.isdir(file_name):
                            shutil.rmtree(file_name)
                        else:
                            os.remove(file_name)
                    await i_m_s_e_g.edit_text(
                        f"Leech Cancelled by <a href='tg://user?id={update.from_user.id}'>{update.from_user.first_name}</a>"
                    )
                except Exception as e:
                    await i_m_s_e_g.edit_text("<i>FAILED</i>\n\n" + str(e) + "\n#error")
        else:
            await bot.answer_callback_query(
                callback_query_id=update.id,
                text="who are you? 🤪🤔🤔🤔",
                show_alert=True,
                cache_time=0,
            )

    if cb_data.startswith("help_msg"):
        if "only" in cb_data:
            buttons = [[InlineKeyboardButton("✖️Close", callback_data="close_help")]]
        else:
            buttons = [
                [
                    InlineKeyboardButton("« Back", callback_data="original_help"),
                    InlineKeyboardButton("✖️Close", callback_data="close_help"),
                ]
            ]
        if "help_msg_1" in cb_data:
            edit_text = HelpCommands.help_msg_1
        if "help_msg_2" in cb_data:
            edit_text = HelpCommands.help_msg_2
        if "help_msg_3" in cb_data:
            edit_text = HelpCommands.help_msg_3
        if "help_msg_4" in cb_data:
            edit_text = HelpCommands.help_msg_4
        if "help_msg_5" in cb_data:
            edit_text = HelpCommands.help_msg_5
        if "help_msg_6" in cb_data:
            edit_text = HelpCommands.help_msg_6
        if "help_msg_7" in cb_data:
            edit_text = HelpCommands.help_msg_7
        if "help_msg_8" in cb_data:
            edit_text = HelpCommands.help_msg_8
        await update.message.edit_text(
            text=edit_text, reply_markup=InlineKeyboardMarkup(buttons)
        )

    if cb_data.startswith("close_help"):
        await update.message.reply_to_message.delete()
        await update.message.delete()

    if cb_data.startswith("original_help"):
        await help_message_f(bot, update.message, is_cb=True)

    elif cb_data == "fuckingdo":
        if (update.from_user.id in AUTH_CHANNEL) or g:
            await bot.answer_callback_query(
                update.id, text="trying to delete...", show_alert=False
            )
            g_d_list = [
                "app.json",
                "venv",
                "rclone.conf",
                "rclone_bak.conf",
                ".gitignore",
                "_config.yml",
                "Dockerfile",
                "extract",
                "Procfile",
                ".heroku",
                ".profile.d",
                "rclone.jpg",
                "README.md",
                "requirements.txt",
                "runtime.txt",
                "start.sh",
                "tobrot",
                "gautam",
                "Torrentleech.txt",
                "vendor",
                "LeechBot.session",
                "LeechBot.session-journal",
                "config.env",
                "sample_config.env",
            ]
            g_list = os.listdir()
            LOGGER.info(g_list)
            g_del_list = list(set(g_list) - set(g_d_list))
            LOGGER.info(g_del_list)
            if len(g_del_list) != 0:
                for f in g_del_list:
                    if os.path.isfile(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
                await update.message.edit_text(f"Deleted {len(g_del_list)} objects 😬")
            else:
                await update.message.edit_text("Nothing to clear 🙄")
        else:
            await update.message.edit_text("You are not allowed to do that 🤭")

    elif cb_data == "fuckoff":
        await bot.answer_callback_query(
            update.id, text="trying to cancel...", show_alert=False
        )
        await update.message.edit_text("Okay! fine 🤬")
