import os

from pyrogram import Client, filters
from pyrogram.handlers import CallbackQueryHandler, MessageHandler

from tobrot import (
    API_HASH,
    APP_ID,
    AUTH_CHANNEL,
    CANCEL_COMMAND_G,
    CLEAR_THUMBNAIL,
    CLONE_COMMAND_G,
    CLONE_TAR_COMMAND,
    CLONE_ZIP_COMMAND,
    COMPLETE_LIST_COMMAND,
    DOWNLOAD_LOCATION,
    GET_SIZE_G,
    GLEECH_COMMAND,
    GLEECH_UNZIP_COMMAND,
    GLEECH_ZIP_COMMAND,
    GPYTDL_COMMAND,
    GYTDL_COMMAND,
    HELP_COMMAND,
    LEECH_COMMAND,
    LEECH_UNZIP_COMMAND,
    LEECH_ZIP_COMMAND,
    LIST_COMMAND,
    LOG_COMMAND,
    PYTDL_COMMAND,
    RENAME_COMMAND,
    RENEWME_COMMAND,
    SAVE_THUMBNAIL,
    STATS_COMMAND,
    STATUS_COMMAND,
    TELEGRAM_LEECH_COMMAND,
    TELEGRAM_LEECH_UNZIP_COMMAND,
    TG_BOT_TOKEN,
    TOGGLE_DOC,
    TOGGLE_VID,
    UPLOAD_COMMAND,
    YTDL_COMMAND,
)
from tobrot.helper_funcs.download import down_load_media_f
from tobrot.helper_funcs.help_func import help_message_f
from tobrot.plugins.call_back_button_handler import button

# the logging things
from tobrot.plugins.choose_rclone_config import rclone_command_f
from tobrot.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tobrot.plugins.incoming_message_fn import (
    g_clonee,
    g_yt_playlist,
    gclone_zip,
    incoming_message_f,
    incoming_purge_message_f,
    incoming_youtube_dl_f,
    rename_tg_file,
)
from tobrot.plugins.new_join_fn import start_fn
from tobrot.plugins.rclone_size import check_size_g, g_clearme
from tobrot.plugins.status_message_fn import (
    cancel_message_f,
    eval_message_f,
    exec_message_f,
    full_list_fn,
    list_fn,
    stats_message_fn,
    status_message_f,
    upload_as_doc,
    upload_as_video,
    upload_document_f,
    upload_log_file,
)

if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    app = Client(
        "LeechBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=343,
    )
    #
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(
            [
                LEECH_COMMAND,
                LEECH_UNZIP_COMMAND,
                LEECH_ZIP_COMMAND,
                GLEECH_COMMAND,
                GLEECH_UNZIP_COMMAND,
                GLEECH_ZIP_COMMAND,
            ]
        )
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_message_handler)
    #
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=filters.command([TELEGRAM_LEECH_COMMAND, TELEGRAM_LEECH_UNZIP_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_telegram_download_handler)
    #
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=filters.command(["purge"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_purge_message_handler)
    #
    incoming_clone_handler = MessageHandler(
        g_clonee,
        filters=filters.command([CLONE_COMMAND_G]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_clone_handler)
    #
    incoming_clonezip_handler = MessageHandler(
        gclone_zip,
        filters=filters.command([CLONE_ZIP_COMMAND, CLONE_TAR_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_clonezip_handler)
    #
    incoming_size_checker_handler = MessageHandler(
        check_size_g,
        filters=filters.command([GET_SIZE_G]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_size_checker_handler)
    #
    incoming_g_clear_handler = MessageHandler(
        g_clearme,
        filters=filters.command([RENEWME_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_g_clear_handler)
    #
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command([YTDL_COMMAND, GYTDL_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_dl_handler)
    #
    incoming_youtube_playlist_dl_handler = MessageHandler(
        g_yt_playlist,
        filters=filters.command([PYTDL_COMMAND, GPYTDL_COMMAND])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_playlist_dl_handler)
    #
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command([STATUS_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(status_message_handler)
    #
    stats_message_handler = MessageHandler(
        stats_message_fn,
        filters=filters.command([STATS_COMMAND, "stats"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(stats_message_handler)
    #
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.command([CANCEL_COMMAND_G]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(cancel_message_handler)
    #
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command(["exec"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(exec_message_handler)
    #
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=filters.command(["eval"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(eval_message_handler)
    #
    rename_message_handler = MessageHandler(
        rename_tg_file,
        filters=filters.command([RENAME_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(rename_message_handler)
    #
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=filters.command([UPLOAD_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_document_handler)
    #
    upload_log_handler = MessageHandler(
        upload_log_file,
        filters=filters.command([LOG_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_log_handler)
    #
    start_cmd_handler = MessageHandler(start_fn, filters=filters.command(["start"]))
    app.add_handler(start_cmd_handler)
    #
    call_back_button_handler = CallbackQueryHandler(button)
    app.add_handler(call_back_button_handler)
    #
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command([f"{SAVE_THUMBNAIL}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(save_thumb_nail_handler)
    #
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command([f"{CLEAR_THUMBNAIL}"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(clear_thumb_nail_handler)
    #
    rclone_config_handler = MessageHandler(
        rclone_command_f, filters=filters.command(["rclone"])
    )
    app.add_handler(rclone_config_handler)
    #
    upload_as_doc_handler = MessageHandler(
        upload_as_doc,
        filters=filters.command([f"{TOGGLE_DOC}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_doc_handler)
    #
    upload_as_video_handler = MessageHandler(
        upload_as_video,
        filters=filters.command([f"{TOGGLE_VID}"]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_as_video_handler)
    #
    help_message_handler = MessageHandler(
        help_message_f,
        filters=filters.command([HELP_COMMAND]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(help_message_handler)
    #
    list_message_handler = MessageHandler(
        list_fn,
        filters=filters.command([LIST_COMMAND, "list", "search"])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(list_message_handler)
    #
    full_list_message_handler = MessageHandler(
        full_list_fn,
        filters=filters.command(
            [COMPLETE_LIST_COMMAND, "fulllist", "fullsearch", "completelist"]
        )
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(full_list_message_handler)
    #
    app.run()
