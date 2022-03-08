# -*- coding: utf-8 -*-
'''
@author: Liang Hanpu
@create date: 2020/10/26
@description: This parameter are ready to prepartion the VASP inputs files for different calculational situation.
'''

from os import system, path
import src.system_cmd
import src.get_path as gp

def VASP_inputs(file_type, method):
    if file_type == 'rel':
        get_relaxation_files(method)
    elif file_type == 'band':
        get_band_files(method)
    elif file_type == 'diele':
        get_diele_files()
    elif file_type == 'absorp':
        get_absorp_files()
    elif file_type == 'elastic':
        get_elastic_files()
    elif file_type == 'elf':
        get_ELF_files()
    elif file_type == 'pcd':
        get_PCD_files()
    elif file_type == 'force':
        get_force_files()
    elif file_type == 'potcar':
        get_POTCAR_files()
    else:
        src.system_cmd.systemError(' No file type of [{0}] in DPT. :('.format(file_type))
    src.system_cmd.systemEcho(' [DPT] - Files Ready!')

def get_relaxation_files(method):
    '''create structural relaxation files.
    energy : only calculate the energy and not relaxation
    2d : only relax ab-axis and not relax c-axis (i.e. vasp_relax_ab)
    gam : only relax Gamma points around
    default : normal relaxation
    '''
    path = gp.get_path()
    # calculate energy or fully relaxation
    if 'energy' in method:
        system('cp {0}/INCARs/Energy/* .'.format(path))
        modify_job('vasp_std')
    else:
        system('cp {0}/INCARs/Relaxation/* .'.format(path))
        if '2d' in method:
            modify_job('vasp_relax_ab')
        elif 'gam' in method:
            modify_job('vasp_gam')
        else:
            modify_job('vasp_std')
    '''
    # add vdW method into INCARs
    if 'optB88' in method:
        system('cp {0}/INCARs/Relaxation/* .'.format(path))'''

def get_band_files(method):
    '''create electronic structure files.
    pbe : calculate band use PBE method
    hse : calculate band use HSE06 method
    '''
    path = gp.get_path()
    if 'pbe' in method:
        system('cp {0}/INCARs/PBE/* .'.format(path))
    elif 'hse' in method:
        system('cp {0}/INCARs/HSE06/* .'.format(path))
    else:
        src.system_cmd.systemError(' Please Enter Right Method [pbe/hse] for band calculation.')
    modify_job('vasp_std')

def get_diele_files():
    path = gp.get_path()
    system('cp {0}/INCARs/Diele/* .'.format(path))
    modify_job('vasp_std')

def get_absorp_files():
    path = gp.get_path()
    system('cp {0}/INCARs/Absorption/* .'.format(path))
    modify_job('vasp_std')

def get_elastic_files():
    path = gp.get_path()
    system('cp {0}/INCARs/Elastic/* .'.format(path))
    modify_job('vasp_std')

def get_ELF_files():
    path = gp.get_path()
    system('cp {0}/INCARs/ELF/* .'.format(path))
    modify_job('vasp_std')

def get_PCD_files():
    path = gp.get_path()
    system('cp {0}/INCARs/PCD/* .'.format(path))
    modify_job('vasp_std')

def get_force_files():
    path = gp.get_path()
    system('cp {0}/INCARs/Force_Constants/* .'.format(path))
    modify_job('vasp_gam')

def modify_job(vasp_type):
    '''replace the path in job files. the path of mpirun is default
    '''
    vasp_path = gp.get_path(vasp_type)
    mpi_path = gp.get_path('mpi')
    system("sed -i 's/MPI_PATH/{0}/g' job-*".format(mpi_path))
    system("sed -i 's/VASP_PATH/{0}/g' job-*".format(vasp_path))

