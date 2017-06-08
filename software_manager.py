# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys
import webbrowser
from os.path import join as pathjoin

from PySide import QtGui, QtCore

import config
from libs.manager import Manager
from libs.splash_screen import SplashScreen
from libs.loadui import load_ui_type, load_style_sheet

uiFile = pathjoin(config.APP_DIR, 'resources/software_manager.ui')
css_file = pathjoin(config.APP_DIR, 'resources/software_manager.css')
ui_form, ui_base = load_ui_type(uiFile)


class SoftwareManagerGUI(ui_form, ui_base):
    def __init__(self):
        super(SoftwareManagerGUI, self).__init__()
        self.setupUi(self)
        self.user_name = os.getenv('USERNAME')
        self.wrappers_dir = config.WRAPPERS
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
        self.dragPos = QtCore.QPoint(0, 0)
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
        self.pushButton_hide.setIcon(QtGui.QIcon(self.add_icon('software_manager_hide.png')))
        self.pushButton_close.setIcon(QtGui.QIcon(self.add_icon('software_manager_close.png')))
        self.pushButton_hide.clicked.connect(self.close)
        self.pushButton_close.clicked.connect(QtGui.qApp.quit)
        for software_name in Manager.sort_data(self.data):
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
            layer_item.setToolTip(u'%s' % software_describe)
            layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.software_commands.addItem(layer_item)
        self.software_commands.itemDoubleClicked.connect(self.launch)
        self.software_commands.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.search_text.textChanged.connect(self.search_software)

        self.pushButton_bottom_icon.clicked.connect(self.popup_web)
        self.search_button.clicked.connect(lambda: self.search_text.setText(''))

        self.user_menu = QtGui.QMenu(self)
        self.user_menu.addSeparator()
        self.user_menu.addAction('')
        self.set_transparency(False)
        self.user_button.setMenu(self.user_menu)
        self.rightButton = False
        self.desktop = QtGui.QDesktopWidget()
        self.move(self.desktop.availableGeometry().width() - self.width(),
                  self.desktop.availableGeometry().height() - self.height())

    def find_item_under_mouse(self, widget):
        viewport_pos = widget.viewport().mapFromGlobal(QtGui.QCursor.pos())
        item = widget.itemAt(viewport_pos)
        return item

    def show_software_item_menu(self):
        item = self.find_item_under_mouse(self.software_commands)
        if item:
            popup_menu = QtGui.QMenu(self)
            view_folder = self._action("Delete Current Item", self.delete_item)
            popup_menu.addAction(view_folder)
            popup_menu.addSeparator()
            popup_menu.exec_(QtGui.QCursor.pos())
            # return item

    def delete_item(self):
        item = self.software_commands.takeItem(self.software_commands.currentRow())
        self.software_commands.setCurrentRow(-1)
        self.data.pop(item.text())
        self.save_profile()

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
        webbrowser.open_new_tab('https://vimeo.com/loong')

    def drag_to_shortcut(self):
        print self.drag_file
        if os.path.exists(self.drag_file):
            software_name = os.path.basename(self.drag_file).split('.')[0]
            software_path = self.drag_file
            if not software_name in self.data:
                software_icon = pathjoin(self.app_dir, 'resources', 'default_software_icon.png').replace('\\', '/')
                self.data.update({
                    software_name:
                        {
                            'path': software_path,
                            'icon': 'default_software_icon.png',
                            'describe': software_name,
                            'order': self.software_commands.count(),
                        }
                })
                image = QtGui.QIcon(software_icon)
                layer_item = QtGui.QListWidgetItem(image, software_name)
                layer_item.setToolTip(u'%s' % software_name)
                layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.software_commands.addItem(layer_item)
                print self.data
                self.save_profile()

    def drag_to_run_program(self):
        if self.drag_file:
            item = self.software_commands.currentItem()
            if item:
                exe_path = self.data[item.text()]['path']
                if exe_path.startswith('.'):
                    exe_path = exe_path.replace('.', self.app_dir, 1)
                command = '"{0}" {1}'.format(exe_path, self.drag_file)
                subprocess.call(command)

    def save_profile(self):
        self.manager.save_local_data(self.data)

    def contextMenuEvent(self, event):
        self.show_software_item_menu()

    def closeEvent(self, event):
        self.gui_show = False
        self.hide()
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
            exe_path = os.path.normpath(exe_path.replace('.', self.wrappers_dir, 1))

        if exe_path.endswith('.bat') or exe_path.endswith('.cmd'):
            command = 'cmd /c start {0}'.format(exe_path)
        elif exe_path.endswith('.lnk'):
            command = '"{0}"'.format(os.path.normpath(exe_path))
        elif exe_path.endswith('.exe'):
            command = '"{0}"'.format(os.path.normpath(exe_path))
        else:
            command = 'cmd /c start "{0}"'.format(os.path.normpath(exe_path))
        # logging.info(command)
        subprocess.Popen(command, shell=True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def add_icon(self, icon_name):
        return pathjoin(self.app_dir, 'resources', icon_name)

    def icon_activated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.gui_show:
                # self.hide()
                self.close()
            else:
                self.show()
                self.move(self.desktop.availableGeometry().width() - self.width(),
                          self.desktop.availableGeometry().height() - self.height())
                self.gui_show = True

    def set_icon(self, index):
        icon = self.iconComboBox.itemIcon(0)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    def search_software(self):
        self.software_commands.clear()
        result = []
        soft_name = self.search_text.text()
        pattem = '.*?'.join(soft_name.lower())
        regex = re.compile(pattem)
        Manager.sort_data(self.data)
        for software_name in self.data.keys():
            match = regex.search(software_name.lower())
            if match:
                result.append((len(match.group()), match.start(), software_name))
        if result:
            sorted_result = [x for _, _, x in sorted(result)]
            for r in sorted_result:
                icon_name = self.data[r]['icon']
                if icon_name:
                    image_path = pathjoin(self.app_dir, 'resources', icon_name)
                else:
                    image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')

                if not os.path.isfile(image_path):
                    image_path = pathjoin(self.app_dir, 'resources', 'default_software_icon.png')
                image = QtGui.QIcon(image_path)
                layer_item = QtGui.QListWidgetItem(image, r)
                describe_msg = 'Describe:\n\t{0}\nPath:\n\t{1}'.format(r,
                                                                       self.data[r].get('path'))
                layer_item.setToolTip(describe_msg)
                layer_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.software_commands.addItem(layer_item)

    def show_message(self, msg):
        icon = QtGui.QSystemTrayIcon.MessageIcon()
        self.trayIcon.showMessage('SoftwareManager', msg, icon, 1000)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = SoftwareManagerGUI()
    gui.setStyleSheet(load_style_sheet(css_file))
    splash = SplashScreen()
    splash.showMessage("Please wait for initialization...", color=QtCore.Qt.red)
    splash.effect()
    app.processEvents()
    gui.show_message(u'Software Manager')
    gui.show()
    splash.finish(gui)
    app.exec_()
