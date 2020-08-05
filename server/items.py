"""
This is the ITEM module and supports all the ReST actions for the
ITEM collection (works with the swagger yaml file)
"""

from datetime import datetime
import json
from flask import make_response, abort

# co2sim
from py2matlabAPI.API_pyco2sim import ApiMatlab

class Model():
    pass


"""Create the model that will be live on the server side after system is loaded."""
model = Model()
model.instance = ApiMatlab()
model.count = 0
model.connected = False


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with API
ITEM = {
    "-": {
        "fname": "-",
        "lname": "-",
        "timestamp": "-",
    },
}


def get_pipe_prop(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    pipe = dict_obj['pipe']
    property = dict_obj['prop']

    if model.connected is False:
        abort(
            406,
            "api is not connected with server, load casefile first",
        )

    else:

        pipe = pipe
        property = property
        var1 = model.instance.get_pipe(pipe, property)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = str(model.count) + "_" "simulation"
        ITEM[new_name] = {
            "lname": property,
            "fname": var1,
            "timestamp": get_timestamp(),
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def get_unit_prop(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    unit = dict_obj['pipe']
    property = dict_obj['prop']

    if model.connected is False:
        abort(
            406,
            "api is not connected with server, load casefile first",
        )

    else:
        # get outlet temp absorber
        var1 = model.instance.get_unit(unit, property)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = str(model.count) + "_" "simulation"
        ITEM[new_name] = {
            "lname": property,
            "fname": var1,
            "timestamp": get_timestamp(),
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def set_pipe_prop(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    pipe = dict_obj['pipe']
    property = dict_obj['prop']
    value = dict_obj['value']

    if model.connected is False:
        abort == True
        abort(
            406,
            "api is not connected with server, connect first",
        )

    else:
        # get outlet temp absorber
        var1 = model.instance.set_pipe(pipe, property, value)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = "simulation:" + "_" + str(model.count)
        ITEM[new_name] = {
            "pipe": pipe,
            "property": property,
            "value": var1,
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def set_pipe_components(prop):
    import ast
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    pipe = dict_obj['pipe']
    # property = dict_obj['prop']
    value = dict_obj['value']
    # convert string to list
    value_list = ast.literal_eval(value)

    if model.connected is False:
        abort == True
        abort(
            406,
            "api is not connected with server, connect first",
        )

    else:
        # get outlet temp absorber
        var1 = model.instance.set_pipe_components(pipe, value_list)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = "simulation:" + "_" + str(model.count)
        ITEM[new_name] = {
            "pipe": pipe,
            "property": 'Not applicable',
            "value": value_list,
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def set_unit_prop(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    pipe = dict_obj['pipe']
    property = dict_obj['prop']
    value = dict_obj['value']

    if model.connected is False:
        abort == True
        abort(
            406,
            "api is not connected with server, connect first",
        )

    else:
        # get outlet temp absorber
        var1 = model.instance.set_unit(pipe, property, value)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = "simulation:" + "_" + str(model.count)
        ITEM[new_name] = {
            "pipe": pipe,
            "property": property,
            "value": var1,
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def get_unit_dict(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    unit = dict_obj['pipe']
    # property = dict_obj['prop']

    if model.connected is False:
        abort(
            406,
            "api is not connected with server, load casefile first",
        )

    else:
        # get outlet temp absorber
        unit_dict = model.instance.get_unit_struct(unit)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = str(model.count) + "_" "simulation"
        ITEM[new_name] = {
            "lname": unit,
            "fname": unit_dict,
            "timestamp": get_timestamp(),
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_

def get_summary_dict(prop):
    """
    {"pipe":"P02","prop":"press"}
    """

    dict_obj = json.loads(prop)
    unit = dict_obj['pipe']
    # property = dict_obj['prop']

    if model.connected is False:
        abort(
            406,
            "api is not connected with server, load casefile first",
        )

    else:
        # get outlet temp absorber
        unit_dict = model.instance.get_summary_struct()

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = str(model.count) + "_" "simulation"
        ITEM[new_name] = {
            "lname": unit,
            "fname": unit_dict,
            "timestamp": get_timestamp(),
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_

def get_pipe_dict(prop):
    dict_obj = json.loads(prop)
    unit = dict_obj['pipe']

    if model.connected is False:
        abort(
            406,
            "api is not connected with server, load casefile first",
        )

    else:
        # get outlet temp absorber
        unit_dict = model.instance.get_pipe_struct(unit)

        # hacking fixme
        new_in = ITEM.get(list(ITEM.keys())[-1])
        new_name = str(model.count) + "_" "simulation"
        ITEM[new_name] = {
            "lname": unit,
            "fname": unit_dict,
            "timestamp": get_timestamp(),
        }

        item_ = ITEM[new_name]  # ITEM.get(lname)

    return item_


def read_all():
    return [ITEM[key] for key in sorted(ITEM.keys())]


def read_one(lname):
    # Does the item_ exist in ITEM?
    if lname in ITEM:
        item_ = ITEM.get(lname)

    else:
        abort(
            404, "item_ with last name {lname} not found".format(lname=lname)
        )

    return item_


def create(item_):
    # the solve function
    if model.connected is False:
        lname = "solver not connected" + str(model.count)
        new_name = lname
    else:
        model.instance.solve()
        model.count = model.count + 1
        new_name = str(model.count) + "_" + "new simulation completed"

    # SISTE I DICTEN
    new_in = ITEM.get(list(ITEM.keys())[-1])
    try:

        ITEM[new_name] = {
            "lname": new_name,
            "fname": new_in['fname'],
            "timestamp": get_timestamp(),
        }
    except:
        ITEM[new_name] = {
            "lname": new_name,
            "fname": new_in['property'],
            "timestamp": get_timestamp(),
        }

    # siste verdi i dict
    return ITEM[new_name], 201


def update(lname, item_):
    # the initialization method
    flowsheetname = item_.get("prop", None)
    if flowsheetname:
        flowsheetname = flowsheetname
    else:
        flowsheetname = 'ExampleAbsorber'

    if flowsheetname != model.instance.flowsheetname:
        model.instance.connect(flowsheetname)
        lname = str(model.count) + "__smulation_" + " is loaded"
        model.connected = True

        ITEM[lname] = {
            "lname": lname,
            "fname": "Net: " + flowsheetname,
            "timestamp": get_timestamp(),
        }
        return ITEM[lname], 201

    else:
        abort(
            406,
            "simulator already initaited ",
        )


def delete(lname):
    """
    This function deletes a item_ from the ITEM structure

    """
    # Does the item_ to delete exist?
    if lname in ITEM:
        del ITEM[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, item_ to delete not found
    else:
        abort(
            404, "item_ with last name {lname} not found".format(lname=lname)
        )
