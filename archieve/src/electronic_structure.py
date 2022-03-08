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

from numpy import array, max, min
import numpy as np
from math import pi, sqrt
from os import system, path
import time, src.system_cmd
from src.one_column_type import one_column_type

def load_EIGENVAL():
    ''' Read all lines in file EIGENVAL
        Get the number of k-points: N_KPOINTS
        Get the number of calculated band: N_BAND
        Get the body of EIGENVAL: EIGENVAL_BODY'''
    global EIGENVAL_BODY, N_ELECTRONS, N_KPOINTS, N_BAND, SPIN
    if path.exists('EIGENVAL') == False:
        src.system_cmd.systemError(' File EIGENVAL not found!')
    src.system_cmd.systemEcho(' [DPT] - Reading EIGENVAL...')
    with open('./EIGENVAL', 'r') as obj:
        content = obj.readlines()
    lines_num = len(content)
    # first 7 lines in EIGENVAL
    EIGENVAL_HEAD = content[0:7]
    # other lines in file
    EIGENVAL_BODY = content[7:]
    while ' \n' in EIGENVAL_BODY:
        EIGENVAL_BODY.remove(' \n')
    N_ELECTRONS = int(EIGENVAL_HEAD[5].split()[0])
    N_KPOINTS = int(EIGENVAL_HEAD[5].split()[1])
    N_BAND = int(EIGENVAL_HEAD[5].split()[2])
    SPIN = int(EIGENVAL_HEAD[0].split()[3])-1


def get_k_points():
    ''' Read the k-points from the file OUTCAR
        Get the k-points data: KPOINTS'''
    global KPOINTS, K, KPOINTS_WEIGHT, BAND_METHOD
    if path.exists('OUTCAR') == False:
        src.system_cmd.systemError(' File OUTCAR not found!')
    src.system_cmd.systemEcho(' [DPT] - Reading OUTCAR...')
    # judge the HSE or PBE
    with open('./INCAR', 'r') as obj:
        incar = obj.read()
    if 'HFSCREEN' in incar:
        BAND_METHOD = 'HSE06'
    else:
        BAND_METHOD = 'PBE'
    src.system_cmd.systemEcho(' [DPT] - Band method: {0}'.format(BAND_METHOD))
    with open('./OUTCAR', 'r') as obj:
        content = obj.readlines()
    # get the k-points data
    for i, line in enumerate(content):
        if '2pi/SCALE' in line:
            kpoints_data = np.array([[float(num) for num in (item.split())[0:4]] for item in content[i+1:i+1+N_KPOINTS]])
            KPOINTS = kpoints_data[:, 0:3]
            KPOINTS_WEIGHT = kpoints_data[:,3]
            break
    else:
        src.system_cmd.systemError(' File OUTCAR is incomplete!')

def get_k_path():
    '''Calculate the k-points path and output to the file KPATH'''
    global KPOINTS, K
    # get all k path
    K = []
    ki_len = 0
    k0 = KPOINTS[0,:]
    for i, ki in enumerate(KPOINTS):
        dkx, dky, dkz = ki[0]-k0[0], ki[1]-k0[1], ki[2]-k0[2]
        dk = np.sqrt(dkx**2 + dky**2 + dkz**2)
        ki_len = ki_len + dk
        K.append(2*3.1415926*ki_len)
        k0 = ki
    # delete extra lines
    extra_num = extra_k_number()
    K = np.array(K[extra_num:])
    KPOINTS = KPOINTS[extra_num:]

def extra_k_number():
    global KPOINTS_WEIGHT, BAND_METHOD
    if BAND_METHOD == 'PBE':
        return 0
    elif BAND_METHOD == 'HSE06':
        for i, w in enumerate(KPOINTS_WEIGHT):
            if abs(w) < 1e-5:
                 return i
        else:
            src.system_cmd.systemError(' Unknown K-Path Weights in OUTCAR')
    else:
        src.system_cmd.systemError(' Unknown Electronic Structure Calculational Method!')

def get_E_fermi():
    ''' Read the fermi level of energy from file OUTCAR
        The fermi energy: Efermi'''
    global EFERMI
    with open('OUTCAR', 'r') as obj:
        content = obj.readlines()
    EFERMI = 0
    for line in content:
        temp = line.split()
        if 'E-fermi' in temp:
            EFERMI = float(temp[2])
            break
    else:
        src.system_cmd.systemError(' E-fermi not found!')
    
