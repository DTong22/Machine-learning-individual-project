"""
Update by OH on 20210710
"""


import numpy as np
import pylab as py
import h5py

from scipy.interpolate import interp1d
from scipy.optimize import leastsq


structures = ['npStruct_2p_Ychain',
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
              'npStruct_6p1_arkus',
              'npStruct_6p2_arkus',
              'npStruct_6p_Ychain',
              'npStruct_6p_Zchain',
              'npStruct_6p_ring',
              'npStruct_6p_ringXZ',
              'npStruct_6p_triangle',
              'npStruct_6p_triangleXZ',
              'npStruct_7p1_arkus',
              'npStruct_7p2_arkus',
              'npStruct_7p3_arkus',
              'npStruct_7p4_arkus',
              'npStruct_7p5_arkus',
              'npStruct_7p_Ychain',
              'npStruct_7p_Zchain',
              'npStruct_7p_ring',
              'npStruct_7p_ringXZ',
              'npStruct_7p_triangle',
              'npStruct_7p_triangleXZ',
              'npStruct_1p_nonint']


def extract_values(t, m, N=3):
    """
    Data used for analysis include:
        - N magnetisation and time data linearly spaced along magnetisation
          axis
        - minimum and maximum M
        - if we want to do slopes we can do that during the processing
    """

    try:

        m_max = max(m)
        m_min = min(m)

        t_vs_m = interp1d(m, t)

        mi = np.linspace(m_min, m_max, N)
        ti = []
        for i in mi:
            ti.append(t_vs_m(i))

    except ValueError:

        mi = np.linspace(m_min, m_max, N)
        ti = []
        for i in mi:
            ti.append(np.nan)

    return mi, ti, m_min, m_max


def cut_data(t, m, tmin=1e-10, tmax=1e5):
    """
    Cut data for fitting in a selected time interval between tmin and tmax.
    
    We choose to cut with respect to time interval, because cutting along
    magnetisation axes can remove negative data for example.
    """
    
    return t[(t > tmin) & (t < tmax)], m[(t > tmin) & (t < tmax)]
    

def y_str(p, x):
    """
    Stretched exponential function used in the fitting.
    """
    return p[0]*np.exp(-(x/p[1])**p[2])


def y_err(p, x, y):
    """
    The error function used in the fitting.
    """
    return y - y_str(p, x)


def fit_stretched(t, m, print_info=0):

    p, p0 = np.zeros(3), np.zeros(3)  # initialise fit parameters
    
    p0[0], p0[1], p0[2] = 1.0, 2e-5, 0.5
    
    success, num_iter = 5, 0
    while success > 4 and num_iter <= 500: # scan through init parameters

        p, success = leastsq(y_err, p0, args=(t, m))
        
        p0[0] = 0.01 + 0.99*np.random.random()
        p0[1] = np.exp(-16 + 12*np.random.random()) # rv between ~ 1e-7 & 1e-2
        p0[2] = 0.01 + 0.99*np.random.random()
        
        num_iter += 1
    
    if print_info == 1:
        print(p, r2(p, t, m))
        print(success)
        
    return p, success


def r2(p, x, y):
    """
    https://en.wikipedia.org/wiki/Coefficient_of_determination
    
    In statistics, the coefficient of determination, denoted R2 or r2 and
    pronounced "R squared", is the proportion of the variance in the dependent
    variable that is predictable from the independent variable(s).

    It is a statistic used in the context of statistical models whose main
    purpose is either the prediction of future outcomes or the testing of
    hypotheses, on the basis of other related information. It provides a
    measure of how well observed outcomes are replicated by the model,
    based on the proportion of total variation of outcomes explained 
    by the model.
    
    x - independet variables
    y - dependent variables
    p - fit parameters from fitting y_str to y(x)
    """
    
    ss_tot = sum((y - np.mean(y))**2.0)
    ss_res = sum(y_err(p, x, y)**2.0)
    
    R2 = 1.0 - ss_res/ss_tot  # coeff of determination
    
    y_res_min = min(y_err(p, x, y)) / np.mean(y) # min residual
    y_res_max = max(y_err(p, x, y)) / np.mean(y) # max residual
    
    return y_res_min, y_res_max, R2


#######################################################################
#######################################################################
#######################################################################

path = "./"

# specify number of time points to extract
N = 3

filename = "csvtable.csv"
fout = open(path + "/" + filename, "w")

np.random.seed(1) # we use random parameter initialisation in least squares

#######################################################################
# write header in the csv file
s = ""
for i in range(N):
    s += "M" + str(i) + "," + "t" + str(i) + ","
s += "Mmin" + "," + \
     "Mmax" + "," + \
     "M0_fit" + "," + \
     "t_fit" + "," + \
     "beta_fit" + "," + \
     "success" + "," + \
     "fit_res_min" + "," + \
     "fit_res_max" + "," + \
     "R2" + "," + \
     "num_part" + "," + \
     "structure" + "," + \
     "realisation" + "\n"
fout.write(s)


for i in structures:

    clust = i.split('_')

    file_path = path + '/' + i + '/spin_mc_red.h5'
    hf = h5py.File(file_path, 'r')

    nrea = hf.attrs['num_realisations']

    for j in range(nrea):
        mtdata = hf[str(j) + '/mt'] # transition matrix

        t = mtdata[:, 0]
        m = mtdata[:, 1]

        mi, ti, mmin, mmax = extract_values(t, m, N)
        print(j, clust[1], clust[2])
        
        t_c, m_c = cut_data(t, m, tmin=1e-6, tmax=1e-2) # cut data for fitting
        p, success = fit_stretched(t_c, m_c)
        y_res_min, y_res_max, R2 = r2(p, t_c, m_c)
        
        # py.semilogx(t, m)
        # py.semilogx(t, y_str(p, t), "--")

        dataout = ""
        for i in range(N, 0, -1):
            dataout += str(mi[i-1]) + "," + str(ti[i-1]) + ","
        dataout += str(mmin) + "," + \
                   str(mmax) + "," + \
                   str(p[0]) + "," + \
                   str(p[1]) + "," + \
                   str(p[2]) + "," + \
                   str(success) + "," + \
                   str(y_res_min) + "," + \
                   str(y_res_max) + "," + \
                   str(R2) + "," + \
                   clust[1][0] + "," + \
                   clust[2] + "," + \
                   str(j) + "\n"
        fout.write(dataout)

    hf.close()
fout.close()
