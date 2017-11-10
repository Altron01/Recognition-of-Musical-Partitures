#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 14:1  

@author: altron01
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2
import os
import time

def eraseLines(img, vec, count):
    size = img.shape
    for j in range(vec.__len__()):
        if count >= vec[j]:
            for i in range(size[0]):
                img[i][j] = 255
    pass

def averageCleaner(img):
    size = img.shape
    #Black points per column
    vec = [0]*size[1]
    #Black points in all img
    nPoints = 0
    #Read by column
    for j in range(size[1]):
        for i in range(size[0]):
            if img[i][j] == 0:
                vec[j] += 1
        nPoints += vec[j]
    #0.85 custom treshold that reduce error produced by notes black points
    #average of black point per column
    average = int(0.85*(nPoints/size[1]))
    eraseLines(img, vec, average)
    pass

def minValueCleaner(img):
    size = img.shape
    nPoints = size[0]
    vec = [0] * size[1]
    for j in range(size[1]):
        for i in range(size[0]):
            if img[i][j] == 0:
                vec[j] += 1
        if(0 < vec[j] < nPoints):
            nPoints = vec[j]
    #1.1 custom threshold that reduce error produced by overbinarized columns
    nPoints = round(nPoints*1.1)
    eraseLines(img, vec, nPoints)
    pass

def probabilityCleaner(img):
    size = img.shape
    vecColumn = [0] * (size[0] + 1)
    vec = [0] * size[1]
    for j in range(size[1]):
        nPoints = 0
        for i in range(size[0]):
            if img[i][j] == 0:
                nPoints += 1
        vecColumn[nPoints] += 1
        vec[j] = nPoints
    index = 0
    for i in range(1, size[0]):
        if vecColumn[index] < vecColumn[i]:
            index = i
    eraseLines(img, vec, index)
    pass

def binarize(img):
    size = img.shape
    for i in range(size[0]):
        for j in range(size[1]):
            img[i][j] = (255 if img[i][j] > 200 else 0)
    pass

def separate(img):
    size = img.shape
    #Setting min values to max posicion possible + 1 to ensure value change
    mini = [size[0] * 2, size[1] * 2]
    #Setting max values to min posicion possible - 1 to ensure value change
    maxi = [-1, -1]
    vec = []
    #Flag found note
    flag_s = False
    #Read by column
    for j in range(size[1]):
        #Flag found point on column
        flag_f = False
        for i in range(size[0]):
            #If black point is found
            if img[i][j] == 0:
                #Note and black point found
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
        #If note found but no point in column
        if(flag_s and not flag_f ):
            #The note have ended
            flag_s = False
            vec.append((mini, maxi))
            #Show image
            #plt.imshow(img[mini[0]: maxi[0], mini[1]: maxi[1]])
            #plt.show()
            #Re-initialize image
            mini = [size[0] * 2, size[1] * 2]
            maxi = [-1, -1]
    return vec
    pass

#dataSetDir, dataSetSeparatedDir, imgName
def prec(dataSetDir, dataSetSeparatedDir, imgName):
    #Leer raw image en folder
    img = cv2.imread(dataSetDir + "/" + imgName + ".png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    container = np.copy(img)
    
    #Clean image from noise and stuff
    binarize(container)
    
    #Cleaner Algorithm here
    stime = time.time()
    #averageCleaner(container)#13
    #minValueCleaner(container)#13
    probabilityCleaner(container)#0
    print("Time", time.time() - stime)
    
    #vector of images positions and sizes
    vec = separate(container)
    container = cv2.cvtColor(container, cv2.COLOR_GRAY2RGB)
    #Create individual image folder
    if not os.path.exists(dataSetSeparatedDir + "/" + imgName):
        os.makedirs(dataSetSeparatedDir + "/" + imgName)
    #For each note separated write it on image folder
    for i in range(vec.__len__()):
        imgSlice = container[vec[i][0][0]:vec[i][1][0],vec[i][0][1]:vec[i][1][1]]
        #if not (imgSlice.shape[0] == 0 or imgSlice.shape[1] == 0):
        #cv2.imwrite(dataSetSeparatedDir + "/" + imgName + "/" + imgName + "_" + str(i) + ".png", imgSlice)
        cv2.imwrite(dataSetSeparatedDir + "/" + imgName + "/" + imgName + "_" + str(i) + ".png", imgSlice)
    pass

#Name of folder with raw images
dataSetDir = "DataSet"
#Name of folder with processed images
dataSetSeparatedDir = dataSetDir + "Separated"
#Create processed images folder
if not os.path.exists(dataSetSeparatedDir):
    os.makedirs(dataSetSeparatedDir)
#Raw image amount
size = os.listdir(dataSetDir).__len__()
for i in range(size - 1):
    #Name of image
    imName = "full_chord" + str(i)
    prec(dataSetDir, dataSetSeparatedDir, imName)