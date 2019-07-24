#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: Liang Hanpu
@create date: 2019/07/22
@description: 
'''
import load_files as lf
import calculate_DOS as cd


def basic_data():
     # read EIGENVAL and get N_KPOINTS, N_BAND
    lf.load_EIGENVAL()
    # read OUTCAR and get all k-points and get KPOINTS
    lf.get_k_points()
    # get k path and delete extra line in KPOINTS and K
    lf.get_k_path()
    # read OUTCAR and get the fermi energy level
    lf.get_E_fermi()
    # get the energy
    lf.get_energy()
    
def electronic_structure(run_code, savetype=None):

    if run_code == 'dos':
        cd.calculate_all_DOS()
    if run_code == 'band':
        basic_data()
        lf.save_band(savetype)
        lf.calculate_band_gap()
    if run_code == 'fat':
        basic_data()
        lf.load_PROCAR()
        lf.save_atom_orbits(savetype)
