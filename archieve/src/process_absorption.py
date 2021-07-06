# -*- coding: utf-8 -*-
'''
@author: Liang Hanpu
@create date: 2020/10/26
@description: This parameter are ready to prepartion the VASP inputs files for different calculational situation.
'''

import os
import src.system_cmd
import src.get_path as gp
import numpy as np

def save_diele(imag, real):
    imag_out = '\n'.join([''.join(['{0:10.5f}'.format(item) for item in line]) for line in imag])
    real_out = '\n'.join([''.join(['{0:10.5f}'.format(item) for item in line]) for line in real])
    with open('DPT.IMAG.dat', 'w') as obj:
        obj.write(imag_out)
    with open('DPT.REAL.dat', 'w') as obj:
        obj.write(real_out)
    src.system_cmd.systemEcho(' [DPT] - Files DPT.IMAG.dat (image part of dielectric function) and DPT.REAL.dat (image part of dielectric function) Be Saved!')
def get_absorption_coefficient(E, imag, real):
    h = 4.1356676969e-15
    omega = 2*np.pi*E/h
    alpha = np.sqrt(2.0)*omega*np.sqrt(np.sqrt(imag**2+real**2)-real)

def process_absorption():
    # find the file vasprun.xml
    if not os.path.exists('vasprun.xml'):
        src.system_cmd.systemError(' File vasprun.xml Not Found!')
    # read the vasprun.xml
    with open('vasprun.xml', 'r') as obj:
        ct = obj.readlines()
    imag = os.popen('''awk 'BEGIN{i=1} /imag/,\
                /\/imag/ \
                 {a[i]=$2 ; b[i]=$3 ; c[i]=$4; d[i]=$5 ; e[i]=$6 ; f[i]=$7; g[i]=$8; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j],c[j],d[j],e[j],f[j],g[j]}' vasprun.xml''').readlines()
    real = os.popen('''awk 'BEGIN{i=1} /real/,\
                /\/real/ \
                 {a[i]=$2 ; b[i]=$3 ; c[i]=$4; d[i]=$5 ; e[i]=$6 ; f[i]=$7; g[i]=$8; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j],c[j],d[j],e[j],f[j],g[j]}' vasprun.xml''').readlines()
    imag = np.array([[float(item) for item in line.split()] for line in imag])
    real = np.array([[float(item) for item in line.split()] for line in real])
    # save imag and real part of dielectric function
    save_diele(imag, real)
    # calculate the absorption coefficient
    absorp = get_absorption_coefficient(imag, real)
