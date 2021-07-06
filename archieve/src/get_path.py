import src.system_cmd

def get_path(path_type='software'):
    if path_type == 'software':
        path = 'software_path'
    elif path_type == 'mpi':
        path = 'MPI_PATH'
    elif path_type == 'vasp_std':
        path = 'VASP_STD_PATH'
    elif path_type == 'vasp_relax_ab':
        path = 'VASP_RELAX_AB_PATH'
    elif path_type == 'vasp_gam':
        path = 'VASP_GAM_PATH'
    elif path_type == 'POTCAR':
        path = 'POTCAR_PATH'
    else:
        src.system_cmd.systemError(' No PATH for [{0}].'.format(path_type))
    return path
