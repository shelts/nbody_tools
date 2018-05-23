#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */

class make_latex_table:
    def __init__(self, data_files, write_file, search_range):
        self.data_files = data_files
        self.write_file = write_file
        self.search_range = search_range
        self.ls = []; self.ft = []; self.rl = []; self.rr = []; self.ml = []; self.mr = []
            
       
        for i in range(len(data_files)):
            self.read_data(i)
        self.write_table()
        self.write_stellar_table()
    def read_data(self, i):
        likes = []; fts = []; rls = []; rrs = []; mls = []; mrs = []
    
        f = open(self.data_files[i], 'r')
        read_data = False

        for line in f:
            if (line.startswith("The best")):
                read_data = True
                continue
            if(read_data):
                line = line.replace('[', '')
                line = line.replace(']', '')
                line = line.replace('\t', '')
                line = line.replace('\n', '')
                ss = line.split(',')
                
                
                lk = (float(ss[1]))
                ft = (float(ss[2]))
                rl = (float(ss[4]))
                rr = (float(ss[5]))
                ml = (float(ss[6]))
                mr = (float(ss[7]))
                
        self.ls.append(lk)
        self.ft.append(ft)
        self.rl.append(rl)
        self.rr.append(rr)
        self.ml.append(ml)
        self.mr.append(mr)
        f.close()
            
            
    def write_table(self):
        f = open(self.write_file, 'w')
        
        f.write("\\begin{center}\n\\begin{table}[!ht]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n")
        f.write("Parameters& Evolve Time & $R_B$ & Radius Ratio ($\\frac{R_B}{R_B + R_D}$) & $M_B$ & Mass Ratio ($\\frac{M_B}{M_B + M_D}$)\\\\\n")
        f.write("\\hline \\hline\n")
        f.write("Search Range\t& " + self.search_range[0] + " & " + self.search_range[1] + " & " + self.search_range[2] + " & " + self.search_range[3] + " & " + self.search_range[4] + " \\\\\n")
        f.write("\\hline\n")
        for i in range(len(self.data_files)):
            f.write("Histogram 1 & " + str(round(self.ft[i], 4)) + " & " + str(round(self.rl[i], 4)) + " & " + str(round(self.rr[i], 4)) + " & " + str(round(self.ml[i], 4)) + " & " + str(round(self.mr[i], 4)) + " \\\\\n")
            f.write("\\hline\n")
        
        f.write("\\end{tabular}\n")
        f.write("\\caption{}\n")
        f.write("\\label{table:}\n")
        f.write("\\end{table}\n\\end{center}\n")
        
        f.close()
        
        
    def write_stellar_table(self):
        f = open(self.write_file, 'a')
        f.write("\n\n\n\n")
        f.write("\\begin{center}\n\\begin{table}[!ht]\n\\centering\n\\begin{tabular}{|c|c|c|c|c|c|}\n\\hline\n")
        f.write("Parameters& Evolve Time (Gy) & $R_B$ (kpc) & $R_D$ (kpc) & $M_B$ ($M_\odot$)& $M_D$ ($M_\odot$)\\\\\n")
        f.write("\\hline \\hline\n")
        for i in range(len(self.data_files)):
            rd = (self.rl[i] / self.rr[i]) * ( 1.0 - self.rr[i])
            md = (self.ml[i] / self.mr[i]) * ( 1.0 - self.mr[i])
            md = md * 222288.47 
            ml = self.ml[i] * 222288.47 
            f.write("Histogram 1 & " + str(round(self.ft[i], 4)) + " & " + str(round(self.rl[i], 4)) + " & " + str(round(rd, 4)) + " & " + str(round(ml, 4)) + " & " + str(round(md, 4)) + " \\\\\n")
            f.write("\\hline\n")
        
        f.write("\\end{tabular}\n")
        f.write("\\caption{}\n")
        f.write("\\label{table:}\n")
        f.write("\\end{table}\n\\end{center}\n")
        
        f.close()
        
        
def main():
    search_range = [ "[3.0 - 6.0]" ,\
                    "[0.1 - 0.5]"  ,\
                    "[0.1 - 0.5]"  ,\
                    "[1.0 - 100.0]",\
                    "[0.01 - 0.95]" \
                        ]
    
    folder = '/home/sidd/Desktop/research/like_surface/run_stats/'
    runs = folder + 'runs_data_3_22_18_pulled_4_18_18/'
    data_files = [runs + 'de_nbody_3_22_2018_v168_20k__data_1',\
                  runs + 'de_nbody_3_22_2018_v168_20k__data_2',\
                  runs + 'de_nbody_3_22_2018_v168_20k__data_3' \
                      ]
    
    write_file = 'latex_table.txt'
    
    make_latex_table(data_files, write_file, search_range)
    
    
main()