# -*- coding: utf-8 -*-
'''
@author: Hanpu Liang
@date: 2019/07/22
@description: Combining E.dat, Energy.dat, and each atomic orbit files into one file origin_plot.dat.
            k   E   s   py  pz  px  dxy dyz dz2 dxz dx2 total
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

import sys, system_cmd
from os import system, path
from numpy import array, shape, tile, ravel, zeros, c_

def data2line(content):
    content = [line.split() for line in content]
    return array(content)

def transport(matrix):
    l = len(matrix)
    c = len(matrix[0])
    new_m = []
    for j in range(c):
        temp = []
        for i in range(l):
            temp.append(matrix[i][j])
        new_m.append(temp)
    return new_m

def one_column_type(k, E, atom=None, orbit=None):
    # get all data to one list
    all_list = []
    # k points
    k = array(k)
    # energy
    E = array(E)
    # the size of Energy
    l, c = shape(E)
    k = tile(k, c)
    E = ravel(E, order='F')
    out_1 = c_[k,E]
    # orbits
    if orbit:
        all_orbits = zeros((l*c, 10))
        orbits = ['s', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2', 'tot']
        for i, item in enumerate(orbits):
            with open('./all_orbits/'+atom+'_'+item+'.dat', 'r') as obj:
                content_all = obj.readlines()
                content_line = data2line(content_all)
                content_line = ravel(content_line, order='F')
                all_orbits[:,i] = content_line.T
        out_1 = c_[out_1,all_orbits]
    out_list = out_1.tolist()
    out_2 = [[float(item) for item in line] for line in out_list]
    if orbit:
        out_str = ['%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f%14.8f'%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11]) for line in out_2]
        out_str.insert(0, '%14s%14s%14s%14s%14s%14s%14s%14s%14s%14s%14s%14s'%('k', 'E', 's', 'py', 'pz', 'px', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2', 'tot'))
    else:
        out_str = ['%14.8f%14.8f'%(line[0],line[1]) for line in out_2]
        out_str.insert(0, '%14s%14s'%('k', 'E'))
    for i in range(c):
        out_str.insert(l*(c-i)+1, ' ')
    if atom == None:
        out_name = './band_data.dat'
        system_cmd.systemEcho('band_data.dat saved!')
    else:
        out_name = './fat_band_'+atom+'.dat'
        system_cmd.systemEcho('fat_band_'+atom+'.dat saved!')
    with open(out_name, 'w') as obj:
        obj.write(' \n'.join(out_str))


