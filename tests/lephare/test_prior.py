import os

import lephare as lp
import numpy as np
from astropy.table import Table


def test_prior(test_data_dir: str):
    test_dir = os.path.abspath(os.path.dirname(__file__))
    os.environ["LEPHAREDIR"] = os.path.join(test_dir, "../data")
    os.environ["LEPHAREWORK"] = os.path.join(test_dir, "../tmp")
    # Read the config file.
    config_file = os.path.join(test_data_dir, "examples/COSMOS.para")
    config = lp.read_config(config_file)
    # Run preparation tasks.
    lp.prepare(config)
    # Read the test input catalogue
    input_file = os.path.join(test_data_dir, "examples/COSMOS_first100specz.fits")
    input = Table.read(input_file)
    # Make a reduced column set for the minimal test
    reduced_cols = []
    for c in input.colnames:
        if not c.startswith("f"):
            reduced_cols.append(c)
        elif "IB527" in c:
            reduced_cols.append(c)
        elif "IB679" in c:
            reduced_cols.append(c)

    # initialise the prior
    def example_prior(lib, obj):
        """An example prior which prohibits redshift above 2"""
        weight = 1.0  # Be default do not change prior
        if lib.red > 2:
            weight = 1.0e-9
        return weight

    output, pdfs, zgrid = lp.process(config, input[reduced_cols], prior=example_prior)
    # Check one of the outputs (results are terrible with just one filter and sparse z grid)
    assert ~np.isclose(output["Z_BEST"][0], 3.58577857627795)  # Should not equal the original redshift
    assert len(zgrid) == 51
    assert np.sum(output["Z_BEST"] > 2) == 0


def test_absmag_prior():
    p = lp.prior()
    s = lp.onesource(0, [0, 1])
    assert np.isclose(p.absmag_prior(s, 0.0, 0.0, 0, 0.0, 0.0, 0.0), 1000000000.0)
