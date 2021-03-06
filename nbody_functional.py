import os
import subprocess
from subprocess import call
import math as mt
import random
# # # # # # # # # # # # # # # # # # # # # #
#        USEFUL CLASSES                   #
# # # # # # # # # # # # # # # # # # # # # #

class nbody_running_env:
    def __init__(self, lua_file, version, path):
        self.lua_file      = lua_file
        self.version       = version
        self.path          = path
    
    def build(self, scratch = None):#function for rebuilding nbody. it will build it in a seperate folder from the client directory
        os.chdir(self.path)
        
        if(scratch):
            os.system("rm -r nbody_test")  
            os.system("mkdir nbody_test")  
        
        os.chdir("nbody_test")

        #following are fairly standard cmake commands
        os.system("cmake -DCMAKE_BUILD_TYPE=Release -DNBODY_DEV_OPTIONS=OFF -DBOINC_RELEASE_NAMES=OFF -DDOUBLEPREC=ON -DNBODY_GL=ON -DNBODY_STATIC=ON -DBOINC_APPLICATION=OFF -DSEPARATION=OFF -DNBODY_OPENMP=ON    " + self.path + "milkywayathome_client/")
        
        #making the binaries. the -j is for multithreaded build/
        os.system("make -j ")
        os.chdir("../")
    
    
    def run(self, parameters, output_hist, comparison_hist = None, pipe = None, manual_body_list = ''):#running function. 2 optional parameters. 
        ft    = str(parameters[0])
        bt    = str(1.0)
        rl    = str(parameters[1])
        rr    = str(parameters[2])
        ml    = str(parameters[3])
        mr    = str(parameters[4])
        print('running nbody')
        os.chdir(self.path + "nbody_test/bin/")
        
        #below is a standard example of running nbody's binary
        #it is incomplete. It has the lua file flag, the output hist flag, and outfile flag
        run_command  = "./milkyway_nbody" + self.version + " \
                         -f " +  self.lua_file + " \
                         -z " +  output_hist + ".hist \
                         -o " +  output_hist + ".out "
        
        #final piece to the run command. includes the number of threads, output format, and visualizer args
        end_piece = "-n 30 -b   --visualizer-bin=" + self.path + "nbody_test/bin/milkyway_nbody_graphics -i " + ft + " " + bt + " " + rl + " " + rr + " " + ml + " " + mr + " " + manual_body_list
        
        if(not comparison_hist): ##this will produce a single run of nbody, without comparing the end result to anything
            run_command += end_piece #completing the run command
       
        elif(comparison_hist):#this willl produce a single run of nbody, comparing the end result to given histogram
            compare_hist_flag = " -h " + comparison_hist + ".hist  " #adding the input argument flag
            run_command +=  compare_hist_flag + end_piece
         
        if(pipe): 
            piping = " 2>> " + pipe  #adding the piping piece to the command to pipe output
            os.system(run_command + piping)
        else:
            os.system(run_command)
   
   
   
    def match_hists(self, hist1, hist2, pipe = None):#will compare to hist without running nbody simulation.
        print("matching histograms: ")
        command = " " + self.path + "nbody_test/bin/milkyway_nbody" + self.version \
                + " -h " + hist2 + '.hist' \
                + " -S " + hist1 + '.hist'
        
        #using call here instead so the format of using it is on record
        if(pipe):#produces the comparison to stdout
            call([command + " 2>>" + pipe ], shell=True)
            
        else:#will pipe the result of the comparison to a file
            call([command], shell=True)
        
        print hist1, "\n", hist2
        print "\n"
        return 0
    
