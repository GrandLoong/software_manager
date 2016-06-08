import urllib2
from PXM_GlobalLibraries.PXM_Pipeline.pxm_shotgun2 import Shotgun

sg = Shotgun('https://pixomondovfx.shotgunstudio.com', "pxm_pipeline", "5e7dd61a5f31bcebb968bd6f351f8ac5f3df6f0a")


def findUserByName(name):
    """
    find a user by name

    Args:
        name (basestring): username to search for

    Returns:
        dict: shotgun dict for a HumanUser

    """
    userInfo = sg.find_one('HumanUser', [['login', 'contains', name]],
                           ['code', 'name', 'sg_abbreviation', 'id', 'login', 'image'])
    return userInfo


def download_url(thumbnail_url, thumbnail_file):
    response = urllib2.urlopen(thumbnail_url)
    with open(thumbnail_file, 'wb') as output:
        output.write(response.read())




# import tempfile
# (_, thumbnail_file) = tempfile.mkstemp(suffix=".jpg")
#
# download_url(findUserByName('hao.long').get('image'),thumbnail_file)