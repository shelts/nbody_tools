#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */

import os
import subprocess
from subprocess import call
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches



def orbital_speeds():
    
    speeds = [47.4, 35.0, 29.8, 24.1,13.1, 9.7, 6.8,5.4, 4.7]
    radii  = [0.39, 0.723, 1, 1.524, 5.203, 9.539, 19.18, 30.06, 39.53]
    plt.figure(figsize=(20, 10))
    plt.tick_params(axis='y', which='major', labelsize=24)
    plt.tick_params(axis='x', which='major', labelsize=24)
    plt.ylabel('Orbital Velocity (km/s)', fontsize=26)
    plt.xlabel('Distance From Sun (AU)', fontsize=26)
    plt.plot(radii, speeds, linestyle = '-', linewidth = 3, color ='k', alpha = 1)
    plt.scatter(radii, speeds, marker = 'o', s = 100, color ='r')
    plt.savefig('orbital_vels.png', format='png')
    
    
    

def bulge(r):
    d = 0.7 #kpc
    M = 1.52954402e5# kpc^3/gy^2  
    a = r * M / (r * (r + d)**2.0)
    return a


def disk(r):
    M = 4.45865888e5  # kpc^3/gy^2  
    b = 6.5 #kpc
    c = 0.26 #kpc
    a = r * M / (r * r + (b + c)**2.)**(3./2.)
    return a

def halo(r):
    v0 = 73.0 #km/s
    d = 12.0 #kpc
    a = 2. * v0 * v0 * r / (r * r + d * d)
    a *= 1.0 / (0.977813107)**2.0 # factor for converting the v0's km/s to kpc/gy
    return a
    
def mw_galaxy_orbital_speeds():
    w_halo = []
    no_halo = []
    rs = [] 
    r = 0.01
    for i in range(1000):
        bulge_a = bulge(r)
        disk_a  = disk(r)
        halo_a  = halo(r)
        
        nh = 0.977813107 * mt.sqrt(r * (bulge_a + disk_a)) #km/s
        h  = 0.977813107 * mt.sqrt(r * (bulge_a + disk_a + halo_a))#km/s
    
        w_halo.append(h)
        no_halo.append(nh)
        rs.append(r )
        
        r += 0.1
    params = {'legend.fontsize': 22,
            'legend.handlelength': 1}
    plt.rcParams.update(params)    
    plt.figure(figsize=(20, 10))
    plt.tick_params(axis='y', which='major', labelsize=24)
    plt.tick_params(axis='x', which='major', labelsize=24)
    plt.ylabel('Orbital Velocity (km/s)', fontsize=26)
    plt.xlabel('Distance From GC (kpc)', fontsize=26)
    plt.xlim(0, 50)
    plt.plot(rs, w_halo, linestyle = '-', linewidth = 3, color ='k', alpha = 1, label = 'with halo')
    
    plt.plot(rs, no_halo, linestyle = '-', linewidth = 3, color ='b', alpha = 1, label = 'without halo')
    plt.legend()
    plt.savefig('mw_orbital_vels.png', format='png')
        

def main():
    #orbital_speeds()
    mw_galaxy_orbital_speeds()
    
main()