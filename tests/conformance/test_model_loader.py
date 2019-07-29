import pytest
import mock
import os
from toggle.core.ModelLoader import ModelLoader, ModelFile


def test_model_loader_sync(default_config):
  default_config.set("System", "model_folder", "./")
  default_config.rest_client = DummyRestClient()
  loader = ModelLoader(default_config)
  loader.sync_models()
  assert (loader.models.count() == 11)


def test_file_model(default_config):
  default_config.rest_client = DummyRestClient()
  file = get_dummy_file()
  if not os.path.isdir("./tmp-pytest"):
    os.mkdir("./tmp-pytest")
  default_config.set("System", "model_folder", "./tmp-pytest")
  m = ModelFile(file, default_config)
  m.add_stl_url("test")
  assert (m.get_stl_name() == "Dolf-Lundgren.stl")
  assert (m.get_name() == "Dolf-Lundgren.gco")
  assert (m.has_stl())
  assert (m.get_stl_hash() == file['links'][0]['hash'])
  assert (m.is_local_machinecode())
  assert (m.get_stl_path() == "./tmp-pytest/Dolf-Lundgren.stl")
  if os.path.isfile("./tmp-pytest/Dolf-Lundgren.stl"):
    os.remove("./tmp-pytest/Dolf-Lundgren.stl")
  assert (m.download_stl())
  assert (m.is_stl_available_locally() == True)
  with open("./tmp-pytest/Dolf-Lundgren.stl") as f:
    assert (f.read() == "Bruce Willis")
  if os.path.isfile("./tmp-pytest/Dolf-Lundgren.stl"):
    os.remove("./tmp-pytest/Dolf-Lundgren.stl")
  if os.path.isdir("./tmp-pytest"):
    os.rmdir("./tmp-pytest")


def get_dummy_file():
  return {
      'display':
          'Dolf-Lundgren.gco',
      'hash':
          '4d80ca23ce7ffa1ede4cf165dd00fc440741cf1c',
      'links': [{
          'hash': '23d9e81c835090eabe405b129f8dba531fe5883e',
          'name': 'Dolf-Lundgren.stl',
          'rel': 'model'
      }],
      'name':
          'Dolf-Lundgren.gco',
      'origin':
          'local',
      'type':
          'machinecode',
      'typePath': ['machinecode', 'gcode']
  }


