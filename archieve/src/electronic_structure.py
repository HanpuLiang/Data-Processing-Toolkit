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
