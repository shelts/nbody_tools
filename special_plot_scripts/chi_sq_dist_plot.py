#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */

import os
import subprocess
from subprocess import call
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
import matplotlib.patches as mpatches



def chi_sq_dist_plot_nsigmasq():
    k = 50.0
    cf = (k / 2.0) - 1.0
    x = 0.1
    xs = []
    func1s = []
    func2s = []
    func3s = []
    while(1):
        func1 = cf * mt.log(x) - x / 2.0
        func2 = func1 - cf * (mt.log(2.0 * cf) - 1.0) 
        if(x < 2.0 * cf):
            func3 = 0.0
        else:
            func3 = func2
            
        xs.append(x)
        func1s.append(func1)
        func2s.append(func2)
        func3s.append(func3)
        if(x > 1000):
            break
        else:
            x += 0.1
            
    #plt.figure(figsize=(15, 15))
    plt.ylim((-200, 100))
    plt.xlim((0, 400))
    plt.tick_params(axis='y', which='major', labelsize=10)
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.xlabel(r'N$_{\sigma}$$^2$', fontsize=16)
    plt.ylabel('Probability', fontsize=16)
    plt.plot(xs, func1s, color='k', linestyle = 'solid', alpha = 1, linewidth = 2)
    plt.plot(xs, func2s, color='b', linestyle = 'dashed', alpha = .5, linewidth = 2)
    plt.plot(xs, func3s, color='r', linestyle = 'dotted', alpha = 1, linewidth = 4)
    
    plt.savefig('/home/sidd/Desktop/research/quick_plots/publish_plots/chi_sq_func3.png', format='png', bbox_inches='tight')
    plt.savefig('chi_sq_func_nsigmasq.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('chi_sq_func_nsigmasq.png', format='png', bbox_inches='tight')
    plt.close()
    #plt.show()
# #


def chi_sq_dist_plot_nsigma():
    k = 50.0
    cf = (k / 2.0) - 1.0
    x = 0.1
    xs = []
    func1s = []
    func2s = []
    func3s = []
    while(1):
        func1 = cf * mt.log(x * x) - x * x / 2.0
        func2 = func1 - cf * (mt.log(2.0 * cf) - 1.0) 
        if(x * x < 2.0 * cf):
            func3 = 0.0
        else:
            func3 = func2
            
        xs.append(x)
        func1s.append(func1)
        func2s.append(func2)
        func3s.append(func3)
        if(x > 1000):
            break
        else:
            x += 0.1
            
    #plt.figure(figsize=(15, 15))
    plt.ylim((-200, 100))
    plt.xlim((0, 50))
    plt.tick_params(axis='y', which='major', labelsize=10)
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.xlabel(r'N$_{\sigma}$', fontsize=16)
    plt.ylabel('Probability', fontsize=16)
    plt.plot(xs, func1s, color='k', linestyle = 'solid', alpha = 1, linewidth = 2)
    plt.plot(xs, func2s, color='b', linestyle = 'dashed', alpha = .5, linewidth = 2)
    plt.plot(xs, func3s, color='r', linestyle = 'dotted', alpha = 1, linewidth = 4)
    
    plt.savefig('/home/sidd/Desktop/research/quick_plots/publish_plots/chi_sq_func3.png', format='png', bbox_inches='tight')
    plt.savefig('chi_sq_func_nsigma.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('chi_sq_func_nsigma.png', format='png', bbox_inches='tight')
    plt.close()
    #plt.show()
# #


def disp_func():
    k = 50.0
    cf = (k / 2.0) - 1.0
    x = 0.1
    xs = []
    func1s = []
    while(1):
        func1 = - x * x / 2.0
            
        xs.append(x)
        func1s.append(func1)
        if(x > 1000):
            break
        else:
            x += 0.1
            
    #plt.figure(figsize=(15, 15))
    plt.ylim((-200, 10))
    plt.xlim((0, 50))
    plt.tick_params(axis='y', which='major', labelsize=10)
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.xlabel(r'N$_{\sigma}$', fontsize=16)
    plt.ylabel('Probability', fontsize=16)
    plt.plot(xs, func1s, color='k', linestyle = 'solid', alpha = 1, linewidth = 2)
    
    #plt.savefig('/home/sidd/Desktop/research/quick_plots/publish_plots/chi_sq_func3.png', format='png', bbox_inches='tight')
    plt.savefig('disp_func_updated.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('disp_func_updated.png', format='png', bbox_inches='tight')
    #plt.show()
    plt.close()

chi_sq_dist_plot_nsigmasq()
chi_sq_dist_plot_nsigma()
disp_func()