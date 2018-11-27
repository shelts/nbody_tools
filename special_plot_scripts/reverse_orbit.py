#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
import os
import subprocess
from subprocess import call
import math as mt
import matplotlib.pyplot as plt
os.system('cp ../nbody_functional.py ./')
from nbody_functional import *




def get_orbit_data(file1):
    f = open(file1, 'r')
    ls = []
    bs = []
    xs = []
    ys = []
    zs = []
    for line in f:
        ss = line.split('\t')
        x = float(ss[0])
        y = float(ss[1])
        z = float(ss[2])
        l = float(ss[3])
        b = float(ss[4])

        xs.append(x)
        ys.append(y)
        zs.append(z)
        ls.append(l)
        bs.append(b)
        
    return xs, ys, zs, ls, bs




def plot(out_file, orbit_ls, orbit_bs):
    out = nbody_outputs(out_file)
    #out.rescale_l()
    out.dark_light_split()

    #plt.figure(figsize=(10, 10))
    xlower = -180.0
    xupper = 180.0
    ylower = -80
    yupper = 80
    
    #plt.xlim((xlower, xupper))
    #plt.ylim((ylower, yupper))
    plt.xlabel('l')
    plt.ylabel('b')
    plt.scatter(218, 53.5, s = 10.)
    plt.scatter(out.dark_l, out.dark_b,  s = 1, color = 'k', alpha=1, marker = '.', label = 'dark matter')
    plt.scatter(out.light_l, out.light_b,  s = 1., color = 'b', marker = '.', label = 'baryons')
    #print orbit_bs
    plt.plot(orbit_ls, orbit_bs, color = 'r')
    #plt.legend()
    plt.savefig('lb_orbit', format='png', bbox_inches='tight')
    #print "plotting:", len(out.light_l) + len(out.dark_l), " points"

def plot2(out_file, orbit_x, orbit_y, orbit_z):
    out = nbody_outputs(out_file)
    ##out.rescale_l()
    out.dark_light_split()
    plt.figure(figsize=(10, 20))
    xlower = .5
    xupper = -.5
    ylower = -.5
    yupper = .5
    
    xlower = -50
    xupper = 50
    ylower = -60
    yupper = 60
    ms = 0.5
    #{ -21.4056, -10.4736, 22.9903 }

    #fig.tight_layout()
    plt.axes().set_aspect('equal')
    plt.subplot(311, aspect='equal')
    plt.tick_params(axis='y', which='major', labelsize=22)
    plt.tick_params(axis='x', which='major', labelsize=22)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('x', fontsize=24)
    plt.ylabel('y', fontsize=24)
    plt.plot(out.dark_x, out.dark_y, '.', markersize = ms, color = 'k', marker = '.')
    plt.plot(out.light_x, out.light_y, '.', markersize = ms, color = 'b', marker = '.')
    plt.plot(orbit_x, orbit_y,'.', markersize = ms, color = 'r', marker = '.')
    plt.plot(-21.4056, -10.4736, '.', markersize = 20, color = 'g', marker = '.')
    
    plt.subplot(312,aspect='equal')
    plt.tick_params(axis='y', which='major', labelsize=22)
    plt.tick_params(axis='x', which='major', labelsize=22)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('x', fontsize=24)
    plt.ylabel('z', fontsize=24)
    plt.plot(out.dark_x, out.dark_z, '.', markersize = ms, color = 'k', marker = '.')
    plt.plot(out.light_x, out.light_z, '.', markersize = ms, color = 'b', marker = '.')
    plt.plot(orbit_x, orbit_z,'.', markersize = ms, color = 'r', marker = '.')
    plt.plot(-21.4056, 22.9903, '.', markersize = 20, color = 'g', marker = '.')
    
    plt.subplot(313, aspect='equal')
    plt.tick_params(axis='y', which='major', labelsize=22)
    plt.tick_params(axis='x', which='major', labelsize=22)
    plt.xlim((xlower, xupper))
    plt.ylim((ylower, yupper))
    plt.xlabel('z', fontsize=24)
    plt.ylabel('y', fontsize=24)
    plt.plot(out.dark_z, out.dark_y, '.', markersize = ms, color = 'k', marker = '.')
    plt.plot(out.light_z, out.light_y, '.', markersize = ms, color = 'b', marker = '.')
    plt.plot(orbit_z, orbit_y,'.', markersize = ms, color = 'r', marker = '.')
    plt.plot(22.9903, -10.4736, '.', markersize = 20, color = 'g', marker = '.')
    plt.savefig('xyz_orbit_evolved.png', format='png', bbox_inches='tight')

def main():
    path = '/home/sidd/Desktop/research/'
    folder = path + 'quick_plots/hists_outs/'
    
    file1 = 'reverse_orbit.out'
    out1 = folder + 'reverse_orbit_evolved.out'
    
    orbit_x, orbit_y, orbit_z, orbit_ls, orbit_bs = get_orbit_data(file1)
    #plot(out1, orbit_ls, orbit_bs)
    plot2(out1, orbit_x, orbit_y, orbit_z)
    
main()