import os, src.system_cmd
import numpy as np

def get_dielectric():
    os.system("grep 'DIELECTRIC TENSOR (including local field effects in DFT' OUTCAR -A 4 | tail -n 3 > dielectric.dat")
    src.system_cmd.systemEcho(' [DPT] - Dielectric tensor save into dielectric.dat successful!')

def get_born_charges():
    tot_atoms = get_total_atoms_number()
    cmd = "grep 'BORN EFFECTIVE CHARGES' OUTCAR -A "+str(int(tot_atoms*4+1))+" > born_charges.dat"
    os.system(cmd)
    src.system_cmd.systemEcho(' [DPT] - Born effective charges save into born_chagres.dat successful!')

def get_total_atoms_number(file_name='POSCAR'):
    with open(file_name, 'r') as obj:
        poscar = obj.readlines()
    tot_atoms = np.sum(np.array([float(item) for item in poscar[6].split()]))
    return tot_atoms

def born_dielectric():
    get_dielectric()
    get_born_charges()
