import os
from shutil import copy2


class Analyser:
    def copyFile(src, dst, file_name):
        #  if not os.path.exists(dst):
        #     os.makedirs(dst, "0755")
        dst = os.path.join(dst, file_name)
        copy2(src, dst)
