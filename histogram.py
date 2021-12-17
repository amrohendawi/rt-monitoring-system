# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:37:52 2019

@author: test
"""

import numpy as np
import matplotlib.pyplot as p

data = np.loadtxt('output')
x = data[:,0]
y = data[:,1]
print(data)

p.hist(data)

