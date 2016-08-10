import json
import os
import pdb
import re

from netCDF4 import Dataset

class VariableMetadata(object):
    '''
    Class to handle required variable meta data

    '''
    def __init__(self, metadata_file, alt_names, alt_methods):
        '''
        Initialize (read and parse) variable meta data json-file

        param metadata_file: path to variable metadata json file
        type metadata_file: string
        param alt_names: path to json file with alternative variable names
        type metadata_file: string
        param alt_methods: path to json file with alternative variable cell_methods
        type metadata_file: string

        '''
        fmeta = open(metadata_file)
        self.jparsed = json.load(fmeta)

        falt_names = open(alt_names)
        self.jalt_names = json.load(falt_names)

        falt_methods = open(alt_methods)
        self.jalt_methods = json.load(falt_methods)

    def get_indice_dict(self, indice_name):
        '''
        Initialize (read and parse) variable meta data json-file

        param indice_name: User specified indice name
        type metadata_file: string

        rtype dict

        '''
        indice_lower = indice_name.lower()
        indice_index = [index['varname'] for index in self.jparsed].index(indice_lower)
        out_meta_dict = self.jparsed[indice_index]
        return out_meta_dict

    def write_metadata(self, variable, key, value):
        '''
        Write key-value pair to output netcdf file variable attribute

        param variable: Netcdf handle to the current variable
        type variable: netCDF4._netCDF4.Variable
        param key: variable attribute key
        type key: string
        param value: variable attribute value
        type value: string

        '''
        variable.setncattr(key, value)

    def get_attributes(self, select_key):
        '''
        Get a zipped list to iterate over keys/values

        param select_key: The key of interest, e.g, "output"
        type select_key: string

        rtype list

        '''
        return zip(self.current_variable_metadata[select_key].keys(),
                   self.current_variable_metadata[select_key].values())

    def set_current_indice(self, indice_to_select):
        '''
        From the full variable metadata json file, find and set the
        metadata for the specified indice.

        param indice_to_select: Retreive metadata for this indice
        type indice_to_select: string

        '''
        self.current_variable_metadata = self.get_indice_dict(indice_to_select)

    def get_alternative_names(self, known_variable):
        '''
        Fetches valid alternative variable names according to
        ICCLIM variable meta data file.

        param known_variable: Default name for input variable for this index
        type known_variable: string

        rtype list

        '''
        return self.jalt_names['input']['known_variables'][known_variable]

    def get_alternative_cmethods(self, known_method):
        '''
        Fetches valid alternative cell_methods according to
        ICCLIM variable meta data file.

        param known_method: Default name for input cell_method for this index
        type known_method: string

        rtype list

        '''
        return self.jalt_methods['input']['known_methods'][known_method]

    def is_cell_method_consistent(self, VARS, indice_name):
        '''
        Checks whether cell method in the input files are consistent
        with the current ICCLIM variable meta data file

        param VARS: Main ICCLIM dictionary
        type VARS: dict
        param indice_name: User specified indice name
        type var_name: string

        rtype bool

        '''
        fcell_methods = []
        for v in VARS.keys():
            inc = Dataset(VARS[v]['files_years'].keys()[0], 'r')
            ncVar = inc.variables[v]
            fcell_methods.append(ncVar.cell_methods)

        # Remove any free text formulation in parenthesis
        set_fc_methods = set([re.sub("\s*\(.*\)$", "", fc_method) for fc_method in fcell_methods])
        fc_methods = list(set_fc_methods)

        ret_value = True
        curr_meta_dict = self.get_indice_dict(indice_name)
        for idx in range(int(curr_meta_dict['n_inputs'])):
            cell_methods = curr_meta_dict['input'][idx]['cell_methods']
            alternative_cmethods = self.get_alternative_cmethods(cell_methods)

            cell_methods = self.convert_to_lower_case_list(cell_methods)
            union = set(alternative_cmethods) & set(fc_methods)

            if len(union) == 0:
                ret_value = ret_value and False
            else:
                # Remove the matched entry
                del(fc_methods[fc_methods.index(list(union)[0])])

        return ret_value

    def is_standard_name_consistent(self, VARS, indice_name):
        '''
        Checks whether user specified variable v and variable attribute
        standard name are consistent according to current ICCLIM variable
        meta data file

        param VARS: Main ICCLIM dictionary
        type VARS: dict
        param indice_name: User specified indice name
        type var_name: string

        rtype bool

        '''
        fstandard_names = []
        for v in VARS.keys():
            inc = Dataset(VARS[v]['files_years'].keys()[0], 'r')
            ncVar = inc.variables[v]
            fstandard_names.append(ncVar.standard_name)

        ret_value = True
        curr_meta_dict = self.get_indice_dict(indice_name)
        for idx in range(int(curr_meta_dict['n_inputs'])):
            jstandard_name = curr_meta_dict['input'][idx]['standard_name']
            if not jstandard_name in fstandard_names:
                ret_value = ret_value and False
            else:
                # Remove the matched entry
                del(fstandard_names[fstandard_names.index(jstandard_name)])

        return ret_value

    def is_varname_consistent(self, var_name, indice_name):
        '''
        Checks whether user specified var_name and indice_name are
        consistent according to current ICCLIM variable meta data file

        param var_name: User specified variable name
        type var_name: string
        param indice_name: User specified indice name
        type var_name: string

        rtype bool

        '''
        ret_value = True
        curr_meta_dict = self.get_indice_dict(indice_name)
        for idx in range(int(curr_meta_dict['n_inputs'])):
            known_variable = curr_meta_dict['input'][idx]['known_variables']
            alternative_names = self.get_alternative_names(known_variable)

            var_name = self.convert_to_lower_case_list(var_name)
            union = set(alternative_names) & set(var_name)

            if len(union) == 0:
                ret_value = ret_value and False

        return ret_value

    def convert_to_lower_case_list(self, invar):
        '''
        Outputs input variable as lower case list

        param invar: User specified variable name
        type invar: string

        rtype list

        '''
        if type(invar) is list:
            lc_list = [name.lower() for name in invar]
        else:
            lc_list = [invar.lower()]
        return lc_list


