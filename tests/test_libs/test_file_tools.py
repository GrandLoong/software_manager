import unittest
import os
import pixoConfig
from pixoLibs import pixoFileTools as pft


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


class PixoFileToolTestsPEK(unittest.TestCase):
    old_site = None

    @classmethod
    def setUpClass(cls):
        PixoFileToolTestsPEK.old_site = makeSite("PEK")

    @classmethod
    def tearDownClass(cls):
        restoreSite(PixoFileToolTestsPEK.old_site)

    def test_pek_asset_pathone(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.getFilename()
        print x
        self.assertEqual(x.project, "ants")
        self.assertEqual(x.project_shortname, "ant")
        self.assertEqual(x.seq, "creature")
        self.assertEqual(x.shot, "crt_kingKong")
        self.assertEqual(x.version, "005")
        self.assertEqual(x.task, "mdl")
        self.assertEqual(x.user, "hal")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, os.path.basename(f1))
        response = x.getFullPath()
        self.assertEqual(response, f1)

    def test_pek_comp_path(self):
        f1 = "Y:/impossibletwo_ipt-3444/b020/070/comps/v131/fullres/ipt_b020_070_comp_v131_zxy.1001.exr"
        x = pft.PathDetails.parse_path(f1)
        print x
        self.assertEqual(x.project, "impossibletwo")
        self.assertEqual(x.project_shortname, "ipt")
        self.assertEqual(x.seq, "b020")
        self.assertEqual(x.shot, "070")
        self.assertEqual(x.version, "131")
        self.assertEqual(x.task, "comp")
        self.assertEqual(x.user, "zxy")
        self.assertEqual(x.ext, "exr")
        response = x.getFullPath()
        self.assertEqual(response, f1)




    def test_pek_asset_pathone_publish(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.getPublishFullPath()

        p1 = 'X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/_publish/' \
             'v005/ant_crt_kingKong_mdl_v005_hal.ma'
        p2 = 'X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/_publish/' \
             'v005/ant_crt_kingKong_mdl_playblast_v005_hal.ma'
        self.assertEqual(response, p1)
        response = x.getPublishFullPath(name="playblast")
        self.assertEqual(response, p2)
        x = pft.PathDetails.parse_path(p2)
        response = x.getPublishFullPath(name="playblast")
        self.assertEqual(response, p2)
        response = x.getPublishFullPath()
        self.assertEqual(response, p2)
        response = x.getPublishFullPath(name=None)
        self.assertEqual(response, p1)

    def test_pek_asset_pathone_render(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        f2 = "Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl"
        x = pft.PathDetails.parse_path(f1)
        response = x.getRenderPath()
        self.assertEqual(response, f2)

        p1 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/fullres/ant_crt_kingKong_mdl_playblast_v005_hal.####.exr'

        p2 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/fullres/ant_crt_kingKong_mdl_v005_hal.####.exr'

        x = pft.PathDetails.parse_path(p2)

        response = x.getRenderFullPath(name="playblast")
        self.assertEqual(response, p1)
        response = x.getRenderFullPath()
        self.assertEqual(response, p1)
        response = x.getRenderFullPath(name=None)
        self.assertEqual(response, p2)

        x = pft.PathDetails.parse_path(f1)
        response = x.getRenderFullPath(name="playblast", render_layer="layerssuck", resolution='resolution')
        p1 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/resolution/layerssuck/ant_crt_kingKong_mdl_playblast_v005_hal.layerssuck.####.exr'
        p2 = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/' \
             'v005/resolution/ant_crt_kingKong_mdl_playblast_v005_hal.####.exr'
        proxy = 'Y:/ants_ant-3629/_library/assets/creature/crt_kingKong/renders/mdl/v005' \
                '/resolution/ant_crt_kingKong_mdl_playblast_v005_hal.mov'\

        self.assertEqual(response, p1)
        y = pft.PathDetails.parse_path(p1)
        response = y.getRenderFullPath(name="playblast", render_layer=None)
        self.assertEqual(response, p2)

        response = y.getRenderProxyObject("playblast")
        r2 = response.getFullPath()
        self.assertEqual(r2, proxy)

    def test_pek_shots_pathone_render(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"
        p1 = "Y:/icefantasy_icf-3595/000/animpipe/elements/3d/anim/v004/fullres/icf_000_animpipe_anim_beauty_v004_car.####.exr"
        x = pft.PathDetails.parse_path(f1)
        response = x.getRenderFullPath(name="beauty")
        self.assertEqual(response, p1)

    def test_pek_version_up(self):
        f1 = "X:/icefantasy_icf-3595/_library/assets/creature/crt_iceBird/cgfx_fur/icf_crt_iceBird_cgfx_fur_v071_mil.ma"
        x = pft.PathDetails.parse_path(f1)
        self.assertEqual(x.shot, "crt_iceBird")
        self.assertEqual(x.task, "cgfx_fur")

    def test_pek_shots_pathone(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.getFullPath()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.version, "004")
        self.assertEqual(x.task, "anim")
        self.assertEqual(x.user, "car")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.getFilename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_asset_pathtwo(self):
        f1 = "X:/ants_ant-3629/_library/assets/characters/chr_DXDaily/mdl/ant_chr_DXDaily_mdl_v002.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.getFullPath()
        self.assertEqual(x.project, "ants")
        self.assertEqual(x.project_shortname, "ant")
        self.assertEqual(x.seq, "characters")
        self.assertEqual(x.shot, "chr_DXDaily")
        self.assertEqual(x.version, "002")
        self.assertEqual(x.task, "mdl")
        self.assertEqual(x.user, "bdl")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.getFilename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_shots_pathtwo(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/cgfx_lingering-dust-slap/icf_000_animpipe_cgfx_lingering-dust-slap_v004_car.ma"
        x = pft.PathDetails.parse_path(f1)
        response = x.getFullPath()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.version, "004")
        self.assertEqual(x.task, "cgfx_lingering-dust-slap")
        self.assertEqual(x.user, "car")
        self.assertEqual(x.ext, "ma")
        self.assertEqual(response, f1)
        response = x.getFilename()
        self.assertEqual(response, os.path.basename(f1))

    def test_pek_shots_paththree(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/cgfx_lingering-dust-slap"
        x = pft.PathDetails.parse_path(f1)
        response = x.getPath()
        self.assertEqual(x.project, "icefantasy")
        self.assertEqual(x.project_shortname, "icf")
        self.assertEqual(x.seq, "000")
        self.assertEqual(x.shot, "animpipe")
        self.assertEqual(x.task, "cgfx_lingering-dust-slap")
        self.assertEqual(response, f1)

    def test_pek_asset_deconstructFilepath(self):
        f1 = "X:/ants_ant-3629/_library/assets/creature/crt_kingKong/mdl/ant_crt_kingKong_mdl_v005_hal.ma"
        root, show, seq, shot, category, task, filename = pft.deconstructFilepath(f1)

        self.assertEqual(root, "X:")
        self.assertEqual(show, "ants_ant-3629")
        self.assertEqual(seq, "creature")
        self.assertEqual(shot, "crt_kingKong")
        self.assertEqual(task, "mdl")
        self.assertEqual(category, "assets")
        self.assertEqual(filename, "ant_crt_kingKong_mdl_v005_hal.ma")

        response = pft.constructFilepath(root, show, seq, shot, category, task, filename)
        r2 = pft.constructFilename("ant", seq, shot, task, "v005", "hal", "ma", category)
        self.assertEqual(response, f1)
        self.assertEqual(r2, os.path.basename(f1))


    def test_pek_shots_deconstructFilepath(self):
        f1 = "X:/icefantasy_icf-3595/000/animpipe/3d/anim/icf_000_animpipe_anim_v004_car.ma"

        root, show, seq, shot, category, task, publish = pft.deconstructFilepath(f1)
        self.assertEqual(show, "icefantasy_icf-3595")
        self.assertEqual(seq, "000")
        self.assertEqual(shot, "animpipe")
        self.assertEqual(task, "anim")
        self.assertEqual(category, "3d")
        self.assertEqual(publish, 'icf_000_animpipe_anim_v004_car.ma')

        response = pft.constructFilepath(root, show, seq, shot, category, task, publish)
        self.assertEqual(response, f1)

    def test_pek_comp_parseeye(self):
        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj_R.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_R.0960.exr"
             ]
        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals("R", result.eye)

        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj_L.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_L.0960.exr"
             ]

        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals("L", result.eye)

        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal.0960.exr"
             ]

        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals(None, result.eye)

    def test_pek_comp_parse(self):
        f = ['Y:/impossibletwo_ipt-3444/b010/020/comps/v139/fullres/ipt_b010_020_comp_v139_dlj.0950.exr',
             # "Y:/impossibletwo_ipt-3444/b010/020/elements/2d/comp_pre_without_lens/v170/fullres/ipt_b010_020_comp-pre_without_lens_v170_dlj.0960.exr",
             "Y:/impossibletwo_ipt-3444/b010/020/elements/3d/cgfx/v131/fullres/ipt_b010_020_cgfx_splosionAmaskB_v131_hal_R.0960.exr"
             ]
        for p in f:
            result = pft.PathDetails.parse_path(p)
            self.assertEquals(p, result.getFullPath())
    """
    def test_version_up(self):

        temp_path = tempfile.mkdtemp()
        print temp_path
        files = [
                 "test_v001_ben.ma",
                 "test_v002_blah.ma",
                 "test_v002_bob.ma",
                 "test_v003_blah.ma"
                 ]
        for x in files:
            pft.touch(os.path.join(temp_path, x))

        result = pft.getLatestVersionNumber(temp_path)
        self.assertEquals(result, "003")


    def test_incremental_version_up(self):

        temp_path = tempfile.mkdtemp()
        print temp_path
        files = [
            "test_v001_ben.ma",
            "test_v002_blah.ma",
            "test_v002-001_blah.ma",
            "test_v002-002_blah.ma",
            "test_v002_bob.ma",
            "test_v003_blah.ma",
            "test_v003-001_blah.ma"
        ]
        for x in files:
            pft.touch(os.path.join(temp_path, x))

        result = pft.getLatestVersionNumber(temp_path)
        self.assertEquals(result, "004")
    """


class PixoFileToolTestsSHX(unittest.TestCase):
    old_site = None

    @classmethod
    def setUpClass(cls):
        PixoFileToolTestsSHX.old_site = makeSite("SHX")

    @classmethod
    def tearDownClass(cls):
        restoreSite(PixoFileToolTestsSHX.old_site)

    def test_shx_asset_deconstructFilepath(self):
        f1 = "Z:/Shotgun/projects/df/_library/assets/Character/BigFish/mdl/df_BigFish_mdl_v002_hal.mb"

        root, show, seq, shot, category, task, publish = pft.deconstructFilepath(f1)
        self.assertEqual(show, "df")
        self.assertEqual(seq, "Character")
        self.assertEqual(shot, "BigFish")
        self.assertEqual(task, "mdl")
        self.assertEqual(category, "assets")
        response = pft.constructFilepath(root, show, seq, shot, category, task, publish)
        self.assertEqual(response, f1)

    def test_shx_shots_deconstructFilepath(self):
        f1 = "Z:/Shotgun/projects/df/014/001/3d/cfx/df_014_001_cfx_v005_wtf.mb"
        root, show, seq, shot, category, task, filename = pft.deconstructFilepath(f1)
        self.assertEqual(show, "df")
        self.assertEqual(seq, "014")
        self.assertEqual(shot, "001")
        self.assertEqual(task, "cfx")
        self.assertEqual(filename, 'df_014_001_cfx_v005_wtf.mb')

        response = pft.constructFilepath(root, show, seq, shot, category, task, filename)
        self.assertEqual(response, f1)

    def test_shx_shots_pathone(self):
        f1 = "Z:/Shotgun/projects/df/014/001/3d/cfx/df_014_001_cfx_v005_ben.mb"

        x = pft.PathDetails.parse_path(f1)
        response = x.getFullPath()
        self.assertEqual(response, f1)
        response = x.getFilename()
        self.assertEqual(response, os.path.basename(f1))

    def test_render_playblast(self):
        x = "Z:/Shotgun/projects/df/000/020/3d/lgt/_renders/v005/df_000_020_lgt_v005_tmk.mov"
        obj = pft.PathDetails.parse_path(x)
        self.assertEqual(obj.task, "lgt")
        self.assertEqual(obj.render_layer, None)
        self.assertEqual(obj.aov, None)
        self.assertEqual(obj.version, "005")
        self.assertEqual(obj.getFullPath(), x)
    
    def test_render_aov(self):
        x = "Z:/Shotgun/projects/df/000/020/3d/lgt/_renders/v004/masterLayer/beauty/df_000_020_lgt_v004_tmk.0001.exr"
        obj = pft.PathDetails.parse_path(x)
        self.assertEqual(obj.task, "lgt")
        self.assertEqual(obj.render_layer, "masterLayer")
        self.assertEqual(obj.aov, "beauty")
        self.assertEqual(obj.version, "004")
        self.assertEqual(obj.getFullPath(), x)

    def test_render_with_comp(self):
        x = "Z:/Shotgun/projects/df/000/020/2d/comp/_renders/v003/output/df_000_020_comp_v003_tmk.0001.exr"
        obj = pft.PathDetails.parse_path(x)
        self.assertEqual(obj.task, "comp")
        self.assertEqual(obj.render_layer, "output")
        self.assertEqual(obj.aov, None)
        self.assertEqual(obj.version, "003")

        self.assertEqual(obj.getFullPath(), x)
 
 
    # playblast = Z:\Shotgun\projects\df\000\020\3d\lgt\_renders\v005\df_000_020_lgt_v005_tmk.mov
    # render_no.rl_noAOV = Z:\Shotgun\projects\df\000\020\3d\lgt\_renders\v004\masterLayer\beauty\df_000_020_lgt_v004_tmk.0001.exr
    # render_rl_aov = Z:\Shotgun\projects\df\000\020\3d\lgt\_renders\v003\masterLayer\beauty\df_000_020_lgt_v003_tmk.0001.exr
    # render_comp = Z:\Shotgun\projects\df\000\020\2d\comp\_renders\v003\output\df_000_020_cmp_v003_tmk.0001.exr

    def test_shx_asset_pathone(self):
        f1 = "Z:/Shotgun/projects/df/_library/assets/Character/BigFish/mdl/df_BigFish_mdl_v002_hal.mb"

        x = pft.PathDetails.parse_path(f1)
        response = x.getFilename()
        self.assertEqual(x.version, "002")
        self.assertEqual(response, os.path.basename(f1))
        response = x.getFullPath()
        self.assertEqual(response, f1)

    def test_shx_asset_pathtwo(self):
        f1 = "Z:/Shotgun/projects/df/_library/assets/Character/DouShouDaily/mdl/df_DouShouDaily_mdl_v056.mb"
        x = pft.PathDetails.parse_path(f1)
        print x
        response = x.getFilename()
        self.assertEqual(x.version, "056")
        self.assertEqual(response, os.path.basename(f1))
        response = x.getFullPath()
        self.assertEqual(response, f1)

    def test_shx_shot2_pathone(self):
        xml_file = 'Z:/Shotgun/projects/df/007/006/3d/lay/_publish/v005/df_007_006_lay_v005_tmk.xml'
        dets = pft.PathDetails.parse_path(xml_file)
        p = dets.getFullPath()
        print dets
        self.assertEqual(xml_file, p)


if __name__ == '__main__':
    unittest.main()
