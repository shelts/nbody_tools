#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */

class half_light:
    def __init__(self, parameters):
        self.rl_correct = parameters[0]
        self.rr_correct = parameters[1]
        self.ml_correct = parameters[2]
        self.mr_correct = parameters[3]
        
        self.rd_correct = (self.rl_correct / self.rr_correct) * (1.0 - self.rr_correct)
        self.md_correct = (self.ml_correct / self.mr_correct) * (1.0 - self.mr_correct)
        
        self.half_mass_radius()
        self.dm_within_half_light()
        
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
    
    def dm_within_half_light(self):
        self.rrs    = []
        self.mrs    = []
        self.mdencs = []
        
        
        #dark matter mass enclosed within the half light radius
        dark_mass_enclosed_half_light = self.md_correct * self.half_mass_radius**3.0 / (self.half_mass_radius**2. + self.rd_correct**2.)**(3.0 / 2.0)
        print 'Dark matter mass enclosed within the half light radius: ', dark_mass_enclosed_half_light
        print 'In solar: ', dark_mass_enclosed_half_light * 222288.47
        print 'Percent of total DM within half-light: ', 100.* dark_mass_enclosed_half_light / self.md_correct
        
        

def main():
    pars = []
    paras = [0.194475845053315, 0.182490907170191, 12.0318227005393, 0.17381456135166]
    #p1 = half_light(paras)
    pars.append(paras)
    
    
    paras = [0.198924848155757, 0.198154361034153, 12.0120493906343, 0.199910776768096]
    #half_light(paras)
    pars.append(paras)
    
    paras = [0.191816401979042, 0.18889116708923, 11.9368132594319, 0.198743736247361]
    #half_light(paras)
    pars.append(paras)
    
    
    #print pars
    ave_paras = []
    for i in range(len(paras)):
        ave = 0
        for j in range(len(pars)):
            ave += pars[j][i] / float(len(pars))
        ave_paras.append(ave)
        
    print ave_paras
    half_light(ave_paras)
    
    
main()#-5.913089623411990