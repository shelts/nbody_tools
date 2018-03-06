#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Algorithm to take in stream data and create a milkyway@home compatible histogram  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
from subprocess import call
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import AutoMinorLocator
from vel_disp import *
from beta_bins import *
        
class beta_data:
    def __init__(self):
        self.sums = []; self.sqsums = []
        self.disp = []; self.disp_err = []
        self.binN = []
        self.beta_coors = []
        
class binned_data:                          # class to store binned data
    def __init__(self):
        self.counts = []
        self.err = []
        
class bin_parameters:                       # class to store binner parameters
    def __init__(self, file_name = None):   # init the data bins since its common between star counts and vgsr disp.
        self.bin_lowers = []                # the lower coordinates for each bin 
        self.bin_uppers = []                # the upper coordinates for each bin
        self.bin_N = []                     # to store the counts from Yannys data to compare with out own binned counts
        self.bin_centers = []                 # to store the bin centers for plotting
        self.Nbins = None                   # the number of bins
        
        if(file_name):                      # if there is a data file with bin beginnings and endings then we can use that
            file_name = open(file_name, "r")
            for line in file_name:
                ss = line.split(" ")
                bn_lower = float(ss[0])             # read the lower and upper bin coordinates from file
                bn_upper = float(ss[1])
                if(len(ss) > 3):
                    bn_n     = float(ss[3])             # the counts yanny has in his data for that bin    
                self.bin_lowers.append(bn_lower)    # store bin upper and lower coordinates
                self.bin_uppers.append(bn_upper)
                if(len(ss) > 3):
                    self.bin_N.append(bn_n)
                self.bin_centers.append(bn_lower + (bn_upper - bn_lower) / 2.0) # center of the bin which is what we will plot
                
            self.Nbins = len(self.bin_lowers) 
            
        else: # regularly size the bins automatically if we don't use Yanny's bin coordinates
            self.Nbins = 10 
            self.bin_start = -30.0
            self.bin_end   = 30.0
            self.bin_size = (abs(self.bin_start - self.bin_end) / self.Nbins)
            self.bin_centers = []
            for i in range(0, self.Nbins):
                self.bin_centers.append(self.bin_start + self.bin_size * (0.5  + i) ) # middle bin coordinates



