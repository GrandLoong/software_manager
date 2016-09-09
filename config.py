import os
import sys
from os.path import join as pathjoin

APP_DIR = os.path.dirname(__file__)
RESOURCES = pathjoin(APP_DIR, 'resources')


def get_local_profile_dir():
    profile = "USERPROFILE"
    if sys.platform != "win32":
        profile = "HOME"
    homedir = os.getenv(profile)
    desktop_profile_dir = pathjoin(homedir, '.SoftwareManager')
    desktop_profile_dir = os.path.normpath(desktop_profile_dir)
    if not os.path.exists(desktop_profile_dir):
        os.mkdir(desktop_profile_dir)
    print desktop_profile_dir
    return desktop_profile_dir
