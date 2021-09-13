import asyncio
import json
import os
import re
import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asyncstdlib.functools import lru_cache, cached_property
from tobrot import RCLONE_CONFIG, LOGGER, DESTINATION_FOLDER, INDEX_LINK, telegraph_token
from tobrot.helper_funcs.display_progress import humanbytes
from telegraph import Telegraph

TELEGRAPHLIMIT = 50

# class listHelper():
#     def __init__(self, message):
#         self.message = message
#         self.to_srch = ''
#         self.msg_list = []
#         self.buttons = []
#
#     def to_search(self):
#         message = self.message
#         to_srch = message.text.split(' ', maxsplit=1)[1]
#         self.to_srch = to_srch
#         return to_srch
#
#     @lru_cache
#     async def list_fn(self, to_srch):
#         if not os.path.exists("rclone.conf"):
#             with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
#                 fole.write(f"{RCLONE_CONFIG}")
#         if os.path.exists("rclone.conf"):
#             with open("rclone.conf", "r+") as file:
#                 con = file.read()
#                 gUP = re.findall("\[(.*)\]", con)[0]
#                 LOGGER.info(gUP)
#         destination = f"{DESTINATION_FOLDER}"
#         command = [
#             "rclone",
#             "lsjson",
#             "--config=./rclone.conf",
#             "-R",
#             "--no-modtime",
#             "--no-mimetype",
#             f"{gUP}:{destination}",
#         ]
#         LOGGER.info(command)
#         gau_tam = await asyncio.create_subprocess_exec(
#             *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
#         )
#         gau, tam = await gau_tam.communicate()
#         json_str = gau.decode("utf-8")
#         json_list = json.loads(json_str)
#         json_srch_list = []
#         msg = ''
#         for item in json_list:
#             if to_srch.lower() in item['Name'].lower():
#                 json_srch_list.append(item)
#         for count, item in enumerate(json_srch_list):
#             if count % maxcount == 0:
#                 msg += "\n\n\n\n\n"
#             if item['IsDir']:
#                 msg += f"\n**{count + 1}.** "
#                 msg += f"**{item['Name']}** (Folder)\n"
#                 gdrive_link = f"https://drive.google.com/folderview?id={item['ID']}"
#                 index = f"{INDEX_LINK}/{item['Path']}/"
#                 index_link = requests.utils.requote_uri(index)
#                 msg += f"[Drive Link]({gdrive_link}) | <a href='{index_link}'>Index Link</a>\n"
#             else:
#                 msg += f"\n**{count + 1}.** "
#                 size = humanbytes(item['Size'])
#                 msg += f"**{item['Name']}** ({size})\n"
#                 gdrive_link = f"https://drive.google.com/file/d/{item['ID']}/view?usp=drivesdk"
#                 index = f"{INDEX_LINK}/{item['Path']}"
#                 index_link = requests.utils.requote_uri(index)
#                 msg += f"[Drive Link]({gdrive_link}) | <a href='{index_link}'>Index Link</a>\n"
#
#         msg_list = msg.strip().split('\n\n\n\n\n')
#         self.msg_list = msg_list
#         buttons = []
#         for i in range(len(msg_list)):
#             button = InlineKeyboardButton(f'{i + 1}', callback_data=f"page_no_:{i + 1}")
#             buttons.append(button)
#         self.buttons = buttons
#         return msg_list
#
#     async def one_page_msg_fn(self):
#         message = self.message
#         msg_list = self.msg_list
#         to_srch = self.to_srch
#         if msg_list[0] == '':
#             await message.reply(f"No Results found for {to_srch}.")
#         else:
#             await message.reply(msg_list[0], disable_web_page_preview=True, quote=True)
#
#     async def more_page_msg_fn(self):
#         message = self.message
#         msg_list = self.msg_list
#         buttons = self.buttons
#         await message.reply(msg_list[0], disable_web_page_preview=True, quote=True,
#                             reply_markup=InlineKeyboardMarkup([buttons]))
#
#     async def edit_page(self, page_no, to_edit):
#         msg_list = self.msg_list
#         buttons = self.buttons
#         await to_edit.edit(text=msg_list[page_no - 1], reply_markup=InlineKeyboardMarkup([buttons]),
#                            disable_web_page_preview=True)

