#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from py2matlabAPI.API_pyco2sim import ApiMatlab


# NB: these tests require a live co2sim instance

class TestConnections(unittest.TestCase):
    model = []

    @classmethod
    def setUpClass(cls):
        """Create the model self.model for use for all tests suite."""
        cls.model = ApiMatlab()
        cls.model.connect('ExampleAbsorber')
        # solve flowsheet and first load all numeric libraries
        #cls.model.solve()

    def test_get_solve(self):
        # get outlet temp absorber
        pipe = 'P02'
        prop = 'temp'
        var1 = self.model.get_pipe(pipe, prop)

        # get outlet temp absorber
        unit = 'Absorber'
        prop = 'length'
        var1 = self.model.get_unit(unit, prop)

    def test_set_and_solve(self):
        pipe = 'P01'
        prop = 'temp'
        value = 320
        self.model.set_pipe(pipe, prop, value)
        unit = 'Absorber'
        prop = 'length'
        value = 15.0
        self.model.set_unit(unit, prop, value)
        value_chk = self.model.get_unit(unit, prop)

        assert (value == value_chk)

    def test_setup_and_run_full_flowsheet(self):
        import client.test_RestAPI
        # main file
        case = "tcp_api"
        # case = "py2mat_api"

        client.test_RestAPI.test(case)

    def test_setup_and_run_full_flowsheet2(self):
        import client.test_RestAPI
        # main file
        # case = "tcp_api"
        case = "py2mat_api"

        client.test_RestAPI.test(case)

    def test_methods_in_REST_API_test_examples(self):
        import client.RestAPI
        # run test located in RESTAPI script
        client.RestAPI.defaulttest()

if __name__ == "__main__":
    unittest.main()
