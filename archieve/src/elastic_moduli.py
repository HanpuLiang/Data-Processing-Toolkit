import numpy as np 
import os
import src.system_cmd

def get_elastic_moduli_tensor(file_name='OUTCAR'):
    # em_ct = os.popen("grep 'TOTAL ELASTIC MODULI' OUTCAR -A 7").readlines()[3:]
    with open(file_name, 'r') as obj:
        outcar = obj.readlines()
    for i, line in enumerate(outcar):
        if 'TOTAL ELASTIC MODULI' in line:
            em_ct = outcar[i+3:i+9]
    tensor = np.array([[float(item) for item in line.split()[1:]] for line in em_ct])
    return tensor

def get_POSCAR(file_name='POSCAR'):
    with open(file_name, 'r') as obj:
        poscar = obj.readlines()
    l = poscar[2:5]
    lattice = np.array([[float(item) for item in line.split()] for line in l])
    return lattice

def convert_standard(tensor, lattice, dimension):
    if dimension == 2:
        tensor = tensor * lattice[2,2]/10   # mutiply vaccum then divide 10
    tensor = np.concatenate((tensor[:,0:3], tensor[:,4:6],np.array([tensor[:,3]]).T), axis=1)
    tensor = np.concatenate((tensor[0:3,:], tensor[4:6,:],np.array([tensor[3,:]])), axis=0)/10
    return tensor

def mechanically_stable(tensor):
    E = np.linalg.eigvals(tensor)
    if np.all(E>0):
        src.system_cmd.systemEcho(' [DPT] - This structure is mechanically stable!')
    else:
        src.system_cmd.systemEcho(' [DPT] * WARNING * This structure is not mechanically stable.')

def calculated_modulous(tensor):
    c11, c22, c12, c21, c66 = tensor[0,0], tensor[1,1], tensor[0,1], tensor[1,0], tensor[5,5]
    E_x, E_y = (c11*c22-c12*c21)/c22, (c11*c22-c12*c21)/c11 # Young's (E_i)
    v_xy, v_yx = c21/c22, c12/c11                           # Poisson's ratios (v_ij)
    G_xy = c66                                              # shear moduli (G_ij)
    return [E_x, E_y, v_xy, v_yx, G_xy]
    

def save_quantities(elastic_tensor, modulous):
    str_elastic_tensor = '\n'.join(['{0:^20.6f}{1:^20.6f}{2:^20.6f}{3:^20.6f}{4:^20.6f}{5:^20.6f}'.format(line[0],line[1],line[2],line[3],line[4],line[5]) for line in elastic_tensor])
    str_modulous = '{0:^20.6f}{1:^20.6f}{2:^20.6f}{3:^20.6f}{4:^20.6f}'.format(modulous[0],modulous[1],modulous[2],modulous[3],modulous[4])
    
    src.system_cmd.systemEcho(' [DPT] - Elastic Constant C_ij (unit N/m)')
    src.system_cmd.systemEcho(str_elastic_tensor)
    head_line = '{0:^20s}{1:^20s}{2:^20s}{3:^20s}{4:^20s}'.format('E_x', 'E_y', 'v_xy', 'v_yx', 'G_xy')
    # head_line = '{0:^20s}{1:^20s}{2:^20s}{3:^20s}{4:^20s}'.format('B', 'G', 'Hv', 'E', 'v')
    src.system_cmd.systemEcho(" [DPT] - Young's modulus E, Poisson's ratios v, and shear moduli G  (unit N/m)")
    src.system_cmd.systemEcho(head_line)
    src.system_cmd.systemEcho(str_modulous)
    save_file(str_elastic_tensor, 'DPT.elastic_constant.dat')
    save_file(head_line+'\n'+str_modulous, 'DPT.modulous.dat')
    src.system_cmd.systemEcho(' [DPT] Files DPT.elastic_constant.dat and DPT.modulous.dat have been created!')

def save_file(out_str, file_name):
    with open(file_name, 'w') as obj:
        obj.write(out_str)


def elastic_moduli(dimension=3):
    # get elastic tensor
    elastic_tensor = get_elastic_moduli_tensor()
    # get lattice in POSCAR
    lattice = get_POSCAR()
    # change to standard form
    elastic_tensor = convert_standard(elastic_tensor, lattice, dimension)
    # make sure the mechanically stable
    mechanically_stable(elastic_tensor)
    # all kinds of modulous and something else
    modulous = calculated_modulous(elastic_tensor)
    # save all quantities
    save_quantities(elastic_tensor, modulous)
