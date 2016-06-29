import json
import os
import pdb


def read_json(jfile):
    jparsed = json.load(jfile)
    return jparsed

jfile = os.path.join('metadata_database', 'climate_indices_b_DEF.json')
jfile_handle = open(jfile)
print read_json(jfile_handle)
