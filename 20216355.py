import time

MAX_TIME = 30
K = 3
SHAKE_STRENGTH = 12

class Item:
    def __init__(self, index, size):
         self.__index = index
         self.__size = size
    
    def getItemIndex(self):
        return self.__index

    def getItemSize(self):
        return self.__size

class Bin:
    def __init__(self, index, capacity):
        self.__index = index
        self.__itemList = []
        self.__capacityAll = capacity
        self.__capacityLeft = capacity

    def getBinIndex(self):
        return self.__index

    def getItemList(self):
        return self.__itemList

    def getBinCapacity(self):
        return self.__capacityAll

    def getCapacityLeft(self):
        return self.__capacityLeft

    def addItem(self, item):
        self.__itemList.append(item)
        self.__capacityLeft -= item.getItemSize()

class Problem:
    def __init__(self, index, name, binCapacity, itemNum, bestObjective):
        self.__index = index
        self.__name = name
        self.__binCapacity = binCapacity
        self.__itemNum = itemNum
        self.__bestObjective = bestObjective
        self.__itemList = []

    def addItem(self, index, size):
        item = Item(index, size)
        self.__itemList.append(item)

    def getProblemName(self):
        return self.__name

    def getItemList(self):
        return self.__itemList

    def getBestObjective(self):
        return self.__bestObjective

    def getBinCapacity(self):
        return self.__binCapacity

    def sortItemList(self):
        itemList = self.getItemList()
        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        return itemList


class Solution:
    def __init__(self, problem, binList, objective):
        self.__problem = problem
        self.__objective = objective
        self.__binList = binList
        self.__feasibility = 0

    def getProblem(self):
        return self.__problem

    def getObjective(self):
        return self.__objective

    def getBinList(self):
        return self.__binList

    def checkFeasibility(self):
        binList = self.getBinList()
        for bin in binList:
            if bin.getCapacityLeft() < 0:
                self.__feasibility
                return
        self.__feasibility
        return

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
            fileHandler.write(" obj=    " + str(problem.getBestObjective()) + "      " + str(solution.getObjective() - problem.getBestObjective()) + "\n")
            for bin in solution.getBinList():
                for item in bin.getItemList():
                    fileHandler.write(str(item.getItemIndex()) + " ")
                fileHandler.write("\n")

#--- Greedy heurictic algorithm ---# 
def greedy_heuristic(problem):
    itemList = problem.sortItemList()
    binIndex  = 0
    binList = []
    bin = Bin(binIndex, problem.getBinCapacity())
    binList.append(bin)

    for item in itemList:
        for bin in binList:
            availableBinList = []
            if bin.getCapacityLeft() > item.getItemSize():
                availableBinList.append(bin)
        # If there are available bins which have enough capacity left,
        # serach for the bin that has the least capacity left and add the item into that bin.
        if len(availableBinList) != 0:
            smallestLeftBin = availableBinList[0]
            for availableBin in availableBinList:
                if availableBin.getCapacityLeft() < smallestLeftBin.getCapacityLeft():
                    smallestLeftBin = availableBin
            addIndex = smallestLeftBin.getBinIndex()
            for bin in binList:
                if bin.getBinIndex() == addIndex:
                    bin.addItem(item)
        # If there are no available bin which has enough capacity left,
        # create a new bin and add the item into that bin.
        else:
            binIndex += 1
            bin = Bin(binIndex, problem.getBinCapacity())
            bin.addItem(item)
            binList.append(bin)
    
    initialSolution = Solution(problem, binList, len(binList))
    return initialSolution

#def can_swap()

#def can_move()

#def apply_move()

def best_descent_vns(nbIdex, currentSolution):
    bestSolution = Solution()
    # copySolution(bestSolution, currentSolution)
    # 
    # if nbIdex == 0:
    #     #
    # elif nbIdex == 1:
    #     #
    # elif nbIndex == 2:
    #     #

    return bestSolution

def vns_shaking(solution, strength):
    # ?
    m = 0
    tryNum = 0
    while m < strength and tryNum < 200:
        # shaking
        tryNum += 1

def variable_neighbourhood_search(problem):
    timeStart = time.time()
    timeSpent = 0
    nbIdex = 0
    bestSolution = Solution(problem)
    # currentSolution = greedy_heuristic(problem)
    # updateBestSolution(currentSolution)

    shakingCount = 0
    while timeSpent < MAX_TIME:
        while nbIdex < K:
            #neighborSolution = best_descent_vns(nb_indx+1, curt_sln)
            # if neighborSolution.getObjective() > currentSolution.getObjective():
            #     copy_solution(neighborSolution, currentSolution)
            #     nbIndex=1
            # else:
                nbIdex += 1
        # updateBestSolution(currentSolution)

        gap = 1000
        if bestSolution.getProblem().getBestObjective() != 0:
            gap = 100 * (bestSolution.getObjective() - bestSolution.getProblem().getBestObjective()) / bestSolution.getProblem().getBestObjective()
        # vns_shaking(currentSolution, SHAKE_STRENGTH)
        # or vns_shaking(currentSolution, shakingCount/100+1) # re-active shaking
        shakingCount += 1

        nbIndex = 0

        timeFinish = time.time()
        timeSpent = timeFinish - timeStart

    return bestSolution


problemList = loadProblem("binpack1.txt")
# itemList = problemList[0].getItemList()
# for item in itemList:
#     print([item.getItemIndex(), item.getItemSize()])

solution0 = greedy_heuristic(problemList[0])
binList = solution0.getBinList()
print(len(binList))
# for bin in binList:
#     itemList = bin.getItemList()
#     string = ""
#     for item in itemList:
#         string = string + str([item.getItemIndex(), item.getItemSize()]) + " "
#     print(string)

solutionList = []
solutionList.append(solution0)
printSolution("binpack1_sln_test.txt", solutionList)