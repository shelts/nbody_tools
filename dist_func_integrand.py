#! /usr/bin/python
#/* Copyright (c) 2018 Siddhartha Shelton */
import random
import math as mt
import matplotlib.pyplot as plt
random.seed(a = 687651463)



class model:
    def __init__(self, rscale, mass):
        self.rs = rscale
        self.m = mass
        
    def density(self, r):
        coeff = (3.0 * self.m) / (4.0 * mt.pi * self.rs**3.0)
        quot = ((r * r) / (self.rs * self.rs))
        
        den = coeff * r * r * (1.0 + quot)**(-5.0 / 2.0)
        return den
    
    def potential(self, r):
        pot = self.m / mt.sqrt( r * r + self.rs * self.rs) #returns negative of potential, psi
        return pot
        
class dist_func:
    def __init__(self, rscale1, mass1, rscale2, mass2, vfrac, r):
        self.light = model(rscale1, mass1)
        self.dark  = model(rscale2, mass2)
        
        esc_v = mt.sqrt( 2.0 * (self.light.potential(r) + self.dark.potential(r))  )
        v = vfrac * esc_v
        self.energy = - 0.5 * v * v + (self.light.potential(r) + self.dark.potential(r)) 
        
        def first_derivative(self, r, light, dark):
            h = 0.001
            
            p1 =   1.0 * light(r - 2.0 * h) + dark( r - 2.0 * h)
            p2 = - 8.0 * light(r - h)       + dark(r - h)  
            p3 = - 1.0 * light(r + 2.0 * h) + dark(r + 2.0 * h)
            p4 =   8.0 * light(r + h)       + dark(r + h) 

            deriv = (p1 + p2 + p3 + p4) / (12.0 * h)
            
            return deriv
        
        def second_derivative(self, r, light, dark)
            real h = 0.001

            p1 = - 1.0 * light(x + 2.0 * h) + dark(x + 2.0 * h)
            p2 =  16.0 * light(x + h)       + dark(x + h)
            p3 = -30.0 * light(x)           + dark(x) 
            p4 =  16.0 * light(x - h)       + dark(x - h)
            p5 = - 1.0 * light(x - 2.0 * h) + dark(x - 2.0 * h)
            deriv = (p1 + p2 + p3 + p4 + p5) / (12.0 * h * h);
            
            return deriv;
        
        
        def integrand(self, r):
            first_deriv_psi      = self.first_derivative(r, self.light.potential, self.darkpotential);
            first_deriv_density  = self.first_derivative(r, self.light.density, self.dark.density);

            second_deriv_psi     = self.second_derivative(r, self.light.potential, self.dark.potential);
            second_deriv_density = self.second_derivative(r, self.light.density, self.dark.density);
    
            if(first_deriv_psi == 0.0):
                first_deriv_psi = 1.0e-6
                
            dsqden_dpsisq = second_deriv_density / (first_deriv_psi) - first_deriv_density * second_deriv_psi / (first_deriv_psi)**2.0
            
            
            diff = abs(self.energy - (self.light.potential(r) + self.dark.potential(r)) )
    
            if(diff == 0.0):
                diff = abs(self.energy - ( light.potential(r + 0.0001) + dark.potential(r + 0.0001)) )
            
            denominator = 1.0 / mt.sqrt( diff );
            
            func = dsqden_dpsisq * denominator; 
    
            return func
        
        

class chosen_rs:
    class integral_values:
       def __init__(self, vf)
            self.body_vf = vf
            self.integral_rs = []
            self.integral_vals = []
            
            int_r = 0.01
            func = dist_func(self.rsl, self.ml, self.rsd, self.md, vf, self.body_r )
            for i in range(1000):
                self.integral_rs.append(int_r)
                temp = func.integrand(int_r)
                self.integral_vals.append(temp)
                int_r += 0.05
                
            
    def __init__(self, body_r, rsl, rsd, ml, md):
        self.body_r
        self.vfs = []
        self.rsl = rsl; self.rsd = rsd; self.ml = ml; self.md = md
    
    def integrand(self, vf):
        values = integral_values(vf)
        self.vfs.append(values)


def main():
    rsl = 0.2
    rsd = 0.8
    ml = 12.
    md = 48.
    
    chosen_r = [0.1, 0.25, 0.5, 0.75]
    chosen_vfrac = [0.25, 0.5, 0.75, 0.9]#fraction of the escape speed
    
    vals = []
    for i in range(0, len(chosen_r)):
        r = chosen_r[i] * (rsl + rsd)
        temp_vals = chosen_rs(r, rsl, rsd, ml, md )
        
        for j in range(0, len(chosen_vfrac)):
            vf = chosen_vfrac[j]
            temps_vals.integrand(vf)
            
        vals.append(temp_vals)
    
main()
            
            
        
        