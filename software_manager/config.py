# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""
import os

from hz.config import HZConfig
from hz.environment import env
from hz.toolkit import create_missing_directories

APP_DIR = os.path.dirname(__file__)
NAME = "softwareManager"
WRAPPERS = '%s/system/wrappers' % env.APP_CONFIG


def get_local_profile_dir():
    settings = HZConfig(NAME)
    folder = settings.get_user_settings_path()
    if not os.path.isdir(folder):
        create_missing_directories(folder)
    return folder
