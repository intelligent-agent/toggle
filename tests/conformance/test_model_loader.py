import pytest
import mock
from toggle.core.ModelLoader import ModelLoader


def test_model_loader_sync(default_config):
  default_config.style = mock.Mock()
  default_config.style.file_base = ""
  default_config.rest_client = DummyRestClient()
  loader = ModelLoader(default_config)
  loader.sync_models()
  assert (loader.models.count() == 8)


class DummyRestClient:
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
                'gcodeAnalysis': {
                    'dimensions': {
                        'depth': 62.293,
                        'height': 11.700000000000001,
                        'width': 62.334
                    },
                    'estimatedPrintTime': 1896.8810937668425,
                    'filament': {
                        'tool0': {
                            'length': 1803.3530900000535,
                            'volume': 4.337572502332163
                        }
                    },
                    'printingArea': {
                        'maxX': 31.168,
                        'maxY': 31.144,
                        'maxZ': 12.05,
                        'minX': -31.166,
                        'minY': -31.149,
                        'minZ': 0.35
                    }
                },
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
                'gcodeAnalysis': {
                    'dimensions': {
                        'depth': 128.559,
                        'height': 16.0,
                        'width': 156.312
                    },
                    'estimatedPrintTime': 1841.9913320970074,
                    'filament': {
                        'tool0': {
                            'length': 2556.0312600001544,
                            'volume': 6.147975662646172
                        }
                    },
                    'printingArea': {
                        'maxX': 156.312,
                        'maxY': 125.559,
                        'maxZ': 16.0,
                        'minX': 0.0,
                        'minY': -3.0,
                        'minZ': 0.0
                    }
                },
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
                'gcodeAnalysis': {
                    'filament': {
                        'tool0': {
                            'length': 622.4,
                            'volume': 4.4
                        }
                    }
                },
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
                'gcodeAnalysis': {
                    'dimensions': {
                        'depth': 137.779,
                        'height': 33.0,
                        'width': 158.646
                    },
                    'estimatedPrintTime': 4568.441229889911,
                    'filament': {
                        'tool0': {
                            'length': 6138.08521000173,
                            'volume': 14.763825105306722
                        }
                    },
                    'printingArea': {
                        'maxX': 158.646,
                        'maxY': 134.779,
                        'maxZ': 33.0,
                        'minX': 0.0,
                        'minY': -3.0,
                        'minZ': 0.0
                    }
                },
                'hash': 'd819511a9c3c3c301bf882d98b94a9c1e205650f',
                'name': 'NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                'origin': 'local',
                'path': 'NewEffector_0.2mm_PLA_MK3S_2h16m.gcode',
                'prints': {
                    'failure': 1,
                    'last': {
                        'date': 1564178531.361719,
                        'success': False
                    },
                    'success': 0
                },
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
