# The solution of Traveling Salesperson Problem by using Ant Colony System algorithm and its 3d simulation with OpenGL
# https://github.com/nsates/acs-tsp-3d
# Enes Ates <enes@enesates.com>
# http://www.enesates.com

import math
import random
import time
from Scene import *
from Ant import *


iteration = 100
ants = []
pheromoneMatrix = []
numberOfAnts = 10

beta = 2 # heuristic parameter
q0 = 0.98 # control parameter for random proportional

rho = 0.1 # evaporation coefficient
ksi = 0.1 # local_pheromone

numberOfCities = 0
cities = []



def calculateDistance(start, end):

    return math.sqrt((start.coordinate[0] - end.coordinate[0]) ** 2.0 +
                        (start.coordinate[1] - end.coordinate[1]) ** 2.0 +
                                (start.coordinate[2] - end.coordinate[2]) ** 2.0)
    

def calculateCost(antTour):
    
    antTourLength = 0
    
    for i in range(0, len(antTour)-1):
        antTourLength += calculateDistance(antTour[i], antTour[i+1])
        
    return antTourLength


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
    
    print "Nearest Neighbor tour length:", tourLength
    strToFile = "\n\nNearest Neighbor tour length:" + str(tourLength)

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
    
    ant.tourLength = calculateCost(ant.tour)
        
        
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


def localSearch(antId, antTour, antTourLength):
    
    for i in range(0, len(antTour)-1):
        for j in range(i+1, len(antTour)):
            newAntTour = list(antTour)
            k, l = i, j
            
            while k < l:
                newAntTour[k], newAntTour[l] = newAntTour[l], newAntTour[k] # swap
                
                k += 1
                l -= 1
            
            newAntTourLength = calculateCost(newAntTour)
            
            if newAntTourLength < antTourLength:
                antTourLength = newAntTourLength
                antTour = newAntTour
                
                print antId,". ant's local search tour. Tour length:", antTourLength
                return antTour, antTourLength
    
    return antTour, antTourLength
                


def initializeTours(bestTour, ants):
    
    del bestTour[:]
    randomCities = range(0,numberOfCities)
    random.shuffle(randomCities)
    
    for i in range(0, len(ants)):
        del ants[i].tour[:]
        ants[i].tourLength = 0
          
        ants[i].tour.append(cities[randomCities[i%10]])


def systemStart(scene, iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, q0, rho, ksi, tau0, resultFile):
    
    initializePheromone(cities, pheromoneMatrix, tau0)
    
    bestTour = []
    globalBestTour = []
    
    globalBestTourLength = 0
    
    strToFile = ""
    
    for i in range (0,iteration):
        print "\n\nIteration",i
        strToFile = "\n\nIteration" + str(i)
        resultFile.write(strToFile)
        
        bestTourLength = 0
        
        initializeTours(bestTour, ants)
        
        for j in range(0,numberOfAnts):
                        
            tourConstruction(ants[j], numberOfCities, list(cities), beta, q0)
            #localSearch()
            localPheromoneUpdate(ants[j], pheromoneMatrix, tau0, ksi)
            
            print "\n", j ,". ant's tour. Tour length: ", ants[j].tourLength
            strToFile = "\n" + str(j) + ". ant's tour. Tour length: " + str(ants[j].tourLength)
            resultFile.write(strToFile)
            
            scene.updateTour(ants[j].tour)
            time.sleep(0.5)
            
            if bestTourLength != 0 and bestTourLength < ants[j].tourLength:
                ants[j].tour, ants[j].tourLength = localSearch(ants[j].id, list(ants[j].tour), ants[j].tourLength)
                
            if bestTourLength == 0 or bestTourLength > ants[j].tourLength:
                bestTourLength = ants[j].tourLength
                bestTour = ants[j].tour
                
                print j,". ant's best tour. Tour length:", bestTourLength
                strToFile = str(j) + ". ant's best tour. Tour length: " + str(bestTourLength)
                resultFile.write(strToFile)
                  
        
        if globalBestTourLength == 0 or globalBestTourLength > bestTourLength:
            globalBestTourLength = bestTourLength
            
            print "\nBest tour until now. Tour length: ", globalBestTourLength
            strToFile = "\nBest tour until now. Tour length: " + str(globalBestTourLength)
            resultFile.write(strToFile)
            
            globalBestTour = bestTour
            scene.updateTour(globalBestTour)
            time.sleep(0.5)
        
        globalPheromoneUpdate(bestTour, bestTourLength, pheromoneMatrix, rho)
        
        
    for i in range(0, len(globalBestTour)+1):
       print "\nBest tour", i, ". city coordinate:",globalBestTour[i].coordinate
       strToFile = "\n\nBest tour"+ str(i) + ". city coordinate:" + str(globalBestTour[i].coordinate)
       resultFile.write(strToFile)
        
    print "\nBest Tour Length:", globalBestTourLength
    strToFile = "\n\nBest Tour Length:" + str(globalBestTourLength)
    resultFile.write(strToFile)
    
    scene.updateTour(globalBestTour)
    time.sleep(0.5)
    resultFile.close()
    
    #===========================================================================
    # for i in range(0,38):
    #    print pheromoneMatrix[i].index(max(pheromoneMatrix[i]))
    #===========================================================================
    
def start(scene, city):
    global cities, numberOfCities
    
    resultFile = open("results","w")
    
    cities = city
    numberOfCities = len(cities)
    
    tau0 = 1/(len(cities) * nearestNeighbor(list(cities))) # copying cities list and send nn algorithm
    
    # tau0 = (n * Cnn )^-1
    
    # create Ants
    for i in range(0,numberOfAnts):
        ants.append(Ant(i))
        
    systemStart(scene,iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, q0, rho, ksi, tau0, resultFile)
    