class nbody_outputs:#a class that takes in data from nbody output files and makes them available
    def __init__(self, file_name):
        self.file_name = file_name
        self.get_data()
        
    def get_data(self):# read in output file
        self.xs = []; self.ys = []; self.zs = []
        self.ls = []; self.bs = []; self.rs = []
        self.vxs = []; self.vys = []; self.vzs = []
        self.vls = []; self.ms = []; self.tps = []
        self.vs = []
        self.gc_rs = []
        f = open(self.file_name, 'r')
        read_data = False
        
        for line in f:
            if (line.startswith("# ignore")):
                read_data = True
                continue
            if(line.startswith("</bodies>")):
                break
            if(read_data):
                ss = line.split(', ')
                ty = int(ss[0])
                x = float(ss[2])
                y = float(ss[3])
                z = float(ss[4])
                gc_r = mt.sqrt(x**2 + y**2 + z**2)
                l = float(ss[5])
                b = float(ss[6])
                r = float(ss[7])
                
                vx = float(ss[8])
                vy = float(ss[9])
                vz = float(ss[10])
                v  = mt.sqrt(vx**2 + vy**2 + vz**2)
                
                m  = float(ss[11])
                vl = float(ss[12])
                self.xs.append(x); self.ys.append(y); self.zs.append(z)
                self.ls.append(l); self.bs.append(b); self.rs.append(r)
                self.vxs.append(vx); self.vys.append(vy); self.vzs.append(vz)
                self.tps.append(ty); self.ms.append(m); self.vls.append(vl)
                self.vs.append(v)
                self.gc_rs.append(gc_r)
            
        f.close()
        
    def dark_light_split(self):#splits the data between baryonic and dark matter
        self.light_x , self.light_y , self.light_z    = ([] for i in range(3))
        self.light_l , self.light_b , self.light_r    = ([] for i in range(3))
        self.light_vx , self.light_vy , self.light_vz = ([] for i in range(3))
        self.light_vl, self.light_m                   = ([] for i in range(2))
        self.light_vs = []
        self.light_gc_rs = []
        
        self.dark_x , self.dark_y , self.dark_z       = ([] for i in range(3))
        self.dark_l , self.dark_b , self.dark_r       = ([] for i in range(3))
        self.dark_vx , self.dark_vy , self.dark_vz    = ([] for i in range(3))
        self.dark_vl, self.dark_m                     = ([] for i in range(2))
        self.dark_vs = []
        self.dark_gc_rs = []
        for i in range(0, len(self.xs)):
            if(self.tps[i] == 0):
                self.light_x.append(self.xs[i])
                self.light_y.append(self.ys[i])
                self.light_z.append(self.zs[i])
                
                self.light_l.append(self.ls[i])
                self.light_b.append(self.bs[i])
                self.light_r.append(self.rs[i])
                
                self.light_vx.append(self.vxs[i])
                self.light_vy.append(self.vys[i])
                self.light_vz.append(self.vzs[i])
                
                self.light_vl.append(self.vls[i])
                self.light_m.append(self.ms[i])
                self.light_gc_rs.append(self.gc_rs[i])
                self.light_vs.append(self.vs[i])
                
            if(self.tps[i] == 1):
                self.dark_x.append(self.xs[i])
                self.dark_y.append(self.ys[i])
                self.dark_z.append(self.zs[i])
                
                self.dark_l.append(self.ls[i])
                self.dark_b.append(self.bs[i])
                self.dark_r.append(self.rs[i])
                
                self.dark_vx.append(self.vxs[i])
                self.dark_vy.append(self.vys[i])
                self.dark_vz.append(self.vzs[i])
                
                self.dark_vl.append(self.vls[i])
                self.dark_m.append(self.ms[i])    
                self.dark_gc_rs.append(self.gc_rs[i])
                self.dark_vs.append(self.vs[i])
                
    def rescale_l(self):#to change l range from [0:360] to [-180:180]
        for i in range(0, len(self.ls)):
            if(self.ls[i] > 180.0):
                self.ls[i] = self.ls[i] - 360.0
    
    def convert_lambda_beta(self, split):#to convert l,b to lambda, beta
        if(split):#if the data was split between light and dark
            self.light_lambdas = []; self.light_betas = []
            self.dark_lambdas  = []; self.dark_betas = []
        else:
            self.betas   = []
            self.lambdas = []
        
        for i in range(0, len(self.ls)):
            lmbda_tmp, beta_tmp = convert_to_Lambda_Beta(self.ls[i], self.bs[i], self.rs[i], False)
            if(split):
                if(self.tps[i] == 0):
                    self.light_lambdas.append(lmbda_tmp)
                    self.light_betas.append(beta_tmp)
                    
                if(self.tps[i] == 1):
                    self.dark_lambdas.append(lmbda_tmp)
                    self.dark_betas.append(beta_tmp)
            else:
                self.lambdas.append(lmbda_tmp)
                self.betas.append(beta_tmp)
            
    def binner_vlos(self, angle_cuttoffs):#bins the line of sight vel between angular cuttoffs
        self.binned_vlos = []
        self.which_bin   = []
        
        bin_size = abs(angle_cuttoffs[0] - angle_cuttoffs[1]) / angle_cuttoffs[2]
        mid_bins = []
        which_lambda = []
        which_beta = []
        #setting up the mid bin coordinates
        for i in range(0, angle_cuttoffs[2]):
            mid_bin = angle_cuttoffs[0] + i * bin_size + bin_size / 2.0
            mid_bins.append(mid_bin)
            
        #transform to lambda beta coordinates from lbr
        self.convert_lambda_beta(True)
        
        for i in range(0, len(self.lambdas)):#go through the different lambda coordinates
            if(self.betas[i] >= angle_cuttoffs[3] and self.betas[i] <= angle_cuttoffs[4]):#if it is between the beta cuttoffs
                for j in range(0, len(mid_bins)):#go through the bin coordinates
                    left_edge  = mid_bins[j] - bin_size / 2.0 #edges of the bin
                    right_edge = mid_bins[j] + bin_size / 2.0 #edges of the bin
                    
                    if(self.lambdas[i] >= left_edge and self.lambdas[i] <= right_edge):#check if the lambda coor falls in the bin
                        self.which_bin.append(mid_bins[j])#which mid bin it should be 
                        self.binned_vlos.append(self.vls[i])#the line of sight vel
                        
                        which_lambda.append(self.lambdas[i])#the coordinate that was put there
                        which_beta.append(self.betas[i])
                        break 
                    
    def binner(self, angle_cuttoffs):#bins the line of sight vel between angular cuttoffs
        self.binned_bm = [] #baryonic matter
        self.which_bin_bm   = [] #baryonic matter bin centers
        
        self.binned_dm = [] #dark matter
        self.which_bin_dm = []   # dm bin centers
        
        total_bm = 0
        total_dm = 0
        
        lambda_lower = angle_cuttoffs[0]
        lambda_upper = angle_cuttoffs[1]
        lambda_N     = angle_cuttoffs[2]
        beta_lower   = angle_cuttoffs[3]
        beta_upper   = angle_cuttoffs[4]
        beta_N       = angle_cuttoffs[5]
        
        bin_size = abs(lambda_lower - lambda_upper) / lambda_N
        self.mid_bins = []

        #setting up the mid bin coordinates
        for i in range(0, lambda_N):
            self.binned_dm.append(0)
            self.binned_bm.append(0)
            mid_bin = lambda_lower + i * bin_size + bin_size / 2.0
            self.mid_bins.append(mid_bin)
            
        # transform to lambda beta coordinates from lbr
        self.dark_light_split()
        self.convert_lambda_beta(True)
        for i in range(len(self.light_lambdas)):#go through the different lambda coordinates
            if(self.light_betas[i] >= beta_lower and self.light_betas[i] <= beta_upper):#if it is between the beta cuttoffs
                for j in range(0, len(self.mid_bins)):#go through the bin coordinates
                    left_edge  = self.mid_bins[j] - bin_size / 2.0 #edges of the bin
                    right_edge = self.mid_bins[j] + bin_size / 2.0 #edges of the bin
                    
                    if(self.light_lambdas[i] >= left_edge and self.light_lambdas[i] <= right_edge):#check if the lambda coor falls in the bin
                        self.which_bin_bm.append(self.mid_bins[j])#which mid bin it should be 
                        self.binned_bm[j] += 1#the line of sight vel
                        total_bm += 1.0
                        break 
                    
        for i in range(len(self.dark_lambdas)):#go through the different lambda coordinates
            if(self.dark_betas[i] >= beta_lower and self.dark_betas[i] <= beta_upper):#if it is between the beta cuttoffs
                for j in range(0, len(self.mid_bins)):#go through the bin coordinates
                    left_edge  = self.mid_bins[j] - bin_size / 2.0 #edges of the bin
                    right_edge = self.mid_bins[j] + bin_size / 2.0 #edges of the bin
                    
                    if(self.dark_lambdas[i] >= left_edge and self.dark_lambdas[i] <= right_edge):#check if the lambda coor falls in the bin
                        self.which_bin_dm.append(self.mid_bins[j])#which mid bin it should be 
                        self.binned_dm[j] += 1 #the line of sight vel
                        total_dm += 1.0
                        break
                    
        self.bm_normed = []
        self.dm_normed = []
        print('baryons included: ', total_bm, 'DM included: ', total_dm)
        for i in range(0, lambda_N):
            self.bm_normed.append(self.binned_bm[i] / total_bm)
            self.dm_normed.append(self.binned_dm[i] / total_dm)
                    
    def cross_selection(self, split, selection_size):
        if(split):#if the data was split between light and dark
            self.sub_light_lambdas = []; self.sub_light_betas = []
            self.sub_dark_lambdas  = []; self.sub_dark_betas = []
            pop_size = len(self.dark_lambdas)
        else:
            self.sub_betas   = []
            self.sub_lambdas = []
            pop_size = len(self.lambdas)
    
    
        counter = 0
        while(counter < selection_size):
            if(split):
                i_d = int(round(random.uniform(0.0, selection_size)))
                i_b = int(round(random.uniform(0.0, selection_size)))
                
                self.sub_light_lambdas.append(self.light_lambdas[i_b])
                self.sub_light_betas.append(self.light_betas[i_b])
                
                self.sub_dark_lambdas.append(self.dark_lambdas[i_d])
                self.sub_dark_betas.append(self.dark_betas[i_d])
                
            else:
                i = int(round(random.uniform(0.0, selection_size)))
                self.sub_lambdas.append(self.lambdas[i])
                self.sub_betas.append(self.betas[i])
            counter += 1
            
            
