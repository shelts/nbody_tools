#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # #
#   This File Works For create_data_hist.py #
# # # # # # # # # # # # # # # # # # # # # # #

class vel_data:     # place to store the velocity data. Makes it a little easier to keep track of the variables
    def __init__(self):
        self.los = []; self.lda = []; self.err = []; 
        self.disp = []; self.disp_err = []; 
        self.bnd_N = [];



class vgsr_data:
    def __init__(self, vgsr_file):
        self.vgsr_file = vgsr_file
        
        self.read_vgsr()
        
    def read_vgsr(self):
        self.vel = vel_data()
        #self.vel_los = []; self.vel_los_lda = []; self.vel_los_err = []
        
        
        f = open(self.vgsr_file, 'r')
        read_data = False
        for line in f:
            if(line.startswith("#")):
                read_data = False
                continue
            else: 
                read_data = True
                
            if(read_data):
                ss = line.split(" ")
                v_disp_lda  = float(ss[50])
                v_disp      = float(ss[29])
                v_err       = float(ss[17])
                #print v_disp, v_err, v_disp_lda
                self.vel.los.append(v_disp)
                self.vel.lda.append(v_disp_lda)
                self.vel.err.append(v_err)
                
        f.close()

    def bin_vgsr(self, bin_lowers = None, bin_uppers = None): # need to bin the data into regularly sized bins
        bnd_vel_sum     = []
        bnd_vel_sqsum   = []
        bnd_vgsr_counts = []
        velDisp_err     = []
        bnd_vel_disp    = []
        vsq_sumerr = []
        v_sumerr = []
        
        if(bin_lowers):
            bin_upper_init = bin_uppers[0]
            bin_lower_init = bin_lowers[0]
        else:
            bin_upper_init = self.bnd.bin_start + self.bnd.bin_size # reinitialize the bin search brackets
            bin_lower_init = self.bnd.bin_start
        
        #obs = [[]]#for debugging
        
        for i in range(0, self.bnd.Nbins):
            bnd_vgsr_counts.append(0.0)
            bnd_vel_sum.append(0.0)
            bnd_vel_sqsum.append(0.0)
            bnd_vel_disp.append(0.0)
            velDisp_err.append(0.0)
            vsq_sumerr.append(0.0)
            v_sumerr.append(0.0)
            
            #obs.append([])#for debugging
        
        for i in range(0, len(self.vel.lda)):     # for every vel coordinate 
            bin_upper = bin_upper_init            # restart at the beginning of the histogram
            bin_lower = bin_lower_init
            
            for j in range(0, self.bnd.Nbins):
                if(bin_lowers):                   # if the bin coordinates were already given then iterate through them #
                    bin_lower = bin_lowers[j]     # current lower bin. determined from given coordinates #
                    bin_upper = bin_uppers[j]     # current upper bin #
                    
                if(self.vel.lda[i] >= bin_lower and self.vel.lda[i] < bin_upper):       # check if coordinate is in bin
                    vsq = self.vel.los[i] * self.vel.los[i]
                    
                    bnd_vel_sum[j]     += self.vel.los[i]                               # needed to calculate the vel dispersion. sum of the vels#
                    bnd_vel_sqsum[j]   += vsq                                           # also needed for vel dispersion. sum of the sqrs of the vels #
                    bnd_vgsr_counts[j] += 1.0                                           # increase the counts in each bin. #
                    
                    ersq = self.vel.err[i] * self.vel.err[i] 
                    v_sumerr[j]   += ersq                                               # propagating the error for the v summation    
                    vsq_sumerr[j] += 4.0 * ersq * vsq                                   # propagating the error for the v sqr summation. its (2*error*v)^2
                    
                    #obs[j].append(self.vel_los[i]) #for debugging
                    #self.bnd_counts[j] += self.star_N[i]
                    
                    break #if bin found no need to keep searching

                if(not bin_lowers):         # if it is standard binning, advance the bins. i.e. bin coordinates were not given
                    bin_lower = bin_upper   # shift the search brackets by 1 bin
                    bin_upper = bin_lower + self.bnd.bin_size

        for i in range(0, self.bnd.Nbins):                                  # go through the bins
            v_sumerr[i]   = v_sumerr[i] ** 0.5                              # error is the square root of the sums
            vsq_sumerr[i] = vsq_sumerr[i] ** 0.5
            
            if(bnd_vgsr_counts[i] > 1):                                     # only calc vel disp if it makes sense to do so.
                N1 = (bnd_vgsr_counts[i] - 1.0)                             # reduced count    
                N2 = (bnd_vgsr_counts[i])                                   # total count
                
                a = bnd_vel_sqsum[i] / N1                                   # coeff1 of vel dispersion equation
                a_err = vsq_sumerr[i] / N1                                  # error gets divided by constant as well    
                
                b = N2 / N1                                                 # coeff 2
                
                c = bnd_vel_sum[i] / N2                                     # coeff 3
                c_err = v_sumerr[i] / N2                                    # error gets divided by constant as well 

                bnd_vel_disp[i] = ( a - b * c * c ) ** 0.5                  # vel dispersion equation rewritten for computational ease 
                
                cc_err = 2.0 * c_err * c                                    # error in the c * c part
                
                bcc_err = cc_err * b                                        # error is multiplied by constant
                
                a_min_b_err = ( a_err * a_err + bcc_err * bcc_err)**0.5     # error in the difference, a - bcc
                #print N1, '\t', N2, '\t', b,'\t',  a, '\t',   a_err, '\t',b, '\t', c, '\t', c_err, '\t',  cc_err, '\t',  bcc_err, '\t', bnd_vel_disp[i], '\t', a_min_b_err
                
                #velDisp_err[i] = a_min_b_err * a_min_b_err / (4.0 * bnd_vel_disp[i])                    # error due to square root. error formula for smething to a power of .5
                velDisp_err[i] = (N2**0.5 / N1 ) * bnd_vel_disp[i]
                #Nerr1 = (bnd_vgsr_counts[i] - 1.0) ** 0.5               # error for reduced count
                #Nerr2 = (bnd_vgsr_counts[i]) ** 0.5                     # error in total count
                #a_err = a * ( (vsq_sumerr[i] / bnd_vel_sqsum[i])**2.0 + (Nerr1 / N1)**2  ) **0.5       # error due to division of two things with error for coeff1
                #b_err = b * ( (Nerr1 / N1 )**2.0 + (Nerr2 / N2)**2 )**0.5                               # error due to division of two things with error for coeff2  
                #c_err = c * ( (v_sumerr[i] / bnd_vel_sum[i])**2.0 + (Nerr2 / N2)**2  ) **0.5           # error due to division of two things with error for coeff3
                #bcc_err = b * c * c * ( (cc_err / (c * c))**2.0 + (b_err / b)**2.0 )**0.5               # error in the b * cc part
                
                
            else:                                                       # if too few items in the bin:
                bnd_vel_disp[i] = -1                               # mark the bin off as negative to be skipped when comparing histograms
        
        self.vel.disp = bnd_vel_disp
        self.vel.disp_err = velDisp_err
        self.vel.bnd_N = bnd_vgsr_counts
        return 0

    def data_clear(self, stage):
        if(stage == 'data lists'):      # first stage of deletion. Deletes stored data
            del self.vel.los            # dels the line of sight vels #
            del self.vel.lda            # dels the coordinates for the line of sight vels #
            del self.vel.err            # dels the errors for the line of sight vels





    def plot_vgsr(self):
        f, ((ax1, ax2, ax3)) = plt.subplots(3, sharex='col')
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        w = 3
        ax1 = plt.subplot(311)
        plt.xlim(40, -50)
        plt.ylim(-300, 300)
        plt.ylabel("v$_{gsr}$")
        plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50], alpha = 0)
        plt.scatter(self.vel.lda, self.vel.los, s = .5, marker = "o", color = "k", alpha = 1)
        
        ax2 = plt.subplot(312)
        plt.xlim(40, -50)
        plt.ylim(0, 18)
        plt.ylabel("$\sigma$")
        plt.xlabel("$\Lambda_{Orphan}$")
        plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50], alpha = 0)
        plt.bar(self.bnd.count_lda, self.vel.disp, width = w, color = "w", edgecolor = "k", alpha = 1)
        
        ax3 = plt.subplot(313)
        plt.xlim(40, -50)
        #plt.ylim(0, 18)
        plt.ylabel("N")
        plt.xlabel("$\Lambda_{Orphan}$")
        plt.xticks( [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50])
        plt.bar(self.bnd.count_lda, self.vel.bnd_N, width = w, color = "w", edgecolor = "k", alpha = 1)
        
        plt.savefig('figure6_recreation.png', format='png')             
        

        plt.savefig('figure6_recreation.png', format='png')        
        plt.clf()