def get_energy():
    '''Calculate the energy relate to the fermi energy'''
    global ENERGY, N_KPOINTS, N_BAND
    # the number of energy band decided by SPIN
    # when SPIN=1, ENERGY only have one, and when SPIN=2, ENERGY have two in third dimension of tensor
    energy_temp = np.zeros((N_BAND, N_KPOINTS, SPIN+1))
    for s in range(SPIN+1):
        E = []
        for i in range(0, N_KPOINTS):
            E_cur_k = np.array([float(line.split()[1+s]) for line in EIGENVAL_BODY[i*(N_BAND+1)+1:(i+1)*(N_BAND+1)]])
            energy_temp[:,i,s] = E_cur_k
    # transpose the tensor (fixed the third axis and transpose the others)
    ENERGY = np.zeros((N_KPOINTS, N_BAND, SPIN+1))
    for s in range(SPIN+1):
        ENERGY[:,:,s] = np.transpose(energy_temp[:,:,s])
    # delete extra line
    extra_num = extra_k_number()
    ENERGY = ENERGY[extra_num:,:,:]
    N_KPOINTS = N_KPOINTS - extra_num
    N_BAND = N_BAND

def split_list(list_cur, step):
    return [list_cur[i:i+step] for i in range(0, len(list_cur), step)]

def load_PROCAR():
    ''' get the data of orbit contribution'''
    global PROCAR_HEAD, PROCAR_BODY
    src.system_cmd.systemEcho(' [DPT] - Reading PROCAR...')
    with open('./PROCAR', 'r') as obj:
        content = obj.readlines()
    PROCAR_HEAD = content[0:3]
    PROCAR_BODY = content[3:]
    for i, item in enumerate(PROCAR_BODY):
        if item == ' \n':
            PROCAR_BODY.pop(i)

def load_POSCAR():
    ''' get the information of each atom in supercell'''
    if path.exists('POSCAR') == False:
        src.system_cmd.systemError(' File POSCAR not found!')
    src.system_cmd.systemEcho(' [DPT] - Reading POSCAR...')
    with open('./POSCAR', 'r') as obj:
        content = obj.readlines()
    atom_type = content[5].split()
    atom_number = content[6].split()
    # {'atom_type':[N_num, N_begin, N_all_atoms]}
    atom_dir = {}
    N_all_atoms = 0
    # get the number of all the atoms
    if len(atom_type) != len(atom_number):
        src.system_cmd.systemError(' Incorrect POSCAR format!')
    for i, item in enumerate(atom_number):
        N_all_atoms = N_all_atoms + int(item)
        src.system_cmd.systemEcho(' [DPT] - Atom [%3s] number: [%5s]'%(atom_type[i],item))
    for i, atom in enumerate(atom_type):
        N_begin_temp = 0
        for j in range(i):
            N_begin_temp = N_begin_temp + int(atom_number[j])
        atom_dir[atom] = [int(atom_number[i]), N_begin_temp, N_all_atoms]
        N_begin_temp = 0
    return atom_dir

def calculate_contribution(N_num, N_begin, N_orbits, N_all_atoms):
    ''' get the atomic contribution from PROCAR'''
    P = []
    extra_num = extra_k_number()
    for i in range(0, N_KPOINTS+extra_num):
        par_mid = 0.0
        for j in range(0, N_BAND):
            par_mid = 0.0
            position = j*(N_all_atoms+3) + i*((N_all_atoms+3)*N_BAND+3)
            tot_line = PROCAR_BODY[4 + N_all_atoms + position].split()
            if tot_line[0] != 'tot':
                src.system_cmd.systemError(' Incorrect PROCAR format!')
            tot_mid = float(tot_line[10])
            for l in range(0, N_num):
                # get the orbit contribution of each band (j) and k (i)
                par_mid = par_mid + float(PROCAR_BODY[4 + N_begin + l + position].split()[N_orbits+1])
            if tot_mid < 0.0001:
                temp = 0
            else:
                temp = par_mid/tot_mid
            P.append(temp)
    return P

