import logging
import os
import random
import string
import time
import datetime
from logging.handlers import RotatingFileHandler
from collections import defaultdict
from sys import exit
from telegraph import Telegraph
import dotenv

if os.path.exists("TorrentLeech.txt"):
    with open("TorrentLeech.txt", "r+") as f_d:
        f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("TorrentLeech.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

user_specific_config = dict()

dotenv.load_dotenv("config.env")

# checking compulsory variable
for imp in ["TG_BOT_TOKEN", "APP_ID", "API_HASH", "OWNER_ID", "AUTH_CHANNEL"]:
    try:
        value = os.environ[imp]
        if not value:
            raise KeyError
    except KeyError:
        LOGGER.critical(f"Oh...{imp} is missing from config.env ... fill that")
        exit()

# The Telegram API things
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

# Get these values from my.telegram.org
# to store the channel ID who are authorized to use the bot
AUTH_CHANNEL = [int(x) for x in os.environ.get("AUTH_CHANNEL", "").split()]

# the download location, where the HTTP Server runs
DOWNLOAD_LOCATION = "./DOWNLOADS"
# Telegram maximum file upload size
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
FREE_USER_MAX_FILE_SIZE = 50000000

AUTH_CHANNEL.append(OWNER_ID)
# chunk size that should be used with requests
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "128"))
# default thumbnail to be used in the videos
DEF_THUMB_NAIL_VID_S = os.environ.get(
    "DEF_THUMB_NAIL_VID_S",
    "https://images.unsplash.com/photo-1562907550-096d3bf9b25c?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=735&q=80",
)
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096
# set timeout for subprocess
PROCESS_MAX_TIMEOUT = 3600
#
SP_LIT_ALGO_RITH_M = os.environ.get("SP_LIT_ALGO_RITH_M", "hjs")
ARIA_TWO_STARTED_PORT = int(os.environ.get("ARIA_TWO_STARTED_PORT", "6800"))
EDIT_SLEEP_TIME_OUT = int(os.environ.get("EDIT_SLEEP_TIME_OUT", "5"))
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = int(
    os.environ.get("MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START", 300)
)
MAX_TG_SPLIT_FILE_SIZE = int(os.environ.get("MAX_TG_SPLIT_FILE_SIZE", "2000000000"))
# add config vars for the display progress
FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR", "Ι")
UN_FINISHED_PROGRESS_STR = os.environ.get("UN_FINISHED_PROGRESS_STR", "·")
# add offensive API
TG_OFFENSIVE_API = os.environ.get("TG_OFFENSIVE_API", None)
CUSTOM_FILE_NAME = os.environ.get("CUSTOM_FILE_NAME", "")
LEECH_COMMAND = os.environ.get("LEECH_COMMAND", "leech")
LEECH_UNZIP_COMMAND = os.environ.get("LEECH_UNZIP_COMMAND", "leechunzip")
LEECH_ZIP_COMMAND = os.environ.get("LEECH_ZIP_COMMAND", "leechzip")
GLEECH_COMMAND = os.environ.get("GLEECH_COMMAND", "gleech")
GLEECH_UNZIP_COMMAND = os.environ.get("GLEECH_UNZIP_COMMAND", "gleechunzip")
GLEECH_ZIP_COMMAND = os.environ.get("GLEECH_ZIP_COMMAND", "gleechzip")
YTDL_COMMAND = os.environ.get("YTDL_COMMAND", "ytdl")
GYTDL_COMMAND = os.environ.get("GYTDL_COMMAND", "gytdl")
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG", "")
DESTINATION_FOLDER = os.environ.get("DESTINATION_FOLDER", "/")
INDEX_LINK = os.environ.get("INDEX_LINK", "")
TELEGRAM_LEECH_COMMAND = os.environ.get("TELEGRAM_LEECH_COMMAND", "tleech")
TELEGRAM_LEECH_UNZIP_COMMAND = os.environ.get(
    "TELEGRAM_LEECH_UNZIP_COMMAND", "tleechunzip"
)
CANCEL_COMMAND_G = os.environ.get("CANCEL_COMMAND_G", "cancel")
GET_SIZE_G = os.environ.get("GET_SIZE_G", "getsize")
STATUS_COMMAND = os.environ.get("STATUS_COMMAND", "status")
STATS_COMMAND = os.environ.get("STATS_COMMAND", "stats")
HELP_COMMAND = os.environ.get("HELP_COMMAND", "help")
SAVE_THUMBNAIL = os.environ.get("SAVE_THUMBNAIL", "savethumbnail")
CLEAR_THUMBNAIL = os.environ.get("CLEAR_THUMBNAIL", "clearthumbnail")
UPLOAD_AS_DOC = os.environ.get("UPLOAD_AS_DOC", "False")
PYTDL_COMMAND = os.environ.get("PYTDL_COMMAND", "pytdl")
GPYTDL_COMMAND = os.environ.get("GPYTDL_COMMAND", "gpytdl")
LOG_COMMAND = os.environ.get("LOG_COMMAND", "log")
CLONE_COMMAND_G = os.environ.get("CLONE_COMMAND_G", "clone")
CLONE_ZIP_COMMAND = os.environ.get("CLONE_ZIP_COMMAND", "clonezip")
CLONE_TAR_COMMAND = os.environ.get("CLONE_TAR_COMMAND", "clonetar")
UPLOAD_COMMAND = os.environ.get("UPLOAD_COMMAND", "upload")
RENEWME_COMMAND = os.environ.get("RENEWME_COMMAND", "renewme")
RENAME_COMMAND = os.environ.get("RENAME_COMMAND", "rename")
LIST_COMMAND = os.environ.get("LIST_COMMAND", "list")
COMPLETE_LIST_COMMAND = os.environ.get("FULL_LIST_COMMAND", "completelist")
TOGGLE_VID = os.environ.get("TOGGLE_VID", "uploadvid")
TOGGLE_DOC = os.environ.get("TOGGLE_DOC", "uploaddoc")

BOT_START_TIME = time.time()
BOT_START_DATETIME = datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
# dict to control uploading and downloading
gDict = defaultdict(lambda: [])
# user settings dict #ToDo
user_settings = defaultdict(lambda: {})
gid_dict = defaultdict(lambda: [])

# Telegraph token things
sname = "".join(random.SystemRandom().choices(string.ascii_letters, k=8))
telegraph = Telegraph()
telegraph.create_account(short_name=sname)
telegraph_token = telegraph.get_access_token()

TELEGRAPHLIMIT = 50


def multi_rclone_init():
    if RCLONE_CONFIG:
        LOGGER.warning("Don't use this var now, put your rclone.conf in root directory")
    if not os.path.exists("rclone.conf"):
        LOGGER.warning("Sed, No rclone.conf found in root directory")
        return
    if not os.path.exists("rclone_bak.conf"):  # backup rclone.conf file
        with open("rclone_bak.conf", "w+", newline="\n", encoding="utf-8") as fole:
            with open("rclone.conf", "r") as f:
                fole.write(f.read())
        LOGGER.info("rclone.conf backuped to rclone_bak.conf!")


multi_rclone_init()
