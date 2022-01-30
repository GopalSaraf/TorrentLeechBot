# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Helper Module containing various sites direct links generators. This module is copied and modified as per need
from https://github.com/AvinashReddy3108/PaperplaneExtended . I hereby take no credit of the following code other
than the modifications. See https://github.com/AvinashReddy3108/PaperplaneExtended/commits/master/userbot/modules/direct_links.py
for original authorship. """

import re
import urllib.parse
from random import choice
from js2py import EvalJs
import requests
from bs4 import BeautifulSoup

from tobrot.helper_funcs.exceptions import DirectDownloadLinkException


def direct_link_generator(text_url: str):
    """direct links generator"""
    if not text_url:
        raise DirectDownloadLinkException("`No links found!`")
    elif "zippyshare.com" in text_url:
        return zippy_share(text_url)
    elif "yadi.sk" in text_url:
        return yandex_disk(text_url)
    # elif 'cloud.mail.ru' in text_url:
    # return cm_ru(text_url)
    elif "mediafire.com" in text_url:
        return mediafire(text_url)
    elif "osdn.net" in text_url:
        return osdn(text_url)
    # elif 'github.com' in text_url:
    # return github(text_url)
    elif "racaty.net" in text_url:
        return racaty(text_url)
    else:
        raise DirectDownloadLinkException(
            f"No Direct link function found for {text_url}"
        )


def zippy_share(url: str) -> str:
    link = re.findall("https:/.(.*?).zippyshare", url)[0]
    response_content = (requests.get(url)).content
    bs_obj = BeautifulSoup(response_content, "lxml")

    try:
        js_script = bs_obj.find("div", {"class": "center",}).find_all(
            "script"
        )[1]
    except:
        js_script = bs_obj.find("div", {"class": "right",}).find_all(
            "script"
        )[0]

    js_content = re.findall(r'\.href.=."/(.*?)";', str(js_script))
    js_content = 'var x = "/' + js_content[0] + '"'

    evaljs = EvalJs()
    setattr(evaljs, "x", None)
    evaljs.execute(js_content)
    js_content = getattr(evaljs, "x")

    return f"https://{link}.zippyshare.com{js_content}"


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    try:
        text_url = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        dl_url = requests.get(api.format(text_url)).json()["href"]
        return dl_url
    except KeyError:
        raise DirectDownloadLinkException(
            "`Error: File not found / Download limit reached`\n"
        )


def mediafire(url: str) -> str:
    """MediaFire direct links generator"""
    try:
        text_url = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No MediaFire links found`\n")
    page = BeautifulSoup(requests.get(text_url).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    return dl_url


def osdn(url: str) -> str:
    """OSDN direct links generator"""
    osdn_link = "https://osdn.net"
    try:
        text_url = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No OSDN links found`\n")
    page = BeautifulSoup(requests.get(text_url, allow_redirects=True).content, "lxml")
    info = page.find("a", {"class": "mirror_link"})
    text_url = urllib.parse.unquote(osdn_link + info["href"])
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    urls = []
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        urls.append(re.sub(r"m=(.*)&f", f"m={mirror}&f", text_url))
    return urls[0]


def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


def racaty(url: str) -> str:
    dl_url = ""
    try:
        text_url = re.findall(r"\bhttps?://.*racaty\.net\S+", url)[0]
    except IndexError:
        raise DirectDownloadLinkException("`No Racaty links found`\n")
    reqs = requests.get(text_url)
    bss = BeautifulSoup(reqs.text, "html.parser")
    op = bss.find("input", {"name": "op"})["value"]
    id = bss.find("input", {"name": "id"})["value"]
    rep = requests.post(text_url, data={"op": op, "id": id})
    bss2 = BeautifulSoup(rep.text, "html.parser")
    dl_url = bss2.find("a", {"id": "uniqueExpirylink"})["href"]
    return dl_url
