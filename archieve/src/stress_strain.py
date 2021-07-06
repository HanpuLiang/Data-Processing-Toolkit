import numpy as np 
import os, copy
import src.system_cmd
from os import path

def get_POSCAR(file_name='POSCAR'):
    if path.exists('POSCAR') == False:
        src.system_cmd.systemError(' File POSCAR not found!')
    with open(file_name, 'r') as obj:
        poscar = obj.readlines()
    lattice = np.array([[float(item) for item in line.split()] for line in poscar[2:5]])
    src.system_cmd.systemEcho(' [DPT] - Reading POSCAR...')
    return [poscar, lattice]

def strain_lattice(lattice, direction, strain):
    new_lattice = copy.deepcopy(lattice)
    if direction == 'x':
        new_lattice[:,0] = lattice[:,0]*(1+strain)
    elif direction == 'y':
        new_lattice[:,1] = lattice[:,1]*(1+strain)
    elif direction == 'z':
        new_lattice[:,2] = lattice[:,2]*(1+strain)
    elif direction == 'xy':
        new_lattice[:,0:2] = lattice[:,0:2]*(1+strain)
    elif direction == 'xyz':
        new_lattice[:,0:3] = lattice[:,0:3]*(1+strain)
    elif direction == 'a':
        new_lattice[0,:] = lattice[0,:]*(1+strain)
    elif direction == 'b':
        new_lattice[1,:] = lattice[1,:]*(1+strain)
    elif direction == 'c':
        new_lattice[2,:] = lattice[2,:]*(1+strain)
    else:
        src.system_cmd.systemError(' Incorrect strain direction!')
    return new_lattice

def save_strain_poscar(poscar, lattice, num):
    lattice_str = ['%15.8f%15.8f%15.8f\n'%(lattice[i,0], lattice[i,1], lattice[i,2]) for i in range(3)]
    temp_poscar = poscar[:]
    temp_poscar[2:5] = lattice_str
    new_poscar = ''.join(temp_poscar)
    file_name = 'DPT.strain.POSCAR.'+str(10000+num)[1:]
    with open(file_name, 'w') as obj:
        obj.write(new_poscar)

def output_information(strain_direction, strain_begin, strain_end, strain_step, sign):
    strain_len = len(np.arange(sign*strain_begin, sign*(strain_end+strain_step), sign*strain_step))
    out_str = ''' [DPT] - Straining Parameters:
    Strain direction      : {0:6s}
    Initial strain length : {1:6.3f}
    End strain length     : {2:6.3f}
    Strain step           : {3:6.3f}
    Total strain number   : {4:6.0f}'''.format(strain_direction, sign*strain_begin, sign*strain_end, sign*strain_step, strain_len)
    src.system_cmd.systemEcho(out_str)

def get_parameters(file_name='system.log'):
    with open(file_name, 'r') as obj:
        log_file = obj.readlines()
    # log_file = [line.split() for line in log_file]
    log_data = []
    for i, line in enumerate(log_file):
        if 'Straining Parameters' in line:
            log_data.append(log_file[i+1:i+6])
    if len(log_data) == 0:
        src.system_cmd.systemEcho(' [DPT] - File system.log not found!')
    cur_parameters = log_data[-1]
    cur_parameters = [item.split() for item in cur_parameters]
    dir, ini, end, step, tot = cur_parameters[0][3], float(cur_parameters[1][4]), float(cur_parameters[2][4]), float(cur_parameters[3][3]), int(cur_parameters[4][4])
    strain_list = np.arange(ini, end+step, step)
    return [strain_list, tot]


def get_press(tot):
    press_list = []
    for i in range(int(tot)):
        dir_name = 'job-'+str(10000+i)[1:]
        cmd = "grep 'in kB ' %s/OUTCAR"%(dir_name)
        res = os.popen(cmd).readlines()
        if len(res) == 0:
            src.system_cmd.systemError('OUTCAR missing in %s'%(dir_name))
        press_list.append(res[-1].split()[2:])
    press_list = np.array([[float(item) for item in line] for line in press_list])
    return press_list

def save_press(press, strain):
    out_file = '\n'.join(['%6.5f  %15.6f %15.6f %15.6f %15.6f %15.6f %15.6f '%(strain[i],press[i,0],press[i,1],press[i,2],press[i,3],press[i,4],press[i,5]) for i in range(len(strain))])
    with open('DPT.stress-strain.dat', 'w') as obj:
        obj.write(out_file)
    src.system_cmd.systemEcho(' [DPT] - File DPT.stress-strain.dat created!')

def get_strain_sign(strain_type):
    if strain_type == 'pos':
        sign = 1.0
    elif strain_type == 'neg':
        sign = -1.0
    else:
        src.system_cmd.systemError(' Wrong Strain Type, Please Enter [pos/neg]')
    return sign

def save_number_strain_relation(strain_list):
    out_str = '\n'.join(['{0} {1:6.3f}'.format(str(10000+i)[1:], strain) for i, strain in enumerate(strain_list)])
    with open('DPT.num_to_strain.dat', 'w') as obj:
        obj.write(out_str)

def stress_strain(strain_direction, strain_begin, strain_end, strain_step, strain_process, strain_type):
    if strain_process == 'cal':
        poscar, lattice_ori = get_POSCAR()
        sign = get_strain_sign(strain_type)
        output_information(strain_direction, strain_begin, strain_end, strain_step, sign)
        strain_list = np.arange(sign*strain_begin, sign*(strain_end+strain_step), sign*strain_step)
        for i, strain in enumerate(strain_list):
            lattice = strain_lattice(lattice_ori, strain_direction, strain)
            save_strain_poscar(poscar, lattice, i)
        save_number_strain_relation(strain_list)
        src.system_cmd.systemEcho(' [DPT] - Strain Finish.')
    elif strain_process == 'plot':
        strain_list, tot = get_parameters()
        press_list = get_press(tot)
        save_press(press_list, strain_list)
