import time
import random
import os

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

    def setItemList(self, list):
        self.__itemList = []
        self.__capacityLeft = self.__capacityAll

        self.__itemList = list
        itemSizeSum = 0
        for item in list:
            itemSizeSum += item.getItemSize()
        self.__capacityLeft = self.__capacityAll - itemSizeSum

    def addItem(self, item):
        self.__itemList.append(item)
        self.__capacityLeft -= item.getItemSize()

    def removeItem(self, item):
        itemIndex = item.getItemIndex()
        for item2 in self.getItemList():
            if item2.getItemIndex() == itemIndex:
                self.getItemList().remove(item2)
                self.__capacityLeft += item.getItemSize()
                break

    def removeAllItem(self):
        self.__itemList = []
        self.__capacityLeft = self.__capacityAll

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
        self.__feasibility = 1

    def getProblem(self):
        return self.__problem

    def getObjective(self):
        self.__objective = len(self.getBinList())
        return self.__objective

    def getBinList(self):
        return self.__binList

    def setBinList(self, binList):
        if self.checkFeasibility() == 1:
            self.__binList = binList
            self.__objective = len(binList)

    def checkFeasibility(self):
        binList = self.getBinList()
        binCapacity = self.__problem.getBinCapacity()
        for bin in binList:
            itemList = bin.getItemList()
            itemSizeSum = 0
            for item in itemList:
                itemSizeSum += item.getItemSize()
            if itemSizeSum > binCapacity:
                self.__feasibility = 0
                return self.__feasibility
        self.__feasibility = 1
        return self.__feasibility

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


