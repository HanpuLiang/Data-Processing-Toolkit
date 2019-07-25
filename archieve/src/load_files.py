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
from math import pi, sqrt
from os import system, path
import time, system_cmd
from one_column_type import one_column_type

def load_EIGENVAL():
    ''' Read all lines in file EIGENVAL
        Get the number of k-points: N_KPOINTS
        Get the number of calculated band: N_BAND
        Get the body of EIGENVAL: EIGENVAL_BODY'''
    global EIGENVAL_BODY, N_KPOINTS, N_BAND
    if path.exists('EIGENVAL') == False:
        system_cmd.systemError('File EIGENVAL not found!')
    system_cmd.systemEcho('Reading EIGENVAL...')
    with open('./EIGENVAL', 'r') as obj:
        content = obj.readlines()
    lines_num = len(content)
    # first 7 lines in EIGENVAL
    EIGENVAL_HEAD = content[0:7]
    # other lines in file
    EIGENVAL_BODY = content[7:]
    while ' \n' in EIGENVAL_BODY:
        EIGENVAL_BODY.remove(' \n')
    N_KPOINTS = int(EIGENVAL_HEAD[5].split()[1])
    N_BAND = int(EIGENVAL_HEAD[5].split()[2])

def get_k_points():
    ''' Read the k-points from the file OUTCAR
        Get the k-points data: KPOINTS'''
    global KPOINTS, K
    if path.exists('OUTCAR') == False:
        system_cmd.systemError('File OUTCAR not found!')
    system_cmd.systemEcho('Reading OUTCAR...')
    with open('./OUTCAR', 'r') as obj:
        content = obj.readlines()
    # get the k-points data
    for i, line in enumerate(content):
        if '2pi/SCALE' in line:
            KPOINTS = [[float(num) for num in (item.split())[0:3]] for item in content[i+1:i+1+N_KPOINTS]]
            break
    else:
        system_cmd.systemError('File OUTCAR is incomplete!')

def get_k_path():
    '''Calculate the k-points path and output to the file KPATH'''
    global KPOINTS, K
    # get all k path
    K = []
    ki_len = 0
    k0 = KPOINTS[0]
    for i, ki in enumerate(KPOINTS):
        dkx, dky, dkz = ki[0]-k0[0], ki[1]-k0[1], ki[2]-k0[2]
        dk = sqrt(dkx**2 + dky**2 + dkz**2)
        ki_len = ki_len + dk
        K.append(ki_len)
        k0 = ki
    # delete extra lines
    extra_num = extra_k_number()
    K = K[extra_num:]
    KPOINTS = KPOINTS[extra_num:]
    # save it into file
    kpoints_str = ['%14.8f' % (k) for i, k in enumerate(K)]
    with open('./K.dat', 'w') as obj:
        obj.write('\n'.join(kpoints_str))
        system_cmd.systemEcho('K.dat saved!')

def extra_k_number():
    ''' Read file KPOINTS.3 and get the extra calculated line''' 
    if path.exists('KPOINTS.3') == False:
        system_cmd.systemError('File KPOINTS.3 not found!')
    with open('./KPOINTS.3', 'r') as obj:
        K3 = obj.readlines()
    count = 0
    for i, line in enumerate(K3):
        if i < 3:
            continue
        if (line.split()[3])[0] != '0':
            count = count + 1
    return count

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
        system_cmd.systemError('E-fermi not found!')
    
def get_energy():
    '''Calculate the energy relate to the fermi energy'''
    global ENERGY, N_KPOINTS, N_BAND
    E = []
    for i in range(0, N_KPOINTS):
        for j in range(0, N_BAND):
            E.append(float(EIGENVAL_BODY[j+1+i*(N_BAND+1)].split()[1])-EFERMI)
    ENERGY = split_list(E, N_BAND)
    # delete extra line
    extra_num = extra_k_number()
    ENERGY = ENERGY[extra_num:]
    N_KPOINTS = N_KPOINTS
    N_BAND = N_BAND

