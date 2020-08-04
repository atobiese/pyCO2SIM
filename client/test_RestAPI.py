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
    o.percentRemoved = (1.0 - out_vap_co2 / in_vap_co2) * 100

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

def f(obj, duty):

    # set new duty
    obj.set_unit('Reboiler', 'flashQ', duty * 3600)
    # solve flowsheet
    obj.solve()
    #get object function
    o = get_summary_data(obj)
    # objectbfunction
    costfunc = o.percentRemoved

    return costfunc

def newtons_method(f, x0, epsilon, obj):
    delta_x = 1.0
    x_i = x0
    f_i = f(obj, x_i)
    x_i_1 = x_i + x0 * 0.001
    Dx = x_i_1 - x_i
    err_i = 1
    stepsize = 10.0 #kW
    setpsizecontrol = True
    while (err_i) > epsilon:
        f_i_1 = f(obj, x_i_1)
        err_i = abs(f_i_1)
        fdot = (f_i_1 - f_i) / (x_i_1 - x_i)

        xNR = x_i_1 - f_i_1 / fdot

        x_i = x_i_1
        #x_i_1 = xNR

        if setpsizecontrol is True:
            next_deltastep = x_i_1 - xNR
            controlled_deltastep = stepsize
            if abs(next_deltastep) < controlled_deltastep:
                x_i_1_ = xNR
            else:
                if (fdot < 0):
                    x_i_1_ = x_i_1 + stepsize
                else:
                    x_i_1_ = x_i_1 - stepsize
        else:
            x_i_1_ = xNR

        x_i_1 = x_i_1_
        f_i = f_i_1


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
    # obj.set_unit('Reboiler', 'flashQ', 80 * 3600)
    obj.solve()

    o = get_summary_data(obj)
    o.percentRemoved
    o.reboilerDuty

    duty = o.reboilerDuty
    cost = f(obj, duty)

    # newtons_method(f, duty, 1e-3, obj)

    duty = obj.get_unit(o.reboilerObj, 'flashQ')



if __name__ == '__main__':
    # main file
    case = "tcp_api"
    #case = "py2mat_api"

    test(case)