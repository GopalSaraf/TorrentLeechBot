import asyncio
import math
import os
import shutil
import time
from pathlib import Path
from subprocess import PIPE, Popen

import pyrogram.types as pyrogram
import requests
from bs4 import BeautifulSoup

from tobrot import (
    DESTINATION_FOLDER,
    EDIT_SLEEP_TIME_OUT,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
)

import re
import urllib.parse as urlparse
from urllib.parse import parse_qs

from tobrot.helper_funcs.create_compressed_archive import (
    create_zip,
    create_tar,
    create_archive,
)
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive


def getIdFromUrl(link: str):
    if "folders" in link or "file" in link:
        regex = r"https://drive\.google\.com/(drive)?/?u?/?\d?/?(mobile)?/?(file)?(folders)?/?d?/([-\w]+)[?+]?/?(w+)?"
        res = re.search(regex, link)
        if res is None:
            raise IndexError("GDrive ID not found.")
        return res.group(5)
    parsed = urlparse.urlparse(link)
    return parse_qs(parsed.query)["id"][0]


class CloneHelper:
    def __init__(self, mess):
        self.g_id = ""
        self.mess = mess
        self.name = ""
        self.title = ""
        self.out = b""
        self.err = b""
        self.lsg = ""
        self.filee = ""
        self.u_id = self.mess.from_user.id
        self.dname = ""
        self.link = ""
        self.is_link_public = True

    def config(self):
        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                self.dname = re.findall("\[(.*)\]", con)[0]

    def get_id(self):
        mes = self.mess
        rep_msg = mes.reply_to_message
        if rep_msg:
            txt = rep_msg.text
        else:
            txt = " ".join(mes.text.split(" ")[1:])
        LOGGER.info(txt)
        mess = txt.split(" ", maxsplit=1)
        self.link = mess[0]
        if len(mess) == 2:
            if "//" in mess[0]:
                self.g_id = getIdFromUrl(mess[0])
            else:
                self.g_id = mess[0]
            LOGGER.info(self.g_id)
            self.name = mess[1]
            self.title = mess[1]
            LOGGER.info(self.name)
        else:
            if "//" in mess[0]:
                self.g_id = getIdFromUrl(mess[0])
            else:
                self.g_id = mess[0]
            LOGGER.info(self.g_id)
            self.name = ""
        return self.g_id, self.name

    def set_name(self):
        if self.name != "":
            pass
        else:
            drive_link = self.link
            try:
                if "export=download" in drive_link:
                    drive_link = "https://drive.google.com/open?id=" + self.g_id
                html_text = requests.get(drive_link).text
                soup = BeautifulSoup(html_text, "lxml")
                title = soup.find("title").text
                if title == "Meet Google Drive – One place for all your files":
                    self.is_link_public = False
                    LOGGER.info(f"Publicly Unavailable {drive_link}")
                else:
                    self.title = title[:-15]
                    if not self.title.upper().endswith(
                        (
                            "MKV",
                            "MP4",
                            "WEBM",
                            "MP3",
                            "M4A",
                            "FLAC",
                            "WAV",
                            "ZIP",
                            "TAR",
                            "RAR",
                        )
                    ):
                        self.name = self.title
            except:
                pass

    async def gcl(self):
        if self.is_link_public:
            self.lsg = await self.mess.reply_text(f"Cloning...you should wait 🤒")
            destination = f"{DESTINATION_FOLDER}"
            idd = "{" f"{self.g_id}" "}"
            cmd = [
                "/app/gopal/gclone",
                "copy",
                "--config=rclone.conf",
                f"{self.dname}:{idd}",
                f"{self.dname}:{destination}/{self.name}",
                "-v",
                "--drive-server-side-across-configs",
                "--transfers=16",
                "--checkers=20",
            ]
            LOGGER.info(cmd)
            pro = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            p, e = await pro.communicate()
            self.out = p
            LOGGER.info(self.out)
            err = e.decode()
            LOGGER.info(err)
            LOGGER.info(self.out.decode())

            if self.name == "":
                reg_f = "INFO(.*)(:)(.*)(:) (Copied)"
                file_n = re.findall(reg_f, err)
                LOGGER.info(file_n[0][2].strip())
                self.name = file_n[0][2].strip()
                self.filee = self.name
        else:
            await self.mess.reply_text("Link provided is not publicly available!")

    async def link_gen_size(self):
        if self.is_link_public:
            if self.name is not None:
                _drive = ""
                if self.name == self.filee:
                    _flag = "--files-only"
                    _up = "File"
                    _ui = ""
                else:
                    _flag = "--dirs-only"
                    _up = "Folder"
                    _drive = "folderba"
                    _ui = "/"
                g_name = re.escape(self.name)
                LOGGER.info(g_name)
                destination = f"{DESTINATION_FOLDER}"

                with open("filter1.txt", "w+", encoding="utf-8") as filter1:
                    print(f"+ {g_name}{_ui}\n- *", file=filter1)

                g_a_u = [
                    "rclone",
                    "lsf",
                    "--config=./rclone.conf",
                    "-F",
                    "i",
                    "--filter-from=./filter1.txt",
                    f"{_flag}",
                    f"{self.dname}:{destination}",
                ]
                LOGGER.info(g_a_u)
                gau_tam = await asyncio.create_subprocess_exec(
                    *g_a_u,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                gau, tam = await gau_tam.communicate()
                LOGGER.info(gau)
                gautam = gau.decode("utf-8")
                LOGGER.info(gautam)
                LOGGER.info(tam.decode("utf-8"))

                if _drive == "folderba":
                    gautii = f"https://drive.google.com/folderview?id={gautam}"
                else:
                    gautii = (
                        f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
                    )

                LOGGER.info(gautii)
                gau_link = re.search("(?P<url>https?://[^\s]+)", gautii).group("url")
                LOGGER.info(gau_link)
                button = []
                button.append(
                    pyrogram.InlineKeyboardButton(
                        text="☁ GDrive Link", url=f"{gau_link}"
                    )
                )

                index_link = INDEX_LINK

                if _flag == "--files-only":
                    indexurl = f"{index_link}/{self.name}"
                else:
                    indexurl = f"{index_link}/{self.name}/"
                tam_link = requests.utils.requote_uri(indexurl)
                LOGGER.info(tam_link)
                button.append(
                    pyrogram.InlineKeyboardButton(
                        text="⚡ Index Link", url=f"{tam_link}"
                    )
                )
                button_markup = pyrogram.InlineKeyboardMarkup([button])
                msg = await self.lsg.edit_text(
                    f"{_up} Cloned successfully in GDrive <a href='tg://user?id={self.u_id}'>😊</a>\
                    \n<b>{self.title}</b>\nTotal objects: Calculating...\nTotal size: Calculating...",
                    reply_markup=button_markup,
                    parse_mode="html",
                )
                g_cmd = [
                    "rclone",
                    "size",
                    "--config=rclone.conf",
                    f"{self.dname}:{destination}/{self.name}",
                ]
                LOGGER.info(g_cmd)
                gaut_am = await asyncio.create_subprocess_exec(
                    *g_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                gaut, am = await gaut_am.communicate()
                g_autam = gaut.decode("utf-8")
                LOGGER.info(g_autam)
                LOGGER.info(am.decode("utf-8"))
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                await msg.edit_text(
                    f"{_up} Cloned successfully in GDrive <a href='tg://user?id={self.u_id}'>😊</a>\
                    \n<b>{self.title}</b>\n{g_autam}",
                    reply_markup=button_markup,
                    parse_mode="html",
                )
        else:
            pass


class TarFolder:
    def __init__(self, mess):
        self.g_id = ""
        self.mess = mess
        self.name = ""
        self.download_location = ""
        self.zipped_file = ""
        self.lsg = ""
        self.u_id = self.mess.from_user.id
        self.dname = ""
        self.link = ""
        self.is_link_public = True

    def config(self):
        if not os.path.exists("rclone_bak.conf"):
            with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fiile:
                fiile.write(f"{RCLONE_CONFIG}")

        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                self.dname = re.findall("\[(.*)\]", con)[0]

    def get_id(self):
        mes = self.mess
        rep_msg = mes.reply_to_message
        if rep_msg:
            txt = rep_msg.text
        else:
            txt = " ".join(mes.text.split(" ")[1:])
        LOGGER.info(txt)
        mess = txt.split(" ", maxsplit=1)
        self.link = mess[0]
        if len(mess) == 2:
            if "//" in mess[0]:
                self.g_id = getIdFromUrl(mess[0])
            else:
                self.g_id = mess[0]
            LOGGER.info(self.g_id)
            self.name = mess[1]
            LOGGER.info(self.name)
        else:
            if "//" in mess[0]:
                self.g_id = getIdFromUrl(mess[0])
            else:
                self.g_id = mess[0]
            LOGGER.info(self.g_id)
            self.name = ""
        return self.g_id, self.name

    def set_name(self):
        if self.name != "":
            pass
        else:
            drive_link = self.link
            try:
                html_text = requests.get(drive_link).text
                soup = BeautifulSoup(html_text, "lxml")
                title = soup.find("title").text
                if title == "Meet Google Drive – One place for all your files":
                    self.is_link_public = False
                    LOGGER.info(f"Publicly Unavailable {drive_link}")
                else:
                    self.name = title[:-15]
                    LOGGER.info(f"Title: {self.name}")
            except:
                pass

    async def download(self):
        if self.is_link_public:
            self.lsg = await self.mess.reply_text(f"Processing...")
            start = time.time()
            download_location = f"/app/{self.name}"
            self.download_location = download_location
            cmd = f"""rclone copy {self.dname}: --drive-root-folder-id {self.g_id} "{download_location}" --config=rclone_bak.conf --drive-acknowledge-abuse -P"""
            LOGGER.info(cmd)
            with Popen(
                cmd, stdout=PIPE, bufsize=1, universal_newlines=True, shell=True
            ) as p:
                prog = ""
                for b in p.stdout:
                    now = time.time()
                    diff = now - start
                    if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0:
                        txt = re.findall("Transferred(.*?)\n", b)[0].strip()
                        if txt:
                            try:
                                current = re.search(":(.*?)/", txt).group(1).strip()
                                total = re.search("/(.*?)iB,", txt).group(1).strip()
                                percent = re.search(",(.*?)%", txt).group(1).strip()
                                if percent == "-":
                                    percent = 0
                                finished_str = "".join(
                                    [
                                        FINISHED_PROGRESS_STR
                                        for i in range(math.floor(int(percent) / 4))
                                    ]
                                )
                                unfinished_str = "".join(
                                    [
                                        UN_FINISHED_PROGRESS_STR
                                        for i in range(
                                            25 - math.floor(int(percent) / 4)
                                        )
                                    ]
                                )
                                speed = re.search("%,(.*?)iB/s", txt).group(1)
                                eta = re.findall("ETA .*", txt)[0].split(" ")[1]
                            except:
                                pass
                            await self.lsg.edit_text(
                                "**Downloading:** {}\n**[{}{}]** **{}%**\n{} **of** {}iB\n**Speed:** {}iB"
                                "/sec\n**ETA:** {}".format(
                                    os.path.basename(self.name),
                                    finished_str,
                                    unfinished_str,
                                    int(percent),
                                    current,
                                    total,
                                    speed,
                                    eta,
                                )
                            )

        else:
            await self.mess.reply_text("Link provided is not publicly available!")

    async def create_compressed(self, is_zip, is_tar):
        if self.is_link_public:
            await self.lsg.edit_text(
                f"Successfully Downloaded {self.name}..\nCreating archive now.."
            )
            if is_zip:
                try:
                    zipped_file = await create_zip(self.download_location)
                except:
                    zipped_file = shutil.make_archive(
                        self.name, "zip", self.download_location
                    )
                    shutil.rmtree(self.download_location)
            elif is_tar:
                try:
                    zipped_file = await create_tar(self.download_location)
                except:
                    zipped_file = await create_archive(self.download_location)
            LOGGER.info(zipped_file)
            self.zipped_file = zipped_file
            await self.lsg.edit_text(
                f"Successfully Downloaded and archived {self.name}..\nUploading now.."
            )

    async def upload(self):
        await upload_to_gdrive(self.zipped_file, self.lsg, self.mess, self.u_id)
