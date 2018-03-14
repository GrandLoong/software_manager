# -*- coding: utf-8 -*-
"""
module author: Long Hao <hoolongvfx@gmail.com>
"""
import glob
import logging
import os

import hz.toolkit as htk
from hz.config import HZConfig

__all__ = ['SoftwareManager']


class _Application(object):
    def __init__(self, data):
        self.data = data
        self.project_name = None

    @property
    def name(self):
        return self.data['name']

    @property
    def path(self):
        return os.path.expandvars(self.data['path'])

    @property
    def icon(self):
        return os.path.expandvars(self.data['icon'])

    @property
    def order(self):
        return self.data['order']

    @property
    def description(self):
        return self.data['description']


class SoftwareManager(object):
    def __init__(self, project_name):
        self.settings = HZConfig('softwareManager',
                                 project_name=project_name,
                                 ext="app")
        user_settings_path = self.settings.get_user_settings_path()
        self.local_data_file = htk.pathjoin(user_settings_path,
                                            'software_profile.yaml')
        logging.info('local file:%s' % self.local_data_file)
        self.data = {}
        self.applications = []
        self.update_app()
        self.build_app = _Application
        for d in self.sort_data():
            self.applications.append(self.build_app(self.data[d]))

    def update_app(self):
        self.data.update(self.global_data)
        self.data.update(self.local_data)

    @property
    def global_data(self):
        all_data = {}
        for d in self.settings.glob_files():
            for app_name in glob.glob("%s/*.app" % d):
                name = os.path.basename(app_name).replace('.app', '')
                data = self.settings.query(name, "application")
                all_data.update({name: data})
                logging.info('load global profile data: \n%s' % data)
        return all_data

    @property
    def local_data(self):
        data = {}
        if os.path.isfile(self.local_data_file):
            data = htk.load_yaml(self.local_data_file)['application']
            logging.info('load local profile data: \n%s' % data)
        return data

    def save_local_data(self, data):
        temp = data.copy()
        for k in self.local_data.keys():
            try:
                data.pop(k)
            except KeyError:
                pass
        temp_data = {'application': temp}
        htk.dump_ymal(self.local_data_file, temp_data)
        logging.info('save profile to local: \n%s' % temp_data)

    def sort_data(self):
        for btn in self.data:
            if 'order' not in self.data[btn]:
                self.data[btn]['order'] = 10
        if self.data:
            return sorted(self.data, key=lambda key: self.data[key]['order'])
