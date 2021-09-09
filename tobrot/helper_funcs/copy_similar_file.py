import os
import time
from shutil import copyfile

# idk
async def copy_file(input_file, output_dir):
    output_file = os.path.join(output_dir, str(time.time()) + ".jpg")
    # https://stackoverflow.com/a/123212/4723940
    copyfile(input_file, output_file)
    return output_file
