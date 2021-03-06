from icclim import icclim
import pdb
from icclim.util import callback
import datetime
import glob
import json
from icclim.util import read

def netcdf_processing():

    save_path = '/Users/xavier/Projets/data/test/results/'
    path_json = "icclim/config_indice.json"

    with open(path_json) as json_data:
            data = json.load(json_data)

    #varname = 'tasmax'
    #slice_mode = 'year'
    out_file = save_path+"outfile_test.nc"
    list_indice = data['icclim']['indice'] 
    
    for indice_param in list_indice:
        print('Calulation: '+str(indice_param))
        if indice_param=='PRCPTOT':
            if list_indice[indice_param]['indice_type']=='simple':
                tr = [datetime.datetime(1960,1,1), datetime.datetime(1980,12,31,13)]


                if 'tas' in list_indice[indice_param]['var_name']:
                    path_in_file = '/Users/xavier/Projets/data/usecase/tasmax_day_CSIRO-Mk3L-1-2_historical_r1i2p1_18510101_20051231.nc'
                    icclim.indice(indice_name=indice_param, time_range = tr, base_period_time_range = tr,
                    in_files=path_in_file, slice_mode='month', var_name='tasmax', ignore_Feb29th=False, 
                    out_file=out_file, callback=callback.defaultCallback2)
                else:
                    path_in_file = "/Users/xavier/Projets/data/test/pr_day_CNRM-CM6-1_highresSST-present_r21i1p1f2_gr_19500101-19991231.nc"

                    icclim.indice(indice_name=indice_param, time_range = tr, base_period_time_range = tr,
                    in_files=path_in_file, slice_mode='month', var_name='pr', ignore_Feb29th=False, 
                    out_file=out_file, callback=callback.defaultCallback2)

if __name__ == "__main__":
    netcdf_processing()


