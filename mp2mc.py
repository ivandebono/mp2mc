#Script to turn MontePython output into CosmoMC-compatible output
#To run:
# $ run mp2mc.py 'folder/' 'newname'

import os
currentdir=os.getcwd()

import sys


folder=sys.argv[1] 

newname=sys.argv[2]


path=folder+newname


from montepython2cosmomc import *

#First, make new chain files with the proper names
mk_cosmomc_chainfilenames(folder,newname)

#Make the ranges files
ndim=mk_cosmomc_ranges(folder,newname)


#Then copy and modify the paramnames file
mk_cosmomc_paramnames(folder,newname)

#Run GetDist to check
from subprocess import call
os.chdir(folder)
call(["python","/PATH/TO/GETDIST/GetDist.py",path]) 


os.chdir(currentdir)