    def calc_derivative_3pointstencil(self, i, j):
        n = len(self.paras)
        if(self.steps):#optimizing step sizes or fix step size
            h1 = self.steps[i]
            h2 = self.steps[j]
        else:
            h1 = 0.001
            h2 = h1
        
        a = self.paras[i]
        b = self.paras[j]
        p = list(self.paras)#copies the list of parameters
        f = open(self.cost.likelihood_file, 'a')
        f.write('working on element ' + str(i) + ',' + str(j) + '\n')
        f.write('starting parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
        
        if(i == j): # straight up second derivative
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f1 = self.cost.get_likelihood(p)
            
            p[i] = a + h1
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f2 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f3 = self.cost.get_likelihood(p)
            
            der = ((f2)) - 2.0 * ((f1)) + ((f3))
            f.write('derivative: %f\n' % (der))
            der = der / (h1 * h1)
            
        else: # second partial derivative
            p[i] = a + h1
            p[j] = b + h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f1 = self.cost.get_likelihood(p)
        
            p[i] = a + h1
            p[j] = b - h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f2 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            p[j] = b + h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f3 = self.cost.get_likelihood(p)
            
            p[i] = a - h1
            p[j] = b - h2
            f.write('derivative parameters:  ' + str(p[0]) + ' ' + str(p[1]) + ' ' + str(p[2]) + ' ' + str(p[3]) + ' ' + str(p[4]) + '\n')
            f4 = self.cost.get_likelihood(p)
            
            der = ((f1)) - ((f2)) - ((f3)) + ((f4))
            f.write('derivative: %f\n' % (der))
            der = der / (4.0 * h1 * h2)
        f.close()
        return der