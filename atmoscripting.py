import numpy as np
import os
import subprocess
import copy

libradtran_path = '/home/mondrik/libradtran/libRadtran-2.0.2'
scratch_dir = '/tmp/'
standard_dict = {}
standard_dict['atmosphere_file'] = os.path.join(libradtran_path,'data/atmmod/afglus.dat')
standard_dict['source solar'] = os.path.join(libradtran_path,'data/solar_flux/kurudz_1.0nm.dat')
standard_dict['mol_abs_param'] = 'SBDART'
standard_dict['rte_solver'] = 'disort'
standard_dict['wavelength'] = '300 1100'
standard_dict['output_quantity'] = 'transmittance'
standard_dict['pressure'] = '550'
standard_dict['sza'] = '50'
standard_dict['aerosol_default'] = ''
standard_dict['aerosol_angstrom'] = '1.2 0.2'
standard_dict['altitude'] = '2.241'
standard_dict['mol_modify'] = 'O3 270 DU'
standard_dict['output_user'] = 'lambda edir'
standard_dict['quiet'] = ''


def get_standard_dict_copy():
    return copy.deepcopy(standard_dict)

def generate_parameter_file(input_dict=standard_dict,output_location=scratch_dir,file_name='params.atmo'):
    file_location = os.path.join(output_location,file_name)
    with open(file_location,'w') as output_file:
        for key, value in input_dict.items():
            output_file.write('{} {}\n'.format(key,value))
    return file_location


def get_atmosphere_transparency(parameter_file,output_location=scratch_dir,output_file_name='transparency.atmo'):
    #libRadtran expects us to be in the bin/ directory of libRadtran, because they define their data paths relative to uvspec...
    old_cwd = os.getcwd()
    os.chdir(os.path.join(libradtran_path,'bin'))
    output_file = os.path.join(output_location,output_file_name)
    subprocess.run(['run_uvspec',parameter_file,output_file])
    os.chdir(old_cwd)
    atmo = np.loadtxt(output_file)
    return atmo

