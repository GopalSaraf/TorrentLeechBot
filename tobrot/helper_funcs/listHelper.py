import json
import os
import re
from subprocess import Popen, PIPE

import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tobrot import RCLONE_CONFIG, LOGGER, DESTINATION_FOLDER, INDEX_LINK
from tobrot.helper_funcs.display_progress import humanbytes

maxcount = 20


class listHelper():
    def __init__(self, message):
        self.message = message
        self.to_srch = ''
        self.msg_list = []
        self.buttons = []

    async def list_fn(self):
        message = self.message
        to_srch = message.text.split(' ', maxsplit=1)[1]
        self.to_srch = to_srch
        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                gUP = re.findall("\[(.*)\]", con)[0]
                LOGGER.info(gUP)
        destination = f"{DESTINATION_FOLDER}"
        command = f"rclone lsjson --config=./rclone.conf {gUP}:{destination} -R"
        pro = Popen(command, stdout=PIPE, shell=True)
        json_str = pro.stdout.read().decode('utf-8')
        json_list = json.loads(json_str)
        json_srch_list = []
        msg = ''
        for item in json_list:
            if to_srch.lower() in item['Name'].lower():
                json_srch_list.append(item)
        for count, item in enumerate(json_srch_list):
            if count % maxcount == 0:
                msg += "\n\n\n\n\n"
            if item['IsDir']:
                msg += f"\n**{count + 1}.** "
                msg += f"**{item['Name']}** (Folder)\n"
                gdrive_link = f"https://drive.google.com/folderview?id={item['ID']}"
                index = f"{INDEX_LINK}/{item['Path']}/"
                index_link = requests.utils.requote_uri(index)
                msg += f"[Drive Link]({gdrive_link}) | <a href='{index_link}'>Index Link</a>\n"
            else:
                msg += f"\n**{count + 1}.** "
                size = humanbytes(item['Size'])
                msg += f"**{item['Name']}** ({size})\n"
                gdrive_link = f"https://drive.google.com/file/d/{item['ID']}/view?usp=drivesdk"
                index = f"{INDEX_LINK}/{item['Path']}"
                index_link = requests.utils.requote_uri(index)
                msg += f"[Drive Link]({gdrive_link}) | <a href='{index_link}'>Index Link</a>\n"

        msg_list = msg.strip().split('\n\n\n\n\n')
        self.msg_list = msg_list
        buttons = []
        for i in range(len(msg_list)):
            button = InlineKeyboardButton(f'{i + 1}', callback_data=f"page_no_:{i + 1}")
            buttons.append(button)
        self.buttons = buttons
        return msg_list

    async def one_page_msg_fn(self):
        message = self.message
        msg_list = self.msg_list
        to_srch = self.to_srch
        if msg_list[0] == '':
            await message.reply(f"No Results found for {to_srch}.")
        else:
            await message.reply(msg_list[0], disable_web_page_preview=True, quote=True)

    async def more_page_msg_fn(self):
        message = self.message
        msg_list = self.msg_list
        buttons = self.buttons
        await message.reply(msg_list[0], disable_web_page_preview=True, quote=True,
                                      reply_markup=InlineKeyboardMarkup([buttons]))

    async def edit_page(self, page_no, to_edit):
        msg_list = self.msg_list
        buttons = self.buttons
        await to_edit.edit(text=msg_list[page_no - 1], reply_markup=InlineKeyboardMarkup([buttons]),
                           disable_web_page_preview=True)
