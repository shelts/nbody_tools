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
name_of_sweeps = 'parameter_sweep_2d_v170'
twoD_names   = ['rr_mr']
titles  = ['Backward Evolve Time (Gyr)',  'Baryon Scale Radius (kpc)', r'Scale Radius Ratio ($R_{B}/(R_{B}+R_{D})$)', 'Baryonic Mass (SMU)',  'Mass Ratio (Baryonic/Total)']
coori = 2
coorj = 4



class half_light:
    def __init__(self):
        self.ml_correct = 12.0
        self.rl_correct = 0.2
        self.rr_correct = 0.2
        self.mr_correct = 0.2
        
        self.rd_correct = (self.rl_correct / self.rr_correct) * (1.0 - self.rr_correct)
        self.md_correct = (self.ml_correct / self.mr_correct) * (1.0 - self.mr_correct)
        
        self.half_mass_radius()
        self.density_half_light_rad()
        
    def half_mass_radius(self):#finding the half light radius
        print 'Calculating the half light radius: '
        r = 0.001
        baryonic_mass_enclosed = self.ml_correct * r**3.0 / (r**2. + self.rl_correct**2.)**(3.0 / 2.0)
        while(baryonic_mass_enclosed <= (0.5 * self.ml_correct)):#check if the baryonic mass enclosed is half the total.
            r += 0.01
            baryonic_mass_enclosed = self.ml_correct * r**3.0 / (r**2. + self.rl_correct**2.)**(3.0 / 2.0)
        
        print 'half_light_radius: ', r
        print 'baryonic mass enclosed: ', baryonic_mass_enclosed
        self.half_mass_radius = r
    
    def density_half_light_rad(self):
        self.rrs    = []
        self.mrs    = []
        self.mdencs = []
        
        print 'Generating constant dark matter mass region'
        r = 0.001
        threshold = 0.3# threshold for the dark matter enclosed region
        
        #dark matter mass enclosed within the half light radius
        
        dark_mass_enclosed_half_light = self.md_correct * self.half_mass_radius**3.0 / (self.half_mass_radius**2. + self.rd_correct**2.)**(3.0 / 2.0)
        
        print 'Dark matter mass enclosed within the half light radius: ', dark_mass_enclosed_half_light
        
        mr = 0.05
        while(mr < 0.95):
            rr = 0.05
            while(rr < 0.5):
                rad_dark_current = (self.rl_correct / rr) * (1.0 - rr)
                mass_dark_current = (self.ml_correct / mr) * (1.0 - mr)
                #mdenc = (3.0 / (4.0 * mt.pi * rd_f**3.0)) * md_f / (1.0 + (r * r)/ (rd_f * rd_f))**(5.0 / 2.0)
                
                dark_mass_enc = mass_dark_current * self.half_mass_radius**3.0 / (self.half_mass_radius**2. + rad_dark_current**2.)**(3.0 / 2.0)
                if(dark_mass_enc > (dark_mass_enclosed_half_light - threshold) and dark_mass_enc < (dark_mass_enclosed_half_light + threshold) ):
                    self.rrs.append(rr)
                    self.mrs.append(mr)
                    self.mdencs.append(dark_mass_enc)
                
                rr += 0.001
            mr += 0.001
    
    

def imshow(sweep):
    fitted = [[0.232420964882834,0.259547435646423], [0.183881619186761, 0.168896086739161], [0.184036020601296, 0.185490490608526]]#test values
    const_half_light = half_light()
    
    likelihood_cutoff = -75
    fntsiz  = 20
    lblsize = 16
    legsize = 22
    x = np.asarray(sweep.vals)
    y = np.asarray(sweep.vals2)
    z = np.asarray(sweep.liks) 
    
    nInterp = 75
    #nInterp = 10
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.figsize=(20, 10)
    plt.sharey=True
    plt.sharex=True
    f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(10, 10))
    f.text(0.5, 0.04, titles[coori], ha='center', fontsize = fntsiz)
    #f.text(0.04, 0.5, titles[coorj], ha='center', rotation='vertical', fontsize = fntsiz)

    plt.subplots_adjust(wspace=0)
    params = {'legend.fontsize': legsize,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    plt.subplot(121)
    plt.tick_params(axis='y', which='major', labelsize=lblsize)
    plt.tick_params(axis='x', which='major', labelsize=lblsize)
    #plt.xlabel(titles[coori], fontsize = fntsiz)
    plt.ylabel(titles[coorj], fontsize = fntsiz)        
    plt.xticks( [ 0.1, 0.2,0.3, 0.4])
    #plt.plot(const_half_light.rrs, const_half_light.mrs, linestyle = '-', linewidth = 5, color ='grey', alpha = 0.5)
    plt.imshow(zi, vmin=likelihood_cutoff, vmax=0, origin='lower', cmap ='winter'  , extent=[x.min(), x.max(), y.min(), y.max()],aspect="auto")
    
    
    
    plt.subplot(122)
    plt.tick_params(axis='y', which='major', labelsize=lblsize)
    plt.tick_params(axis='x', which='major', labelsize=lblsize)
    #constant DM mass region:
    plt.plot(const_half_light.rrs, const_half_light.mrs, linestyle = '-', linewidth = 5, color ='grey', alpha = 0.5)
    plt.xticks( [ 0.1, 0.2,0.3, 0.4])
    #fitted points:
    for i in range(len(fitted)):
        plt.scatter(fitted[i][0], fitted[i][1], s=20, marker= 'o',  color='k', alpha=1, edgecolors='none')
    
    #correct answer:
    plt.scatter(0.2, 0.2, s=20, marker= 'x',  color='k', alpha=1, edgecolors='none')
    plt.yticks([])
    plt.imshow(zi, vmin=likelihood_cutoff, vmax=0, origin='lower', cmap ='winter'  , extent=[x.min(), x.max(), y.min(), y.max()], aspect="auto")
    #plt.colorbar()
    cbar = plt.colorbar()
    cbar.set_label('Likelihood',size=fntsiz)
    cbar.ax.tick_params(labelsize=lblsize) 

    
    plt.savefig(folder + name_of_sweeps + '/heat_map.png', format='png', dpi = 300, bbox_inches='tight')
    
    
def main():
    correct = [3.95, 0.2, 0.2, 12, 0.2]
    sweep = sweep_data(folder, name_of_sweeps, twoD_names[0], 2)
    sweep.plottable_list()
    
    #contour(sweep)
    imshow(sweep)
main()