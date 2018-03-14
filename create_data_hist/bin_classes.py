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

