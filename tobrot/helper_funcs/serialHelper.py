import os
from tobrot.helper_funcs.download import download_tg
from datetime import date, datetime, timedelta
import numpy as np
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive


async def anu_fn(client, message):
    if message.reply_to_message is not None:
        user_id = message.from_user.id
        file, mess_age = await download_tg(client, message)
        start_date = date(2021, 9, 1)
        start_serial_no = 355
        today = date.today()
        total_days = (today - start_date).days
        sundays = int(np.busday_count(start_date, today, weekmask='Sun'))
        working_days = total_days - sundays
        today_serial_no = start_serial_no + working_days
        serial_name = f"E{today_serial_no} {today.day} {datetime.strptime(str(today.month), '%m').strftime('%B')}.mp4"
        if file:
            os.rename(file, serial_name)
        else:
            return
        await upload_to_gdrive(serial_name, mess_age, message, user_id, is_anu=True)
    else:
        await message.reply_text(
            "Reply to a Anupama serial to upload to GDrive."
        )


async def shubh_laabh_fn(client, message):
    if message.reply_to_message is not None:
        user_id = message.from_user.id
        file, mess_age = await download_tg(client, message)
        start_date = date(2021, 9, 13)
        start_serial_no = 1
        today = date.today()
        yesterday = today - timedelta(days=1)
        total_days = (today - start_date).days
        saturdays = int(np.busday_count(start_date, today, weekmask='Sat'))
        sundays = int(np.busday_count(start_date, today, weekmask='Sun'))
        working_days = total_days - sundays - saturdays
        today_serial_no = start_serial_no + working_days
        command = message.command[0]
        if command == 'slt':
            serial_name = f"Shubh Laabh E{today_serial_no} {today.day} {datetime.strptime(str(today.month), '%m').strftime('%B')}.mp4"
        else:
            serial_name = f"Shubh Laabh E{today_serial_no - 1} {yesterday.day} {datetime.strptime(str(yesterday.month), '%m').strftime('%B')}.mp4"
        if file:
            os.rename(file, serial_name)
        else:
            return
        await upload_to_gdrive(serial_name, mess_age, message, user_id, is_shubh_laabh=True)
    else:
        await message.reply_text(
            "Reply to a Shubh Laabh serial to upload to GDrive."
        )
