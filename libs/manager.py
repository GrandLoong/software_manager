import os
from os.path import join as pathjoin
from .dependencies import yaml

import config


class Manager:
    def __init__(self):
        self.global_data_file = pathjoin(config.APP_DIR, "config/software_profile.yaml")
        self.local_data_file = pathjoin(config.get_local_profile_dir(), 'software_profile.yaml')
        self.global_data = self.get_global_data()
        self.local_data = self.get_local_data()

    def get_global_data(self):
        return yaml.load(file(self.global_data_file))['application']

    def get_local_data(self):
        if os.path.isfile(self.local_data_file):
            return yaml.load(file(self.local_data_file))['application']
        return {}

    def save_local_data(self, data):
        temp = data.copy()
        for k in self.get_global_data().keys():
            try:
                data.pop(k)
            except KeyError:
                pass
        temp_data = {'application': temp}
        with open(self.local_data_file, 'w') as f:
            yaml.safe_dump(temp_data, f, default_flow_style=False)
        print temp_data

    @staticmethod
    def sort_data(datas):
        for btn in datas:
            if 'order' not in datas[btn]:
                datas[btn]['order'] = 10
        if datas:
            return sorted(datas, key=lambda key: datas[key]['order'])
        else:
            return {}
if __name__ == '__main__':
    m = Manager()
    print m.global_data
    print m.local_data
