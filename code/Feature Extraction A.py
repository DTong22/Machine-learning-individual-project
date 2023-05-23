import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def fprime_central(f, x0, h=1e-1):
    return (f(x0+h) - f(x0-h)) / (2*h)

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
        if any(char.isdigit() for char in j):

            dset = f[j]
            
            a = np.array(dset['mt'])    # convert to np array
            x = np.log(a[:,0])          # column 1, log time
            y = a[:,1]                  # column 2, magnetism
            
            m1 = y[0]*0.5       # midpoint of magnetisation
            m2 = y[0]*0.333       # 1/3 of magnetisation
            m3 = y[0]*0.666       # 2/3 of magnetisation
            y_values = [m1, m2, m3]     # list of y (magnetisation) values
            
            interp_fn = interpolate.interp1d(x, y, 'quadratic')     # create the interpolated function
            f2 = interpolate.interp1d(y, x, bounds_error=False)     # inverse interpolate function
            x_values = f2(y_values)
            
            grad = fprime_central(f2, m1)
            
            #assign a value to each curve to determine if it has fully relaxed
            if y[-1] == y[-2]:
                relaxed = 1
            else:
                relaxed = 0
            
            t_half = [i, relaxed, grad]
            t_half.extend(x_values)
            t_half.extend(best_vals)
            t_halves.append(t_half)

t_halves_np = np.array(t_halves)
print(len(t_halves_np))
np.savetxt('fulldata_new11.csv', t_halves_np, fmt= '%s', delimiter= ',')

plt.plot(x, y)
plt.xlabel('log time')
plt.ylabel('magnetism')
plt.grid()

plt.plot(x, y)
plt.plot(x_values[0], y_values[0], 'o', label = 't half')
plt.xlabel('log time')
plt.ylabel('magnetism')
plt.legend()