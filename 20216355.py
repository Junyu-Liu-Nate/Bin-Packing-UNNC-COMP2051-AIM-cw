import time
import random
import os
import copy
import sys, getopt

#----- Specify the global constants -----#
MAX_TIME = 30               # The maximun running time for one instance
NUM_OF_RUNS = 1             # The number of runs
K = 3                       # The number of neighbors
SHAKE_STRENGTH = 12         # The strength of VNS shaking

#----- Class for item -----#
class Item:
    # self.__index stores the index of item
    # self.__size stores the size of item
    def __init__(self, index, size):
         self.__index = index
         self.__size = size
    
    # Getters
    def getItemIndex(self):
        return self.__index

    def getItemSize(self):
        return self.__size

#----- Class for Bin -----#
class Bin:
    # self.__index stores the index of bin
    # self.__itemList stores the items that are packed in this bin
    # self.__capacityAll stores the original capacity of the bin (when no items are packed)
    # self.__capacityLeft stores the residual capacity of the bin
    def __init__(self, index, capacity):
        self.__index = index
        self.__itemList = []
        self.__capacityAll = capacity
        self.__capacityLeft = capacity

    # Getters
    def getBinIndex(self):
        return self.__index

    def getItemNum(self):
        return len(self.__itemList)

    def getItemList(self):
        return self.__itemList

    def getBinCapacity(self):
        return self.__capacityAll

    def getCapacityLeft(self):
        return self.__capacityLeft

    def getCapacityLoaded(self):
        return self.__capacityAll - self.__capacityLeft

    # Reset the item list of this bin
    def setItemList(self, list):
        self.__itemList = []
        self.__capacityLeft = self.__capacityAll

        self.__itemList = list
        itemSizeSum = 0
        for item in list:
            itemSizeSum += item.getItemSize()
        
        self.__capacityLeft = self.getBinCapacity() - itemSizeSum

    # Add an item into this bin
    def addItem(self, item):
        self.__itemList.append(item)
        self.__capacityLeft -= item.getItemSize()

    # Remove an item from this bin
    def removeItem(self, item):
        self.__capacityLeft += item.getItemSize()
        self.getItemList().remove(item)

    # Remove all items in this bin
    def removeAllItem(self):
        self.__itemList = []
        self.__capacityLeft = self.__capacityAll

    # Find the largest size item in this bin
    def findLargestItem(self):
        itemList = self.getItemList()

        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        
        return itemList[0]

    # Find the smallest size item in this bin
    def findSmallestItem(self):
        itemList = self.getItemList()

        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() > itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        
        return itemList[0]

#----- Class for Problem -----#
class Problem:
    # self.__index indicates the index of the problem
    # self.__name indicates the name of the problem
    # self.__binCapacity indicates the bin capacity of this problem
    # self.__itemNum indicates the number od items in this problem
    # self.__bestObjective indicates the best objective of bin number in this problem
    # self.__itemList indicates the list of items in this problem 
    def __init__(self, index, name, binCapacity, itemNum, bestObjective):
        self.__index = index
        self.__name = name
        self.__binCapacity = binCapacity
        self.__itemNum = itemNum
        self.__bestObjective = bestObjective
        self.__itemList = []

    # Getters
    def getProblemName(self):
        return self.__name

    def getItemList(self):
        return self.__itemList

    def getBestObjective(self):
        return self.__bestObjective

    def getBinCapacity(self):
        return self.__binCapacity

    # Add an item into the item list
    def addItem(self, index, size):
        item = Item(index, size)
        self.__itemList.append(item)

    # Sort the item list from the largest size item to the smallest item size
    def sortItemList(self):
        itemList = self.getItemList()
        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        return itemList

#----- Class for Solution -----#
class Solution:
    # self.__problem indicates the problem instance that this solution aims to solve
    # self.__objective indicates the objective of this solution (number of bins used)
    # self.__binList indicates the list of bins of this solution
    # self.__feasibility indicates the feasibility of this solution
    def __init__(self, problem, binList, objective):
        self.__problem = problem
        self.__objective = objective
        self.__binList = binList
        self.__feasibility = 1

    # Getters
    def getProblem(self):
        return self.__problem

    def getObjective(self):
        self.__objective = len(self.getBinList())
        return self.__objective

    def getBinList(self):
        return self.__binList

    # Reset the bin list of this solution
    def setBinList(self, binList):
        if self.checkFeasibility() == 1:
            self.__binList = binList
            self.__objective = len(binList)
        else:
            print("Alert!!! Bin is overflowed!!!")

    # Check the feasibility of this solution
    def checkFeasibility(self):
        binList = self.getBinList()
        binCapacity = self.__problem.getBinCapacity()
        for bin in binList:
            itemList = bin.getItemList()
            itemSizeSum = 0
            for item in itemList:
                itemSizeSum += item.getItemSize()
            if itemSizeSum > binCapacity:
                print(itemSizeSum)
                os.exit()
                self.__feasibility = 0
                return self.__feasibility
        self.__feasibility = 1
        return self.__feasibility

    # Check the 2nd-level fitness of the solution
    def fitnessEvaluation(self):
        binList = self.getBinList()
        residualCapacityList = []
        for bin in binList:
            residualCapacityList.append(bin.getCapacityLeft())
        average = sum(residualCapacityList) / len(residualCapacityList)
        mse = 0
        for residualCapacity in residualCapacityList:
            mse += (residualCapacity - average) * (residualCapacity - average)
        
        return mse

