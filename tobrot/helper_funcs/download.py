import asyncio
import os
import time
from datetime import datetime
from pathlib import Path

from tobrot import DOWNLOAD_LOCATION, LOGGER, TELEGRAM_LEECH_UNZIP_COMMAND
from tobrot.helper_funcs.create_compressed_archive import unzip_me, get_base_name
from tobrot.helper_funcs.display_progress import Progress
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive


async def down_load_media_f(client, message):
    if len(message.command) == 1:
        user_command = message.command[0]
        user_id = message.from_user.id
        LOGGER.info(user_id)
        mess_age = await message.reply_text("Processing...", quote=True)
        if not os.path.isdir(DOWNLOAD_LOCATION):
            os.makedirs(DOWNLOAD_LOCATION)
        if message.reply_to_message is not None:
            try:
                m = message.reply_to_message
                media = (
                    m.document
                    or m.video
                    or m.audio
                    or m.voice
                    or m.video_note
                    or m.animation
                )
                filename = media.file_name
            except:
                filename = ""
            start_t = datetime.now()
            download_location = str(Path().resolve()) + "/"
            c_time = time.time()
            prog = Progress(user_id, client, mess_age, filename, True)
            try:
                the_real_download_location = await client.download_media(
                    message=message.reply_to_message,
                    file_name=download_location,
                    progress=prog.progress_for_pyrogram,
                    progress_args=("", c_time),
                )
            except Exception as g_e:
                await mess_age.edit(str(g_e))
                LOGGER.error(g_e)
                return
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            LOGGER.info(the_real_download_location)
            await asyncio.sleep(10)
            if the_real_download_location:
                await mess_age.edit_text(
                    f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds"
                )
            else:
                await mess_age.edit_text("😔 Download Cancelled or some error happened")
                return
            the_real_download_location_g = the_real_download_location
            if user_command == TELEGRAM_LEECH_UNZIP_COMMAND.lower():
                try:
                    check_ifi_file = get_base_name(the_real_download_location)
                    file_up = await unzip_me(the_real_download_location)
                    if os.path.exists(check_ifi_file):
                        the_real_download_location_g = file_up
                except Exception as ge:
                    LOGGER.info(ge)
                    LOGGER.info(
                        f"Can't extract {os.path.basename(the_real_download_location)}, Uploading the same file"
                    )
            await upload_to_gdrive(
                the_real_download_location_g, mess_age, message, user_id
            )
        else:
            await mess_age.edit_text(
                "Reply to a Telegram Media, to upload to the GDrive. If you want to rename and upload then menion name after command giving space."
            )
    else:
        usr_id = message.from_user.id
        if not message.reply_to_message:
            await message.reply("😔 No downloading source provided 🙄", quote=True)
            return
        if len(message.command) > 1:
            msg_list = message.text.strip().split(" ")
            file, mess_age = await download_tg(client, message)
            if (
                msg_list[-1]
                .upper()
                .endswith(("MKV", "MP4", "WEBM", "MP3", "M4A", "FLAC", "WAV"))
            ):
                new_name = str(Path().resolve()) + "/" + " ".join(msg_list[1:])
            else:
                try:
                    file_ext = str(file).split(".")[-1]
                    new_name = (
                        str(Path().resolve())
                        + "/"
                        + " ".join(msg_list[1:])
                        + "."
                        + file_ext
                    )
                except:
                    new_name = str(Path().resolve()) + "/" + " ".join(msg_list[1:])
            try:
                if file:
                    os.rename(file, new_name)
                else:
                    return
            except Exception as g_g:
                LOGGER.error(g_g)
                await message.reply_text("g_g")
            await upload_to_gdrive(new_name, mess_age, message, usr_id)


async def download_tg(client, message):
    user_id = message.from_user.id
    LOGGER.info(user_id)
    mess_age = await message.reply_text("**Downloading...**", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        try:
            m = message.reply_to_message
            media = (
                m.document
                or m.video
                or m.audio
                or m.voice
                or m.video_note
                or m.animation
            )
            filename = media.file_name
        except:
            filename = ""
        start_t = datetime.now()
        download_location = str(Path("./").resolve()) + "/"
        c_time = time.time()
        prog = Progress(user_id, client, mess_age, filename, True)
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=prog.progress_for_pyrogram,
                progress_args=("", c_time),
            )
        except Exception as g_e:
            await mess_age.edit(str(g_e))
            LOGGER.error(g_e)
            return
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(5)
        if the_real_download_location:
            await mess_age.edit_text(
                f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds"
            )
        else:
            await mess_age.edit_text("😔 Download Cancelled or some error happened")
            return
    return the_real_download_location, mess_age