class nbody_histograms:#a class that takes in data from nbody histogram files and makes them available
    def __init__(self, file_name):
        self.file_name = file_name
        self.get_data()
        
    def get_data(self):#read in the histogram
        #self.ft = []; self.bt = []; self.perc = []
        self.lbins = []; self.counts = []; self.count_err = []; self.bd = []; self.bd_error = []; self.vd = []; self.vd_error = []
        read_data = False
        bt_found = False
        ft_found = False
        
        lines = open(self.file_name, 'r')
        for line in lines:
            if(line.startswith("# Evolve backward time = ")):
                bt_found = True
                bt = line.split('# Evolve backward time = ')
                bt = bt[1].split('\n') 
                bt = float(bt[0])
                self.bt = bt
                
            if(line.startswith("# Evolve forward time = ")):
                ft_found = True
                ft = line.split('# Evolve forward time = ')
                ft = ft[1].split('\n') 
                ft = float(ft[0])
                self.ft = ft
                
            if(bt_found and ft_found):
                percent = self.ft / self.bt
                self.perc = percent 
                bt_found = False
                ft_found = False
                
                
            if (line.startswith("betaBins")):
                read_data = True
                continue
            if(line.startswith("</histogram>")):
                break
            
            if(read_data):
                if(line.startswith("\n")):
                    continue
                else:
                    ss = line.split(' ')
                    self.lbins.append(    float(ss[1]))
                    self.counts.append(   float(ss[3]))
                    self.count_err.append(float(ss[4]))
                    self.bd.append(       float(ss[5]))
                    self.bd_error.append( float(ss[6]))
                    self.vd.append(       float(ss[7]))
                    self.vd_error.append( float(ss[8]))
                    
        lines.close()
    
    
    