def get_POTCAR_files():
    '''read POSCAR and get POTCAR
    '''
    potcar_choose = {'H':'H', 
            'He':'He', 
            'Li':'Li_sv', 
            'B':'B', 
            'Be':'Be', 
            'C':'C', 
            'N':'N', 
            'O':'O', 
            'F':'F', 
            'Ne':'Ne', 
            'Na':'Na_pv', 
            'Mg':'Mg', 
            'Al':'Al', 
            'Si':'Si', 
            'P':'P', 
            'S':'S', 
            'Cl':'Cl', 
            'Ar':'Ar', 
            'K':'K_sv', 
            'Ca':'Ca_sv', 
            'Sc':'Sc_sv', 
            'Ti':'Ti_sv', 
            'V':'V_sv', 
            'Cr':'Cr_sv', 
            'Mn':'Mn_pv', 
            'Fe':'Fe', 
            'Co':'Co', 
            'Ni':'Ni', 
            'Cu':'Cu', 
            'Zn':'Zn', 
            'Ga':'Ga_d', 
            'Ge':'Ge_d', 
            'As':'As', 
            'Se':'Se', 
            'Br':'Br', 
            'Kr':'Kr', 
            'Rb':'Rb_sv', 
            'Sr':'Sr_sv', 
            'Y':'Y_sv', 
            'Zr':'Zr_sv', 
            'Nb':'Nb_sv', 
            'Mo':'Mo_sv', 
            'Tc':'Tc_pv', 
            'Ru':'Ru_pv', 
            'Rh':'Rh_pv', 
            'Pd':'Pd', 
            'Ag':'Ag', 
            'Cd':'Cd', 
            'In':'In_d', 
            'Sn':'Sn_d', 
            'Sb':'Sb', 
            'Te':'Te', 
            'I':'I', 
            'Xe':'Xe', 
            'Cs':'Cs_sv', 
            'Ba':'Ba_sv', 
            'La':'La', 
            'Ce':'Ce', 
            'Pr':'Pr_3', 
            'Nd':'Nd_3', 
            'Pm':'Pm_3', 
            'Sm':'Sm_3', 
            'Eu':'Eu_2', 
            'Gd':'Gd_3', 
            'Tb':'Tb_3', 
            'Dy':'Dy_3', 
            'Ho':'Ho_3', 
            'Er':'Er_3', 
            'Tm':'Tm_3', 
            'Yb':'Yb', 
            'Lu':'Lu', 
            'Hf':'Hf_pv', 
            'Ta':'Ta_pv', 
            'W':'W_sv', 
            'Re':'Re', 
            'Os':'Os', 
            'Ir':'Ir', 
            'Pt':'Pt', 
            'Au':'Au', 
            'Hg':'Hg', 
            'Tl':'Tl_d', 
            'Pb':'Pb_d', 
            'Bi':'Bi_d', 
            'Po':'Po_d', 
            'At':'At_d', 
            'Rn':'Rn', 
            'Fr':'Fr_sv', 
            'Ra':'Ra_sv', 
            'Ac':'Ac', 
            'Th':'Th', 
            'Pa':'Pa', 
            'U':'U', 
            'Np':'Np', 
            'Pu':'Pu', 
            'Am':'Am', 
            'Cm':'Cm', 
            'Bk':'Bk', 
            'Cf':'Cf', 
            'Es':'Es', 
            'Fm':'Fm', 
            'Md':'Md', 
            'No':'No', 
            'Lr':'Lr', 
            'Rf':'Rf', 
            'Db':'Db', 
            'Sg':'Sg', 
            'Bh':'Bh', 
            'Hs':'Hs', 
            'Mt':'Mt', 
            'Ds':'Ds', 
            'Rg':'Rg', 
            'Cn':'Cn'}
    # read POSCAR
    if not path.exists('POSCAR'):
        src.system_cmd.systemError(' POSCAR Not Found!')
    src.system_cmd.systemEcho(' [DPT] - Reading POSCAR...')
    with open('POSCAR', 'r') as obj:
        poscar = obj.readlines()
    atoms = poscar[5].split()
    src.system_cmd.systemEcho(' [DPT] - Finding File {0}'.format(' '.join(['POTCAR_{0}'.format(potcar_choose[atom]) for atom in atoms])))
    potcar_path = gp.get_path('POTCAR')
    poscar_files = ' '.join(['{0}/{1}/POTCAR'.format(potcar_path, potcar_choose[atom]) for atom in atoms])
    system('cat {0} > POTCAR'.format(poscar_files))
    src.system_cmd.systemEcho(' [DPT] - Combine POTCAR Successfully!')
