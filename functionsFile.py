import math
import numpy as np;
import functionsFile as fn

def euclideanDist(a,b):
    temp=0
    for i in range(len(a)):
        temp+=((a[i]-b[i])**2)
    return math.sqrt(temp)

def findClosest(i, array):
    if i==len(array)-1:
        print('Error in closest')
        return (0,i)
    closest=euclideanDist(array[i],array[i+1])
    closestind=i+1
    for j in (i+1,len(array)-1):
        if euclideanDist(array[i],array[j])<closest:
            closest=euclideanDist(array[i],array[j])
            closestind=j
            
    return  (closest,closestind)

