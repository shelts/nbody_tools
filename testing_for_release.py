#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *

lmc_dir = '/home/shelts/research/'
sid_dir = '/home/sidd/Desktop/research/'
sgr_dir = '/Users/master/sidd_research/'
path = lmc_dir

linux   = True
windows = False
multi   = True

args_run = [4.0, 0.2, 0.2, 12., 0.2]

args_comp1 = [4.0, 0.2, 0.2, 12., 0.2]
args_comp2 = [4.0, 0.3, 0.4, 11., 0.3]

lua = path + 'lua/' + "EMD_v170.lua"

versions = ['_1.68_x86_64-pc-linux-gnu__mt', '_1.68_x86_64-pc-linux-gnu', '_1.68_windows_x86_64__mt.exe', '_1.68_windows_x86_64.exe']

correctans_hist = 'testing'


if(linux):
    if(multi):
        version = versions[0]
    else:
        version = versions[1]
        
if(windows):
    if(multi):
        version = versions[2]
    else:
        version = versions[3]
        
nbody = nbody_running_env(lua, '', path)
simulations_hist = version + '_1'
nbody.run(args_comp1, simulations_hist, correctans_hist, 'likes.txt', '')

simulations_hist = version + '_2'
nbody.run(args_comp2, simulations_hist, correctans_hist, 'likes.txt', '')
