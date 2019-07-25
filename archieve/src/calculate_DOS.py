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
from load_files import load_POSCAR
import system_cmd
from os import path

def get_E_number(content):
    global N_E
    count = 0
    for i, item in enumerate(content):
        if i < 6:
            continue
        if len(item.split()) == 3:
            count = count + 1
        else:
            break
    N_E = count
            
def load_DOSCAR(all_num):
    ''' load POSCAR and get the DOS, energy, and partial DOS'''
    global TOTAL_DOS, PDOS, E_DOS
    if path.exists('DOSCAR') == False:
        system_cmd.systemError('File DOSCAR not found!')
    system_cmd.systemEcho('Reading DOSCAR...')
    with open('./DOSCAR', 'r') as obj:
        content = obj.readlines()
    get_E_number(content)
    TOTAL_DOS = [float(line.split()[1]) for line in content[6:6+N_E]]
    E_DOS = [float(line.split()[0]) for line in content[6:6+N_E]]
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
    s_DOS = cur_atom_DOS[:,0]
    p_DOS = sum(cur_atom_DOS[:,1:4], 1)
    d_DOS = sum(cur_atom_DOS[:,4:], 1)
    return (s_DOS, p_DOS, d_DOS)

def save_DOS(s, p, d, atom):
    ''' save each atom's DOS into files'''
    s, p, d = s.tolist(), p.tolist(), d.tolist()
    all_out = ['%14.9f%14.9f%14.9f%14.9f%14.9f'%(E_DOS[i],TOTAL_DOS[i],s[i],p[i],d[i]) for i, item in enumerate(s)]
    all_out.insert(0, '%14s%14s%14s%14s%14s'%('E','TOTAL',atom+'_s',atom+'_p',atom+'_d'))
    with open('./'+atom+'_dos.dat', 'w') as obj:
        obj.write('\n'.join(all_out))
    system_cmd.systemEcho(atom+'_dos.dat saved!')

def calculate_all_DOS():
    atom_dir = load_POSCAR()
    for item in atom_dir:
        all_num = atom_dir[item][2]
        break
    load_DOSCAR(int(all_num))
    for i, atom in enumerate(atom_dir):
        s, p, d = calculate_atom_DOS(atom_dir[atom][0], atom_dir[atom][1])
        save_DOS(s, p, d, atom)
