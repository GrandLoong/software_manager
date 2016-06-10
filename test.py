a = {'application': {
    '3ds Max 2014': {'department': '', 'path': 'C:/Users/Public/Desktop/3ds Max 2014.lnk', 'describe': '3ds Max 2014',
                     'icon': 'default_software_icon.png'},
    'Houdini FX 151': {'department': '', 'path': 'C:/Users/Public/Desktop/Houdini FX 151.0.377.lnk',
                       'describe': 'Houdini FX 151', 'icon': 'default_software_icon.png'},
    'Sublime Text 3': {'department': '', 'path': 'C:/Users/hao.long/Desktop/Sublime Text 3.lnk',
                       'describe': 'Sublime Text 3', 'icon': 'default_software_icon.png'},
    'JetBrains PyCharm 2016': {'department': '', 'path': 'C:/Users/Public/Desktop/JetBrains PyCharm 2016.1.4(64).lnk',
                               'describe': 'JetBrains PyCharm 2016', 'icon': 'default_software_icon.png'}}}
b = {'application': 'test'}

import yaml
f = open('c:/test.yaml', 'w')
yaml.safe_dump(a, f)
f.close()

