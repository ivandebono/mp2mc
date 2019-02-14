import glob
import re
import pandas as pd
import os
import shutil    

    
  
def mk_cosmomc_chainfilenames(folder,newname):
    if not glob.glob(folder): print('Folder not found')
    files=glob.glob(folder+'*__*.txt')
    extension='.txt'
    if not files: print('No chain files to rename')   
    else:
        for i,f in enumerate(files):           
            newfile=shutil.copy(f, folder+newname+'_'+str(i+1)+extension)
            print(f,'copied to', newfile)
        

def mk_cosmomc_ranges(folder,newname):

    paramfile=glob.glob(folder+'*.param')[0]
    print('Used',paramfile)

    cosmo=[]
    with open(folder+newname+'.ranges','w+') as newparamfile:
        with open(paramfile,'r') as f:
            for line in f:
                if not line.startswith('#'):
                    if line.startswith('data.parameters'):
                        paramname=line.split('[', 1)[1].split(']')[0]
                        paramname=paramname.strip("''")
                        moreinfo=(line.split('[', 1)[1].split(']')[1]).split(',')
                        bestfit=re.sub(r"[=[]]",r"",moreinfo[0]).strip()
                        minimum=moreinfo[1].strip()
                        if minimum == 'None': minimum='N'
                        maximum=moreinfo[2].strip()                        
                        if maximum == 'None': maximum='N'
                        typeparam=moreinfo[5].strip()
                        if typeparam == "'derived'":
                            paramname=paramname+"*"
                        if typeparam=="'nuisance'":
                            paramname=paramname+"*"
                        if typeparam=="'cosmo'":cosmo.append(typeparam)
                        newparamfile.writelines(paramname.ljust(30) + minimum.ljust(10) + maximum.ljust(10)+'\n')

    return len(cosmo)

def rd_cosmomc_rangesfile(folder,newname):
        #Read list of parameters from the ranges file we just created
    rangesfile=glob.glob(folder+newname+'.ranges')[0]
    print(rangesfile)

    with open(rangesfile,'r') as f:
        data=f.readlines()

    params=[]
    for line in data:
        #Remove asterisk from middle of parameter names
        if '*' in (line.split()[0])[:-1]:
            params.append(((line.split()[0])[:-1].replace('*',''))+(line.split()[0])[-1])
        else:
            params.append(line.split()[0])
        
    return params


def mk_cosmomc_paramnames(folder,newname):
    f=glob.glob(folder)
    if not f: print('Folder not found')
    
    filewewant=glob.glob(folder+newname+'.paramnames')
    #If the file already exists, do nothing
    if not filewewant:
        print('Creating .params file in CosmoMC format')
                
        params=rd_cosmomc_rangesfile(folder,newname)
       
        paramnamesfile=glob.glob(folder+'*_.paramnames')[0]
        if not paramnamesfile:
            print('No paramnames files to rename')
   
        else:
            paramnamesmp=shutil.copy(paramnamesfile, folder+newname+'.MONTEPYTHONparamnames')
            paramnamescosmomc=folder+newname+'.paramnames'
        
            with open(paramnamesmp,'r') as origfile:
                lines=origfile.readlines()
            with open(paramnamescosmomc,'w') as newfile:
                for line in lines:
                    for p in params:
                        if (line.split('\t')[0]).strip() == p.rstrip('*'):
                            newfile.writelines(p+'\t'+line.split('\t')[1])     