def convert_to_Lambda_Beta(x1, x2, x3, cartesian):#can convert l,b or x,y,z to lambda beta
    # note: this uses a left handed coordinate system #
    # it assumes that xyz are lefted handed. l,b are  #
    # assumed to be right handed. stupid              #
    left_handed = False                                #
    # this is the system that is used in MW@home.     #

    phi   = mt.radians(128.79)
    theta = mt.radians(54.39)
    psi   = mt.radians(90.70)
    
    if(cartesian):
        x_coor = x1
        y_coor = x2
        z_coor = x3
        if(left_handed):
            x_coor += 8.0 #convert to solar centric
        else:
            x_coor -= 8.0 
    else:
        l = mt.radians(x1)
        b = mt.radians(x2)
        
        x_coor = mt.cos(l) * mt.cos(b) #this is solar centered x
        y_coor = mt.sin(l) * mt.cos(b) #also, the r doesn't really matter. It cancels
        z_coor = mt.sin(b)
    
    #A = MB
    B = [x_coor, y_coor, z_coor]
    
    M_row1 = [mt.cos(psi) * mt.cos(phi) - mt.cos(theta) * mt.sin(phi) * mt.sin(psi),
            mt.cos(psi) * mt.sin(phi) + mt.cos(theta) * mt.cos(phi) * mt.sin(psi),
            mt.sin(psi) * mt.sin(theta)]
    
    M_row2 = [-mt.sin(psi) * mt.cos(phi) - mt.cos(theta) * mt.sin(phi) * mt.cos(psi),
            -mt.sin(psi) * mt.sin(phi) + mt.cos(theta) * mt.cos(phi) * mt.cos(psi),
            mt.cos(psi) * mt.sin(theta)]
    
    M_row3 = [mt.sin(theta) * mt.sin(phi), 
            -mt.sin(theta) * mt.cos(phi),
            mt.cos(theta)]
    
    A1 = M_row1[0] * B[0] + M_row1[1] * B[1] + M_row1[2] * B[2]
    A2 = M_row2[0] * B[0] + M_row2[1] * B[1] + M_row2[2] * B[2]
    A3 = M_row3[0] * B[0] + M_row3[1] * B[1] + M_row3[2] * B[2]
    
    if(left_handed):
        A3 = -A3

    beta = mt.asin(A3 / mt.sqrt(A1 * A1 + A2 * A2 + A3 * A3))
    lamb = mt.atan2(A2, A1)
    
    beta = mt.degrees(beta)
    lamb = mt.degrees(lamb)
    
    return lamb, beta


