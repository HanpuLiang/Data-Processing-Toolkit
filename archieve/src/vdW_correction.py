# -*- coding: utf-8 -*-
'''
@author: Liang Hanpu
@create date: 2020/10/26
@description: This parameter are ready to prepartion the VASP inputs files for different calculational situation.
'''

import os
import src.system_cmd
import src.get_path as gp

def add_vdW_correction(vdW_method):
    optB88 = '''
# optB88 vdW correction 
GGA      = BO
LUSE_VDW = .TRUE.
AGGAC    = 0.0000
PARAM1   = 0.183333 
PARAM2   = 0.220000
'''
    optB86b = '''
# optB86b vdW correction 
GGA      = MK
LUSE_VDW = .TRUE.
AGGAC    = 0.0000
PARAM1   = 0.1234 
PARAM1   = 1.0000
'''
    optPBE = '''
# optPBE vdW correction 
GGA      = OR
LUSE_VDW = .TRUE.
AGGAC    = 0.0000
'''
    vdw_DF = '''
# vdW-DF vdW correction 
GGA      = RE
LUSE_VDW = .TRUE.
AGGAC    = 0.0000
'''
    vdw_DF2 = '''
# vdW-DF2 vdW correction 
GGA      = ML
LUSE_VDW = .TRUE.
AGGAC    = 0.0000
Zab_vdW  = -1.8867
'''
    method_dict = {'optB88':optB88,
                   'optB86b':optB86b,
                   'optPBE':optPBE,
                   'vdW-DF':vdw_DF,
                   'vdW-DF2':vdw_DF2}
    if vdW_method in method_dict.keys():
        modify_INCARs(vdW_method, method_dict[vdW_method])
    else:
        src.system_cmd.systemError(' Wrong vdW correction Method.\n The Method You Can Choose: \n    optB88, optB86b, optPBE, vdW-DF, vdW-DF2')

def modify_INCARs(vdW_method, vdw_str):
    # first, code will find all the files in this directory
    dir_files = os.listdir('.')
    if 'INCAR' not in ' '.join(dir_files):
        src.system_cmd.systemEcho(' [DPT] - There is no INCAR in this directory.')
    else:
        for f in dir_files:
            if os.path.isdir(f):
                continue
            # second, choose the INCAR
            if 'INCAR' in f:
                # judge the INCAR
                with open(f, 'r') as obj:
                    incar = obj.read()
                if 'luse_vdw' in incar.lower():
                    src.system_cmd.systemEcho(' [DPT] Warning: {0} already have vdW correction!'.format(f))
                    continue
                # third, write the vdW correction into INCAR
                with open(f, 'a') as obj:
                    obj.write(vdw_str)
                get_vdW_kernel()
                src.system_cmd.systemEcho(' [DPT] - {0} is corrected by vdW. Method: {1}'.format(f, vdW_method))
        
def get_vdW_kernel():
    path = gp.get_path()
    os.system('cp {0}/lib/vdw_kernel.bindat .'.format(path))