import os

import numpy as np
import pytest

from lephare import flt
from lephare.filterSvc import FilterSvc

test_dir = os.path.abspath(os.path.dirname(__file__))
test_data_dir = os.path.join(test_dir, "../data")

filter_file = os.path.join(test_data_dir, "filt/subaru/IB527.pb")


def test_flt_class():
    tophat = flt(100.0, 200.0, 50)
    assert tophat.name == ""
    # this is wrong but an effect of improper C++ code
    assert tophat.width() == 101.0
    #
    f = flt(-1, filter_file, trans=1, calib=1)
    assert f.width() == pytest.approx(241.9479, 1.0e-4)
    assert f.lambdaMean() == pytest.approx(5262.2831, 1.0e-4)


def test_filtersvc():
    f = FilterSvc.from_file(filter_file, trans=1, calib=0)
    assert f.width() == pytest.approx(241.9479, 1.0e-4)
    assert f.lambdaMean() == pytest.approx(5262.2831, 1.0e-4)

    g = FilterSvc.from_svo(-1, "Subaru/Suprime.IB527", "AB")
    if g is not None:
        assert np.allclose(f.data()[1], g.data()[1])
    else:
        print("SVO not tested due to exception raised : server not reachable?")
    #
    fltvec = FilterSvc.from_config(os.path.join(test_data_dir, "examples/COSMOS.para"))
    assert len(fltvec) == 30