class listHelper():
    def __init__(self, message):
        self.telegraph_content = []
        self.path = []
        self.message = message
        self.to_srch = ''
        self.msg_list = []
        self.button = []

    def edit_telegraph(self):
        nxt_page = 1
        prev_page = 0
        for content in self.telegraph_content:
            if nxt_page == 1:
                content += f'<b><a href="https://telegra.ph/{self.path[nxt_page]}">Next</a></b>'
                nxt_page += 1
            else:
                if prev_page <= self.num_of_path:
                    content += f'<b><a href="https://telegra.ph/{self.path[prev_page]}">Prev</a></b>'
                    prev_page += 1
                if nxt_page < self.num_of_path:
                    content += f'<b> | <a href="https://telegra.ph/{self.path[nxt_page]}">Next</a></b>'
                    nxt_page += 1
            Telegraph(access_token=telegraph_token).edit_page(path=self.path[prev_page],
                                                              title='TorrentLeech Search',
                                                              author_name='TorrentLeech',
                                                              html_content=content)
        return

    async def drive_list(self, to_srch):
        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                gUP = re.findall("\[(.*)\]", con)[0]
        LOGGER.info(gUP)
        destination = f"{DESTINATION_FOLDER}"
        command = [
            "rclone",
            "lsjson",
            "--config=./rclone.conf",
            "-R",
            "--no-modtime",
            "--no-mimetype",
            f"{gUP}:{destination}",
        ]
        LOGGER.info(command)
        gau_tam = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        gau, tam = await gau_tam.communicate()
        json_str = gau.decode("utf-8")
        json_list = json.loads(json_str)
        json_srch_list = []
        msg = f'<h4>Search Result For <b>{to_srch} :</b></h4><br>'
        content_count = 0
        all_contents_count = 0
        for item in json_list:
            if to_srch.lower() in item['Name'].lower():
                json_srch_list.append(item)
        for count, item in enumerate(json_srch_list):
            msg += f"<code><b>{count + 1}.</b> "
            msg += f"<b>{item['Name']}</b><br>"
            if item['IsDir']:
                msg += '📁 Folder<br></code>'
                gdrive_link = f"https://drive.google.com/folderview?id={item['ID']}"
                index = f"{INDEX_LINK}/{item['Path']}/"
                index_link = requests.utils.requote_uri(index)
            else:
                size = humanbytes(item['Size'])
                msg += f"📄 {size}<br></code>"
                gdrive_link = f"https://drive.google.com/file/d/{item['ID']}/view?usp=drivesdk"
                index = f"{INDEX_LINK}/{item['Path']}"
                index_link = requests.utils.requote_uri(index)
            msg += f"<b><a href='{gdrive_link}'>Drive Link</a> | <a href='{index_link}'>Index Link</a></b><br><br>"
            content_count += 1
            all_contents_count += 1

            if content_count == TELEGRAPHLIMIT:
                self.telegraph_content.append(msg)
                msg = ""
                content_count = 0

        if msg != '':
            self.telegraph_content.append(msg)

        if len(self.telegraph_content) == 0:
            return "", None

        for content in self.telegraph_content:
            self.path.append(Telegraph(access_token=telegraph_token).create_page(
                title='TorrentLeech Search',
                author_name='TorrentLeech',
                html_content=content
            )['path'])

        self.num_of_path = len(self.path)
        if self.num_of_path > 1:
            self.edit_telegraph()

        msg = f"<b>Found <code>{all_contents_count}</code> results for <code>{to_srch}</code></b>."
        button = [[InlineKeyboardButton("🔎 VIEW", url=f"https://telegra.ph/{self.path[0]}")]]

        return msg, InlineKeyboardMarkup(button)
