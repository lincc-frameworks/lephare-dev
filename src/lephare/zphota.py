import time

import numpy as np

from lephare._lephare import (  # , read_lib, read_doc_filters, readOutKeywords, GalMag, bestFilter, maxkcolor
    GalMag,
    PhotoZ,
    keyword,
)
from lephare.runner import Runner

__all__ = [
    "Zphota",
]

global zphota_config_keys
zphota_config_keys = [
    "CAT_IN",
    "INP_TYPE",
    "CAT_MAG",
    "CAT_FMT",
    "CAT_LINES",
    "ZPHOTLIB",
    "PARA_OUT",
    "CAT_OUT",
    "CAT_TYPE",
    "ERR_SCALE",
    "ERR_FACTOR",
    "BD_SCALE",
    "GLB_CONTEXT",
    "FORB_CONTEXT",
    "MASS_SCALE",
    "MAG_ABS",
    "MAG_ABS_AGN",
    "MAG_REF",
    "NZ_PRIOR",
    "ZFIX",
    "Z_INTERP",
    "Z_METHOD",
    "DZ_WIN",
    "MIN_THRES",
    "PROB_INTZ",
    "SPEC_OUT",
    "FIR_LIB",
    "FIR_LMIN",
    "FIR_CONT",
    "FIR_SCALE",
    "FIR_FREESCALE",
    "FIR_SUBSTELLAR",
    "MABS_METHOD",
    "MABS_CONTEXT",
    "MABS_REF",
    "MABS_FILT",
    "MABS_ZBIN",
    "RF_COLORS",
    "M_REF",
    "APPLY_SYSSHIFT",
    "AUTO_ADAPT",
    "ADAPT_BAND",
    "ADAPT_LIM",
    "ADAPT_CONTEXT",
    "ADAPT_ZBIN",
    "PDZ_OUT",
    "PDZ_TYPE",
    "PDZ_MABS_FILT",
    "ADD_EMLINES",
    "ADDITIONAL_MAG",
    "LIMITS_ZBIN",
    "LIMITS_MAPP_REF",
    "LIMITS_MAPP_SEL",
    "LIMITS_MAPP_CUT",
    "Z_STEP",
    "VERBOSE",
]

nonestring = "NONE"


class Zphota(Runner):
    def __init__(self, config_file=None):
        super().__init__(zphota_config_keys, config_file)

    def run(self, **kwargs):
        # update keymap and verbosity based on call arguments
        # this is only when the code is called from python session
        self.verbose = kwargs.pop("verbose", self.verbose)
        for k, v in kwargs.items():
            if k == "typ":
                self.typ = v.upper()
                continue
            if k == "config":
                self.config = config_file
                continue
            if k.upper() in self.keymap.keys():
                self.keymap[k.upper()] = keyword(k.upper(), str(v))
        self.keymap["c"] = keyword("c", self.config)

        print(self.keymap["Z_STEP"])
        print(self.keymap["COSMOLOGY"])
        print(self.keymap["Z_STEP"].split_double("0.1", 3))

        photoz = PhotoZ(self.keymap)
        autoadapt = (self.keymap["AUTO_ADAPT"]).split_string("YES", 1)[0]
        if autoadapt == "YES":
            adaptSrcs = photoz.read_autoadapt_sources()
            photoz.prep_data(adaptSrcs)
            a0, a1 = photoz.run_autoadapt(adaptSrcs)
            offsets = ",".join(np.array(a0).astype(str))
            offsets = "# Offsets from auto-adapt: " + offsets + "\n"
            photoz.outputHeader += offsets
        else:
            a0 = []
            a1 = []
            for k in range(photoz.imagm):
                a0.append(0.0)
                a1.append(0.0)

        opaOut = GalMag.read_opa()

        fitSrcs = photoz.read_photoz_sources()
        photoz.prep_data(fitSrcs)
        photoz.run_photoz(fitSrcs, a0, a1)
        photoz.write_outputs(fitSrcs, int(time.time()))

    def end(self):
        super().end()


if __name__ == "__main__":
    runner = Zphota()
    runner.run()
    runner.end()