# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""
# Import build-in modules.
import glob
import os
import random
import re
import shutil
import traceback
import webbrowser

# Import third-party modules.
import hz.awesome_ui.css as awesome_css
import hz.toolkit as htk
import openmetadata as om
from Qt import QtCore, QtGui, QtWidgets
from hz.applauncher import Profile
from hz.awesome_ui.widgets import AnimatedSystemTrayIcon
from hz.awesome_ui.widgets import AwesomeSplashScreen
from hz.awesome_ui.widgets import MessageDisplay
from hz.awesome_ui.widgets import RenderAwesomeUI
from hz.config import HZConfig
from hz.environment import env
from hz.resources import HZResources

# Import local modules.
from software_manager.config import APP_DIR
from software_manager.config import NAME
from software_manager.config import WRAPPERS
from software_manager.config import get_local_profile_dir
from software_manager.item import SoftwareManagerItemGUI
from software_manager.manager import SoftwareManager
from software_manager.skin import SoftwareManagerSkinUI

LOGGING = htk.get_logger(NAME)
LOGGING.setLevel(htk.get_logger_level())


class SoftwareManagerError(IOError):
    def __init__(self, argv):
        LOGGING.error(argv)


class SoftwareManagerGUI(QtWidgets.QWidget):
    def __init__(self, ui_file):
        super(SoftwareManagerGUI, self).__init__()
        # parent custom widget
        RenderAwesomeUI(ui_file=ui_file, parent_widget=self, css_file=CSS_FILE)
        # init attribute
        self.offset = None
        self.app_launchers = htk.get_launchers()
        self.resources = HZResources()
        self.user_name = env.USERNAME.string
        self.local_profile_folder = get_local_profile_dir()
        self.drag_file = ''
        self.wrappers_dir = WRAPPERS
        self.app_dir = APP_DIR
        self.icon_combo_box = QtWidgets.QComboBox()
        self.user_image = htk.pathjoin(self.local_profile_folder, "user.png")
        self.delete = False
        self.gui_show = True
        self.drag_pos = QtCore.QPoint(0, 0)
        self.right_button = False
        self.background_image = None
        _image = om.read(self.local_profile_folder, 'skin')

        # init windows
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.Window |
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.WindowSoftkeysRespondHint)
        self.comboBox_project_list.addItems(self.get_project_list())

        self.set_current_project()

        self.icon_combo_box.addItem(self.icon("default_software_icon.png"),
                                    "Dmyz")
        self.quit_action = QtWidgets.QAction("exit", self,
                                             triggered=QtWidgets.QApplication.quit)
        open_log_action = QtWidgets.QAction("Explore Log Folder ",
                                            self,
                                            triggered=self.go_to_log_folder)

        self.open_local_folder = QtWidgets.QAction(
            "Open Local Settings Folder",
            self,
            triggered=self.explore_local_settings_folder)
        project_manager_action = QtWidgets.QAction("project manager",
                                                   self,
                                                   triggered=self.go_to_log_folder)

        self.tray_icon_menu = QtWidgets.QMenu(self)
        if _image:
            self.background_image = _image.encode("utf-8").replace("\\", "/")

        self.skin_action = QtWidgets.QAction('Skin Store', self,
                                             triggered=self.show_skin_widget)

        self.change_css = QtWidgets.QMenu('Change CSS', self.tray_icon_menu)

        default = QtWidgets.QAction("default", self.change_css,
                                    triggered=self.change_css_default)

        self.change_css.addAction(default)

        self.tray_icon_menu.addAction(self.skin_action)

        self.tray_icon_menu.addAction(self.open_local_folder)

        self.tray_icon_menu.addAction(project_manager_action)

        self.tray_icon_menu.addAction(open_log_action)

        random_skin_aciton = self._action("random_skin", self._skin_timer)
        random_skin_aciton.setCheckable(True)
        status = om.read(self.local_profile_folder, "random_skin")
        if status:
            random_skin_aciton.setChecked(status)

        self.tray_icon_menu.addAction(random_skin_aciton)

        self.tray_icon_menu.addMenu(self.change_css)
        self.tray_icon_menu.addAction(self.quit_action)
        gif_file = HZResources.get_icon_resources("default_software_icon.gif")
        self.tray_icon = AnimatedSystemTrayIcon(QtGui.QMovie(gif_file),
                                                self)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.icon_combo_box.currentIndexChanged.connect(self.set_icon)
        self.setWindowIcon(self.icon("default_software_icon.png"))
        self.icon_combo_box.setCurrentIndex(1)
        self.tray_icon.show()
        self.tray_icon.setToolTip('HZ')
        self.tray_icon.activated.connect(self.icon_activated)
        self.setAcceptDrops(True)
        self.set_transparency(True)

        if os.path.isfile(self.user_image):
            self.user_button.setIcon(
                self.create_round_thumbnail(self.user_image))
        else:
            self.user_button.setIcon(self.create_round_thumbnail(
                self.icon("default_user_thumb.png", True)))

        self.pushButton_bottom_icon.setIcon(self.icon("software_name.png"))
        self.pushButton_top_icon.setIcon(self.icon("hz_label.png"))
        self.pushButton_hide.setIcon(self.icon("software_manager_hide.png"))
        self.pushButton_close.setIcon(self.icon("software_manager_close.png"))
        self.pushButton_hide.clicked.connect(self.close)
        self.pushButton_close.clicked.connect(QtWidgets.QApplication.quit)
        self.tool_box = QtWidgets.QToolBox()
        self.software_commands = QtWidgets.QListWidget(self)
        self.software_commands.itemDoubleClicked.connect(self.launch)
        self.software_commands.setContextMenuPolicy(
            QtCore.Qt.ActionsContextMenu)
        self.verticalLayout_3.addWidget(self.software_commands)
        self.search_text.textChanged.connect(self.search_software)
        self.pushButton_bottom_icon.clicked.connect(self.popup_web)

        self.user_menu = QtWidgets.QMenu(self)

        self.user_menu.addSeparator()

        user_action = QtWidgets.QAction("change user image", self,
                                        triggered=self.set_user_image)

        self.user_menu.addAction(user_action)

        self.user_button.setMenu(self.user_menu)

        self.desktop = QtWidgets.QDesktopWidget()

        self.move(self.desktop.availableGeometry().width() - self.width(),
                  self.desktop.availableGeometry().height() - self.height())

        self.save_current_project()
        self.set_items()
        self.comboBox_project_list.activated.connect(self.set_items)
        self.update_info_file = htk.pathjoin(self.resources.resources_root,
                                             'update.txt')
        self.file_watcher = QtCore.QFileSystemWatcher([self.update_info_file])
        self.file_watcher.fileChanged.connect(self.on_file_changed)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_task)
        self.timer.start(1000)
        if self.background_image:
            self.set_background_image_css(
                self.background_image.decode("utf-8"))
        else:
            self.set_background_image_css(self.get_skin())
        self.skin_timer = QtCore.QTimer(self)
        self.skin_timer.timeout.connect(self.random_skin)
        if status:
            self.skin_timer.start(20000)

    def show_skin_widget(self):
        skin_gui = SoftwareManagerSkinUI(self)
        skin_gui.exec_()

    def _skin_timer(self):
        status = self.sender().isChecked()
        if status:
            self.skin_timer.start(20000)
        else:
            self.skin_timer.stop()
        om.write(self.local_profile_folder, "random_skin", status)

    def set_background_image_action(self):
        skin_path = self.sender().data()
        om.write(self.local_profile_folder, 'skin', skin_path)
        self.set_background_image_css(skin_path.replace("\\", '/'))

    def random_skin(self):
        self.set_background_image_css(self.get_skin())

    def get_skins(self):
        all_files = glob.glob("%s/skin/*.png" % HZResources.resources_root)
        all_files.extend(
            glob.glob("%s/skin/*.png" % self.local_profile_folder))
        return all_files

    def get_skin(self):
        all_files = glob.glob("%s/skin/*.png" % HZResources.resources_root)
        all_files.extend(
            glob.glob("%s/skin/*.png" % self.local_profile_folder))
        index = random.randrange(0, len(all_files), 1)
        LOGGING.info(
            "find skin: %s" % all_files[index].replace("\\", '/').decode(
                "gbk"))
        return all_files[index].replace("\\", '/').decode("gbk")

    def set_background_image_css(self, image):
        awesome_css.set_background_image(self.mainFrame, image)

    def change_background_image(self):
        image = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image",
                                                      "/home/jana",
                                                      "Image Files (*.png)")
        if image[0]:
            shutil.copy(image[0], self.background_image)
            self.set_background_image_css(image[0])

    def on_file_changed(self, path):
        self.show_message_for_file(path)

    def set_items(self):
        self.software_commands.clear()
        project_name = self.comboBox_project_list.currentText()
        self.manager = SoftwareManager(project_name)
        for app_ in self.manager.applications:
            icon_name = app_.icon
            app_.project_name = project_name
            if icon_name:
                image_path = self.icon(icon_name, True)
            else:
                image_path = self.icon("default_software_icon.png", True)
            if not os.path.isfile(image_path):
                image_path = self.icon("default_software_icon.png", True)
            image = QtGui.QIcon(image_path)
            layer_widget = SoftwareManagerItemGUI(app_, self)
            layer_widget.set_icon(image)
            profiles = self.get_profiles(app_.name, project_name)
            if profiles:
                layer_widget.set_list(profiles.keys())
                temp_name = om.read(self.local_profile_folder,
                                    '%s_%s' % (project_name, app_.name))
                if temp_name:
                    layer_widget.set_current_item(temp_name)
            else:
                layer_widget.set_list([app_.name])
            layer_item = QtWidgets.QListWidgetItem(self.software_commands)
            layer_item.setSizeHint(QtCore.QSize(layer_widget.width() - 10,
                                                layer_widget.height()))
            layer_item.path = app_.path
            layer_item.name = app_.name
            layer_item.profiles = profiles
            layer_item.setToolTip(u'%s' % app_.description)
            self.software_commands.setItemWidget(layer_item, layer_widget)
        self.save_current_project()

    @staticmethod
    def create_round_thumbnail(image_path):
        image = QtGui.QImage(image_path)
        canvas_size = 80
        base_image = QtGui.QPixmap(canvas_size, canvas_size)
        base_image.fill(QtCore.Qt.transparent)

        thumb = QtGui.QPixmap.fromImage(image)
        thumb.scaled(canvas_size,
                     canvas_size,
                     QtCore.Qt.KeepAspectRatioByExpanding,
                     QtCore.Qt.SmoothTransformation)
        return thumb

    def get_profiles(self, app_name, project_name):
        profiles = {}
        settings = HZConfig("%s/applauncher/profiles/*" % app_name,
                            project_name=project_name)
        sub_folders = settings.glob_files()
        for sub_folder in sub_folders:
            if self._is_package(sub_folder):
                p = Profile(sub_folder)
                profiles.update({p.label: sub_folder})
        LOGGING.info('all profiles: %s' % profiles)
        return profiles

    @staticmethod
    def _is_package(package_path):
        if (os.path.isfile(package_path) or
                package_path.split(os.path.sep)[-1].startswith('@@')):
            return False
        return 'profile.yaml' in os.listdir(package_path)

    def set_user_image(self):
        image = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image",
                                                      "/home/jana",
                                                      "Image Files (*.png)")
        if image[0]:
            shutil.copy(image[0], self.user_image)
            self.user_button.setIcon(
                self.create_round_thumbnail(self.user_image))

    def change_css_default(self):
        css_skin = """
        QFrame#mainFrame
            {
            background-color: #31363b;
            border-radius: 15px;
            }
        """
        self.mainFrame.setStyleSheet(css_skin)
        file_ = HZResources.get_css_resources("software_manager")
        awesome_css.set_style_sheet(self, file_)

    def set_transparency(self, enabled):
        if enabled:
            self.setAutoFillBackground(False)
        else:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, enabled)
        self.repaint()

    @staticmethod
    def go_to_log_folder():
        htk.start(htk.get_log_folder())

    def explore_local_settings_folder(self):
        htk.start(self.local_profile_folder)

    def set_current_project(self):
        project_name = om.read(self.local_profile_folder, 'project')
        if project_name:
            self.comboBox_project_list.setCurrentIndex(
                self.comboBox_project_list.findText(project_name.lower()))

    def save_current_project(self):
        project_name = self.comboBox_project_list.currentText()
        om.write(self.local_profile_folder, 'project', project_name)

    @staticmethod
    def get_project_list():
        root = htk.pathjoin(env.APP_CONFIG.string, 'settings', 'projects')
        return [x for x in os.listdir(root) if
                os.path.isdir(htk.pathjoin(root, x)) and not x.startswith('.')]

    def get_app_version(self, app_):
        project_name = self.comboBox_project_list.currentText()
        setting_folder = htk.get_server_project_settings_folder(project_name)
        profile = htk.pathjoin(setting_folder, app_, 'profile.yaml')
        if os.path.isfile(profile):
            profile = Profile(profile)
            return ["%s_%s" % (app_, v) for v in profile.application_version]

    @staticmethod
    def find_item_under_mouse(widget):
        viewport_pos = widget.viewport().mapFromGlobal(QtGui.QCursor.pos())
        item = widget.itemAt(viewport_pos)
        return item

    def show_software_item_menu(self):
        item = self.find_item_under_mouse(self.software_commands)
        if item:
            popup_menu = QtWidgets.QMenu(self)
            view_folder = self._action("Delete Current Item", self.delete_item)
            popup_menu.addAction(view_folder)
            popup_menu.addSeparator()
            popup_menu.exec_(QtGui.QCursor.pos())
            # return item

    def delete_item(self):
        item = self.software_commands.takeItem(
            self.software_commands.currentRow())
        self.software_commands.setCurrentRow(-1)
        try:
            self.manager.data.pop(item.text())
        except KeyError:
            LOGGING.error(traceback.format_exc())
        finally:
            self.save_profile()

    def _action(self, name, callback=None, icon_path=None):
        """ Create an action and store it in self.actions.
        """
        action = QtWidgets.QAction(self)
        action.setText(name)
        if icon_path:
            action.setIcon(icon_path)
        if callback:
            action.triggered.connect(callback)
        return action

    @staticmethod
    def popup_web():
        webbrowser.open_new_tab('http://192.168.100.136')

    def drag_to_shortcut(self):
        LOGGING.info(self.drag_file)
        if os.path.exists(self.drag_file):
            software_name = os.path.basename(self.drag_file).split('.')[0]
            software_path = self.drag_file
            if software_name not in self.manager.data:
                software_icon = self.icon("default_software_icon")
                temp_data = {
                    'name': software_name,
                    'path': software_path,
                    'icon': 'default_software_icon.png',
                    'description': software_name,
                    'order': self.software_commands.count()}
                self.manager.data.update(
                    {software_name.replace(" ", ""): temp_data})
                app_ = self.manager.build_app(temp_data)
                image = QtGui.QIcon(software_icon)
                layer_widget = SoftwareManagerItemGUI(app_, self)
                layer_widget.set_icon(image)
                layer_widget.set_list([app_.name])
                layer_item = QtWidgets.QListWidgetItem(self.software_commands)
                layer_item.setToolTip(u'%s' % app_.name)
                layer_item.setSizeHint(QtCore.QSize(layer_widget.width() - 10,
                                                    layer_widget.height()))
                layer_item.setTextAlignment(
                    QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
                self.software_commands.setItemWidget(layer_item, layer_widget)
                LOGGING.info(self.manager.data)
                self.save_profile()

    def drag_to_run_program(self):
        LOGGING.debug(self.manager.data)
        env.HZ_PROJECT_NAME.set(self.comboBox_project_list.currentText())
        item = self.find_item_under_mouse(self.software_commands)
        if item:
            self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            exe_path = item.path
            if exe_path.startswith('.'):
                exe_path = os.path.normpath(
                    exe_path.replace('.', self.wrappers_dir, 1))
            else:
                exe_path = os.path.expandvars(exe_path)
            if not os.path.exists(exe_path):
                LOGGING.error(traceback.format_exc())
                MessageDisplay(NAME,
                               'Not Find \n%s \nin "software_profile.yaml"'
                               % exe_path,
                               MessageDisplay.CRITICALa)
            elif item.name.lower() in self.app_launchers:
                widget = self.software_commands.itemWidget(item)
                profile_name = widget.comboBox.currentText()
                try:
                    profile_path = item.profiles[profile_name]
                    LOGGING.info('load current profile: %s' % profile_path)
                    if os.path.isdir(profile_path):
                        command = '{0} -lp {1} {2}'.format(exe_path,
                                                           profile_path,
                                                           self.drag_file)
                        LOGGING.info('run launcher: %s' % command)
                        htk.start(command)
                except:
                    LOGGING.error(traceback.format_exc())
                finally:
                    self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            else:
                command = '{0} {1}'.format(exe_path, self.drag_file)
                try:
                    LOGGING.info(command)
                    htk.start(command)
                except:
                    LOGGING.error(traceback.format_exc())
                finally:
                    self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def save_profile(self):
        self.manager.save_local_data(self.manager.data)

    def closeEvent(self, event):
        self.gui_show = False
        self.hide()
        self.tray_icon.showMessage(NAME, 'Running in the background.')
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_name = None
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
            try:
                for url in event.mimeData().urls():
                    file_name = '{0}'.format(url.toLocalFile())
            except UnicodeEncodeError:
                pass

            self.drag_file = file_name
            if os.path.isfile(self.drag_file):
                self.drag_to_run_program()

    def mouseMoveEvent(self, event):
        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except:
            pass

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def launch(self):
        LOGGING.debug(self.manager.data)
        env.HZ_PROJECT_NAME.set(self.comboBox_project_list.currentText())
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        item = self.software_commands.currentItem()
        exe_path = item.path
        if exe_path.startswith('.'):
            exe_path = os.path.normpath(
                exe_path.replace('.', self.wrappers_dir, 1))
        else:
            exe_path = os.path.expandvars(exe_path)
        if not os.path.exists(exe_path):
            LOGGING.error(traceback.format_exc())
            MessageDisplay(NAME,
                           'Not Find \n%s \nin "software_profile.yaml"' % exe_path,
                           MessageDisplay.CRITICAL)

        elif item.name.lower() in self.app_launchers:
            widget = self.software_commands.itemWidget(item)
            profile_name = widget.comboBox.currentText()
            try:
                profile_path = item.profiles[profile_name]
                LOGGING.info('load current profile: %s' % profile_path)
                if os.path.isdir(profile_path):
                    command = '{0} -lp {1}'.format(exe_path, profile_path)
                    LOGGING.info('run launcher: %s' % command)
                    htk.start(command)
            except:
                LOGGING.error(traceback.format_exc())
                MessageDisplay(NAME, traceback.format_exc(),
                               MessageDisplay.CRITICAL)
            finally:
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        else:
            command = '{0}'.format(exe_path)
            try:
                LOGGING.info(command)
                htk.start(command)
            except:
                LOGGING.error(traceback.format_exc())
                MessageDisplay(NAME, traceback.format_exc(),
                               MessageDisplay.CRITICAL)
            finally:
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def icon(self, icon_name, ispath=False):
        icon_path = self.resources.get_icon_resources(icon_name)
        if ispath:
            return icon_path

        return QtGui.QIcon(icon_path)

    def icon_activated(self, reason):
        if reason in (QtWidgets.QSystemTrayIcon.Trigger,
                      QtWidgets.QSystemTrayIcon.DoubleClick):
            if self.gui_show:
                self.close()
            else:
                self.show()
                self.move(
                    self.desktop.availableGeometry().width() - self.width(),
                    self.desktop.availableGeometry().height() - self.height())
                self.gui_show = True

    def set_icon(self, index):
        icon = self.icon_combo_box.itemIcon(0)
        self.tray_icon.setIcon(icon)
        self.setWindowIcon(icon)
        self.tray_icon.setToolTip(self.icon_combo_box.itemText(index))

    def search_software(self):
        result = []
        self.software_commands.clear()
        soft_name = self.search_text.text()
        regularly = '.*?'.join(soft_name.lower())
        regex = re.compile(regularly)
        project_name = self.comboBox_project_list.currentText()

        for app_ in self.manager.applications:
            match = regex.search(app_.name.lower())
            if match:
                result.append((len(match.group()), match.start(), app_))
        if result:
            sorted_result = [x for _, _, x in sorted(result)]
            for app_ in sorted_result:
                icon_name = app_.icon
                app_.project_name = project_name
                if icon_name:
                    image_path = self.icon(icon_name, True)
                else:
                    image_path = self.icon("default_software_icon.png", True)

                if not os.path.isfile(image_path):
                    image_path = self.icon("default_software_icon.png")
                image = QtGui.QIcon(image_path)
                layer_widget = SoftwareManagerItemGUI(app_, self)
                layer_widget.set_icon(image)
                profiles = self.get_profiles(app_.name, project_name)
                if profiles:
                    layer_widget.set_list(profiles.keys())
                    temp_value = om.read(self.local_profile_folder,
                                         '%s_%s' % (project_name, app_.name))
                    if temp_value:
                        layer_widget.set_current_item(temp_value)
                else:
                    layer_widget.set_list([app_.name])
                layer_item = QtWidgets.QListWidgetItem(self.software_commands)
                layer_item.setSizeHint(QtCore.QSize(layer_widget.width() - 10,
                                                    layer_widget.height()))
                layer_item.path = app_.path
                layer_item.name = app_.name
                layer_item.profiles = profiles
                layer_item.setToolTip(u'%s' % app_.description)
                self.software_commands.setItemWidget(layer_item, layer_widget)

    def time_task(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        icon = QtWidgets.QSystemTrayIcon.MessageIcon()
        if text == "17:20:01":
            update_info = QtWidgets.QApplication.translate(
                "ship_console",
                "请大家记得填timeLog",
                None,
                QtWidgets.QApplication.UnicodeUTF8)
            self.tray_icon.showMessage(NAME, update_info, icon,
                                       200000)

    def show_message_for_file(self, msg_file):
        icon = QtWidgets.QSystemTrayIcon.MessageIcon()
        if msg_file:
            with open(msg_file, 'r') as f:
                str_ = f.readlines()
                update_info = QtWidgets.QApplication.translate(
                    "ship_console",
                    "\n".join(str_),
                    None,
                    QtWidgets.QApplication.UnicodeUTF8)
            self.tray_icon.showMessage(NAME, update_info, icon,
                                       200000)

    def show_message(self, msg):
        icon = QtWidgets.QSystemTrayIcon.MessageIcon()
        update_info = QtWidgets.QApplication.translate(
            "ship_console",
            msg,
            None,
            QtWidgets.QApplication.UnicodeUTF8)
        self.tray_icon.showMessage(NAME, update_info, icon,
                                   200000)

    @staticmethod
    def check_update_info():
        g = SoftwareManagerNoteGUI()
        g.check_update()


if __name__ == "__main__":
    APP = QtWidgets.QApplication([])
    APP_NAME = "software_manager"
    CSS_FILE = HZResources.get_css_resources(APP_NAME)
    GUI = SoftwareManagerGUI(HZResources.get_ui_resources(APP_NAME))
    IMAGE_PATH = HZResources.get_icon_resources("HZ.png")
    SPLASH = AwesomeSplashScreen(IMAGE_PATH)
    APP.processEvents()
    SPLASH.showMessage("version: 1.1")
    SPLASH.effect()
    APP.setOrganizationName(APP_NAME)
    APP.setApplicationName(APP_NAME)
    APP.processEvents()
    GUI.show()
    SPLASH.finish(GUI)
    # GUI.check_update_info()
    APP.exec_()
