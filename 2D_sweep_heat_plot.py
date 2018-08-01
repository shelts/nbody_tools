#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.interpolate import griddata

path = '/home/sidd/Desktop/research/'
folder = path + "like_surface/"
#name_of_sweeps = '2D_hists'
name_of_sweeps = 'parameter_sweep_2d'
twoD_names   = ['rr_mr']
titles  = ['Backward Evolve Time (Gyr)',  'Baryon Scale Radius (kpc)', r'Scale Radius Ratio ($R_{B}/(R_{B}+R_{D})$)', 'Baryonic Mass (SMU)',  'Mass Ratio (Baryonic/Total)']
coori = 2
coorj = 4

def contour(sweep):
    #print sweep.vals
    #print sweep.vals2
    #print sweep.liks
    X, Y, Z, = np.array([]), np.array([]), np.array([])
    for i in range(len(sweep.vals)):
            X = np.append(X,sweep.vals[i])
            Y = np.append(Y,sweep.vals2[i])
            Z = np.append(Z,sweep.liks[i])

    # create x-y points to be used in heatmap
    xi = np.linspace(X.min(),X.max(),1000)
    yi = np.linspace(Y.min(),Y.max(),1000)

    # Z is a matrix of x-y values
    zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='nearest')

    # colorbar range
    zmin = -50
    zmax = 0
    zi[(zi<zmin) | (zi>zmax)] = None

    # Create the contour plot
    plt.contourf(xi, yi, zi, 100, cmap=plt.cm.rainbow, vmax=zmax, vmin=zmin)
    plt.colorbar()  
    plt.savefig(folder + name_of_sweeps + '/heat_map.png', format='png', dpi = 300)   
    




def imshow(sweep):
    out1 = [[0.2, 0.25], [0.23, 0.185], [.243,.234]]#test values
    x = np.asarray(sweep.vals)
    y = np.asarray(sweep.vals2)
    z = np.asarray(sweep.liks) 
    
    nInterp = 50
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    
    plt.xlabel(titles[coori])
    plt.ylabel(titles[coorj])        
    
    for i in range(len(out1)):
        plt.scatter(out1[i][0], out1[i][1], s=20, marker= 'o',  color='k', alpha=1, edgecolors='none')
    
    plt.imshow(zi, vmin=-50, vmax=0, origin='lower', cmap ='GnBu'  , extent=[x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()
    #plt.show()
    plt.savefig(folder + name_of_sweeps + '/heat_map.png', format='png', dpi = 300)
    
    
def main():
    correct = [3.95, 0.2, 0.2, 12, 0.2]
    sweep = sweep_data(folder, name_of_sweeps, twoD_names[0], 2)
    sweep.plottable_list()
    
    #contour(sweep)
    imshow(sweep)
main()