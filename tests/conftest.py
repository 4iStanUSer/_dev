import os
from pytest import fixture
import distutils

import pytest

TEST_FILES_FOLDER = 'expected'


@fixture
def datadir(tmpdir, request):
    par_path = os.path.dirname(request.module.__file__)
    short_name, _ = os.path.splitext(os.path.basename(request.module.__file__))
    data_folder = os.path.join(par_path, TEST_FILES_FOLDER, short_name)
    if os.path.isdir(data_folder):
        distutils.dir_util.copy_tree(data_folder, str(tmpdir))
    return tmpdir