def best_descent_vns(nbIndex, currentSolution):
    # copySolution(bestSolution, currentSolution)
    #bestNeighbor = currentSolution
    bestNeighbor = Solution(currentSolution.getProblem(), currentSolution.getBinList(), currentSolution.getObjective())
    # 
    if nbIndex == 1:
        binList = currentSolution.getBinList()

        for bin1 in binList:
            for bin2 in binList:
                if bin1.getBinIndex() == bin2.getBinIndex():
                    continue

                if bin1.getCapacityLoaded() == 0 or bin2.getCapacityLoaded() == 0:
                    continue

                indicator = 0
                for item in bin1.getItemList():
                    if item.getItemSize() <= bin2.getCapacityLeft():
                        indicator == 1
                        bin2.addItem(item)
                        bin1.removeItem(item)
                        if bin1.getCapacityLoaded() == 0:
                            #binList.remove(bin1)
                            break

                if indicator == 1:
                    for item in bin2.getItemList():
                        if item.getItemSize() <= bin1.getCapacityLeft():
                            bin1.addItem(item)
                            bin2.removeItem(item)
                            if bin2.getCapacityLoaded() == 0:
                                #binList.remove(bin2)
                                break
        
        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)
        bestNeighbor.setBinList(binList)
        return bestNeighbor

    elif nbIndex == 2:
        binList = currentSolution.getBinList()
        for bin1 in binList:
            for bin2 in binList:
                if bin1.getBinIndex() == bin2.getBinIndex():
                    continue
                for bin3 in binList:
                    if bin1.getBinIndex() == bin3.getBinIndex() or bin2.getBinIndex() == bin3.getBinIndex():
                        continue

                    if bin1.getCapacityLoaded() == 0 or bin2.getCapacityLoaded() == 0 or bin3.getCapacityLoaded():
                        continue

                    indicator = 0
                    for item in bin1.getItemList():
                        if item.getItemSize() <= bin2.getCapacityLeft():
                            indicator = 1
                            bin2.addItem(item)
                            bin1.removeItem(item)
                            if bin1.getCapacityLoaded() == 0:
                                #binList.remove(bin1)
                                break
                        elif item.getItemSize() <= bin3.getCapacityLeft():
                            indicator = 1
                            bin3.addItem(item)
                            bin1.removeItem(item)
                            if bin1.getCapacityLoaded() == 0:
                                #binList.remove(bin1)
                                break
                    
                    if indicator == 1:
                        for item in bin2.getItemList():
                            if item.getItemSize() <= bin1.getCapacityLeft():
                                indicator = 1
                                bin1.addItem(item)
                                bin2.removeItem(item)
                                if bin2.getCapacityLoaded() == 0:
                                    #binList.remove(bin2)
                                    break
                            elif item.getItemSize() <= bin3.getCapacityLeft():
                                indicator = 1
                                bin3.addItem(item)
                                bin2.removeItem(item)
                                if bin2.getCapacityLoaded() == 0:
                                    #binList.remove(bin2)
                                    break

                    if indicator == 1:
                        for item in bin3.getItemList():
                            if item.getItemSize() <= bin1.getCapacityLeft():
                                indicator = 1
                                bin1.addItem(item)
                                bin3.removeItem(item)
                                if bin3.getCapacityLoaded() == 0:
                                    #binList.remove(bin3)
                                    break
                            elif item.getItemSize() <= bin2.getCapacityLeft():
                                indicator = 1
                                bin2.addItem(item)
                                bin3.removeItem(item)
                                if bin3.getCapacityLoaded() == 0:
                                    #binList.remove(bin3)
                                    break

                    # itemList = []
                    # for item in bin1.getItemList():
                    #     itemList.append(item)
                    # for item in bin2.getItemList():
                    #     itemList.append(item)
                    # for item in bin3.getItemList():
                    #     itemList.append(item)
                    
                    # for i in range(len(itemList) - 1):
                    #     for j in range(len(itemList) - i - 1):
                    #         if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    #             itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]

                    # bin1ItemList = bin1.getItemList()
                    # # print(len(bin1ItemList))
                    # bin2ItemList = bin2.getItemList()
                    # bin3ItemList = bin3.getItemList()

                    # bin1.removeAllItem()
                    # #print([len(bin1ItemList), len(bin1.getItemList())])
                    # # print("-----------")
                    # bin2.removeAllItem()
                    # bin3.removeAllItem()

                    # indicator = 1
                    # counter = 0
                    # for item in itemList:
                    #     if indicator == 1:
                    #         if bin1.getCapacityLeft() >= item.getItemSize():
                    #             bin1.addItem(item)
                    #             indicator = 2
                    #             counter += 1
                    #         elif bin2.getCapacityLeft() >= item.getItemSize():
                    #             bin2.addItem(item)
                    #             indicator = 1
                    #             counter += 1
                    #         else:
                    #             break
                    #     elif indicator == 2:
                    #         if bin2.getCapacityLeft() >= item.getItemSize():
                    #             bin2.addItem(item)
                    #             indicator = 1
                    #             counter += 1
                    #         elif bin1.getCapacityLeft() >= item.getItemSize():
                    #             bin1.addItem(item)
                    #             indicator = 2
                    #             counter += 1
                    #         else:
                    #             break

                    # itemSizeSum = 0
                    # itemSizeSum1 = 0
                    # itemSizeSum2 = 0
                    # for item in itemList:
                    #     itemSizeSum += item.getItemSize()
                    # for item in bin1.getItemList():
                    #     itemSizeSum1 += item.getItemSize()
                    # for item in bin2.getItemList():
                    #     itemSizeSum2 += item.getItemSize()
                    # # print([itemSizeSum,itemSizeSum1,itemSizeSum2])
                    # # if itemSizeSum > 450:
                    # #     os.exit()

                    # if itemSizeSum - (itemSizeSum1 + itemSizeSum2) > bin3.getCapacityLeft():
                    #     #print("Stay")
                    #     bin1.setItemList(bin1ItemList)
                    #     bin2.setItemList(bin2ItemList)
                    #     bin3.setItemList(bin3ItemList)
                    # else:
                    #     #print("Update")
                    #     if counter == len(itemList):
                    #         binList.remove(bin3)
                    #     else:
                    #         for item in itemList[counter:]:
                    #             bin3.addItem(item)
                    #             # if bin3.getCapacityLeft() < 0:
                    #             #     os.exit()

        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)

        bestNeighbor.setBinList(binList)
        print("Finish searching in neighbor 2")
        return bestNeighbor

    elif nbIndex == 3:
        binList = currentSolution.getBinList()
        for bin1 in binList:
            for bin2 in binList:
                if bin1.getBinIndex() == bin2.getBinIndex():
                    continue
                for bin3 in binList:
                    if bin1.getBinIndex() == bin3.getBinIndex() or bin2.getBinIndex() == bin3.getBinIndex():
                        continue
                    for bin4 in binList:
                        if bin1.getBinIndex() == bin4.getBinIndex() or bin2.getBinIndex() == bin4.getBinIndex() or bin3.getBinIndex() == bin4.getBinIndex():
                            continue

                        itemList = []
                        for item in bin1.getItemList():
                            itemList.append(item)
                        for item in bin2.getItemList():
                            itemList.append(item)
                        for item in bin3.getItemList():
                            itemList.append(item)
                        for item in bin4.getItemList():
                            itemList.append(item)

                        for i in range(len(itemList) - 1):
                            for j in range(len(itemList) - i - 1):
                                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]

                        bin1ItemList = bin1.getItemList()
                        bin2ItemList = bin2.getItemList()
                        bin3ItemList = bin3.getItemList()
                        bin4ItemList = bin4.getItemList()

                        bin1.removeAllItem()
                        bin2.removeAllItem()
                        bin3.removeAllItem()
                        bin4.removeAllItem()

                        indicator = 1
                        counter = 0
                        for item in itemList:
                            if indicator == 1:
                                if bin1.getCapacityLeft() > item.getItemSize():
                                    bin1.addItem(item)
                                    indicator = 2
                                    counter +=1
                                elif bin2.getCapacityLeft() > item.getItemSize():
                                    bin2.addItem(item)
                                    indicator = 3
                                    counter +=1
                                elif bin3.getCapacityLeft() > item.getItemSize():
                                    bin3.addItem(item)
                                    indicator = 1
                                    counter +=1
                                else:
                                    break
                            elif indicator == 2:
                                if bin2.getCapacityLeft() > item.getItemSize():
                                    bin2.addItem(item)
                                    indicator = 3
                                    counter += 1
                                elif bin3.getCapacityLeft() > item.getItemSize():
                                    bin3.addItem(item)
                                    indicator = 1
                                    counter +=1
                                elif bin1.getCapacityLeft() > item.getItemSize():
                                    bin1.addItem(item)
                                    indicator = 2
                                    counter +=1
                                else:
                                    break
                            elif indicator == 3:
                                if bin3.getCapacityLeft() > item.getItemSize():
                                    bin3.addItem(item)
                                    indicator == 1
                                    counter += 1
                                elif bin1.getCapacityLeft() > item.getItemSize():
                                    bin1.addItem(item)
                                    indicator = 2
                                    counter +=1
                                elif bin2.getCapacityLeft() > item.getItemSize():
                                    bin2.addItem(item)
                                    indicator = 3
                                    counter +=1
                                else:
                                    break

                        itemSizeSum = 0
                        itemSizeSum1 = 0
                        itemSizeSum2 = 0
                        itemSizeSum3 = 0
                        for item in itemList:
                            itemSizeSum += item.getItemSize()
                        for item in bin1.getItemList():
                            itemSizeSum1 += item.getItemSize()
                        for item in bin2.getItemList():
                            itemSizeSum2 += item.getItemSize()
                        for item in bin3.getItemList():
                            itemSizeSum3 += item.getItemSize()

                        if itemSizeSum - (itemSizeSum1 + itemSizeSum2 + itemSizeSum3) > bin4.getCapacityLeft():
                            bin1.setItemList(bin1ItemList)
                            bin2.setItemList(bin2ItemList)
                            bin3.setItemList(bin3ItemList)
                            bin4.setItemList(bin4ItemList)
                        else:
                            if counter == len(itemList):
                                binList.remove(bin4)
                            else:
                                for item in itemList[counter:]:
                                    bin4.addItem(item)
                    
        bestNeighbor.setBinList(binList)
        print("Finish searching in neighbor 3")
        return bestNeighbor   

    return bestNeighbor

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
    nbIndex = 1
    #bestSolution = Solution(problem)
    currentSolution = greedy_heuristic(problem)
    bestSolution = currentSolution

    shakingCount = 0
    while timeSpent < MAX_TIME:
        while nbIndex < K:
            neighborSolution = best_descent_vns(nbIndex, currentSolution)
            if neighborSolution.getObjective() < currentSolution.getObjective():
                bestSolution = neighborSolution
                currentSolution = neighborSolution
                nbIndex=1
                print("Change neighor " + str(nbIndex))
            else:
                nbIndex += 1
                print("Change neighor " + str(nbIndex))

        # neighborSolution = best_descent_vns(nbIndex, currentSolution)
        # if neighborSolution.getObjective() < currentSolution.getObjective():
        #     bestSolution = neighborSolution
        #     currentSolution = neighborSolution

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


problemList = loadProblem("binpack3.txt")
# itemList = problemList[0].getItemList()
# for item in itemList:
#     print([item.getItemIndex(), item.getItemSize()])

solution0 = greedy_heuristic(problemList[0])
#solution1 = best_descent_vns(0, solution0)
solution1 = variable_neighbourhood_search(problemList[0])
binList = solution1.getBinList()
print(len(binList))

# for bin in binList:
#     itemList = bin.getItemList()
#     string = ""
#     for item in itemList:
#         string = string + str([item.getItemIndex(), item.getItemSize()]) + " "
#     print(string)

solutionList = []
solutionList.append(solution1)
printSolution("binpack3_sln_test.txt", solutionList)