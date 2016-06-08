import os
from os.path import join as pathjoin
import yaml

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
        for k in self.get_global_data().keys():
            try:
                data.pop(k)
            except KeyError:
                pass
        temp_data = {'application': data}
        with open(self.local_data_file, 'w') as f:
            yaml.safe_dump(temp_data, f)
        print temp_data


if __name__ == '__main__':
    m = Manager()
    print m.global_data
    print m.local_data
    print 'a'