class data:#class system for reading in data and making a data histogram
    def __init__(self, on_field_counts_file, off_field_counts_file):
        self.on_field_counts_file = on_field_counts_file
        self.off_field_counts_file = off_field_counts_file
        
        self.ON_count_err = []
        self.OFF_count_err = []
        #self.negate = True
        self.negate = False
        self.read_counts()
        self.data_correction()
        
    def read_counts(self):
        self.ON_star_N_lbda = []; self.OFF_star_N_lbda = [];
        self.ON_star_N_beta = []; self.OFF_star_N_beta = [];
        self.beta_ON  = beta_data()
        self.beta_OFF = beta_data()
        self.bin_ON   = binned_data()
        self.bin_OFF  = binned_data()
        
        f = open(self.on_field_counts_file, 'r')
        g = open(self.off_field_counts_file, 'r')
        read_data = False
        for line in f:
            if(line.startswith("#")):
                read_data = False
                continue
            else: 
                read_data = True
                
            if(read_data):
                line = line.strip(" ")#remove the leading and trailing empty space
                line = line.replace('   ', ' ')#the data is not regularly spaced
                line = line.replace('  ', ' ')

                ss = line.split(" ")
                #print ss
                str_N_lbda  = float(ss[0])
                str_N_beta  = float(ss[1])
                if(len(ss) > 1):
                    str_N       = float(ss[3])
                
                if(self.negate):
                    str_N_lbda = -str_N_lbda
                    
                self.ON_star_N_lbda.append(str_N_lbda)
                self.ON_star_N_beta.append(str_N_beta)
        read_data = False
        for line in g:
            if(line.startswith("#")):
                read_data = False
                continue
            else: 
                read_data = True
                
            if(read_data):
                line = line.strip(" ")#remove the leading and trailing empty space
                line = line.replace('   ', ' ')#the data is not regularly spaced
                line = line.replace('  ', ' ')

                ss = line.split(" ")
                str_N_lbda  = float(ss[0])
                str_N_beta  = float(ss[1])
                if(len(ss) > 1):
                    str_N       = float(ss[3])
                
                if(self.negate):
                    str_N_lbda = -str_N_lbda
                    
                self.OFF_star_N_lbda.append(str_N_lbda)
                self.OFF_star_N_beta.append(str_N_beta)
        f.close()
        g.close()
    
    def data_correction(self):
        cut = -15
        #if(self.negate):
            #cut = -cut
            
        for i in range(0, len(self.ON_star_N_lbda)):
            if(self.ON_star_N_lbda[i] < cut):
                self.ON_star_N_beta[i] += 0.00628 * self.ON_star_N_lbda[i]**2.0 + 0.42 * self.ON_star_N_lbda[i] + 5.00
                
        for i in range(0, len(self.OFF_star_N_lbda)):
            if(self.OFF_star_N_lbda[i] < cut):
                self.OFF_star_N_beta[i] += 0.00628 * self.OFF_star_N_lbda[i]**2.0 + 0.42 * self.OFF_star_N_lbda[i] + 5.00
    
    def bin_counts(self, star_N_lbda, star_N_beta, field):#need to bin the data into regularly sized bins
        bnd_counts = []
        beta_sums = []; beta_sqsums = []; beta_binN = []
        
        #obs = [[]]#for debugging
        bin_lower = None
        bin_upper = None
        
        if(self.bnd.bin_lowers):
            bin_upper_init = self.bnd.bin_uppers[0]
            bin_lower_init = self.bnd.bin_lowers[0]
        else:
            bin_upper_init = self.bnd.bin_start + self.bnd.bin_size     #reinitiaze the bin search brackets
            bin_lower_init = self.bnd.bin_start
        
        
        for i in range(0, self.bnd.Nbins):
            bnd_counts.append(0.0)
            beta_sums.append(0.0)
            beta_sqsums.append(0.0)
            beta_binN.append(0.0)
            if(field == "ON"):
                self.beta_ON.beta_coors.append([])
            else:
                self.beta_OFF.beta_coors.append([])
        
            #obs.append([])#for debugging
            
        for i in range(0, len(star_N_lbda)):        #go through all the stars
            bin_upper = bin_upper_init              #restart at the beginning of the histogram
            bin_lower = bin_lower_init
            
            #print bin_lower, bin_upper
            for j in range(0, self.bnd.Nbins):
                if(self.bnd.bin_lowers):
                    bin_lower = self.bnd.bin_lowers[j]       #current lower bin
                    bin_upper = self.bnd.bin_uppers[j]       #current upper bin
                
                if(star_N_lbda[i] >= bin_lower and star_N_lbda[i] < bin_upper):
                    bnd_counts[j]      += 1.0

                    beta_sums[j]       += star_N_beta[i]
                    beta_sqsums[j]     += star_N_beta[i]**2.
                    beta_binN[j]       += 1.0
                    
                    if(field == "ON"):
                        self.beta_ON.beta_coors[j].append(star_N_beta[i])
                    elif(field == "OFF"):
                        self.beta_OFF.beta_coors[j].append(star_N_beta[i])
                        
                    #obs[j].append(star_N_lbda[i])  #for debugging
                    break                           #if bin found no need to keep searching

                if(not self.bnd.bin_lowers):                 #if it is standard binning, advance the bins
                    bin_lower = bin_upper           #shift the search brackets by 1 bin
                    bin_upper = bin_lower + self.bnd.bin_size
                #print bin_lower, bin_upper
        if(field == "ON"):
            self.bin_ON.counts  = bnd_counts
            self.beta_ON.sums   = beta_sums
            self.beta_ON.sqsums = beta_sqsums
            self.beta_ON.binN   = beta_binN
            #print self.beta_ON.beta_coors
        elif(field == "OFF"):
            self.bin_OFF.counts  = bnd_counts
            self.beta_OFF.sums   = beta_sums
            self.beta_OFF.sqsums = beta_sqsums
            self.beta_OFF.binN   = beta_binN
            #print self.beta_OFF.beta_coors
        
        del star_N_lbda, bnd_counts, star_N_beta, beta_sums, beta_sqsums, beta_binN
        
        return 0
    
    def binned_diff(self):                                                                          # take the difference between the on and off fields.
        self.beta_diff = beta_data()
        self.bin_diff = binned_data()

        if(len(self.bin_ON.counts) > 0 and len(self.bin_OFF.counts) > 0):
            for i in range(0, len(self.bin_ON.counts)):
                self.bin_diff.counts.append((self.bin_ON.counts[i] - self.bin_OFF.counts[i]))           # find the difference in the on and off field in each bin
                self.bin_diff.err.append( (self.bin_ON.counts[i] + self.bin_OFF.counts[i])**0.5)    # error in the difference. The error in the counts is the sq root of the counts. The sum of the squares is then this.    
                
                #self.beta_diff.sums.append(  (self.beta_ON.sums[i]   - self.beta_OFF.sums[i]))
                #self.beta_diff.sqsums.append((self.beta_ON.sqsums[i] - self.beta_OFF.sqsums[i]))
                #self.beta_diff.binN.append(  abs(self.beta_ON.binN[i]   - self.beta_OFF.binN[i]))
                
                self.beta_diff.sums.append(  (self.beta_ON.sums[i]))
                self.beta_diff.sqsums.append((self.beta_ON.sqsums[i] ))
                self.beta_diff.binN.append(  abs(self.beta_ON.binN[i]))
    
    def beta_dispersion(self):
        for i in range(0, len(self.beta_diff.sums)):
            sums = self.beta_diff.sums[i]
            sqsums = self.beta_diff.sqsums[i]
            
            N = self.beta_diff.binN[i]
            if(N > 2):
                dispsq = sqsums / (N - 1.)
                #print dispsq, sqsums, sums**2.
                dispsq -= ( N / (N - 1.) ) * (sums / N)**2.
                #print dispsq, ( N / (N - 1.) ) * (sums / N)**2., N, '\n'
                dispsq = dispsq**0.5
                self.beta_diff.disp.append(dispsq)
            else:
                self.beta_diff.disp.append(-1)
                
    
    def normalize_counts(self, N, Nerr):# need to normalize counts in the mw@home data histogram
        self.bin_normed = binned_data()
        f_turn_offs = 7.5
        self.mass_per_count = 1.0 / 222288.47   # each count represents about 5 solar masses #
        total = 0.0
        total_error = 0.0
        
        for i in range(0, len(N)):
            N[i] *= f_turn_offs
            Nerr[i] *= f_turn_offs
            total += N[i]                       # calc the total counts #
            total_error +=  Nerr[i] * Nerr[i]   # total error is sum in quadrature of each error #
        total_error = total_error **0.5         # take the sqr root #
        
        self.total_count = total                # for use when printing the histogram
        c2 = total_error / total                # coeff for use later #
        for i in range(0, len(N)):
            self.bin_normed.counts.append(N[i] / total)  # normalized counts #
            
            if(N[i] > 0):                       # error for bins with counts in them #
                c1 = Nerr[i] / N[i]             # another coeff #     
                er = (N[i] / total) * (c1 * c1 + c2 *c2)**0.5 # follows the error formula for division of two things with error, in this case the individual count and the total #
                self.bin_normed.err.append(er)
                ###self.N_error.append( (N[i]**0.5) / total)
            else:
                self.bin_normed.err.append(1.0 / total)              # if there is no counts, then the error is set to this default #


    def plot_counts(self):
        plt.xlim(50, -50)
        plt.ylim(0, 1500)
        plt.xlabel("$\Lambda_{Orphan}$")
        plt.ylabel("N")
        plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
        #plt.tick_params(which='minor', length=4, color='r')
        w = 2.6
        if(len(self.bin_ON.counts) > 0):
            plt.bar(self.bnd.bin_centers, self.bin_ON.counts, width = w, color = "w", edgecolor = "k", alpha = 1)
        if(len(self.bin_OFF.counts) > 0):
            plt.bar(self.bnd.bin_centers, self.bin_OFF.counts, width = w, color = "w", edgecolor = "r", alpha = 0.5)
        
        if(len(self.bin_diff.counts) > 0):
            plt.bar(self.bnd.bin_centers, self.bin_diff.counts, width = w, color = "b", edgecolor = "b", alpha = 0.5)
            #plt.bar(self.bnd.bin_centers, self.bnd.bin_N, width = w, color = "k", edgecolor = "b", alpha = 0.5)
        plt.savefig('plots/figure5_recreation.png', format='png')
        plt.clf()
        #plt.show()
    
    def plot_simN_normed(self):
        plt.xlim(50, -50)
        #plt.ylim(0, 1500)
        plt.xlabel("$\Lambda_{Orphan}$")
        plt.ylabel("N")
        plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
        #plt.tick_params(which='minor', length=4, color='r')
        w = 2.6
        plt.bar(self.bnd.bin_centers, self.bin_normed.counts, width = w, color = "b", edgecolor = "b", alpha = 0.5)
        plt.savefig('plots/figure5_simunits_normed.png', format='png')
        plt.clf()
        #plt.show()   
        
        
    def make_mw_hist(self, vgsr = None):
        hist = open("data_hist_fall_2017.hist", "w")
        hist.write("# Orphan Stream histogram \n# Generated from data from Dr. Yanny from Orphan stream paper\n# format is same as other MW@Home histograms\n#\n#\n")
        hist.write("n = %i\n" % (int(self.total_count)))
        hist.write("massPerParticle = %.15f\n" % (self.mass_per_count))
        hist.write("lambdaBins = %i\nbetaBins = 1\n" % (len(self.bnd.bin_centers)))
        for i in range(0, len(self.bnd.bin_centers)):
            if(vgsr == None):
                hist.write("1 %.15f %.15f %.15f %.15f %.15f %.15f\n" % (self.bnd.bin_centers[i], 0, self.bin_normed.counts[i], self.bin_normed.err[i],  -1, -1)) # not using vgsr anymore
            else:
                hist.write("1 %.15f %.15f %.15f %.15f %.15f %.15f\n" % (self.bnd.bin_centers[i], 0, self.bin_normed.counts[i], self.bin_normed.err[i],  vgsr.vel.disp[i], vgsr.vel.disp_err[i]))
   
    def data_clear(self, stage):
        if(stage == 'data lists'):      # first stage of deletion. Deletes stored data
            del self.ON_star_N_lbda     # delets the on and off field data when no longer needed #
            del self.OFF_star_N_lbda
            del self.ON_star_N_beta
            del self.OFF_star_N_beta
        if(stage == 'binned counts'):   # stage deletes the binned data for each field
            del self.bin_ON
            del self.bin_OFF
            del self.beta_ON
            del self.beta_OFF
        if(stage == 'binned diff'):     # deletes binned data of the difference between fields after normalization
            del self.bin_diff
            del self.bnd.bin_N

    
