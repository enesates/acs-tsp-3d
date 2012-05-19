#-*- coding: utf-8 -*-
# The solution of Traveling Salesperson Problem by using Ant Colony System algorithm and its 3d simulation with OpenGL
# https://github.com/nsates/acs-tsp-3d
# Enes Ateş <enes@enesates.com>
# http://www.enesates.com

import math
from Ant import *


class City(object):
    def __init__(self, x, y, cityId):
        self.id = cityId
        self.coordinate = [x,y]
        
        
def createCities(numberOfCities):
    cities.append(City(100,260,0))
    cities.append(City(150,100,1))
    cities.append(City(200,120,2))
    cities.append(City(30,200,3))
    cities.append(City(225,123,4))
    cities.append(City(250,250,5))
    cities.append(City(124,90,6))
    cities.append(City(50,221,7))
    cities.append(City(152,152,8))
    cities.append(City(80,80,9))

# nearest neighbor for initialization pheromone
def nearestNeighbor(cities):
    
    path = []
    remove = 0
    tourLength = 0
    
    startingCity = cities[len(cities)-1]
    path.append(startingCity)
    cities.remove(startingCity)
    print "ates"
    
    
    while len(cities) > 0:
        minDistance = math.sqrt((startingCity.coordinate[0] - cities[0].coordinate[0])**2.0 +
                                  (startingCity.coordinate[1] - cities[0].coordinate[1])**2.0)
        remove = 0
        for i in range(1,len(cities)):
            distance = math.sqrt((startingCity.coordinate[0] - cities[i].coordinate[0])**2.0 +
                                  (startingCity.coordinate[1] - cities[i].coordinate[1])**2.0)
            if distance!=0  and  distance < minDistance:
                minDistance = distance
                nextCity = cities[i]
                remove = i
        startingCity = nextCity        
        cities.pop(remove)
        path.append(nextCity)
        tourLength += minDistance
            
    path.append(path[0])
    
    return tourLength

      

def initializePheromone(cities, pheromoneMatrix):
    # Tau0 = (n · Lmn )^-1
    nearestNeighborLength = nearestNeighbor(list(cities))
    
    for i in range(0,len(cities)):
        pheromoneMatrix.append([])
        for j in range(0, len(cities)):
            if i == j:
                pheromoneMatrix[i].append(0)
            else:    
                pheromoneMatrix[i].append(1/(len(cities) * nearestNeighborLength))
                

def tourConstruct(ant, cities, beta):
    return 0 
    

def systemStart(iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, ro, x):
    
    initializePheromone(cities, pheromoneMatrix)
    
    for i in range (0,iteration):
       for j in range(0,numberOfAnts):
           tourConstruct(ants[j], cities, beta)
           localPheromoneUpdate()
           globalPheromoneUpdate()
            

if __name__ == "__main__":
    
    iteration = 100
    cities = []
    ants = []
    pheromoneMatrix = []
    numberOfCities = 10
    numberOfAnts = 10
    
    beta = 2 # heuristic parameter
    q0 = 0.8 # control parameter for random proportional
    
    ro = 0.1 # evaporation coefficient
    x = 0.1 # local_pheromone
    
    createCities(numberOfCities)
    
    # create Ants
    for i in range(0,numberOfAnts):
        ants.append(Ant(i))
    
    systemStart(iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, ro, x)
   
    