def split_list(list_cur, step):
    return [list_cur[i:i+step] for i in range(0, len(list_cur), step)]

def load_PROCAR():
    ''' get the data of orbit contribution'''
    global PROCAR_HEAD, PROCAR_BODY
    system_cmd.systemEcho('Reading PROCAR...')
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
        system_cmd.systemError('File POSCAR not found!')
    system_cmd.systemEcho('Reading POSCAR...')
    with open('./POSCAR', 'r') as obj:
        content = obj.readlines()
    atom_type = content[5].split()
    atom_number = content[6].split()
    # {'atom_type':[N_num, N_begin, N_all_atoms]}
    atom_dir = {}
    N_all_atoms = 0
    # get the number of all the atoms
    if len(atom_type) != len(atom_number):
        system_cmd.systemError('Incorrect POSCAR format!')
    for i, item in enumerate(atom_number):
        N_all_atoms = N_all_atoms + int(item)
        system_cmd.systemEcho('Atom [%3s] number: [%5s]'%(atom_type[i],item))
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
    for i in range(0, N_KPOINTS):
        par_mid = 0.0
        for j in range(0, N_BAND):
            par_mid = 0.0
            position = j*(N_all_atoms+3) + i*((N_all_atoms+3)*N_BAND+3)
            tot_line = PROCAR_BODY[4 + N_all_atoms + position].split()
            if tot_line[0] != 'tot':
                system_cmd.systemError('Incorrect PROCAR format!')
            tot_mid = float(tot_line[10])
            for l in range(0, N_num):
                # get the orbit contribution of each band (j) and k (i)
                par_mid = par_mid + float(PROCAR_BODY[4 + N_begin + l + position].split()[N_orbits])
            P.append(par_mid/tot_mid)
    return P

def save_band(savetype=None):
    ''' save band data into file'''
    extra_num = extra_k_number()
    system_cmd.systemEcho('[ %15s : %10.6f ]'%('E-fermi', EFERMI))
    system_cmd.systemEcho('[ %15s : %10d ]'%('K points number', N_KPOINTS-extra_num))
    system_cmd.systemEcho('[ %15s : %10d ]'%('Band number', N_BAND-extra_num))
    if savetype == True:
        one_column_type(K, ENERGY)
    elif savetype == None:
        with open('./Energy.dat', 'w') as obj:
            E_str1 = [[str(i2) for i2 in i1] for i1 in ENERGY]
            E_str2 = ['\t'.join(item) for item in E_str1]
            obj.write('\n'.join(E_str2))
            system_cmd.systemEcho('Energy.dat saved!')

def save_atom_orbits(savetype=None):
    ''' save orbit's data into file'''
    if not path.exists('all_orbits'):
        system('mkdir all_orbits')
        system_cmd.systemEcho('all_orbits/ created!')
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
        system_cmd.systemEcho('Atom %3s\'s orbits file saved!'%(atom))
        if savetype == True:
            one_column_type(K, ENERGY, atom, savetype)

def calculate_band_gap():
    band_array = array(ENERGY)
    VBM_num = 0
    # find the valence band maxmium
    for i, item in enumerate(band_array[-1,:]):
        if item < 0 and band_array[-1, i+1] > 0:
            VBM_num = i
            break
    VBM = max(band_array[:, 0:VBM_num+1])
    CBM = min(band_array[:, VBM_num+1:])
    band_gap = CBM - VBM 
    system_cmd.systemEcho('[ CBM : %10.6f ]'%(CBM))
    system_cmd.systemEcho('[ VBM : %10.6f ]'%(VBM))
    system_cmd.systemEcho('[ Gap : %10.6f ]'%(band_gap))
    

if __name__ == '__main__':
    load_EIGENVAL()
    get_k_points()
    get_k_path()
    get_E_fermi()
    get_energy()
    load_PROCAR()
    save_atom_orbits(True)
