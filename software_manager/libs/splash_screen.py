# -*- coding:utf8 -*-
import time
from os.path import join as pathjoin

from PySide import QtGui, QtCore

from software_manager import config


class SplashScreen(QtGui.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(QtGui.QPixmap(pathjoin(
            config.RESOURCES, "tray_icon.png")),
                                           QtCore.Qt.WindowStaysOnTopHint)

    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            new_opacity = self.windowOpacity() + 0.02
            if new_opacity > 1:
                break

            self.setWindowOpacity(new_opacity)
            self.show()
            t -= 1
            time.sleep(0.04)

        time.sleep(2)
        t = 0
        while t <= 50:
            new_opacity = self.windowOpacity() - 0.02
            if new_opacity < 0:
                break

            self.setWindowOpacity(new_opacity)
            t += 1
            time.sleep(0.04)

    def showMessage(self, message, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, color=QtCore.Qt.green):
        return super(SplashScreen, self).showMessage(message, alignment, color)
