#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 14:1  

@author: altron01
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 12:35:12 2017

@author: altron01
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import time

def fill(img, size, vec, count):
    for i in range(vec.__len__()):
        if count > vec[i]:
            for j in range(size[0]):
                img[j][i] = 255
    pass

def eraseLine(img, size):
    vec = []
    count = 0
    for j in range(size[1]):
        aux = 0
        for i in range(size[0]):
            if img[i][j] == 0:
                aux += 1
                count += 1
        vec.append(aux)
    count = int(0.85*(count/size[1]))
    fill(img, size, vec, count)
    pass

def eraseLine2(img, size):
    count = size[0]
    vec = []
    for j in range(size[1]):
        aux = 0
        for i in range(size[0]):
            if img[i][j] == 0:
                aux += 1
        vec.append(aux)
        if(aux < count and aux != 0):
            count = aux
    count = round(count*1.1)
    fill(img, size, vec, count)
    pass

def clean(img, size):
    for i in range(size[0]):
        for j in range(size[1]):
            img[i][j] = (255 if img[i][j] > 200 else 0)
    pass

def separate(img, size):
    mini = [size[0] * 2, size[1] * 2]
    maxi = [-size[0] * 2, -size[1] * 2]
    vec = []
    flag_s = False
    for j in range(size[1]):
        flag_f = False
        for i in range(size[0]):
            if img[i][j] == 0:
                flag_s = True
                flag_f = True
                if mini[0] > i:
                    mini[0] = i
                if mini[1] > j:
                    mini[1] = j
                if maxi[0] < i:
                    maxi[0] = i
                if maxi[1] < j:
                    maxi[1] = j
        if(not flag_f and flag_s):
            flag_s = False
            vec.append((mini, maxi))
            plt.imshow(img[mini[0]: maxi[0], mini[1]: maxi[1]])
            plt.show()
            print(mini, maxi)
            mini = [size[0] * 2, size[1] * 2]
            maxi = [-size[0] * 2, -size[1] * 2]
    return vec
    pass

def prec(img, dirName, name):
    container = np.copy(img)
    size = container.shape
    clean(container, size)
    eraseLine2(container, size)
    vec = separate(container, size)
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    os.makedirs(dirName + "/" + name)
    for i in range(vec.__len__()):
        cv2.imwrite(dirName + "/" + name + "/" + name + "_" + str(i) + ".png", container[vec[i][0][0]:vec[i][1][0],vec[i][0][1]:vec[i][1][1]])
    pass
dataSetDir = "DataSet"
dataSetSeparatedDir = dataSetDir + "Separated"
os.makedirs(dataSetSeparatedDir)
size = os.listdir(dataSetDir).__len__()
for i in range(size - 1):    
    imName = "full_chord" + str(i)
    img = cv2.imread(dataSetDir + "/" + imName + ".png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    prec(img, dataSetSeparatedDir, imName)