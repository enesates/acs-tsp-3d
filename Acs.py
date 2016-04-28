# The solution of Traveling Salesperson Problem by using Ant Colony System algorithm and its 3d simulation with OpenGL

import math
import random
import time
from Scene import *
from Ant import *


iteration = 20
ants = []
pheromoneMatrix = []
numberOfAnts = 10

Q = 10 # constant representing the amount of pheromone an ant put on the path

alpha = 1.0 # heuristic parameter
beta = 3.0 # heuristic parameter
q0 = 0.9 # control parameter for random proportional

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


def nearestNeighbor(cities, resultFile):
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
    tourLength += calculateDistance(nextCity, path[0])
    
    print "Nearest Neighbor tour length:", tourLength
    strToFile = "\n\nNearest Neighbor tour length:" + str(tourLength)
    resultFile.write(strToFile)

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
            tauEthaVal = math.pow(pheromoneMatrix[currentCity.id][i], alpha) * math.pow(1.0/calculateDistance(currentCity, cities[i]), beta) 
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
    ant.tour.append(ant.tour[0])
    
    ant.tourLength = calculateCost(ant.tour)
        
        
def localPheromoneUpdate(ant, phrMatrix, tau0, ksi):
    
    for i in range(0, len(ant.tour)-1):
        current = ant.tour[i].id
        next = ant.tour[i+1].id

        phrMatrix[current][next] = ((1 - ksi) * phrMatrix[current][next] ) + (ksi * tau0)
        phrMatrix[next][current] = phrMatrix[current][next]


def globalPheromoneUpdate(globalBestTour, globalBestTourLength, phrMatrix, rho):
    
    for i in range(0, len(globalBestTour)-1):
        current = globalBestTour[i].id
        next = globalBestTour[i+1].id

        phrMatrix[current][next] = ((1 - rho) * phrMatrix[current][next] ) + (Q * (1/globalBestTourLength))
        phrMatrix[next][current] = phrMatrix[current][next]


def localSearch(antId, antTour, antTourLength, resultFile):
    
    
    while True:
        
        best = antTourLength
        
        for i in range(0, len(antTour)-1):
            for j in range(i+1, len(antTour)):
                newAntTour = list(antTour)
                k, l = i, j
                
                while k < l:
                    newAntTour[k], newAntTour[l] = newAntTour[l], newAntTour[k] # swap
                    
                    if k == 0:
                        newAntTour[len(antTour)-1] = newAntTour[k]
                    
                    if l == len(antTour)-1:
                        newAntTour[0] = newAntTour[l]
                    
                    k += 1
                    l -= 1
                
                newAntTourLength = calculateCost(newAntTour)
                
                if newAntTourLength < antTourLength:
                    antTourLength = newAntTourLength
                    antTour = newAntTour
                                        
                    
        if best == antTourLength:
            print antId+1,". ant's local search tour. Tour length:", antTourLength
            strToFile = "\n" + str(antId+1) + ". ant's local search tour. Tour length:" + str(antTourLength)
            resultFile.write(strToFile)
            
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
        strToFile = "\n\n\nIteration " + str(i)
        resultFile.write(strToFile)

        bestTourLength = 0
        
        initializeTours(bestTour, ants)
        
        for j in range(0,numberOfAnts):
                        
            tourConstruction(ants[j], numberOfCities, list(cities), beta, q0)
            #localSearch()
            localPheromoneUpdate(ants[j], pheromoneMatrix, tau0, ksi)
            
            print "\n", j+1 ,". ant's tour. Tour length: ", ants[j].tourLength
            strToFile = "\n\n" + str(j+1) + ". ant's tour. Tour length: " + str(ants[j].tourLength)
            resultFile.write(strToFile)
            
            scene.updateTour(ants[j].tour)
            time.sleep(0.5)
            
            ants[j].tour, ants[j].tourLength = localSearch(ants[j].id, list(ants[j].tour), ants[j].tourLength, resultFile)
               
            if bestTourLength == 0 or bestTourLength > ants[j].tourLength:
                bestTourLength = ants[j].tourLength
                bestTour = ants[j].tour
                
                print j+1,". ant's tour is the best tour. Tour length:", bestTourLength
                strToFile = "\n" + str(j+1) + ". ant's tour is the best tour. Tour length: " + str(bestTourLength)
                resultFile.write(strToFile)
                  
        
        if globalBestTourLength == 0 or globalBestTourLength > bestTourLength:
            globalBestTourLength = bestTourLength
            
            print "\nBest tour until now. Tour length: ", globalBestTourLength
            strToFile = "\n\nBest tour until now. Tour length: " + str(globalBestTourLength)
            resultFile.write(strToFile)
            
            globalBestTour = bestTour
            scene.updateTour(globalBestTour)
            time.sleep(0.5)
        
        globalPheromoneUpdate(globalBestTour, globalBestTourLength, pheromoneMatrix, rho)
        
        
    for i in range(0, len(globalBestTour)):
       print "\nBest tour", i+1, ". city coordinate:",globalBestTour[i].coordinate
       strToFile = "\n\nBest tour "+ str(i+1) + ". city coordinate:" + str(globalBestTour[i].coordinate)
       resultFile.write(strToFile)
        
    print "\nBest Tour Length: ", globalBestTourLength
    strToFile = "\n\nBest Tour Length: " + str(globalBestTourLength)
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
    
    tau0 = 1/(len(cities) * nearestNeighbor(list(cities), resultFile)) # copying cities list and send nn algorithm
    
    # tau0 = (n * Cnn )^-1
    
    # create Ants
    for i in range(0,numberOfAnts):
        ants.append(Ant(i))
        
    systemStart(scene,iteration, cities, ants, pheromoneMatrix, numberOfCities, numberOfAnts, beta, q0, rho, ksi, tau0, resultFile)
    
