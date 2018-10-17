#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
import matplotlib.pyplot as plt
import numpy as np
import math as mt
import scipy
from scipy.interpolate import griddata
import matplotlib.gridspec as gridspec

class timestep:
    def __init__(self, baryon_scale, baryon_mass):
        self.baryon_mass  = baryon_mass
        self.baryon_scale = baryon_scale
        self.create_surface()
        
    def get_timestep(self, rscale_d, mass_d):#returns the appropiate timestep
        #Mass of a single dark matter sphere enclosed within light rscale
        #print mass_d, rscale_d
        mass_enc_d = mass_d * (self.baryon_scale)**3.  * ( (self.baryon_scale)**2. + (rscale_d)**2.  )**(-3.0/2.0)

        #Mass of a single light matter sphere enclosed within dark rscale
        mass_enc_l = self.baryon_mass * (rscale_d)**3. * ( (self.baryon_scale)**2. + (rscale_d)**2.  )**(-3.0/2.0)

        s1 = (self.baryon_scale)**3. / (mass_enc_d + self.baryon_mass)
        s2 = (rscale_d)**3. / (mass_enc_l + mass_d)

        #return the smaller time step
        if(s1 < s2):
            s = s1
        else:
            s = s2
        
        #I did it this way so there was only one place to change the time step. 
        t = (1 / 100.0) * (mt.pi * (4.0/3.0) * s)**(1.0/2.0)
        #print t
        return t
    
    def get_dark_parameters_rd(self, rr):#get the dark matter scale radius
        rscale_t  = self.baryon_scale / rr
        rscale_d  = rscale_t *  (1.0 - rr)
        return rscale_d
    
    def get_dark_parameters_md(self, mr):#get the dark matter mass
        dwarfMass = self.baryon_mass / mr
        mass_d    = dwarfMass * (1.0 - mr)
        return mass_d
        
    def create_surface(self):
        self.mrs = []
        self.rrs = []
        self.timesteps = []
        rr = 0.001
        mr = 0.001
        rr_cutoff = 0.95
        mr_cutoff = 0.95
        
        rd = self.get_dark_parameters_rd(rr)
        md = self.get_dark_parameters_md(mr)
        
        while(rr < rr_cutoff):
            mr = 0.001
            rd = self.get_dark_parameters_rd(rr)
            while(mr < mr_cutoff):
                md = self.get_dark_parameters_md(mr)
                #print 'ratios', rr,  mr, rd, md
                t = self.get_timestep(rd, md)
                self.mrs.append(mr)
                self.rrs.append(rr)
                self.timesteps.append(t)
                mr += 0.001
            rr += 0.001
            
            

def imshow(time):
    min_color = 5e-7
    max_color = 1e-5
    #likelihood_cutoff = -75
    fntsiz  = 16
    lblsize = 14
    legsize = 22
    x = np.asarray(time.rrs)
    y = np.asarray(time.mrs)
    z = np.asarray(time.timesteps) 
    
    nInterp = 75
    #nInterp = 10
    xi, yi = np.linspace(x.min(), x.max(), nInterp), np.linspace(y.min(), y.max(), nInterp)
    xi, yi = np.meshgrid(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    plt.figsize=(20, 10)

    plt.subplots_adjust(wspace=0)
    params = {'legend.fontsize': legsize,
            'legend.handlelength': 1}
    plt.rcParams.update(params)
    
    plt.tick_params(axis='y', which='major', labelsize=lblsize)
    plt.tick_params(axis='x', which='major', labelsize=lblsize)
    #plt.xticks( [ 0.2, 0.4])
    plt.ylabel('Mass Ratio (Baryonic/Total)', fontsize = fntsiz)        
    plt.xlabel(r'Scale Radius Ratio ($R_{B}/(R_{B}+R_{D})$)', fontsize = fntsiz)
    plt.xlim((0.01, .7))
    plt.ylim((0.001, .2))
    im = plt.imshow(zi, vmin=min_color, vmax=max_color, origin='lower', cmap ='plasma'  , extent=[x.min(), x.max(), y.min(), y.max()],aspect="auto")
    plt.colorbar(format='%.0e')
    plt.savefig('./timestep_surface.png', format='png', dpi = 300, bbox_inches='tight')
    plt.savefig('./timestep_surface.pdf', format='pdf', dpi = 300, bbox_inches='tight')
    
    
    
    
def main():
    baryon_mass = 0.1
    baryon_scale = 0.05
    print 'creating surface'
    time = timestep(baryon_scale, baryon_mass)
    print 'plotting'
    imshow(time)

main()
    