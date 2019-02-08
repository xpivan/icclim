import json
import os

config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/config_indice.json"

def read_config_file(config_file=config_file):
    with open(config_file) as json_data:
            data = json.load(json_data)
    return data

def get_icclim_indice_config(config_structure=config_structure):
        #Loading config from icclim for the dispel4py wps workflow
        return config_structure["icclim"]["indice"].keys()

def get_icclim_slice_mode(config_structure=config_structure):
        #Loading config from icclim for the dispel4py wps workflow
        return config_structure["icclim"]["slice_mode"] 

def get_disp4py_config(config_structure=config_structure):
        #Loading config from icclim for the dispel4py wps workflow
        conf_filename = config_structure["C4I"]["dispel4py_wps"]["configFileName"]
        json_structure = config_structure["C4I"]["dispel4py_wps"]["jsonStructure"]
        return conf_filename, json_structure