#--- Load problem from file ---#
def loadProblem(fileName):
    problemList = []
    with open(fileName, "r") as fileHandler:
        problemNum = int(fileHandler.readline())
        for i in range(0, problemNum):
            problemName = fileHandler.readline()
            problemInfo = fileHandler.readline()
            problemInfoList = problemInfo.split()
            problem = Problem(i, problemName, int(problemInfoList[0]), int(problemInfoList[1]), int(problemInfoList[2]))

            for j in range(0, int(problemInfoList[1])):
                itemSize = int(fileHandler.readline())
                problem.addItem(j, itemSize)
            
            problemList.append(problem)

    return problemList

#--- Print solution to file ---#
def printSolution(fileName, solutionList):
    solutionNum = len(solutionList)
    with open(fileName, "w") as fileHandler:
        fileHandler.write(str(solutionNum) + "\n")
        for solution in solutionList:
            problem = solution.getProblem()
            fileHandler.write(problem.getProblemName().lstrip(" "))
            fileHandler.write(" obj=   " + str(solution.getObjective()) + "       " + str(solution.getObjective() - problem.getBestObjective()) + "\n")
            for bin in solution.getBinList():
                for item in bin.getItemList():
                    fileHandler.write(str(item.getItemIndex()) + " ")
                fileHandler.write("\n")

#--- Greedy heurictic algorithm ---# 
# Greedy Search with best fit
def greedy_heuristic(problem):
    itemList = problem.sortItemList()
    binIndex  = 0
    binList = []
    bin = Bin(binIndex, problem.getBinCapacity())
    binList.append(bin)

    for item in itemList:
        indicator = 0
        for bin in binList:
            if item.getItemSize() <= bin.getCapacityLeft():
                bin.addItem(item)
                indicator = 1
                break
        if indicator == 0:
            binIndex += 1
            bin = Bin(binIndex, problem.getBinCapacity())
            bin.addItem(item)
            binList.append(bin)

    initialSolution = Solution(problem, binList, len(binList))
    return initialSolution

