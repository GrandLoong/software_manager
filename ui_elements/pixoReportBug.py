# -*- coding: utf-8 -*-
import time
import socket
from PySide import QtCore
from pixoLibs.pixoPipeEmail import mail
import pixoLibs.pixoShotgun as psg
from ui_elements.loadui import loadUiType
import pixoConfig

ISOTIMEFORMAT = '%Y-%m-%d %X'

UI_FILE = pixoConfig.UI_DIR + '/pixopipe_report_bug.ui'
form, base = loadUiType(UI_FILE)


class pixoReportBug(form, base):
    def __init__(self, parent=None):
        """Super, loadUi, signal connections"""
        super(pixoReportBug, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint)
        self.pushButton_commit.clicked.connect(self.commit)
        self.lineEdit_Email.setText(psg.getMySGInfo()['login'])

    def commit(self):
        authorEmail = self.lineEdit_Email.text()
        mailSubject = self.lineEdit_Subject.text()
        strBugText = self.textEdit_bugcontext.toPlainText()
        mailBody = self.tr('Time:  \t') + time.strftime(ISOTIMEFORMAT, time.localtime())
        mailBody += self.tr('\nApp in:\t') + pixoConfig.APP_PATH
        mailBody += self.tr('\nHost:  \t') + socket.gethostname()
        mailBody += self.tr('\nUser:  \t') + authorEmail
        mailBody += self.tr('\n\n\t') + strBugText
        mail.sendmail(pixoConfig.PixoConfig.get_variable('slackbugmail'), mailSubject, mailBody)
        self.close()
