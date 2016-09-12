import unittest
import os
import pixoConfig
import pixoLibs.pixoFileTools as pft


def makeSite(site):
    pixoConfig.PixoConfig.data = None
    pft.PathDetails.datare = None
    pft.PathDetails.path_strings = None

    f = pixoConfig.PixoConfig.get_local_site_filepath()
    old_value = None
    if os.path.exists(f):
        with open(f) as file_stream:
            old_value = file_stream.read()

    with open(f, "w") as file_stream:
        file_stream.write(site)
    return old_value


def restoreSite(site):
    f = pixoConfig.PixoConfig.get_local_site_filepath()
    if site is None:
        os.remove(f)
    else:
        with open(f, "w") as file_stream:
            file_stream.write(site)


class PicoConfigPEK(unittest.TestCase):
    old_site = None

    @classmethod
    def setUpClass(cls):
        PicoConfigPEK.old_site = makeSite("PEK")

    @classmethod
    def tearDownClass(cls):
        restoreSite(PicoConfigPEK.old_site)

    def test_project_settings_str(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        response = pixoConfig.ProjectSettings.get(f1, "test/var1")
        self.assertEqual(response, 123)
        response = pixoConfig.ProjectSettings.get(f1, "test/var2")
        self.assertEqual(response, "abc")
        response = pixoConfig.ProjectSettings.get(f1, "test")
        self.assertEqual(response, {'var1': 123,
                                    'var2': 'abc'})


class PicoConfigSHX(unittest.TestCase):
    old_site = None

    @classmethod
    def setUpClass(cls):
        PicoConfigSHX.old_site = makeSite("SHX")

    @classmethod
    def tearDownClass(cls):
        restoreSite(PicoConfigSHX.old_site)


if __name__ == '__main__':
    unittest.main()