def main():
    use_vgsr = False
    use_yanny_bins = True
    calc_beta_dispersions = True
    make_hist = False
    normalize_counts =  False
    
    plot_counts = True
    plot_normed_counts = False
    
    # name of the data files # 
    vgsr_file = "my16lambet2bg.specbhb.dist.lowmet.stream"
    on_field_counts_file = "l270soxlbfgcxNTbcorr.newon"
    off_field_counts_file = "l270soxlbfgcxNTbcorr.newoff"
    bin_data = "data_from_yanny.dat"
    bin_data = "custom_bins4.dat"
    
    dat = data(on_field_counts_file, off_field_counts_file)
    # initiaze bins parameters #
    if(use_yanny_bins):
        dat.bnd = bin_parameters(bin_data)
    else:
        dat.bnd = bin_parameters()
    #print dat.bnd.bin_centers
    # get the data  #
    
    # bin the star counts #
    dat.bin_counts(dat.ON_star_N_lbda,  dat.ON_star_N_beta,  "ON" )
    dat.bin_counts(dat.OFF_star_N_lbda, dat.OFF_star_N_beta, "OFF")
    
    # clears the data lists, only need binned data #
    dat.data_clear('data lists')                            

    # get the binned diff of the two fields. also the error in the difference #
    dat.binned_diff()  
    #print dat.bin_ON.counts
    #print dat.bin_OFF.counts
    print dat.bin_diff.counts
    #print dat.bnd.bin_centers
    # plot the binned counts #
    if(plot_counts):
        dat.plot_counts()                                       
    
    # bin the beta counts #
    if(calc_beta_dispersions):
        betas = bin_betas(dat.beta_ON.beta_coors, dat.beta_OFF.beta_coors, dat.bnd)
    
    # deletes the on and off field bin data. only need bin diff data # 
    dat.data_clear('binned counts')                         
    
    
    # normalize the binned counts #
    if(normalize_counts):
        dat.normalize_counts(dat.bin_diff.counts, dat.bin_diff.err)
    
    if(plot_normed_counts):
        dat.plot_simN_normed()  
    
    # deletes binned diff. only need converted #
    dat.data_clear('binned diff')
    
    # makes the actual mw@h histogram #
    if(use_vgsr and make_hist):
        vgsr_dat = vgsr_data(vgsr_file)
        # bin the vgsr los, and vel disp #
        vgsr_dat.bin_vgsr(dat.bnd.bin_lowers, dat.bnd.bin_uppers)
    
        # plot the vgsr points #
        #vgsr_dat.plot_vgsr()                                         
        vgsr_dat.clear('data lists')
        dat.make_mw_hist(vgsr_dat)
    elif(make_hist):
        dat.make_mw_hist()
main()
    