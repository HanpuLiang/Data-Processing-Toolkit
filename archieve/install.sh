#!/bin/bash

echo "
  *--------------*---*
  | Data         | D | 
  |   Processing | P |
  |     Toolkit  | T |
  *--------------*---*
  Version: 0.4
"

#==============#
echo "===================="
echo " Installing DPT ..."
echo "===================="

#==============#
whichPython=`which python | grep -v "no python" | grep python | wc -l`
if [ $whichPython -eq 1 ]; then
    echo "Python found at :" `which python`
fi

#==============#
usr=`whoami`
path=/home/$usr/software/DPT-0.4
echo "Install DPT at $path"
mkdir -p $path

#==============#
echo "================================"
echo " Copying files, please wait ..."
echo "================================"

cp * $path/. -rf
chmod +x $path/DPT
echo "
#=== ---- DPT-0.4 ---- ===
export PATH=$path/:\$PATH
#=== ----------------- ===" >> ~/.bashrc

#=============#
echo "
DPT is installed successfully!

You can check DPT by \"DPT -h\"

Enjoy DPT!
"