class DummyRestClient:
  def download_model(self, url):
    return bytes(b"Bruce Willis")

  def get_list_of_files(self):
    return {
        'files': [
            {
                'display':
                    'Motor-bottom-back.gco',
                'hash':
                    '4d80ca23ce7ffa1ede4cf165dd00fc440741cf1c',
                'links': [{
                    'hash': '23d9e81c835090eabe405b129f8dba531fe5883e',
                    'name': 'Motor-bottom-back.stl',
                    'rel': 'model'
                }],
                'name':
                    'Motor-bottom-back.gco',
                'origin':
                    'local',
                'path':
                    'Motor-bottom-back.gco',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/Motor-bottom-back.gco',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/Motor-bottom-back.gco'
                },
                'size':
                    3065879,
                'type':
                    'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'date': 1564177863,
                'display': 'Effector-base_0.3mm_PLA_MK3_27m.gcode',
                'hash': '7ff2c73315e5b6cace66ae7212b1fb7c4ccd4761',
                'name': 'Effector-base_0.3mm_PLA_MK3_27m.gcode',
                'origin': 'local',
                'path': 'Effector-base_0.3mm_PLA_MK3_27m.gcode',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/Effector-base_0.3mm_PLA_MK3_27m.gcode',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/Effector-base_0.3mm_PLA_MK3_27m.gcode'
                },
                'size': 928155,
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'date': 1564148857,
                'display': 'FlowSupport_0.2mm_PLA_MK3S_47m.gcode',
                'hash': '60f07248e6019a0be489accf74636ccd8d74acd6',
                'name': 'FlowSupport_0.2mm_PLA_MK3S_47m.gcode',
                'origin': 'local',
                'path': 'FlowSupport_0.2mm_PLA_MK3S_47m.gcode',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/FlowSupport_0.2mm_PLA_MK3S_47m.gcode',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/FlowSupport_0.2mm_PLA_MK3S_47m.gcode'
                },
                'size': 2572211,
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'date':
                    1564353110,
                'display':
                    'Motor-bottom-back.stl',
                'hash':
                    '23d9e81c835090eabe405b129f8dba531fe5883e',
                'links': [{
                    'hash': '4d80ca23ce7ffa1ede4cf165dd00fc440741cf1c',
                    'name': 'Motor-bottom-back.gco',
                    'rel': 'machinecode'
                }],
                'name':
                    'Motor-bottom-back.stl',
                'origin':
                    'local',
                'path':
                    'Motor-bottom-back.stl',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/Motor-bottom-back.stl',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/Motor-bottom-back.stl'
                },
                'size':
                    205084,
                'type':
                    'model',
                'typePath': ['model', 'stl']
            },
            {
                'date':
                    1564354511,
                'display':
                    'calibration-cube.gco',
                'hash':
                    '038e55f72e7cc685eefcac771df948807954243c',
                'links': [{
                    'hash': 'ffead561c4a9bcfb4d2808dad1b7e31b81ddca25',
                    'name': 'calibration-cube.stl',
                    'rel': 'model'
                }],
                'name':
                    'calibration-cube.gco',
                'origin':
                    'local',
                'path':
                    'calibration-cube.gco',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/calibration-cube.gco',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/calibration-cube.gco'
                },
                'size':
                    89289,
                'type':
                    'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'date': 1564177884,
                'display': 'NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                'hash': 'd819511a9c3c3c301bf882d98b94a9c1e205650f',
                'name': 'NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                'origin': 'local',
                'path': 'NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/NewEffector_0.2mm_PLA_MK3S_2h16m.gcode'
                },
                'size': 5420175,
                'statistics': {
                    'averagePrintTime': {},
                    'lastPrintTime': {}
                },
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'date': 1564353077,
                'display': 'Effector-base.stl',
                'hash': '13ac807e74b65d066caf7343f0493d6bf5691daa',
                'name': 'Effector-base.stl',
                'origin': 'local',
                'path': 'Effector-base.stl',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/Effector-base.stl',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/Effector-base.stl'
                },
                'size': 141684,
                'type': 'model',
                'typePath': ['model', 'stl']
            },
            {
                'date':
                    1564354472,
                'display':
                    'calibration-cube.stl',
                'hash':
                    'ffead561c4a9bcfb4d2808dad1b7e31b81ddca25',
                'links': [{
                    'hash': '038e55f72e7cc685eefcac771df948807954243c',
                    'name': 'calibration-cube.gco',
                    'rel': 'machinecode'
                }],
                'name':
                    'calibration-cube.stl',
                'origin':
                    'local',
                'path':
                    'calibration-cube.stl',
                'refs': {
                    'download':
                        'http://kamikaze.local:5000/downloads/files/local/calibration-cube.stl',
                    'resource':
                        'http://kamikaze.local:5000/api/files/local/calibration-cube.stl'
                },
                'size':
                    684,
                'type':
                    'model',
                'typePath': ['model', 'stl']
            },
            {
                'display': 'lcl/effector-base_0.3mm_pla_mk3_27m.gcode',
                'name': 'lcl/effector-base_0.3mm_pla_mk3_27m.gcode',
                'origin': 'sdcard',
                'path': 'lcl/effector-base_0.3mm_pla_mk3_27m.gcode',
                'refs': {
                    'resource':
                        'http://kamikaze.local:5000/api/files/sdcard/lcl/effector-base_0.3mm_pla_mk3_27m.gcode'
                },
                'size': 928155,
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'display': 'lcl/flowsupport_0.2mm_pla_mk3s_47m.gcode',
                'name': 'lcl/flowsupport_0.2mm_pla_mk3s_47m.gcode',
                'origin': 'sdcard',
                'path': 'lcl/flowsupport_0.2mm_pla_mk3s_47m.gcode',
                'refs': {
                    'resource':
                        'http://kamikaze.local:5000/api/files/sdcard/lcl/flowsupport_0.2mm_pla_mk3s_47m.gcode'
                },
                'size': 2572211,
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            },
            {
                'display': 'lcl/neweffector_0.2mm_pla_mk3s_2h16m.gcode',
                'name': 'lcl/neweffector_0.2mm_pla_mk3s_2h16m.gcode',
                'origin': 'sdcard',
                'path': 'lcl/neweffector_0.2mm_pla_mk3s_2h16m.gcode',
                'refs': {
                    'resource':
                        'http://kamikaze.local:5000/api/files/sdcard/lcl/neweffector_0.2mm_pla_mk3s_2h16m.gcode'
                },
                'size': 5420175,
                'type': 'machinecode',
                'typePath': ['machinecode', 'gcode']
            }
        ],
        'free':
            1313705984,
        'total':
            3660771328
    }
