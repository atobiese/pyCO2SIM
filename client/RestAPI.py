#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This defines the api from python-matlab engine
Options of running co2sim as a service by using API signatures.

The file needs to be accessible on the CLIENT-side, and creates http rest calls via a common
set of methods.
see the main part of this file for examples or the test_RESTAPI file.
USAGE: from client_old.RestAPI import RESTApi
"""

import requests
import json
import urllib.parse
import logging

_LOG = logging.getLogger(__name__)
logging.debug("Begin")


# _LOG.setLevel(logging.DEBUG)


class RESTApi(object):
    def __init__(self, url, flowsheetname):

        self.url = url
        self.flowsheetname = flowsheetname

        self.data = []
        self.results = {}

    def connect(self):
        # initiates and loads flowshet
        url_spec = self.url + "api/items/str"
        payload = """{"prop": """ + '"' + self.flowsheetname + '"' + ""","value":"-"}"""
        headers = {"content-type": "application/json"}
        res = requests.put(url_spec, data=payload, headers=headers)

        # check if matlab class-hierarchy simnet is built
        dict_obj = json.loads(res.content.decode())
        _LOG.info(dict_obj)
        return dict_obj

    def solve(self):
        # run the network solver
        _LOG.info("Running simulation")
        # runs a simulation
        url_spec = self.url + "api/items"
        payload = (
            """{"fname": """ + '"' + self.flowsheetname + '"' + ""","lname":"-"}"""
        )
        headers = {"content-type": "application/json"}
        res = requests.post(url_spec, data=payload, headers=headers)

        # check if matlab class-hierarchy simnet is built
        dict_obj = json.loads(res.content.decode())
        _LOG.info(dict_obj["lname"])
        return dict_obj

    def get_pipe(self, pipe, prop):

        url_spec = self.url + "api/results/"
        values_ = (
            """{"pipe": """
            + '"'
            + pipe
            + '"'
            + ""","prop": """
            + '"'
            + prop
            + '"'
            + "}"
            ""
        )
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.get(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
            property = dict_obj["lname"]  # property
            value = dict_obj["fname"]  # value'
        except:
            dict_obj = -1
            property = -1
            value = -1

        _LOG.info("var={}".format((value)))

        return value  # , property, dict_obj

    def get_unit(self, unit, prop):

        url_spec = self.url + "api/unit/"
        values_ = (
            """{"pipe": """
            + '"'
            + unit
            + '"'
            + ""","prop": """
            + '"'
            + prop
            + '"'
            + "}"
            ""
        )
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.get(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
            property = dict_obj["lname"]  # property
            value = dict_obj["fname"]  # value'
        except:
            dict_obj = -1
            property = -1
            value = -1
        # pipe = dict_obj['pipe']

        _LOG.info("var={}".format((value)))

        return value  # , property, dict_obj

    def set_pipe(self, pipe, prop, value):
        url_spec = self.url + "api/set/"
        values_ = (
            """{"pipe": """
            + '"'
            + pipe
            + '"'
            + ""","prop": """
            + '"'
            + prop
            + '"'
            + ""","value": """
            + '"'
            + str(value)
            + '"'
            + "}"
            ""
        )
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.post(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
        except:
            dict_obj = -1
            value = -1

        _LOG.info("value:__{} set_pipe---Success".format(value))
        return value  # , dict_obj

    def set_unit(self, unit, prop, value):
        url_spec = self.url + "api/setunit/"
        values_ = (
            """{"pipe": """
            + '"'
            + unit
            + '"'
            + ""","prop": """
            + '"'
            + prop
            + '"'
            + ""","value": """
            + '"'
            + str(value)
            + '"'
            + "}"
            ""
        )
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.post(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
        except:
            dict_obj = -1
            value = -1

        _LOG.info("value:__{} set_unit---Success".format(value))
        return value  # , dict_obj

    def set_pipe_components(self, pipe, value):
        url_spec = self.url + "api/setpipecomponents/"
        values_ = (
            """{"pipe": """
            + '"'
            + pipe
            + '"'
            + ""","value": """
            + '"'
            + str(value)
            + '"'
            + "}"
            ""
        )
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.post(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
        except:
            dict_obj = -1
            value = -1

        _LOG.info("value:__{} set_components---Success".format(value))
        return value  # , dict_obj

    def get_pipe_struct(self, pipe):

        url_spec = self.url + "api/pipe_d/"
        values_ = """{"pipe": """ + '"' + pipe + '"' + "}" ""
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.get(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
            property = dict_obj["lname"]  # property
            value = dict_obj["fname"]  # value'
        except:
            dict_obj = -1
            property = -1
            value = -1
        # pipe = dict_obj['pipe']

        _LOG.info("value:__{} get full pipe---Success".format(value))
        return value

    def get_summary_struct(self):
        pipe = "dummy"
        url_spec = self.url + "api/summary_d/"
        values_ = """{"pipe": """ + '"' + pipe + '"' + "}" ""
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.get(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
            property = dict_obj["lname"]  # property
            value = dict_obj["fname"]  # value'
        except:
            dict_obj = -1
            property = -1
            value = -1
        # pipe = dict_obj['pipe']

        _LOG.info("value:__{} get full pipe---Success".format(value))
        return value

    def get_unit_struct(self, pipe):

        url_spec = self.url + "api/unit_d/"
        values_ = """{"pipe": """ + '"' + pipe + '"' + "}" ""
        values = urllib.parse.quote(str(values_))
        # hack to raplace from double to single quotation mark (fixme fat)
        d1 = values.replace("%27", "%22")
        url_query = url_spec + d1
        res = requests.get(url_query)
        try:
            dict_obj = json.loads(res.content.decode())
            property = dict_obj["lname"]  # property
            value = dict_obj["fname"]  # value'
        except:
            dict_obj = -1
            property = -1
            value = -1

        _LOG.info("value:__{} get_unit---Success".format(value))

        return value


def defaulttest():
    # test script
    # connect and load flowsheet
    url = "http://127.0.0.1:5001/"
    flowsheet = "ExampleAbsorber"
    flowsheet = "ExampleTillerClosedLoop_val_orig_astarita_ng"

    # setup class
    obj = RESTApi(url, flowsheet)
    # connect to simulator
    obj.connect()

    # get outlet temp absorber
    pipe = "P02"
    prop = "temp"
    var1 = obj.get_pipe(pipe, prop)
    var1 = obj.get_pipe(pipe, "press")
    var1 = obj.get_pipe(pipe, "flow")

    pipe = "P01"
    prop = "temp"
    value = 320
    obj.set_pipe(pipe, prop, value)
    unit = "Absorber"
    prop = "length"
    value = 15.0
    var = obj.get_unit(unit, prop)
    obj.set_unit(unit, prop, value)
    obj.set_pipe(pipe, prop, value)
    value_chk = obj.get_pipe(pipe, prop)

    # get outlet temp absorber
    pipe = "P02"
    prop = "temp"
    var2 = obj.get_pipe(pipe, prop)

    molar_vec = (0.5, 0.5, 0.5, 0.5, 0.5)
    obj.set_pipe_components("P01", molar_vec)
    pipe_dict = obj.get_pipe_struct("P02")
    pipe_dict["amine"]
    # unit_dict = obj.get_unit_struct('Absorber')
    # unit_dict['type']

    var = obj.get_unit(unit, prop)

    struct = obj.get_summary_struct()
    a = 1


if __name__ == "__main__":
    defaulttest()
