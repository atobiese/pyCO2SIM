#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import logging
from definitions import TEMP_DIR
import matplotlib.pyplot as plt

_LOG = logging.getLogger(__name__)

# run this to start logging
logging.debug("Begin")
_LOG.setLevel(logging.DEBUG)


class Results(object):
    def __init__(self, abs_filename):

        self.abs_filename = abs_filename
        self.data = []
        self.lg_ratio = []
        self.df = pd.read_csv(self.abs_filename)  # Previously performed simulations

    def get_ucurve_min(s, restrict, height, mol_conc_co2, plot):

        """
        restrict = 50.0
        height = 20.0
        mol_conc_CO2 = 0.06
        """
        # --------------------------------
        # FIXME (hent inn gassstrømdata)
        gasflow = 11.4139  # kmol/h
        mwag = 28.253328  # kg/kmol
        gasflow_m = gasflow * mwag
        mwal = 23.75  # kg/kmol
        # --------------------------------

        acc = 0.05
        res_min = restrict - acc
        res_max = restrict + acc
        # cols = list(s.df.columns)

        # query the data
        db_results = s.df.loc[
            (s.df["capture_rate"] >= res_min)
            & (s.df["capture_rate"] <= res_max)
            & (s.df["absorber_height"] == height)
            & (s.df["fluegas_CO2"] == mol_conc_co2)
        ]

        nr_points = len(db_results)
        print(f"nr points found {nr_points}")

        if nr_points is 0:
            print(f"no points were found: {nr_points}, exiting")
            row_opt = -1
            lg_ = -1
            return row_opt, lg_, nr_points

        liqflow_m = db_results["solvent_circ_rate"] * mwal
        s.lg_ratio = gasflow_m / liqflow_m

        # best case wrt SRD
        idxmin = db_results["srd"].idxmin()
        row_opt = s.df.iloc[idxmin]
        lg_ = row_opt["solvent_circ_rate"] * mwal / gasflow_m

        print(row_opt)
        print(f" lg_ratio {lg_}")
        print(f"nr points found {nr_points}")

        # plot
        if plot:
            dx = [0] * 4
            dy = [0] * 4
            text = [""] * 4
            xlabel = [""] * 4
            ylabel = [""] * 4

            propx = ["srd"]
            propy = "solvent_circ_rate", "lean_loading", "richLoading", "lg_ratio"

            for k in range(0, 3):

                dx[k] = db_results[propx]
                dy[k] = db_results[propy[k]]
                text[k] = ""  # name
                xlabel[k] = propy[k]
                ylabel[k] = propx

            propx = "srd"
            propy = "lg_ratio"
            name = "lg_ratio rate vs duty"
            dx[3] = db_results[propx]
            dy[3] = s.lg_ratio
            text[3] = ""  # name
            xlabel[3] = propy
            ylabel[3] = propx

            fig, ax = plt.subplots(nrows=2, ncols=2)
            # plt.rcParams.update({'font.size': 10})
            fig.suptitle(
                f"capture: {restrict}% nr_points: {nr_points}, between {res_min}-{res_max}% \n "
                f"gas_co2_in: {mol_conc_co2 * 100.}%, height: {height}"
                f""" Min(srd)={row_opt['srd']:.2f}""",
                fontsize=8,
            )
            k = 0
            for i, row in enumerate(ax):
                for j, col in enumerate(row):
                    col.plot(
                        dy[k],
                        dx[k],
                        marker=".",
                        markerfacecolor="red",
                        color="blue",
                        linewidth=1,
                    )
                    col.set(xlabel=xlabel[k], ylabel=ylabel[k], title=text[k])
                    col.grid()
                    k += 1

            # plt.show()

        return row_opt, lg_, nr_points


def main():
    filename = "matrix_90_20_temp_in_48C_2.csv"
    abs_filename = TEMP_DIR + "/" + filename
    # pre-process
    o = Results(abs_filename)

    # row_opt, lg_, nr_points = o.get_ucurve_min(restrict=50.0, height=20, mol_conc_co2=0.06, plot=True)

    # NB, data below must be matched to the simulated results, wrt chosen absorber height and inlet concentration
    captures = np.linspace(20, 90, 8)
    heights = [15.0, 20.0]
    mol_conc_co2 = 0.06

    for height in heights:
        for caps in captures:
            row_opt, lg_, nr_points = o.get_ucurve_min(
                restrict=caps, height=height, mol_conc_co2=mol_conc_co2, plot=True
            )
        plt.show()


if __name__ == "__main__":
    main()
