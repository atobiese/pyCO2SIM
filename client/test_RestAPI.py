#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example file that runs co2sim from python. If matlab is installed locally, the same methods
are called. See options below for the two usages.

UI tester location http://xxxxx:5001/api/ui/

"""

from client.RestAPI import RESTApi
from py2matlabAPI.API_pyco2sim import ApiMatlab
from client.co2sim_dataminer import get_summary_data


def test(case):
    # case = "tcp_api"
    # case = "py2mat_api"

    # note that the methods are identical, but different classes (internal or external)

    if case == "tcp_api":
        print("running over web")
        # connect and load flowsheet
        # url = "http://178.164.32.34:5001/"
        url = "http://127.0.0.1:5001/"
        # # flowsheet = 'ExampleAbsorber'
        flowsheet = "ExampleTillerClosedLoop"
        # # setup class
        obj = RESTApi(url, flowsheet)
        # # connect to simulator
        obj.connect()

    elif case == "py2mat_api":
        print("running locally")
        # opening connection to local co2sim methods
        obj = ApiMatlab()
        obj.connect("ExampleTillerClosedLoop")

    # solve flowsheet
    obj.solve()

    o = get_summary_data(obj, bypass=False)
    unit_name = "Reboiler"
    reboilerDuty_prev = obj.get_unit(unit_name, "flashQ")
    var = obj.set_unit(unit_name, "flashQ", reboilerDuty_prev * 0.95)
    obj.solve()
    get_summary_data(obj, bypass=False)

    # reboilerDuty_prev = obj.get_unit(unit_name, 'flashQ')
    # var = obj.set_unit(unit_name, 'flashQ', reboilerDuty_prev*.95)
    # obj.solve()
    # get_summary_data(obj, bypass=False)
    #
    # reboilerDuty_prev = obj.get_unit(unit_name, 'flashQ')
    # var = obj.set_unit(unit_name, 'flashQ', reboilerDuty_prev*.95)
    # obj.solve()
    # get_summary_data(obj, bypass=False)


if __name__ == "__main__":
    # main file
    case = "tcp_api"
    # case = "py2mat_api"

    test(case)
