#!/bin/bash

version=0.8.3

echo "
  *--------------*---*
  | Data         | D | 
  |   Processing | P |
  |     Toolkit  | T |
  *--------------*---*
  Version: $version
   Author: Liang Hanpu
"

#=====You can set this parameters by yourself===#

usr=`whoami`
BIN=/home/$usr/bin                  # the path you want install DPT
MPI_PATH=mpirun                     # the path of mpirun
VASP_STD_PATH=vasp_std              # the path of vasp_std
VASP_RELAX_AB_PATH=vasp_relax_ab    # the path of vasp_std for 2D materials
VASP_GAM_PATH=vasp_gam              # the path of vasp_gam
POTCAR_PATH=/home/$usr/POTCAR/PBE   # the path of POTCAR files

#=======End of parameters setting area==========#

echo "===================="
echo " [DPT] - Installing DPT ..."

whichPython=`which python | grep -v "no python" | grep python | wc -l`
if [ $whichPython -eq 1 ]; then
    echo " [DPT] - Python found at :" `which python`
fi

echo "===================="

path=`pwd`
chmod +x ./DPT
chmod +x ./lib/chgsum.pl
chmod +x ./lib/bader
sed -i "s|software_path|$path|g" ./src/get_path.py
sed -i "s|MPI_PATH|$MPI_PATH|g" ./src/get_path.py
sed -i "s|VASP_STD_PATH|$VASP_STD_PATH|g" ./src/get_path.py
sed -i "s|VASP_RELAX_AB_PATH|$VASP_RELAX_AB_PATH|g" ./src/get_path.py
sed -i "s|VASP_GAM_PATH|$VASP_GAM_PATH|g" ./src/get_path.py
sed -i "s|POTCAR_PATH|$POTCAR_PATH|g" ./src/get_path.py

rm $BIN/DPT -f
ln -s $path/DPT $BIN/DPT

echo "====================
 [DPT] - DPT is installed successfully!
====================
 [DPT] - You can check DPT by \"DPT -h\"
====================
 [DPT] - Enjoy DPT!
"
