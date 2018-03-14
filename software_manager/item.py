# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""

import hz.awesome_ui.css as awesome_css
import openmetadata as om
from Qt import QtWidgets, QtGui, QtCore
from hz.awesome_ui.widgets import RenderAwesomeUI
from hz.resources import HZResources


class SoftwareManagerItemGUI(QtWidgets.QWidget):
    def __init__(self, app, parent):
        name = "software_manager_item"
        super(SoftwareManagerItemGUI, self).__init__()
        ui_file = HZResources.get_ui_resources(name)
        RenderAwesomeUI(ui_file, parent_widget=self)
        self.app = app
        self.parent = parent
        self.comboBox.activated.connect(self.save_current_name)
        self.pushButton.clicked.connect(self.parent.launch)
        open_hand_cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.setCursor(open_hand_cursor)
        awesome_css.set_style_sheet(self, HZResources.get_css_resources(name))

    def save_current_name(self, value):
        om.write(self.parent.local_profile_folder,
                 '%s_%s' % (self.app.project_name, self.app.name), value)

    def set_icon(self, image):
        self.pushButton.setIcon(image)

    def set_list(self, list_):
        self.comboBox.addItems(list_)

    def set_current_item(self, value):
        self.comboBox.setCurrentIndex(value)