#--- Best Descent Neighorhood searching algorithm ---# 
def best_descent_vns(nbIndex, currentSolution):
    # Copy the solutions for operation
    currentSolutionCopy = copy.deepcopy(currentSolution)
    bestNeighbor = copy.deepcopy(currentSolution)
    
    binList = currentSolutionCopy.getBinList()

    # The first neighbor
    # The heuristic of neighborhood 1 is selecting the bin that has the largest residual capacity 
    # and try move the items in that bin to a sorted list rest of the bins (sorted from the largest 
    # residual capacity to the smallest residual capacity) using best fit descent heuristic. 
    # If there are no items left in the chosen bin after moving, remove the bin from the bin list.
    if nbIndex == 1: 
        # Sort the list of bins       
        for i in range(len(binList) - 1):
            for j in range(len(binList) - i - 1):
                if binList[j].getCapacityLeft() < binList[j + 1].getCapacityLeft():
                    binList[j], binList[j + 1] = binList[j + 1], binList[j]
        
        # Get the bin that has the largest residual space
        binListRest = binList[1:]

        # Try to put the items in the chosen bin to other bins
        for item in binList[0].getItemList():
            for i in range(len(binListRest) - 1):
                for j in range(len(binListRest) - i - 1):
                    if binListRest[j].getCapacityLeft() > binListRest[j + 1].getCapacityLeft():
                        binListRest[j], binListRest[j + 1] = binListRest[j + 1], binListRest[j]

            for binRest in binListRest:
                if binRest.getCapacityLeft() >= item.getItemSize():
                    binRest.addItem(item)
                    binList[0].removeItem(item)
                    break
        
        # If there are bins in which all items has been cleared, remove the bin.
        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)
        
        # Reset the bin list for the solution.
        bestNeighbor.setBinList(binList)
        return copy.deepcopy(bestNeighbor)

    # The second neighbor
    # The heuristic of neighborhood 2 is iteratively choosing two bins from the bin list 
    # and swap the largest size item in from the bin that has larger residual capacity with 
    # a combination of smaller size items in the other bin (Only valid swaps are accepted to 
    # prevent overflow in bins).
    elif nbIndex == 2:
        # Iteratively switch the largest item in a bin with smaller item (combinations) of another bin.
        for bin1 in binList:
            for bin2 in binList:
                if bin1.getBinIndex() == bin2.getBinIndex():
                    continue

                if bin1.getCapacityLoaded() == 0 or bin2.getCapacityLoaded() == 0:
                    continue

                # Switch the largest item in a bin that has larger residual capacity 
                # with smaller item (combinations) of another bin.
                if bin1.getCapacityLeft() > bin2.getCapacityLeft():
                    largestItem1 = bin1.findLargestItem()
                    if bin2.findSmallestItem().getItemSize() >= largestItem1.getItemSize():
                        continue
                    
                    # Move items in the transferlist
                    transferItemList = []
                    transferSum = 0
                    for item in bin2.getItemList():
                        if largestItem1.getItemSize() - transferSum > item.getItemSize() and bin2.getCapacityLeft() + transferSum + item.getItemSize() - largestItem1.getItemSize() >= 0:
                            transferItemList.append(item)
                            transferSum += item.getItemSize()
                    
                    transferItemSum = 0
                    for transferItem in transferItemList:
                        transferItemSum += transferItem.getItemSize()

                    # Check whether can move and then move
                    if len(transferItemList) != 0:
                        bin1.removeItem(largestItem1)
                        for transferItem in transferItemList:
                            bin1.addItem(transferItem)
                            bin2.removeItem(transferItem)
                        bin2.addItem(largestItem1)

                    # Prompt aleart if the solution is infeasible
                    if bin1.getCapacityLeft() < 0:
                        print("bin1 alert!")
                    elif bin2.getCapacityLeft() < 0:
                        print("bin2 alert!")

        # Set the item list of the two swaping bins
        itemList = []
        for bin in binList:
            for item in bin.getItemList():
                itemList.append(item)
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)

        bestNeighbor.setBinList(binList)
        return copy.deepcopy(bestNeighbor)

    # The third neighbor
    # The heuristic of neighborhood 3 is iteratively choosing two bins from the bin list 
    # and move out all items of these two bins and then re-fill these items into 
    # the two bins using greedy heuristic.
    elif nbIndex == 3:
        # Iteratively select two bins
        for bin1 in binList:
            for bin2 in binList:
                if bin1.getBinIndex() == bin2.getBinIndex():
                    continue

                if bin1.getCapacityLoaded() == 0 or bin2.getCapacityLoaded() == 0:
                    continue

                bin1Copy = copy.deepcopy(bin1)
                bin2Copy = copy.deepcopy(bin2)

                # Move all items of the selected two bins into one list
                itemList = []
                for item in bin1Copy.getItemList():
                    itemList.append(item)
                for item in bin2Copy.getItemList():
                    itemList.append(item)

                # Sort the item list
                for i in range(len(itemList) - 1):
                    for j in range(len(itemList) - i - 1):
                        if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                            itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]

                bin1Copy.removeAllItem()
                bin2Copy.removeAllItem()

                indicator = 1
                avalability = 1
                counter = 0

                # Use best fit to refill the items into the two bins
                for item in itemList:
                    if indicator == 1:
                        if bin1Copy.getCapacityLeft() >= item.getItemSize():
                            bin1Copy.addItem(item)
                            counter += 1
                            indicator = 2
                        elif bin2Copy.getCapacityLeft() >= item.getItemSize():
                            bin2Copy.addItem(item)
                            counter += 1
                            indicator = 1
                        else:
                            break
                    elif indicator == 2:
                        if bin2Copy.getCapacityLeft() >= item.getItemSize():
                            bin2Copy.addItem(item)
                            counter += 1
                            indicator = 1
                        elif bin1Copy.getCapacityLeft() >= item.getItemSize():
                            bin1Copy.addItem(item)
                            counter += 1
                            indicator = 2
                        else:
                            break

                if counter < len(itemList):
                    avalability = 0

                if avalability != 0:
                    bin1 = bin1Copy
                    bin2 = bin2Copy
        
        # If there are bins in which all items has been cleared, remove the bin.
        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)
        
        # Reset the bin list for the solution.
        bestNeighbor.setBinList(binList)
        return bestNeighbor
    
    return copy.deepcopy(bestNeighbor)

