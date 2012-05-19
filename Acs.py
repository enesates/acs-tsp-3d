# The solution of Traveling Salesperson Problem by using Ant Colony System algorithm and its 3d simulation with OpenGL
# https://github.com/nsates/acs-tsp-3d
# Enes Ates <enes@enesates.com>
# http://www.enesates.com

import math
import random
from Ant import *


class City(object):
    def __init__(self, x, y, cityId):
        self.id = cityId
        self.coordinate = [x,y]
        
        
def createCities(cities):
    file = open("uruguay734_optimal79114.tsp","r")
    
    for i in range(0,734):
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        cities.append(City(float(line[1]), float(line[2]), i))
        

def calculateDistance(start, end):

    return math.sqrt((start.coordinate[0] - end.coordinate[0]) ** 2.0 +
                                  (start.coordinate[1] - end.coordinate[1]) ** 2.0)

def nearestNeighbor(cities):
    # nearest neighbor for initialization pheromone
    path = []
    remove = 0
    tourLength = 0
    
    startingCity = cities[len(cities)-1]
    path.append(startingCity)
    cities.remove(startingCity)    
    
    while len(cities) > 0:
        minDistance = calculateDistance(startingCity, cities[0])
        remove = 0
        for i in range(1,len(cities)):
            
            distance = calculateDistance(startingCity, cities[i])
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
      

def initializePheromone(cities, pheromoneMatrix, tau0):
    # tau0 = (n * Cnn )^-1

    for i in range(0,len(cities)):
        pheromoneMatrix.append([])
        for j in range(0, len(cities)):
            if i == j:
                pheromoneMatrix[i].append(0)
            else:    
                pheromoneMatrix[i].append(tau0)           

def calculateTauEtha(currentCity, cities, beta, tauEtha):
    
    total = 0
    
    for i in range(0,len(cities)):
        try:
            tauEthaVal = pheromoneMatrix[currentCity.id][i] * math.pow(1.0/calculateDistance(currentCity, cities[i]), beta) 
        except ZeroDivisionError:
            tauEthaVal = 0
        tauEtha.append(tauEthaVal)
        total += tauEthaVal
    return total


def findNextCity(currentCity, cities, beta, q0):

    rand = random.random()
    tauEtha = []
    
    totalTauEtha = calculateTauEtha(currentCity, cities, beta, tauEtha)
    
    if rand < q0:
        argmax = max(tauEtha)
        return cities[tauEtha.index(argmax)]
    
    else:
        roulette = 0
        rand = random.uniform(0, totalTauEtha)
        for i in range(0,len(cities)):
            
            roulette += tauEtha[i]
            if rand < roulette:
                return cities[i]
            

def tourConstruction(ant, numberOfCities, cities, beta, q0):
    currentCity = ant.tour[0]
    cities.remove(currentCity)
    
    for i in range(0,numberOfCities-2):
        
        nextCity = findNextCity(currentCity, cities, beta, q0)
        ant.tour.append(nextCity)
        currentCity = nextCity
        cities.remove(nextCity)
        
    ant.tour.append(cities.pop())
    
    for i in range(0, len(ant.tour)-1):
        ant.tourLength += calculateDistance(ant.tour[i], ant.tour[i+1])
        
        
def localPheromoneUpdate(ant, phrMatrix, tau0, ksi):
    
    for i in range(0, len(ant.tour)-1):
        current = ant.tour[i].id
        next = ant.tour[i+1].id
        phrMatrix[current][next] = ((1 - ksi) * phrMatrix[current][next] ) + (ksi * tau0)
        phrMatrix[next][current] = phrMatrix[current][next]
      

def globalPheromoneUpdate(bestTour, bestTourLength, phrMatrix, rho):
    
    for i in range(0, len(bestTour)-1):
        current = bestTour[i].id
        next = bestTour[i+1].id
        phrMatrix[current][next] = ((1 - rho) * phrMatrix[current][next] ) + (rho * (1/bestTourLength))
        phrMatrix[next][current] = phrMatrix[current][next]


def initializeTours(bestTour, ants):
    
    del bestTour[:]
    
    randomCities = range(0,numberOfCities)
    random.shuffle(randomCities)
    
    for i in range(0, len(ants)):
        del ants[i].tour[:]
        ants[i].tourLength = 0
          
        ants[i].tour.append(cities[randomCities[i%10]])


def systemStart(iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, q0, rho, ksi, tau0):
    
    initializePheromone(cities, pheromoneMatrix, tau0)
    
    bestTour = []
    globalBestTour = []
    
    globalBestTourLength = 0
    
    for i in range (0,iteration):
        print "iteration",i
        
        bestTourLength = 0
        
        initializeTours(bestTour, ants)
        
        for j in range(0,numberOfAnts):
                        
            tourConstruction(ants[j], numberOfCities, list(cities), beta, q0)
            #localSearch()
            localPheromoneUpdate(ants[j], pheromoneMatrix, tau0, ksi)
            
            if bestTourLength == 0 or bestTourLength > ants[j].tourLength:
                bestTourLength = ants[j].tourLength
                bestTour = ants[j].tour
        
        if globalBestTourLength == 0 or globalBestTourLength > bestTourLength:
            globalBestTourLength = bestTourLength
            globalBestTour = bestTour
        
        globalPheromoneUpdate(bestTour, bestTourLength, pheromoneMatrix, rho)
        
    for i in globalBestTour:
       print "Best Tour :",i.coordinate
        
    print "Best Tour Length:", globalBestTourLength
    
            

if __name__ == "__main__":
    
    iteration = 100
    cities = []
    ants = []
    pheromoneMatrix = []
    numberOfAnts = 10
    
    beta = 2.5 # heuristic parameter
    q0 = 0.9 # control parameter for random proportional
    
    rho = 0.1 # evaporation coefficient
    ksi = 0.1 # local_pheromone
    
    createCities(cities)
    numberOfCities = len(cities)
    
    tau0 = 1/(len(cities) * nearestNeighbor(list(cities))) # copying cities list and send nn algorithm
    # tau0 = (n * Cnn )^-1
    
    # create Ants
    for i in range(0,numberOfAnts):
        ants.append(Ant(i))
    
    systemStart(iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, q0, rho, ksi, tau0)
   
    