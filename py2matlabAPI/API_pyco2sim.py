#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THis defines the api between python and the matlab engine

Options of running co2sim as a service externally by using set restful-API signatures.

@atobiese
"""

import matlab.engine
from definitions import ROOT_DIR

CURRENT_DIR = ROOT_DIR + '\\py2matlabAPI'  # path to store system generated conf files


class ApiMatlab(object):

    def __init__(self):
        self.data = []
        self.flowsheetname = []
        self.results = {}
        self.eng = []

    def connect(self, flowsheetname):
        self.flowsheetname = flowsheetname
        eng = matlab.engine.start_matlab()

        # set_pipeup matlab behind server (only needs to be done on connect(?)
        eng.addpath(CURRENT_DIR, nargout=0)

        eng.pyco2sim(nargout=0)
        st = 'simnet = {}'.format(flowsheetname)
        eng.eval(st, nargout=0)
        st = 'simnet.PrintStreams'
        eng.eval(st, nargout=0)

        # check if matlab class-hierarchy simnet is built
        istrue = isinstance((eng.workspace['simnet']), object)
        if istrue:
            print('set_pipeup connection and loaded flowsheeet---Done!', type(eng.workspace['simnet']))
            self.eng = eng

    def get_pipe(self, pipe, prop):
        # getters
        # example
        # prop = 'temp'
        # pipe = 'P02'
        eng = self.eng

        # create signature
        st = """var = simnet.FindPipe("{}").Struct.{};""".format(pipe, prop)
        eng.eval(st, nargout=0)
        var = eng.workspace['var']

        print("\n")
        print("var:__", var)

        return var

    def get_unit(self, unit, prop):
        # getters
        # prop = 'temp'
        # pipe = 'P02'
        eng = self.eng

        # create signature
        st = """var = simnet.FindUnit("{}").Struct.{};""".format(unit, prop)
        eng.eval(st, nargout=0)
        var = eng.workspace['var']

        print("\n")
        print("var:__", var)

        return var

    def set_pipe(self, pipe, prop, value):
        eng = self.eng
        st = """simnet.FindPipe("{}").Stream.FindParameter("{}").ConvValue = {};""".format(pipe, prop, value)
        eng.eval(st, nargout=0)

        # check if it was properly set_pipe to hierarchy
        var = self.get_pipe(pipe, prop)
        diff = var - float(value)
        print("\n")
        print("var:__", var)
        print('set_pipe---Done!')

        if diff == 0:
            return var

    def set_pipe_components(self, pipe, molar_vec):
        eng = self.eng
        # check number of components in flowsheet
        st = """var = simnet.FindPipe("{}").Struct.ncomp;""".format(pipe)
        eng.eval(st, nargout=0)
        ncomp = int(eng.workspace['var'])
        if ncomp != len(molar_vec):
            print("error!")

        for index, item in enumerate(molar_vec):
            st = """simnet.FindPipe("{}").Struct.molfrac({}) = {};""".format(pipe, index + 1, molar_vec[index])
            eng.eval(st, nargout=0)
        st = """simnet.FindPipe("{}").UpdateFromStruct();""".format(pipe)
        eng.eval(st, nargout=0)
        st = """simnet.FindPipe("{}").Stream.UpdateFromStruct();""".format(pipe)
        eng.eval(st, nargout=0)

        # check if it was properly set_pipe to hierarchy
        # check_pipestruct = self.get_pipe_struct(pipe)
        # diff = var - float(value)
        # print("\n")
        # print("var:__", var)
        # # print('set_pipe---Done!')
        #
        # if diff == 0:
        #     return var

    def set_unit(self, unit, prop, value):
        eng = self.eng
        st = """simnet.FindUnit("{}").FindParameter("{}").ConvValue = {};""".format(unit, prop, value)
        eng.eval(st, nargout=0)

        # check if it Swas properly set_pipe to hierarchy
        var = self.get_unit(unit, prop)
        diff = var - float(value)
        print("\n")
        print("var:__", var)
        print('set_pipe---Done!')

        if diff == 0:
            return var

    def get_pipe_struct(self, pipe):
        eng = self.eng

        # create signature
        # return the full stream structure
        struct = """struct = simnet.FindPipe("{}").Struct;""".format(pipe)
        eng.eval(struct, nargout=0)
        struct = eng.workspace['struct']  # eng.eval("var")

        print("\n")
        print("struct:__", struct)
        json_stuct = obj_to_dict(struct)
        return json_stuct

    def get_unit_struct(self, unit):
        eng = self.eng

        # create signature
        # return the full stream structure
        struct = """struct = simnet.FindUnit("{}").Struct;""".format(unit)
        eng.eval(struct, nargout=0)
        struct = eng.workspace['struct']  # eng.eval("var")

        print("\n")
        print("struct:__", struct)
        json_stuct = obj_to_dict(struct)
        return json_stuct

    def solve(self):
        # run the network solver
        eng = self.eng
        print("Running simulation")
        eng.eval('simnet.Solve;', nargout=0)


# helperfile to convert matlab structures to python lists before serlization

import json
import types


def obj_to_dict(obj):
    if type(obj) is dict:
        res = {}
        for k, v in obj.items():
            res[k] = obj_to_dict(v)
        return res
    elif type(obj) is list:
        return [obj_to_dict(item) for item in obj]
    elif type(obj) is types.SimpleNamespace:
        return obj_to_dict(vars(obj))
    elif isinstance(obj, matlab.double):
        return obj._data.tolist()
    elif isinstance(obj, matlab.object):
        return None

    # finally, return the full recursived structure as packed json
    return json.dumps(obj)


def main():
    obj = ApiMatlab()
    obj.connect('ExampleAbsorber')

    # get outlet temp absorber
    pipe = 'P02'
    prop = 'temp'
    var1 = obj.get_pipe(pipe, prop)

    # solve flowsheet
    # obj.solve()

    pipe = 'P01'
    prop = 'temp'
    value = 320
    obj.set_pipe(pipe, prop, value)
    unit = 'Absorber'
    prop = 'length'
    value = 15.0
    obj.set_unit(unit, prop, value)
    value_chk = obj.get_unit(unit, prop)

    assert (value == value_chk)
    # solve flowsheet
    # obj.solve()

    # get outlet temp absorber
    pipe = 'P02'
    prop = 'temp'
    var2 = obj.get_pipe(pipe, prop)

    diff = var2 - var1
    pipe_dict = obj.get_pipe_struct('P02')
    unit_dict = obj.get_unit_struct('Absorber')

    molar_vec = (.5, .5, .5, .5, .5)
    obj.set_pipe_components('P01', molar_vec)


if __name__ == '__main__':
    main()
