'''
@author: Liang Hanpu
@create date: 2019/08/25
@description: This parameter is the interface between VASP and bader chager analysis scripts.
'''
from os import system, path
import src.system_cmd
import src.get_path as gp

def bader_charge_analysis():
    software_path = gp.get_path()
    if (path.exists('ARCCAR0') or path.exists('AECCAR2')) == False:
        src.system_cmd.systemError('File ARCCAR0 or ARCCAR2 not found!')
    system('sh '+software_path+'/lib/run_chgsum.sh '+software_path)
    if (path.exists('CHGCAR') or path.exists('CHGCAR_sum')) == False:
        src.system_cmd.systemError('File CHGCAR or CHGCAR_sum not found!')
    system(software_path+'/lib/bader CHGCAR -ref CHGCAR_sum')


