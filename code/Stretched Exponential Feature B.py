import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate

def st_exp(x, c, tau, beta, y_offset):
        return c*(np.exp(-(x/tau)**beta))+y_offset
             
t_halves = []   # initialise array for t halves

path = 'C:/Users/44798/OneDrive - University of Southampton/Individual Project Daniel Tong/clusterdata_1000rea_20200318_reduced'

structures = ['npStruct_1p_nonint',
            'npStruct_2p_Ychain',
             'npStruct_2p_Zchain',
             'npStruct_2p_arkus',
             'npStruct_3p_Ychain',
             'npStruct_3p_Zchain',
             'npStruct_3p_arkus',
             'npStruct_3p_arkusXZ',
             'npStruct_4p_Ychain',
             'npStruct_4p_Zchain',
             'npStruct_4p_arkus',
             'npStruct_4p_ring',
             'npStruct_4p_ringXZ',
             'npStruct_4p_triangle',
             'npStruct_4p_triangleXZ',
             'npStruct_5p_Ychain',
             'npStruct_5p_Zchain',
             'npStruct_5p_arkus',
             'npStruct_5p_pyramide',
             'npStruct_5p_ring',
             'npStruct_5p_ringXZ',
             'npStruct_5p_triangle',
             'npStruct_5p_triangleXZ',
             'npStruct_6p_Ychain',
             'npStruct_6p_Zchain',
             'npStruct_6p_ring',
             'npStruct_6p_ringXZ',
             'npStruct_6p_triangle',
             'npStruct_6p_triangleXZ',
             'npStruct_6p1_arkus',
             'npStruct_6p2_arkus',
             'npStruct_7p_Ychain',
             'npStruct_7p_Zchain',
             'npStruct_7p_ring',
             'npStruct_7p_ringXZ',
             'npStruct_7p_triangle',
             'npStruct_7p_triangleXZ',
             'npStruct_7p1_arkus',
             'npStruct_7p2_arkus',
             'npStruct_7p3_arkus',
             'npStruct_7p4_arkus',
             'npStruct_7p5_arkus']

for i in structures:

    clust = i.split('_')

    fp = path + '/' + i + '/spin_mc_red.h5'
    f = h5py.File(fp, 'r')

    for j in f:
        #if j =='4':
        #if j in ('0', '1','2', '3', '5', '6', '7'):
        if any(char.isdigit() for char in j):    
            dset = f[j]
            
            a = np.array(dset['mt'])    # convert to np array
            x = -np.log(a[:,0])          # column 1, log time
            y = a[:,1]                  # column 2, magnetism
            
            m1 = y[0]*0.5       # calculate midpoint of y using first and last
            y_values = [m1]     # list of y values to find x
               
            interp_fn = interpolate.interp1d(x, y, 'quadratic')     # create the interpolated function
            f2 = interpolate.interp1d(y, x, bounds_error=False)     # inverse interpolate function
            x_values = f2(y_values)
            
            try:
                best_vals = curve_fit(st_exp, x, y, maxfev=3000)
            except:
                pass
          
            t_half = [i]
            t_half.extend(x_values)
            
            try:
                t_half.extend(best_vals)
            except:
                pass
            t_halves.append(t_half)
            
            t_half = [i]
            t_half.extend(best_vals)
            t_halves.append(t_half)

t_halves_np = np.array(t_halves)
print(len(t_halves_np))
np.savetxt('stretchedexp.csv', t_halves_np, fmt= '%s', delimiter= ',')

print(t_half)

fig, ax = plt.subplots(1, 1)
ax.plot(x, y, label="data")
ax.plot(x, st_exp(x,*best_vals), label="fit")
ax.legend(loc="best")