class GlobalMetadata(object):
    '''
    Class to handle required global meta data

    '''
    def __init__(self, metadata_file):
        '''
        Initialize (read and parse) global meta data json-file

        param metadata_file: path to global metadata json file
        type metadata_file: string


        rtype list
        '''
        fmeta = open(metadata_file)
        self.jparsed = json.load(fmeta)

    def get_attributes(self):
        '''
        Get a zipped list to iterate over keys/values

        '''
        return self.jparsed['global'].keys()

    def is_mandatory(self, attribute):
        '''
        Check if the requested attribute is mandatory

        param attribute: Requested attribute in the global metadata json-file
        param type: string

        rtype bool
        '''
        mandatory = self.jparsed['global'][attribute]['ATTR_MANDATORY']
        if mandatory == '1':
            ret_value = True
        elif mandatory == '0':
            ret_value = False
        else:
            raise ValueError("Invalid value for ATTR_MANDATORY in attribute " + attribute)
        return ret_value

    def write_metadata(self, attribute, out_nc):
        '''
        Write key-value pair to output netcdf file variable attribute

        param attribute: Requested attribute in the global metadata json-file
        param type: string
        param out_nc: Netcdf output file handle
        param type: type 'netCDF4._netCDF4.Dataset
        '''
        # Write mandatory output
        if self.is_mandatory(attribute):
            out_nc.setncattr(attribute, self.jparsed['global'][attribute]['ATTR_VALUE'])
        # Write non-mandatory output if non-empty
        else:
            if 'ATTR_VALUE' in self.jparsed['global'][attribute]:
                if len(self.jparsed['global'][attribute]['ATTR_VALUE'].strip()) > 0:
                    out_nc.setncattr(attribute, self.jparsed['global'][attribute]['ATTR_VALUE'])
