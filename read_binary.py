import ctypes

import numpy as np
import pandas as pd
import os

folder_in = "data/"
ext_macro = ".macro.dat"
ext_micro = ".micro.dat"

def get_file_list(folder,ext):
    list_files = os.listdir(folder)
    return [os.path.join(folder, f) for f in list_files if (ext in f)]

def bin_to_df(dat,dtypes):
    col_names = list(zip(*dtypes))[0]
    df = pd.DataFrame(columns=col_names)
    for i in range(len(col_names)):
        if (len(dtypes[i])) == 2:
            df[col_names[i]] = dat[col_names[i]]
        else:
            df[col_names[i]] = pd.Series(dat[col_names[i]].tolist())
    return df
def read_binary_macro(file_macro):
    ntypes = np.fromfile(file_macro, dtype=ctypes.c_int32, count=1)[0]
    dtypes = [('time', ctypes.c_double), ('Ntot', ctypes.c_int32), ('N_c', ctypes.c_int32),
              ('N', ctypes.c_int32, (ntypes,)), ('Nm', ctypes.c_int32, (ntypes,))]
    dat = np.fromfile(file_macro,dtype=dtypes,offset=ctypes.sizeof(ctypes.c_int32))
    col_names = list(zip(*dtypes))[0]
    df = bin_to_df(dat,dtypes)
    return df
def read_binary_micro(file_micro):
    ntypes = np.fromfile(file_micro, dtype=ctypes.c_int32,count=1)[0]
    dtypes = [('time', ctypes.c_double), ('C', ctypes.c_int32,(ntypes,))]
    dat = np.fromfile(file_micro,dtype=dtypes,offset=ctypes.sizeof(ctypes.c_int32))
    df = bin_to_df(dat,dtypes)
    return df

def tostr(X):
    str = ""
    if X < 0:
        X= -1*X
        str = str+"n"
    str = str+ ('%f' % X).rstrip('0').rstrip('.')
    return str

def get_folder_name(Ni, q, F):
    strN = "Ni_"+tostr(Ni[0])
    strQ = "_q_"+tostr(q[0])
    strF = "_F_"+tostr(F[0][0])
    for i in range(0,len(Ni)):
        if not i==0:
            strN = strN+ "-"+tostr(Ni[i])
            strQ = strQ+ "-"+tostr(q[i])
        for j in range(0,len(Ni)):
            if not (i==0 and j==0):
                strF = strF + "-"+tostr(F[i][j])
    strOut = strN+strQ+strF
    return strOut


class dataMacroMC:
        def __init__(self,_Ntypes,_Ni,_q,_F):
            assert (_Ntypes>0) and (len(_Ni)==_Ntypes) and (len(_q)==_Ntypes) and (len(_F)==_Ntypes)
            for Fi in _F:
                assert len(Fi) == _Ntypes
            self.Ntypes= _Ntypes
            self.Ni= _Ni
            self.q = _q
            self.F = _F
            self.folder_name = get_folder_name(self.Ni,self.q,self.F)
            self.list_files = get_file_list(os.path.join(folder_in,self.folder_name),ext_macro)
            self.dfs = [read_binary_macro(f) for f in self.list_files]
            self.df = pd.concat(self.dfs).reset_index(drop=True)


class dataMicroMC:
    def __init__(self, _Ntypes, _Ni, _q, _F):
        assert (_Ntypes > 0) and (len(_Ni) == _Ntypes) and (len(_q) == _Ntypes) and (len(_F) == _Ntypes)
        for Fi in _F:
            assert len(Fi) == _Ntypes
        self.Ntypes = _Ntypes
        self.Ni = _Ni
        self.q = _q
        self.F = _F
        self.folder_name = get_folder_name(self.Ni, self.q, self.F)
        self.list_files = get_file_list(os.path.join(folder_in, self.folder_name), ext_micro)
        self.dfs = [read_binary_micro(f) for f in self.list_files]
        self.df = pd.concat(self.dfs).reset_index(drop=True)









