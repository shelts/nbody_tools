#/* Copyright (c) 2018 Siddhartha Shelton */
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Classes to store bin information                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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
        self.bin_centers = []                 # to store the bin centers for plotting
        self.bin_N = []                     # to store the counts from Yannys data to compare with out own binned counts
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
            self.Nbins = 24 
            self.bin_start = -36.0
            self.bin_end   = 36.0
            self.bin_size = (abs(self.bin_start - self.bin_end) / self.Nbins)
            self.bin_centers = []
            for i in range(0, self.Nbins):
                self.bin_lowers.append(self.bin_start + self.bin_size * (i) )
                self.bin_centers.append(self.bin_start + self.bin_size * (0.5  + i) ) # middle bin coordinates
                self.bin_uppers.append(self.bin_start + self.bin_size * (1.0  + i) )

class field:#class system for reading in data
    def __init__(self, field_file):
        self.data_file = field_file

        self.negate = False
        self.read_counts()
        
        
    def read_counts(self):
        self.star_lmda = []; 
        self.star_beta = []; 
        
        f = open(self.data_file, 'r')
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
                    
                self.star_lmda.append(str_N_lbda)
                self.star_beta.append(str_N_beta)
        f.close()
        
        
class data_correction:
    def __init__(self, field):
        cut = -15
        for i in range(0, len(field.star_lmda)):
            if(field.star_lmda[i] < cut):
                field.star_beta[i] += 0.00628 * field.star_lmda[i]**2.0 + 0.42 * field.star_lmda[i] + 5.00
                
                
class bin_counts:
    def __init__(self, field_data, field_hist_parameters):#need to bin the data into regularly sized bins
        bnd_counts = []; beta_sums = []; beta_sqsums = []; beta_binN = []
        
        self.beta_data   = beta_data()
        self.binned_data = binned_data()
        #obs = [[]]#for debugging
        
        for i in range(field_hist_parameters.Nbins):        #initial the counts and sums
            bnd_counts.append(0.0)
            beta_sums.append(0.0)
            beta_sqsums.append(0.0)
            beta_binN.append(0.0)
            
            self.beta_data.beta_coors.append([])
        
            #obs.append([])#for debugging
            
        for i in range(len(field_data.star_lmda)):             #go through all the stars
            bin_upper = field_hist_parameters.bin_uppers[0]           #restart at the beginning of the histogram
            bin_lower = field_hist_parameters.bin_lowers[0]
            
            #print bin_lower, bin_upper
            for j in range(field_hist_parameters.Nbins):
                bin_lower = field_hist_parameters.bin_lowers[j]       #current lower bin
                bin_upper = field_hist_parameters.bin_uppers[j]       #current upper bin
                
                if(field_data.star_lmda[i] >= bin_lower and field_data.star_lmda[i] < bin_upper):
                    bnd_counts[j]      += 1.0

                    beta_sums[j]       += field_data.star_beta[i]
                    beta_sqsums[j]     += field_data.star_beta[i]**2.
                    beta_binN[j]       += 1.0
                    
                    self.beta_data.beta_coors[j].append(field_data.star_beta[i]) # storing the beta coordinates for current bin
                        
                    #obs[j].append(field_data.star_lmda[i])  #for debugging
                    break                           #if bin found no need to keep searching

        self.binned_data.counts  = bnd_counts
        self.beta_data.sums   = beta_sums
        self.beta_data.sqsums = beta_sqsums
        self.beta_data.binN   = beta_binN
        
        del bnd_counts,  beta_sums, beta_sqsums, beta_binN
        
    
    
    
class get_binned_difference:
    def __init__(self, On_field_binned, Off_field_binned):
        self.binned_data = binned_data()

        if(len(On_field_binned.binned_data.counts) > 0 and len(Off_field_binned.binned_data.counts) > 0):
            for i in range(len(On_field_binned.binned_data.counts)):
                diff = (On_field_binned.binned_data.counts[i] - Off_field_binned.binned_data.counts[i])
                self.binned_data.counts.append(diff)           # find the difference in the on and off field in each bin
                
                err = (On_field_binned.binned_data.counts[i] + Off_field_binned.binned_data.counts[i])**0.5
                self.binned_data.err.append(err)    # error in the difference. The error in the counts is the sq root of the counts. The sum of the squares is then this.    
                
                
                
class normalize:
    def __init__(self, N, Nerr):# need to normalize counts in the mw@home data histogram
        self.binned_data = binned_data()
        f_turn_offs = 13
        self.mass_per_count = 1.0 / 222288.47   # each count represents about 5 solar masses #
        total = 0.0
        total_error = 0.0
        
        for i in range(0, len(N)):
            N[i] *= f_turn_offs
            Nerr[i] *= f_turn_offs
            if(N[i] >= 0.0):
                total += N[i]                       # calc the total counts #
                total_error +=  Nerr[i] * Nerr[i]   # total error is sum in quadrature of each error #
        total_error = total_error **0.5         # take the sqr root #
        
        self.total_count = total                # for use when printing the histogram
        c2 = total_error / total                # coeff for use later #
        for i in range(0, len(N)):
            self.binned_data.counts.append(N[i] / total)  # normalized counts #
            
            if(N[i] > 0):                       # error for bins with counts in them #
                c1 = Nerr[i] / N[i]             # another coeff #     
                er = (N[i] / total) * (c1 * c1 + c2 *c2)**0.5 # follows the error formula for division of two things with error, in this case the individual count and the total #
                self.binned_data.err.append(er)
                ###self.N_error.append( (N[i]**0.5) / total)
            else:
                self.binned_data.err.append(1.0 / total)              # if there is no counts, then the error is set to this default #



class make_mw_hist:
    def __init__(self, bnd_diff_normed, hist_paras, vgsr = None):
        hist = open("data_hist_spring_2018_refac.hist", "w")
        hist.write("# Orphan Stream histogram \n# Generated from data from Dr. Yanny from Orphan stream paper\n# format is same as other MW@Home histograms\n#\n#\n")
        hist.write("n = %i\n" % (int(bnd_diff_normed.total_count)))
        hist.write("massPerParticle = %.15f\n" % (bnd_diff_normed.mass_per_count))
        hist.write("lambdaBins = %i\nbetaBins = 1\n" % (len(hist_paras.bin_centers)))
        for i in range(0, len(hist_paras.bin_centers)):
            if(vgsr == None):
                hist.write("1 %.15f %.15f %.15f %.15f %.15f %.15f %.15f %.15f\n" % (hist_paras.bin_centers[i], 0, bnd_diff_normed.binned_data.counts[i], bnd_diff_normed.binned_data.err[i],  -1, -1, -1, -1)) # not using vgsr anymore
            else:
                hist.write("1 %.15f %.15f %.15f %.15f %.15f %.15f\n" % (hist_paras.bin_centers[i], 0, bnd_diff_normed.binned_data.counts[i], bnd_diff_normed.binned_data.err[i],  vgsr.vel.disp[i], vgsr.vel.disp_err[i]))
   