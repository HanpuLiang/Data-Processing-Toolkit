# -*- coding: utf-8 -*-
'''
@author: Hanpu Liang
@create date: 2019/07/22
@description: This code integrates to get the energy band data, PDOS, and fat energy band data.
MIT License

Copyright (c) 2019 Hanpu Liang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import src.system_cmd, numpy as np
from os import system, path
import src.get_path as gp

def thermal_electric(te_action, te_dimension):
    '''
    MAIN PROCESS FLOW FUNCTION.
    '''
    if te_action == 'none':
        src.system_cmd.systemError('Please input the parameters you want. [relax/band/process]')
    elif te_action == 'relax':
        create_relax_files(te_dimension)
    elif te_action == 'band':
        create_band_files(te_dimension)
    elif te_action == 'process':
        process_te_data(te_dimension)

######################################################## 
##
##  Part I
##  Create Relaxation Directory
##
######################################################## 

def create_relax_files(te_dimension):
    '''create directory and copy all relaxtion files'''
    # find the POSCAR and POTCAR in this directory
    if path.exists('POSCAR') == False or path.exists('POTCAR') == False:
        src.system_cmd.systemError(' File POSCAR or POTCAR not found!')
    # create relaxation/ and it's subdirectory
    if path.exists('relaxation'):
        system('rm relaxation/ -rf')
    system('mkdir relaxation')
    strain_range, strain_dimension = get_strain_range(te_dimension)
    for sd in strain_dimension:
        for sr in strain_range:
            cur_dir = 'relaxation/{0}/{1:4.3f}'.format(sd, sr)
            if path.exists(cur_dir):
                system('rm {0}/*'.format(cur_dir))
            else:
                system('mkdir -p '+cur_dir)
            get_relaxation_files(cur_dir, sd, sr)
            print(' Directory {0} create!'.format(cur_dir))
    print(' [DPT] - All relaxation files are ready!'.format(cur_dir))
    
def get_relaxation_files(cur_dir, sd, sr):
    '''copy files from software and modify POSCAR'''
    software_path = gp.get_path()
    system('cp {0}/lib/te/relaxation/* ./{1}/.'.format(software_path, cur_dir))
    system('cp POTCAR ./{0}/POTCAR'.format(cur_dir))
    system("sed -i s/job-name/DPT-rel-{0}{1}/g job-rel.pbs".format(sd, sr))
    # strain the POSCAR
    strain_POSCAR(cur_dir, sd, sr)

def strain_POSCAR(cur_dir, sd, sr):
    with open('POSCAR', 'r') as obj:
        poscar = obj.readlines()
    vecs = np.array([[float(item) for item in line.split()] for line in poscar[2:5]])
    if sd == 'x':
        vecs[:,0] = sr * vecs[:,0]
    elif sd == 'y':
        vecs[:,1] = sr * vecs[:,1]
    elif sd == 'z':
        vecs[:,2] = sr * vecs[:,2]
    vecs_strained = [' {0:21.016f} {1:21.016f} {2:21.016f}\n'.format(line[0],line[1],line[2]) for line in vecs]
    poscar[2:5] = vecs_strained
    with open('{0}/POSCAR'.format(cur_dir), 'w') as obj:
        obj.write(''.join(poscar))

def get_strain_range(te_dimension):
    '''get the strain range and strain dimension. maybe these can be inputed by reading input files.'''
    strain_range = [0.99, 0.995, 1.00, 1.005, 1.01]
    if te_dimension == 2:
        strain_dimension = ['x', 'y']
    elif te_dimension == 3:
        strain_dimension = ['x', 'y', 'z']
    else:
        src.system_cmd.systemError(' Wrong te_dimension parameters, please enter 2 or 3.')
    return strain_range, strain_dimension

######################################################## 
##
##  Part II
##  Create Band Directory
##
######################################################## 

def create_band_files(te_dimension):
    '''check the files in relaxation dir and create energy band calculation job.'''
    # check the brillious path file KPOINTS.3
    if path.exists('KPOINTS.3') == False:
        src.system_cmd.systemError(' File KPOINTS.3 not found!')
    # check the band directory
    if path.exists('band'):
        system('rm band/ -rf')
    system('mkdir band')
    strain_range, strain_dimension = get_strain_range(te_dimension)
    for sd in strain_dimension:
        for sr in strain_range:
            cur_dir = 'band/{0}/{1:4.3f}'.format(sd, sr)
            rel_dir = 'relaxation/{0}/{1:4.3f}'.format(sd, sr)
            # find band directory
            if not path.exists(rel_dir):
                src.system_cmd.systemError(' Directory {0} not found!'.format(rel_dir))
            # clear band directory
            if path.exists(cur_dir):
                system('rm {0}/*'.format(cur_dir))
            else:
                system('mkdir -p '+cur_dir)
            get_band_files(cur_dir, rel_dir, sd, sr)
            print(' Directory {0} create!'.format(cur_dir))
    print(' [DPT] - All band files are ready!'.format(cur_dir))

def get_band_files(cur_dir, rel_dir, sd, sr):
    '''copy band files and make sure CONTCAR in relaxation directory exists.'''
    software_path = gp.get_path()
    system('cp {0}/lib/te/band/* ./{1}/.'.format(software_path, cur_dir))
    system('cp ./{0}/CONTCAR ./{1}/POSCAR'.format(cur_dir))
    system('cp ./{0}/POTCAR ./{1}/POTCAR'.format(cur_dir))
    system('cp KPOINTS.3 ./{1}/KPOINTS.3'.format(cur_dir))
    system("sed -i s/job-name/DPT-band-{0}{1}/g job-band.pbs".format(sd, sr))

######################################################## 
##
##  Part III
##  Processing The Data of Relaxation and Energy Band
##
######################################################## 

def process_te_data(te_dimension):
    '''Processing the data, calculate the ...'''
    strain_range, strain_dimension = get_strain_range(te_dimension)
    if not path.exists('output'):
        system('mkdir output')
        print('output/ created!')
    with open('./output/te_input.dat', 'w') as obj:
        obj.write('# {0} {1} {2} {3}\n'.format('E1', 'A0', 'B2', 'ms'))
    for sd in strain_dimension:
        # initial cbm, vbm and energy array
        cbm_all = np.zeros(len(strain_range))
        vbm_all = np.zeros(len(strain_range))
        F_all = np.zeros(len(strain_range))
        for i, sr in enumerate(strain_range):
            # get the cbm, vbm and energy of each structrues 
            src.system_cmd.systemEcho(' [DPT] ### Direction: [{0}] Formation: [{1}] ###'.format(sd, sr))
            rel_dir = 'relaxation/{0}/{1}'.format(sd, sr)
            band_dir = 'band/{0}/{1}'.format(sd, sr)
            cbm, vbm, E_fermi = get_band_parameters(band_dir)
            vac = get_vac(rel_dir)
            F_all[i] = get_free_energy(rel_dir)
            cbm_all[i] = cbm - vac
            vbm_all[i] = vbm - vac

def get_band_parameters(band_dir):
    '''use DPT and get band parameters'''
    system('cd {0} && DPT-b > band_data.dat'.format(band_dir))
    with open('{0}/band_data.dat'.format(band_dir), 'r') as obj:
        band_data = obj.readlines()
    E_fermi, vbm, cbm = -999, -999, -999
    for line in b_d:
        temp = line.split()
        if len(temp) == 0:
            continue
        if temp[1] == 'E-fermi':
            E_fermi = float(temp[3])
        if temp[1] == 'VBM':
            vbm = float(temp[3])
        if temp[1] == 'CBM':
            cbm = float(temp[3])
    if E_fermi == -999 or vbm == -999 or cbm == -999:
        src.system_cmd.systemError(' band_data.data missed!')
    src.system_cmd.systemEcho(' [DPT] - CBM energy: {0:8.5f} (eV)'.format(cbm))
    src.system_cmd.systemEcho(' [DPT] - VBM energy: {0:8.5f} (eV)'.format(vbm))
    src.system_cmd.systemEcho(' [DPT] - Fermi energy level: {0:8.5f} (eV)'.format(E_fermi))
    return cbm, vbm, E_fermi

def get_atoms_num(line):
    atom_num = np.sum(np.array([float(item) for item in line.split()]))
    return int(atom_num)

def get_vac(rel_dir):
    '''get vacuum staticelectric potential'''
    with open(rel_dir+'/LOCPOT', 'r') as obj:
        locpot = obj.readlines()
    atom_num = get_atoms_num(locpot[6])
    k = [float(item) for item in locpot[8+atom_num+1].split()]
    all_vac = np.array([[float(item) for item in line.split()] for line in locpot[8+atom_num+2:-1]]).flatten()
    step = 10
    z_vac = np.sum(all_vac[0:step])/step - E_fermi
    src.system_cmd.systemEcho(' [DPT] - Vacuum potential (z-axis): {0:8.5f} (eV)'.format(z_vac))
    return z_vac

def get_free_energy(rel_dir):
    '''get free energy'''
    with open(rel_dir+'/OUTCAR', 'r') as obj:
        outcar = obj.read()
    F = (findall('free  *energy  *TOTEN  *=(.*) eV', outcar))[-1]
    src.system_cmd.systemEcho(' [DPT] - Total free energy: {0:8.5f} (eV)'.format(float(F)))
    return float(F)

