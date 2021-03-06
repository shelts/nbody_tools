#! /usr/bin/python
#/* Copyright (c) 2016 Siddhartha Shelton */
from nbody_functional import *
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.interpolate import griddata
import matplotlib.gridspec as gridspec


path = '/home/sidd/Desktop/research/'
folder = path + "like_surface/"
#name_of_sweeps = '2D_hists'
#name_of_sweeps = 'parameter_sweep_2d_v170'
name_of_sweeps = 'parameter_sweep_2d_v174_simulated_hist'
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
    
    

def imshow(sweep, const_half_light):
    #fitted = [[0.235449047582905,0.269766858968207], [0.173454370530649,0.166652986169686], [0.219882548707629,0.23749775053657]]#test values
    #fitted = [[0.282291462697629,0.345760264545573], [0.213388844765707,0.203773596841339], [0.243460580326148,0.314222556206743]]#test values
    fitted = [[0.199125487778006, 0.22195363970244], [0.19827770887759,0.238590596229027], [0.196378867869936,0.221402554565405]]
    #fitted = [[0.5,0.01], [0.462,0.011], [.431,.01]]#test values
    
    
    #likelihood_cutoff = -10000
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
    f, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(15, 15))
    f.text(0.5, 0.04, titles[coori], ha='center', fontsize = fntsiz)

    plt.subplots_adjust(wspace=0)
    params = {'legend.fontsize': legsize,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    plt.subplot(121)
    plt.tick_params(axis='y', which='major', labelsize=lblsize)
    plt.tick_params(axis='x', which='major', labelsize=lblsize)
    plt.xticks( [ 0.2, 0.4])
    plt.ylabel(titles[coorj], fontsize = fntsiz)        
    
    im = plt.imshow(zi, vmin=likelihood_cutoff, vmax=0, origin='lower', cmap ='winter'  , extent=[x.min(), x.max(), y.min(), y.max()],aspect="auto")
    
    
    
    plt.subplot(122)
    plt.tick_params(axis='y', which='major', labelsize=lblsize)
    plt.tick_params(axis='x', which='major', labelsize=lblsize)
    plt.xticks( [  0.2, 0.4])
    plt.yticks([])

    im = plt.imshow(zi, vmin=likelihood_cutoff, vmax=0, origin='lower', cmap ='winter'  , extent=[x.min(), x.max(), y.min(), y.max()], aspect="auto")
    
    #constant DM mass region:
    plt.plot(const_half_light.rrs, const_half_light.mrs, linestyle = '-', linewidth = 5, color ='r', alpha = 0.5, zorder=1)

    #fitted points:
    colors = ['k', 'k', 'k']
    for i in range(len(fitted)):
        plt.scatter(fitted[i][0], fitted[i][1], s=80, marker= 'o',  color=colors[i], alpha=1, edgecolors='none', zorder=2)
    
    #correct answer:
    plt.scatter(0.2, 0.2, s=120, marker= 'x',  color='chartreuse', alpha=1, edgecolors='none', zorder=3)



    cb_ax = f.add_axes([0.905, 0.11, 0.03, 0.77])
    cbar = f.colorbar(im, cax=cb_ax)
    cbar.set_label('Likelihood',size=fntsiz)
    cbar.ax.tick_params(labelsize=lblsize) 

    #plt.tight_layout()
    plt.savefig(folder + name_of_sweeps + '/heat_map.png', format='png', dpi = 300, bbox_inches='tight')
    plt.savefig(folder + name_of_sweeps + '/heat_map.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    
def main():
    correct = [3.95, 0.2, 0.2, 12, 0.2]
    sweep = sweep_data(folder, name_of_sweeps, twoD_names[0], 2)
    sweep.plottable_list()
    
    #contour(sweep)
    const_half_light = half_light()
    imshow(sweep,const_half_light)
main()