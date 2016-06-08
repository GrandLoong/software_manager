# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui  # , QtUiTools
from ui_elements.loadui import loadUiType
import logging
import pixoConfig
from pixoLibs import pixoShotgun as psg
from os.path import normpath
import json

UI_FILE = pixoConfig.UI_DIR + '/pixopipe_sg_login.ui'
form, base = loadUiType(UI_FILE)


def find_sg_login_file_location():
    return normpath(pixoConfig.PixoConfig.get_pixoConfig_dir() + "/shotgun_login.sglogin")


def writeSGUserDataToFile(user_info):
    login_setting_file = find_sg_login_file_location()

    with open(login_setting_file, "w") as f:
        json.dump(user_info, f, indent=4)
        logging.info(user_info)


def read_login():
    login_setting_file = find_sg_login_file_location()
    with open(login_setting_file, "r") as f:
        login_dict = json.load(f)
    return login_dict


class SG_Login(form, base):
    def __init__(self, parent=None):
        """Super, loadUi, signal connections"""
        super(SG_Login, self).__init__(parent)
        self.setupUi(self)
        self.accepted_user = None
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.pushButton.clicked.connect(self.create_login_file)

    def create_login_file(self):
        shotgun_Login_name = self.lineEdit.text()
        user_info = psg.findUserByName(shotgun_Login_name)
        if user_info:
            writeSGUserDataToFile(user_info)
            self.accepted_user = user_info['login']
            self.close()
        else:
            QtGui.QMessageBox.warning(self, self.tr('Unknown User'), self.tr("The user specified does not exist"),
                                      QtGui.QMessageBox.Cancel)
