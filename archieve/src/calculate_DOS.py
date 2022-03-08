'''
@author: Hanpu Liang
@data:2019/7/23
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
from numpy import array, zeros, sum
import numpy as np
from src.electronic_structure import load_POSCAR
import src.system_cmd
from os import path

def get_Efermi():
    global E_F
    if path.exists('OUTCAR') == False:
        src.system_cmd.systemError('File OUTCAR not found!')
    with open('./OUTCAR', 'r') as obj:
        content = obj.readlines()
    for line in content:
        if 'E-fermi' in line:
            ct = line.split()
            E_F = float(ct[2])
            break
    else:
        src.system_cmd.systemError('File OUTCAR not finished, E-fermi missed!')
    
        

def load_DOSCAR(all_num):
    ''' load POSCAR and get the DOS, energy, and partial DOS'''
    global TOTAL_DOS, PDOS, E_DOS, N_E, SPIN
    if path.exists('DOSCAR') == False:
        src.system_cmd.systemError('File DOSCAR not found!')
    src.system_cmd.systemEcho(' [DPT] - Reading DOSCAR...')
    with open('./DOSCAR', 'r') as obj:
        content = obj.readlines()
    N_E = int(float(content[5].split()[2]))
    data_total = array([[float(item) for item in line.split()] for line in content[6:6+N_E]])
    TOTAL_DOS = data_total[:,1:]
    if TOTAL_DOS.shape[1] == 4:
        SPIN = 2
    elif TOTAL_DOS.shape[1] == 2:
        SPIN = 1
    else:
        src.system_cmd.systemError('Format of DOSCAR is wrong!')
    E_DOS = data_total[:,0].reshape((N_E,1)) - E_F
    PDOS = [line.split()[1:] for line in content[N_E+6:]]
    for i in range(all_num):
        PDOS.pop(N_E*i)
    PDOS = list2array(PDOS)

def list2array(l):
    l = array([[float(i2) for i2 in i1] for i1 in l])
    return l

def calculate_atom_DOS(N_num, N_begin):
    ''' calculate each atom's DOS'''
    cur_atom_DOS = zeros((N_E,1))
    for i in range(N_begin, N_num+N_begin):
        cur_point = N_E*i
        cur_atom_DOS = cur_atom_DOS + PDOS[cur_point:cur_point+N_E]
    
    if SPIN == 1:
        s_DOS = cur_atom_DOS[:,0].reshape((N_E,1))
        p_DOS = sum(cur_atom_DOS[:,1:4], 1).reshape((N_E,1))
        d_DOS = sum(cur_atom_DOS[:,4:], 1).reshape((N_E,1))
        partial_DOS = np.concatenate((s_DOS, p_DOS, d_DOS), axis=1)
        atom_DOS = np.sum(partial_DOS, axis=1)
        
    elif SPIN == 2:
        UP_s_DOS = cur_atom_DOS[:,0].reshape((N_E,1))
        DOWN_s_DOS = cur_atom_DOS[:,1].reshape((N_E,1))
        UP_p_DOS = (cur_atom_DOS[:,2] + cur_atom_DOS[:,4] + cur_atom_DOS[:,6]).reshape((N_E,1))
        DOWN_p_DOS = (cur_atom_DOS[:,3] + cur_atom_DOS[:,5] + cur_atom_DOS[:,7]).reshape((N_E,1))
        UP_d_DOS = (cur_atom_DOS[:,8] + cur_atom_DOS[:,10] + cur_atom_DOS[:,12] + cur_atom_DOS[:,14] + cur_atom_DOS[:,16]).reshape((N_E,1))
        DOWN_d_DOS = (cur_atom_DOS[:,9] + cur_atom_DOS[:,11] + cur_atom_DOS[:,13] + cur_atom_DOS[:,15] + cur_atom_DOS[:,17]).reshape((N_E,1))
        partial_DOS = np.concatenate((UP_s_DOS, DOWN_s_DOS, UP_p_DOS, DOWN_p_DOS, UP_d_DOS, DOWN_d_DOS), axis=1)
        atom_DOS_UP = UP_s_DOS + UP_p_DOS + UP_d_DOS
        atom_DOS_DOWN = DOWN_s_DOS + DOWN_p_DOS + DOWN_d_DOS
        atom_DOS = np.concatenate((atom_DOS_UP, atom_DOS_DOWN), axis=1)
    return atom_DOS, partial_DOS

def save_DOS(atom_tot, p_dos, atom):
    ''' save each atom's DOS into files'''
    out_data = np.column_stack((E_DOS, atom_tot, p_dos))
    out_data_str = [''.join(['{0:20.9f}'.format(item) for item in line]) for line in out_data]
    if SPIN == 1:
        title_label = ['{0:14s}'.format('E'), '{0:14s}'.format(atom+'_tot'), '{0:14s}'.format(atom+'_s'), '{0:14s}'.format(atom+'_p'), 
            '{0:14s}'.format(atom+'_d')]
    elif SPIN == 2:
        title_label = ['{0:14s}'.format('E'), '{0:14s}'.format(atom+'_UP_tot'), '{0:14s}'.format(atom+'_DOWN_tot'), 
            '{0:14s}'.format(atom+'_UP_s'), '{0:14s}'.format(atom+ '_DOWN_s'), 
            '{0:14s}'.format(atom+ '_UP_p'), '{0:14s}'.format(atom+ '_DOWN_p'), 
            '{0:14s}'.format(atom+ '_UP_d'), '{0:14s}'.format(atom+ '_DOWN_d')]
    title = ''.join(title_label)
    out_data_str.insert(0, title)
    with open('./DPT.'+atom+'_dos.dat', 'w') as obj:
        obj.write('\n'.join(out_data_str))
    src.system_cmd.systemEcho(' [DPT] - DPT.'+atom+'_dos.dat saved!')

def save_tot():
    all_out = [''.join(['{0:20.9f}'.format(E_DOS[i,0])]+['{0:20.9f}'.format(item) for item in line]) for i, line in enumerate(TOTAL_DOS)]
    
    # all_out = ['%14.9f%14.9f'%(E_DOS[i],TOTAL_DOS[i]) for i, item in enumerate(E_DOS)]
    all_out.insert(0, '%14s%14s%14s%14s%14s'%('E','DOS(UP)', 'DOS(DOWN)', 'Int.DOS(UP)', 'Int.DOS(DOWN)'))
    with open('./DPT.TOTAL_dos.dat', 'w') as obj:
        obj.write('\n'.join(all_out))
    src.system_cmd.systemEcho(' [DPT] - DPT.TOTAL_dos.dat saved!')

def calculate_all_DOS():
    get_Efermi()
    atom_dir = load_POSCAR()
    for item in atom_dir:
        all_num = atom_dir[item][2]
        break
    load_DOSCAR(int(all_num))
    save_tot()
    for i, atom in enumerate(atom_dir):
        atom_tot, partial_dos = calculate_atom_DOS(atom_dir[atom][0], atom_dir[atom][1])
        save_DOS(atom_tot, partial_dos, atom)