#--- VNS shaking algorithm ---# 
# The shaking mechanism is to randomly choose two bins from the bin list 
# and swap the largest item of these two bins if the swap is available. 
# This diversification operation gives more possible space for searching and operating in all three neighborhoods.
def vns_shaking(solution, strength):
    # Exchange the largest item in two randomly chosen bins
    m = 0
    tryNum = 0

    binList = solution.getBinList()

    # When shaking strength and iteration number are less than the set values, do the shaking
    while m < strength and tryNum < 200:
        # Randomly select two bins
        randomIndex1 = random.randint(0, len(binList) - 1)
        randomIndex2 = random.randint(0, len(binList) - 1)
        while randomIndex1 == randomIndex2:
            randomIndex2 = random.randint(0, len(binList) - 1)

        bin1 = binList[randomIndex1]
        bin2 = binList[randomIndex2]

        largestItem1 = bin1.findLargestItem()
        largestItem2 = bin2.findLargestItem()

        # Check whether the swap can be done and do the swap
        if bin1.getCapacityLeft() + largestItem1.getItemSize() - largestItem2.getItemSize() >= 0 and bin2.getCapacityLeft() - largestItem1.getItemSize() + largestItem2.getItemSize() >= 0:
            bin1.removeItem(largestItem1)
            bin1.addItem(largestItem2)
            bin2.removeItem(largestItem2)
            bin2.addItem(largestItem1)
            m += 1

        tryNum += 1

#--- Variable Neighbourhood Search algorithm ---# 
def variable_neighbourhood_search(problem, Max_Time):
    # Starts check the time
    timeStart = time.time()
    timeSpent = 0

    # Initialize the solution using Greedy Search
    nbIndex = 1
    currentSolution = greedy_heuristic(problem)
    bestSolution = currentSolution

    while timeSpent < Max_Time:
        # Can be used to save running time
        # if bestSolution.getObjective() <= bestSolution.getProblem().getBestObjective():
        #     break

        while nbIndex <= K:
            # Calculate the best neighborhood solution
            neighborSolution = best_descent_vns(nbIndex, currentSolution)

            # 1st-level fitness
            # If the neighbor solution has a smaller object value, update the current and best solution.
            if neighborSolution.getObjective() < currentSolution.getObjective():
                #print("Update better solution " + str(neighborSolution.getObjective()))
                bestSolution = neighborSolution
                currentSolution = neighborSolution
                nbIndex = 1
            # 2nd-level fitness
            # The second-level fitness function is calculated when there is no update in the first-level fitness function. 
            # In the second-level fitness function, the uniformity of the residual spaces of each bin in the bin list is calculated 
            # by the Euclidian Distance of these residual spaces to the mean residual space. The reason for the second-level 
            # fitness function is based on an experimental observation, in which more unevenly distributed (in terms of residual space) 
            # bin lists have higher chance to be optimized (e.g., remove a bin) by the following heuristics. Thus, although the bin number 
            # (direct objective) of the neighboring solution is not decreased, if it has a more uneven distributed bin list than the current solution, 
            # the current solution is still updated.
            elif neighborSolution.fitnessEvaluation() > currentSolution.fitnessEvaluation():
                currentSolution = neighborSolution
                nbIndex = 1
            # If no better improvement, move on to the next neighbor
            else:
                nbIndex += 1

        # Perform VNS shaking
        vns_shaking(currentSolution, SHAKE_STRENGTH)

        nbIndex = 1

        # Check the running time
        timeFinish = time.time()
        timeSpent = timeFinish - timeStart

    return bestSolution

#--- Main function ---# 
def main(argv):
    # Read the command line with the format of '20216355.py -s <inputfile> -o <outputfile>'
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hs:o:t:",["ifile=", "ofile=", "max_time="])
    except getopt.GetoptError:
      print('Please input as: 20216355.py -s <inputfile> -o <outputfile> -t <maxtime>')
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Please input as: 20216355.py -s <inputfile> -o <outputfile> -t <maxtime>')
            sys.exit()
        elif opt in ("-s", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--max_time"):
            MAX_TIME = int(arg)

    # Load the problem
    problemList = loadProblem(inputfile)

    # Solve the problems in the problem file
    objectDeviation = []
    solutionList = []
    print("Start calculating ...")
    for problem in problemList:
        solution = variable_neighbourhood_search(problem, MAX_TIME)
        objectDeviation.append(len(solution.getBinList()) - problem.getBestObjective())
        solutionList.append(solution)
        print("Finish calcualting " + str(solution.getProblem().getProblemName().replace("\n", "")) + ", the deviation to best objective is " + str(len(solution.getBinList()) - problem.getBestObjective()))
    print("Finish calculating all!\nYou can check the solution file")
    # Print to the solution file
    #print(objectDeviation)
    printSolution(outputfile, solutionList)


if __name__ == "__main__":
    main(sys.argv[1:])