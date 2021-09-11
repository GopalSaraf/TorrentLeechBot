# from tobrot import AUTH_CHANNEL
#
#
# async def AdminCheck(client, chat_id, user_id):
#     chat = await client.get_chat(chat_id)
#     if chat.type == "private" and chat_id in AUTH_CHANNEL:
#         return True
#     SELF = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
#     admin_strings = ["creator", "administrator"]
#     # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
#     if SELF.status not in admin_strings:
#         return False
#     else:
#         return True
from subprocess import Popen, PIPE
import json
import subprocess

command = 'rclone lsjson torrgsbot:'
to_srch = 'genius'

p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# errcode = p.wait()
json_str = p.stdout.read().decode('utf-8')
# errmess = p.stderr.read()


json_list = json.loads(json_str)
print(json_list)

for item in json_list:
    if to_srch.lower() in item['Name'].lower():
        if item['IsDir']:
            print(item['Name'], item['ID'])
        else:
            print(item['Name'], item['Size'])