def save_band(savetype=None, E_0='fermi'):
    ''' save band data into file'''
    global VBM
    extra_num = extra_k_number()
    src.system_cmd.systemEcho(' [DPT] - Basic electronic structure parameters')
    src.system_cmd.systemEcho('     [ %17s : %10d ]'%('Electrons number', N_ELECTRONS))
    src.system_cmd.systemEcho('     [ %17s : %10d ]'%('K points number', N_KPOINTS))
    src.system_cmd.systemEcho('     [ %17s : %10d ]\n'%('Band number', N_BAND))
    calculate_band_gap()
    set_Energy_to_Fermi(E_0)
    if savetype == True:
        one_column_type(K, ENERGY)
    elif savetype == None:
        # save it into file
        if SPIN == 0:
            file_name = ['DPT.BAND.dat']
        elif SPIN == 1:
            file_name = ['DPT.BAND.UP.dat', 'DPT.BAND.DOWN.dat']
        for s in range(SPIN+1):
            out_files = np.concatenate((K.reshape(N_KPOINTS, 1), ENERGY[:,:,s]), axis=1)
            with open(file_name[s], 'w') as obj:
                E_str = '\n'.join([''.join(['{0:16.10f}'.format(item) for item in line]) for line in out_files])
                obj.write(E_str)
                src.system_cmd.systemEcho(' [DPT] - {0} saved!'.format(file_name[s]))

def save_atom_orbits(savetype=None):
    ''' save orbit's data into file'''
    if not path.exists('all_orbits'):
        system('mkdir all_orbits')
        src.system_cmd.systemEcho(' [DPT] - all_orbits/ created!')
    atom_dir = load_POSCAR()
    orbits = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2', 'tot']
    extra_num = extra_k_number()
    for j, atom in enumerate(atom_dir):
        for i, orbit in enumerate(orbits):
            atom_contribution = split_list(
                                    calculate_contribution(
                                        atom_dir[atom][0], atom_dir[atom][1], i, atom_dir[atom][2]), 
                                    N_BAND)
            atom_contribution = atom_contribution[extra_num:]
            with open('./all_orbits/'+atom+'_'+orbit+'.dat', 'w') as obj:
                ac_str1 = [['%14.8f'%(i2) for i2 in i1] for i1 in atom_contribution]
                ac_str2 = [''.join(item) for item in ac_str1]
                obj.write('\n'.join(ac_str2))
        src.system_cmd.systemEcho(' [DPT] - Atom %3s\'s orbits file saved!'%(atom))
        if savetype == True:
            one_column_type(K, ENERGY, atom, savetype)

def calculate_band_gap():
    global VBM
    band_array = ENERGY.copy()
    VBM_num = int(N_ELECTRONS/2)
    VBM = max(band_array[:, 0:VBM_num, 0])
    CBM = min(band_array[:, VBM_num:, 0])
    band_gap = CBM - VBM 
    src.system_cmd.systemEcho(' [DPT] - VBM, CBM and Gap (unit eV)')
    src.system_cmd.systemEcho('     [ %17s : %10.6f ]'%('E-fermi',EFERMI))
    src.system_cmd.systemEcho('     [ %17s : %10.6f ]'%('CBM',CBM))
    src.system_cmd.systemEcho('     [ %17s : %10.6f ]'%('VBM',VBM))
    src.system_cmd.systemEcho('     [ %17s : %10.6f ]\n'%('Gap',band_gap))

def set_Energy_to_Fermi(E_0):
    global ENERGY
    if E_0.lower() == 'fermi':
        ENERGY = ENERGY - EFERMI
        src.system_cmd.systemEcho(' [DPT] - E = 0 Be Set to Fermi Energy!')
    elif E_0.lower() == 'vbm':
        ENERGY = ENERGY - VBM
        src.system_cmd.systemEcho(' [DPT] - E = 0 Be Set to VBM!')
    else:
        src.system_cmd.systemError(' Wrong Fermi Level Parameter!')
    

if __name__ == '__main__':
    load_EIGENVAL()
    get_k_points()
    get_k_path()
    get_E_fermi()
    get_energy()
    set_Energy_to_Fermi()
    load_PROCAR()
    save_atom_orbits(True)
