import pytest
from os import listdir, getcwd
from os.path import isfile, join, basename, dirname, abspath

def test_all_config_files(default_config):
    default = default_config
    path = default.config_location
    config_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    for f in config_files:
        assert(default.check_file_valid(f))
