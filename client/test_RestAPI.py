#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example file that runs co2sim from python. If matlab is installed locally, the same methods
are called. See options below for the two usages.

UI tester location http://xxxxx:5001/api/ui/

"""

from client.RestAPI import RESTApi
from py2matlabAPI.API_pyco2sim import ApiMatlab



def get_summary_data(obj):
    # utilities
    class Data():
        pass

    #pipename/unit mapping
    o = Data()
    o.inputAbsGObj = 'V1'
    o.outputAbGObj = 'V2'
    o.reboilerObj = 'Reboiler'
    o.lean = 'P09'
    o.rich = 'P03'

    pobj = obj.get_pipe_struct(o.inputAbsGObj)
    # in_vap_co2 = obj.Struct.flow*obj.Struct.molfrac(obj.Struct.componentlocations.CO2)
    ipy_co2 = int(float(pobj['componentlocations']['CO2'])) - 1
    ipy_mea = int(float(pobj['componentlocations']['MEA'])) - 1
    in_vap_co2 = float(pobj['flow']) * pobj['molfrac'][ipy_co2]
    pobj = obj.get_pipe_struct(o.outputAbGObj)
    out_vap_co2 = float(pobj['flow']) * pobj['molfrac'][ipy_co2]
    o.percentRemoved = (1 - out_vap_co2 / in_vap_co2) * 100

    o.reboilerDuty = obj.get_unit(o.reboilerObj, 'flashQ') / 3600  # kW
    reboilerTemp = obj.get_unit(o.reboilerObj, 'flashT') - 273.15

    leanObj = obj.get_pipe_struct(o.lean)
    richObj = obj.get_pipe_struct(o.rich)
    o.leanLoading = leanObj['molfrac'][ipy_co2] / leanObj['molfrac'][ipy_mea]
    o.richLoading = richObj['molfrac'][ipy_co2] / richObj['molfrac'][ipy_mea]
    o.srd = (o.reboilerDuty * 3600) / ((in_vap_co2 - out_vap_co2) * 44) / 1000

    # display summary
    print('*' * 50)
    print('Percent Removed:     {:<20f}'.format(o.percentRemoved))
    print('Reboiler duty:       {:<20f}'.format(o.reboilerDuty))
    print('Reboiler temp:       {:<20f}'.format(reboilerTemp))
    print('Lean Loading:        {:<20f}'.format(o.leanLoading))
    print('Rich Loading:        {:<20f}'.format(o.richLoading))
    print('SRD:                 {:<20f} GJ/kg CO2 removed'.format(o.srd))
    print('*' * 20)
    print('simulation log can be found at port 5000  http://URL:5000/')

    return o

def test(case):
    # case = "tcp_api"
    # case = "py2mat_api"

    #note that the methods are identical, but different classes (internal or external)

    if case == "tcp_api":
        print("running over web")
        # connect and load flowsheet
        url = "http://178.164.32.34:5001/"
        # # flowsheet = 'ExampleAbsorber'
        flowsheet = 'ExampleTillerClosedLoop'
        # # setup class
        obj = RESTApi(url, flowsheet)
        # # connect to simulator
        obj.connect()

    elif case == "py2mat_api":
        print("running locally")
        # opening connection to local co2sim methods
        obj = ApiMatlab()
        obj.connect('ExampleTillerClosedLoop')

    # solve flowsheet
    obj.solve()


    o = get_summary_data(obj)

    reboilerDuty_prev = obj.get_unit(o.reboilerObj, 'flashQ')
    var = obj.set_unit('Reboiler', 'flashQ', reboilerDuty_prev*.95)
    obj.solve()
    get_summary_data(obj, o)

    reboilerDuty_prev = obj.get_unit(o.reboilerObj, 'flashQ')
    var = obj.set_unit('Reboiler', 'flashQ', reboilerDuty_prev*.95)
    obj.solve()
    get_summary_data(obj, o)

    reboilerDuty_prev = obj.get_unit(o.reboilerObj, 'flashQ')
    var = obj.set_unit('Reboiler', 'flashQ', reboilerDuty_prev*.95)
    obj.solve()
    get_summary_data(obj, o)


if __name__ == '__main__':
    # main file
    case = "tcp_api"
    # case = "py2mat_api"

    test(case)