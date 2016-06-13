# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from os.path import join as pathjoin

import webbrowser

from PySide import QtGui, QtCore

import config
from libs.manager import Manager
from libs.splash_screen import SplashScreen
from ui_elements.loadui import loadUiType, loadStyleSheet

uiFile = pathjoin(os.path.dirname(__file__), 'resources/software_manager.ui')
css_file = pathjoin(os.path.dirname(__file__), 'resources/software_manager.css')
ui_form, ui_base = loadUiType(uiFile)


class SoftwareManagerGUI(ui_form, ui_base):
    def __init__(self):
        super(SoftwareManagerGUI, self).__init__()
        self.setupUi(self)
        self.user_name = os.getenv('USERNAME')
        self.manager = Manager()
        self.app_dir = config.APP_DIR
        self.iconComboBox = QtGui.QComboBox()
        self.iconComboBox.addItem(QtGui.QIcon(self.add_icon('tray_icon.png')), "Dmyz")
        self.quitAction = QtGui.QAction("exit", self, triggered=QtGui.qApp.quit)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.iconComboBox.currentIndexChanged.connect(self.set_icon)
        self.setWindowIcon(QtGui.QIcon(self.add_icon('tray_icon.png')))
        self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()
        self.trayIcon.setToolTip('Software Manager')
        self.trayIcon.activated.connect(self.icon_activated)
        self.setAcceptDrops(True)
        self.delete = False
        self.gui_show = True
        self.dragPos = 0

        self.data = self.manager.global_data
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        local_data = self.manager.local_data

        if len(local_data.keys()) > 0:
            self.data.update(local_data)

        self.search_magnifier.setPixmap(self.add_icon('search_dark.png'))
        self.search_button.setIcon(QtGui.QIcon(self.add_icon('icon_inbox_clear.png')))
        self.user_button.setIcon(QtGui.QIcon(self.add_icon('default_user_thumb.png')))
        self.pushButton_bottom_icon.setIcon(QtGui.QIcon(self.add_icon('software_name.png')))
        self.pushButton_top_icon.setIcon(QtGui.QIcon(self.add_icon('software_name.png')))

        for software_name in self.data.keys():
            icon_name = self.data[software_name]['icon']
            if icon_name:
                image_path = pathjoin(self.app_dir, 'resources', icon_name)
            else:
                image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')

            if not os.path.isfile(image_path):
                image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')
            image = QtGui.QIcon(image_path)
            layer_item = QtGui.QListWidgetItem(image, software_name)
            software_describe = self.data[software_name]['describe']
            self.html_msg = """
            <span style=" font-weight:600; color:#85cd00;">Describe:<br></span></p>
            <span style=" width:400px; font-weight:600; color:#85cd00;">    {0}</span></p>
            """
            layer_item.setToolTip(u'%s' % software_describe)
            layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.software_commands.addItem(layer_item)

        self.software_commands.itemDoubleClicked.connect(self.launch)
        # self.software_commands.itemClicked.connect(self.find_item_under_mouse)
        self.software_commands.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # self.software_commands.customContextMenuRequested.connect(self.find_item_under_mouse)
        self.search_text.textChanged.connect(self.search_software)

        self.pushButton_bottom_icon.clicked.connect(self.popup_web)
        self.search_button.clicked.connect(lambda: self.search_text.setText(''))

        self.user_menu = QtGui.QMenu(self)
        self.user_menu.addSeparator()
        self.user_menu.addAction('')
        self.set_transparency(True)
        self.user_button.setMenu(self.user_menu)
        self.rightButton = False
        self.desktop = QtGui.QDesktopWidget()
        self.move(self.desktop.availableGeometry().width() - self.width(),

                  self.desktop.availableGeometry().height() - self.height())  # 初始化位置到右下角
        splash = QtGui.QSplashScreen()
        splash.setPixmap(QtGui.QPixmap(self.add_icon('tray_icon.png')))
        splash.show()

    def find_item_under_mouse(self, widget):
        viewportPos = widget.viewport().mapFromGlobal(QtGui.QCursor.pos())
        item = widget.itemAt(viewportPos)
        return item

    def show_software_item_menu(self):
        item = self.find_item_under_mouse(self.software_commands)
        if item:
            popupMenu = QtGui.QMenu(self)
            viewFolder = self._action("Delete Current Item", self.delete_item)
            popupMenu.addAction(viewFolder)
            popupMenu.addSeparator()
            popupMenu.exec_(QtGui.QCursor.pos())
            # return item

    def delete_item(self):
        item = self.software_commands.takeItem(self.software_commands.currentRow())
        self.software_commands.setCurrentRow(-1)
        self.data.pop(item.text())

    def _action(self, name, callback=None, icon_path=None):
        """ Create an action and store it in self.actions.
        """
        action = QtGui.QAction(self)
        action.setText(name)
        if icon_path:
            action.setIcon(icon_path)
        if callback:
            action.connect(action, QtCore.SIGNAL("triggered()"), callback)
        return action

    def show_right_menu(self):
        print self.sender().button()
        # if QtCore.Qt.RightButton:
        #     print 'show_right_menu'

    def set_transparency(self, enabled):
        if enabled:
            self.setAutoFillBackground(False)
        else:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, enabled)
        self.repaint()

    @staticmethod
    def popup_web():
        webbrowser.open_new_tab('https://pixomondovfx.shotgunstudio.com')

    def drag_to_shortcut(self):
        print self.drag_file
        if os.path.exists(self.drag_file):
            software_name = os.path.basename(self.drag_file).split('.')[0]
            software_path = self.drag_file
            if not software_name in self.data:
                software_icon = pathjoin(self.app_dir, 'resources', 'pixomondo.png').replace('\\', '/')
                self.data.update({software_name: {'path': software_path, 'icon': 'pixomondo.png',
                                                  'describe': software_name, 'order': self.software_commands.count()}})
                image = QtGui.QIcon(software_icon)
                layer_item = QtGui.QListWidgetItem(image, software_name)
                layer_item.setToolTip(self.html_msg.format(software_name))
                layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.software_commands.addItem(layer_item)
                print self.data

    def drag_to_run_program(self):
        if self.drag_file:
            item = self.software_commands.currentItem()
            if item:
                exe_path = self.data[item.text()]['path']
                if exe_path.startswith('.'):
                    exe_path = exe_path.replace('.', self.app_dir, 1)
                command = 'call "{0}" {1}'.format(exe_path, self.drag_file)
                subprocess.Popen(command, shell=True)

    def save_profile(self):
        self.manager.save_local_data(self.data)

    def contextMenuEvent(self, event):
        self.show_software_item_menu()

    def closeEvent(self, event):
        self.hide()
        self.save_profile()
        event.ignore()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.search_text.deselect()
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            if event.source() is self:
                event.setDropAction(QtCore.Qt.MoveAction)
            else:
                event.setDropAction(QtCore.Qt.CopyAction)
        url = event.mimeData().urls()
        if url:
            # Workaround for OSx dragging and dropping
            try:
                for url in event.mimeData().urls():
                    fname = '{0}'.format(url.toLocalFile())
            except UnicodeEncodeError:
                fname = None
            self.drag_file = fname
            if self.drag_file.endswith('.lnk') or self.drag_file.endswith('.exe') or self.drag_file.endswith('.bat'):
                self.software_commands.setCurrentRow(-1)
                self.drag_to_shortcut()
            else:
                self.drag_to_run_program()

    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self.move(e.globalPos() - self.dragPos)
            e.accept()

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.dragPos = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()
        if e.button() == QtCore.Qt.RightButton and self.rightButton == False:
            self.rightButton = True

    def launch(self):
        print self.data
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        item = self.software_commands.currentItem()
        exe_path = self.data[item.text()]['path']
        if exe_path.startswith('.'):
            exe_path = exe_path.replace('.', self.app_dir, 1)
        command = 'call "{0}"'.format(exe_path)
        subprocess.Popen(command, shell=True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def add_icon(self, icon_name):
        return pathjoin(self.app_dir, 'resources', icon_name)

    def icon_activated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.gui_show:
                # self.hide()
                self.close()
                self.gui_show = False
            else:
                self.show()
                self.move(self.desktop.availableGeometry().width() - self.width(),
                          self.desktop.availableGeometry().height() - self.height())  # 初始化位置到右下角
                self.gui_show = True

    def set_icon(self, index):
        icon = self.iconComboBox.itemIcon(0)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    def search_software(self):
        self.software_commands.clear()
        soft_name = self.search_text.text()
        for software_name in self.data.keys():
            if soft_name.lower() in software_name.lower():
                icon_name = self.data[software_name]['icon']
                if icon_name:
                    image_path = pathjoin(self.app_dir, 'resources', icon_name)
                else:
                    image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')

                if not os.path.isfile(image_path):
                    image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')
                image = QtGui.QIcon(image_path)
                layer_item = QtGui.QListWidgetItem(image, software_name)
                layer_item.setToolTip(self.html_msg.format(software_name))
                layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.software_commands.addItem(layer_item)

    def show_message(self, msg):
        icon = QtGui.QSystemTrayIcon.MessageIcon()
        self.trayIcon.showMessage('SoftwareManager', msg, icon, 1000)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # QtGui.QApplication.setQuitOnLastWindowClosed(False)
    gui = SoftwareManagerGUI()
    gui.setStyleSheet(loadStyleSheet(css_file))
    splash = SplashScreen()
    splash.effect()
    app.processEvents()  # ＃设置启动画面不影响其他效果
    # gui.show_message(u'software manager')
    gui.show()
    splash.finish(gui)
    app.exec_()