class sweep_data:
    class sweep_val:
        def __init__(self, parameter_val, likelihood, parameter_val2 = None):
            self.val = parameter_val
            self.lik = likelihood
            if(parameter_val2):
                self.val2 = parameter_val2
            
    def __init__(self, folder, sweep_name, sweep_parameter, dim):
        self.folder = folder
        self.sweep_name = sweep_name
        self.sweep_parameter = sweep_parameter
        self.dim = dim
        self.values = []

        self.parse()
        self.sort()
        
    def parse(self):
        location = self.folder + self.sweep_name + '/' + self.sweep_name
        likelihood_file = open(location + '/' + self.sweep_parameter + '' + '.txt', 'r')
        data_file = open(location + '/' + self.sweep_parameter + '_vals' + '.txt', 'r')
        parameter_vals = []
        if(self.dim == 2):
            parameter_vals2 = []
        likes = []
        counter_l = 0
        counter_g = 0
        
        for line in likelihood_file:
            if (line.startswith("<search_likelihood")):
                ss = line.split('<search_likelihood>')#splits the line between the two sides the delimiter
                ss = ss[1].split('</search_likelihood>')#chooses the second of the split parts and resplits
                ss = ss[0].split('\n') 
                likes.append(float(ss[0]))
                counter_l += 1
                
        for line in data_file:
            if(self.dim == 1):
                l = float(line)
                parameter_vals.append(l)
            else:
                l = line.split('\t')
                parameter_vals.append(float(l[0]))
                parameter_vals2.append(float(l[1]))
            counter_g +=1
            
        if(counter_l != counter_g):
            print( counter_l, counter_g)
            print( 'WARNING: likelihood_data and parameter_val data length mismatch')
        else:
            self.dataN = counter_l
            
        likelihood_file.close()
        data_file.close()
        
        for i in range(0, len(likes)):
            if(self.dim == 1):
                p = self.sweep_val(parameter_vals[i], likes[i])
            else:
                p = self.sweep_val(parameter_vals[i], likes[i], parameter_vals2[i])
            
            self.values.append(p)
        
        del parameter_vals, likes
        
        if(self.dim > 1):
            del parameter_vals2
    
        return 0
    
    def sort(self): # sorts the data from least to greatest in terms of the first parameter
        val_new = []
        val_tmp = []
        
        unsorted = True
        
        while(unsorted):
            for i in range(0, self.dataN - 1):
                if(self.values[i].val > self.values[i + 1].val):
                    val_tmp  = self.values[i]
                    val_tmp2 = self.values[i + 1]
                    self.values[i] = val_tmp2
                    self.values[i + 1] = val_tmp
                    
            unsorted = False
            for i in range(0, self.dataN - 1):
                diff = self.values[i + 1].val - self.values[i].val
                if(diff >= 0):
                    continue
                else:
                    
                    unsorted = True
        return 0
    
    def plottable_list(self, correct_value = None):
        self.vals = []
        self.liks = []
        self.corr = []
        self.cor2 = []
        if(self.dim > 1):
            self.vals2 = []
            
        for i in range(0, self.dataN):
            self.vals.append(self.values[i].val)
            self.liks.append(self.values[i].lik)
            
            if(correct_value):
                self.corr.append(correct_value)
                self.cor2.append(-10.0 * i)
            if(self.dim > 1):
                self.vals2.append(self.values[i].val2)
      
      
class binner:
    def __init__(self, bin_ranges, bin_N, vals_to_bin):
        self.lower_range = bin_ranges[0]
        self.upper_range = bin_ranges[1]
        self.binN = bin_N
        self.vals = vals_to_bin
        self.counts = []
        self.bin_centers = []
        self.bin_vals()
        
    def bin_vals(self):
        self.bin_width = abs(self.upper_range - self.lower_range) / float(self.binN)
        loc = self.lower_range + self.bin_width / 2.0
        for i in range(self.binN):
            self.counts.append(0)
            self.bin_centers.append(loc)
            loc += self.bin_width
        
        for i in range(len(self.vals)):
            for j in range(self.binN):
                left_edge  = self.bin_centers[j] - self.bin_width / 2.0
                right_edge = self.bin_centers[j] + self.bin_width / 2.0
                
                if(self.vals[i] >= left_edge and self.vals[i] <= right_edge):
                    self.counts[j] += 1
                    break
                