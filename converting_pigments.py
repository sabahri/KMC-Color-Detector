# References: 
# http://www.brucelindbloom.com/index.html?Eqn_Lab_to_XYZ.html
# http://brucelindbloom.com/index.html?Math.html

import numpy as np
import matplotlib as plt

epsilon = 0.008856
kappa = 903.3

class cielab:
    def __init__(self, L, a, b):
        self.L = L 
        self.a = a 
        self.b = b 
    
    def lab_to_XYZ(L,a,b, Xr,Yr,Zr):
        fy = (L + 16)/116
        fx = a/500 + fy
        fz = fy - b/200

        if fx**3 > epsilon:
            xr = fx**3
        else:
            xr = (116*fx - 16)/116
        
        if L > kappa*epsilon:
            yr = ((L + 16)/116)**3
        else:
            yr = L/kappa
        
        if fz**3 > epsilon:
            zr = fz**3
        else:
            zr = (116*fz - 16)/kappa

        return(xr*Xr,yr*Yr,zr*Zr)

        def XYZ_to_RGB(X,Y,Z):

# CIE L*a*b* values measured by artistpigments.org
prim_blue = cielab(41.30, -9.46, -53.73)
rose_tyr = cielab(37.97, 64.17,-2.28)
lemon_yell = cielab(92.15, -7.04, 89.05)
jet_black = cielab(17.69, 0.26, -0.58)
perm_white = cielab(96.52, -0.14, 3.34)

# Converting to XYZ

