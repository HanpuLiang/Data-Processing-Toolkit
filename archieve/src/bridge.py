#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: Hanpu Liang
@create date: 2019/07/22
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

import src.electronic_structure as es
import src.calculate_DOS as cd
import src.bader_charge as bc
import src.born_dielectric as diele
import src.elastic_moduli as em
import src.stress_strain as ss
import src.thermal_electric as te
import src.VASP_inputs as vi
import src.vdW_correction as vc
import src.process_absorption as pa
import src.system_cmd

def basic_data():
     # read EIGENVAL and get N_KPOINTS, N_BAND
    es.load_EIGENVAL()
    # read OUTCAR and get all k-points and get KPOINTS
    es.get_k_points()
    # get k path and delete extra line in KPOINTS and K
    es.get_k_path()
    # read OUTCAR and get the fermi energy level
    es.get_E_fermi()
    # get the energy
    es.get_energy()
    
def bridge(run_code, strain_direction='xy', strain_begin=0, strain_end=0.1, \
    strain_step=0.01, strain_process='cal', savetype=None, dimension=3, \
        te_action='none', te_dimension=2, strain_type='pos', file_type='rel', \
            method='no', vdW_method='optB88', E_0='fermi'):
    src.system_cmd.Open_screen()

    if run_code == 'dos':
        cd.calculate_all_DOS()
    if run_code == 'band':
        basic_data()
        es.save_band(savetype, E_0)
        # es.calculate_band_gap()
    if run_code == 'fat':
        basic_data()
        es.load_PROCAR()
        es.save_atom_orbits(savetype)
    if run_code == 'bader':
        bc.bader_charge_analysis()
    if run_code == 'diele':
        diele.born_dielectric()
    if run_code == 'absorp':
        pa.process_absorption()
    if run_code == 'hard':
        em.elastic_moduli(dimension=dimension)
    if run_code == 'strain':
        ss.stress_strain(strain_direction, strain_begin, strain_end, strain_step, strain_process, strain_type)
    if run_code == 'te':
        te.thermal_electric(te_action, te_dimension)
    if run_code =='vasp':
        vi.VASP_inputs(file_type.lower(), method.lower())
    if run_code == 'vdw':
        vc.add_vdW_correction(vdW_method)


