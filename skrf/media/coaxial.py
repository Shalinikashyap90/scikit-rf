# -*- coding: utf-8 -*-
#       coaxial.py
##
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later versionpy.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

'''
.. module:: skrf.media.coaxial
============================================================
coaxial (:mod:`skrf.media.coaxial`)
============================================================

A coaxial transmission line defined in terms of its inner/outer diameters and permittivity
'''

#from copy import deepcopy
from scipy.constants import  epsilon_0, mu_0, pi
from numpy import sqrt, log

from distributedCircuit import DistributedCircuit

# used as substitutes to handle mathematical singularities.
INF = 1e99

class Coaxial(DistributedCircuit):
    '''
    '''
    ## CONSTRUCTOR
    def __init__(self, frequency,  Dint, Dout, epsilon_r=1, tan_delta=0, sigma=INF, *args, **kwargs):
        '''
        coaxial transmission line constructor.
        
        Parameters
        ----------
        frequency : :class:`~skrf.frequency.Frequency` object
        Dint : number, or array-like
            inner conductor diameter, in m
        Dout : number, or array-like
            outer conductor diameter, in m
        epsilon_r=1 : number, or array-like
            relative permittivity of the dielectric medium
        tan_delta=0 : numbe, or array-like 
            loss tangent of the dielectric medium    
        sigma=infinity : number, or array-like
            conductors electrical conductivity, in S/m

        TODO : different conductivity in case of different conductor kind

        Notes
        ----------
        Dint, Dout, epsilon_r, tan_delta, sigma can all be vectors as long as they are the same
        length
        
        References
        ---------
        .. [#] Pozar, D.M.; , "Microwave Engineering", Wiley India Pvt. Limited, 1 sept. 2009  



        '''
                
        freq = frequency.copy()
        self.Dint, self.Dout = Dint,Dout 
        self.epsilon_r, self.tan_delta, self.sigma = epsilon_r, tan_delta, sigma
        self.epsilon_prime = epsilon_0*self.epsilon_r        
        self.epsilon_second = epsilon_0*self.epsilon_r*self.tan_delta
                
        # surface resistance
        omega = 2.*pi*freq.f
        mu_r=1.
        Rs = sqrt(omega*mu_0*mu_r/(2.*self.sigma))
        
        # inner and outer radius
        a = Dint/2. 
        b = Dout/2.

        # derivation of distributed circuit parameters        
        R = Rs/(2.*pi)*(1./a + 1./b)
        L = mu_0/(2.*pi)*log(b/a) 
        C = 2.*pi*self.epsilon_prime/log(b/a)
        G = 2.*pi*omega*self.epsilon_second/log(b/a)

        DistributedCircuit.__init__(self,\
                freq, C, L, R, G, \
                *args, **kwargs)
        
        
    def __str__(self):
        f=self.frequency
        try:
            output =  \
                'Coaxial Transmission Line.  %i-%i %s.  %i points'%\
                (f.f_scaled[0],f.f_scaled[-1],f.unit, f.npoints) + \
                '\nDint= %.2f mm, Dout= %.2f mm '% \
                (self.Dint*1e3, self.Dout*1e3) +\
                '\nCharacteristic Impedance='+str(self.characteristic_impedance)+' Ohm' \
                '\nPort impedance Z0='+str(self.z0)+' Ohm'  
        except(TypeError):
            output =  \
                'Coaxial Transmission Line.  %i-%i %s.  %i points'%\
                (f.f_scaled[0],f.f_scaled[-1],f.unit, f.npoints) + \
                '\nDint= %.2f mm, Dout= %.2f mm '% \
                (self.Dint[0]*1e3, self.Dout[0]*1e3) +\
                '\nCharacteristic Impedance='+str(self.characteristic_impedance[0])+' Ohm' \
                '\nPort impedance Z0='+str(self.z0[0])+' Ohm'  
        return output
