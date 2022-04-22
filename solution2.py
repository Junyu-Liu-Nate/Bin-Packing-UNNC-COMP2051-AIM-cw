import time
import random
import os
import copy

MAX_TIME = 30
K = 5
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
        
        self.__capacityLeft = self.getBinCapacity() - itemSizeSum

    def addItem(self, item):
        self.__itemList.append(item)
        self.__capacityLeft -= item.getItemSize()

    def removeItem(self, item):
        itemIndex = item.getItemIndex()
        for item2 in self.getItemList():
            if item2.getItemIndex() == itemIndex:
                self.__capacityLeft += item.getItemSize()
                self.getItemList().remove(item2)
                break

    def removeAllItem(self):
        self.__itemList = []
        self.__capacityLeft = self.__capacityAll

    def findLargestItem(self):
        itemList = self.getItemList()
        #print(len(itemList))

        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        
        return itemList[0]

    def findSmallestItem(self):
        itemList = self.getItemList()
        #print(len(itemList))

        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() > itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]
        
        return itemList[0]


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
        else:
            print("Alert!!! Bin is overflowed!!!")
            os.exit()

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

def getRandomIndex(rate):
    start = 0
    index = 0
    randnum = random.randint(1, sum(rate))

    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index

def best_descent_vns(nbIndex, currentSolution):
    currentSolutionCopy = copy.deepcopy(currentSolution)
    bestNeighbor = copy.deepcopy(currentSolution)
    
    binList = currentSolutionCopy.getBinList()

    if nbIndex == 1:
        for bin in binList:
            if len(bin.getItemList()) == 0:
                continue

            bin1List = bin.getItemList()
            for i in range(len(bin1List) - 1):
                for j in range(len(bin1List) - i - 1):
                    if bin1List[j].getItemSize() < bin1List[j + 1].getItemSize():
                        bin1List[j], bin1List[j + 1] = bin1List[j + 1], bin1List[j]

            for item in bin1List:
                for binNext in binList:
                    if len(binNext.getItemList()) == 0:
                        continue

                    if binNext.getBinIndex() == bin.getBinIndex():
                        continue

                    if item.getItemSize() <= binNext.getCapacityLeft():
                        bin.removeItem(item)
                        binNext.addItem(item)
                        break
        
        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)

        bestNeighbor.setBinList(binList)
        return bestNeighbor
    
    # if nbIndex == 1:
    #     for bin in binList:
    #         if len(bin.getItemList()) == 0:
    #             continue
    #         largestItem = bin.findLargestItem()
    #         for binNext in binList:
    #             if len(binNext.getItemList()) == 0:
    #                 continue

    #             if binNext.getBinIndex() == bin.getBinIndex():
    #                 continue

    #             if largestItem.getItemSize() <= binNext.getCapacityLeft():
    #                 bin.removeItem(largestItem)
    #                 binNext.addItem(largestItem)
    #                 break

    #     for bin in binList:
    #         if bin.getCapacityLoaded() == 0:
    #             binList.remove(bin)

    #     bestNeighbor.setBinList(binList)
    #     return bestNeighbor
    
    elif nbIndex == 2:

        itemNumSum = 0
        for bin in binList:
            itemNumSum += bin.getItemNum()
        averageNum = itemNumSum / len(binList)

        newBinList = []
        counter = 0
        for bin in binList:
            if bin.getItemNum() > averageNum:
                newBin = Bin(len(binList) + counter, bin.getBinCapacity())
                k = round(bin.getItemNum() / 2)
                sampleList = random.sample(bin.getItemList(), k)
                newBin.setItemList(sampleList)
                newBinList.append(newBin)
                for sampleItem in sampleList:
                    bin.removeItem(sampleItem)
                counter += 1
        
        for newBin in newBinList:
            binList.append(newBin)

        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)

        bestNeighbor.setBinList(binList)
        return bestNeighbor

    elif nbIndex == 3:

        for i in range(len(binList) - 1):
            for j in range(len(binList) - i - 1):
                if binList[j].getCapacityLeft() < binList[j + 1].getCapacityLeft():
                    binList[j], binList[j + 1] = binList[j + 1], binList[j]

        largestCapacityBin = binList[0]
        largestItem = largestCapacityBin.findLargestItem()

        randomIndex = random.randint(1, len(binList) - 1)
        randomBin = binList[randomIndex]

        if randomBin.findSmallestItem().getItemSize() >= largestItem.getItemSize():
            bestNeighbor.setBinList(binList)
            return bestNeighbor

        transferItemList = []
        transferSum = 0
        for item in randomBin.getItemList():
            if largestItem.getItemSize() - transferSum >= item.getItemSize():
                transferItemList.append(item)
                transferSum += item.getItemSize()

        binList[0].removeItem(largestItem)
        for transferItem in transferItemList:
            binList[0].addItem(transferItem)
            binList[randomIndex].removeItem(transferItem)
        binList[randomIndex].addItem(largestItem)

        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)

        bestNeighbor.setBinList(binList)
        return bestNeighbor

    elif nbIndex == 4:

        for i in range(len(binList) - 1):
            for j in range(len(binList) - i - 1):
                if binList[j].getCapacityLeft() < binList[j + 1].getCapacityLeft():
                    binList[j], binList[j + 1] = binList[j + 1], binList[j]
        
        capacityLeftList = []
        for bin in binList:
            capacityLeftList.append(bin.getCapacityLeft())
        capacityLeftAll = sum(capacityLeftList)
        rateList = []
        for capacityLeft in capacityLeftList:
            rateList.append(round(capacityLeft / capacityLeftAll * 100))
        rateListSum = sum(rateList)
        if rateListSum > 100:
            bias = rateListSum - 100
            rateList[0] + bias
        elif rateListSum < 100:
            bias = 100 - rateListSum
            rateList[0] - bias
        randomIndex1 = getRandomIndex(rateList)
        randomIndex2 = getRandomIndex(rateList)
        while randomIndex1 == randomIndex2:
            randomIndex2 = getRandomIndex(rateList)

        bin1 = binList[randomIndex1]
        bin2 = binList[randomIndex2]

        itemList = []
        for item in bin1.getItemList():
            itemList.append(item)
        for item in bin2.getItemList():
            itemList.append(item)

        bin1.removeAllItem()
        bin2.removeAllItem()

        for i in range(len(itemList) - 1):
            for j in range(len(itemList) - i - 1):
                if itemList[j].getItemSize() < itemList[j + 1].getItemSize():
                    itemList[j], itemList[j + 1] = itemList[j + 1], itemList[j]

        for item in itemList:
            if bin1.getCapacityLeft() >= item.getItemSize():
                bin1.addItem(item)
            else:
                bin2.addItem(item)

        if bin2.getCapacityLoaded() == 0:
            binList.remove(bin2)

        for bin in binList:
            if bin.getCapacityLoaded() == 0:
                binList.remove(bin)
        
        bestNeighbor.setBinList(binList)
        return bestNeighbor

    elif nbIndex == 5:
        for i in range(len(binList) - 1):
            for j in range(len(binList) - i - 1):
                if binList[j].getCapacityLeft() < binList[j + 1].getCapacityLeft():
                    binList[j], binList[j + 1] = binList[j + 1], binList[j]
        
        capacityLeftList = []
        for bin in binList[1:]:
            capacityLeftList.append(bin.getCapacityLeft())
        capacityLeftAll = sum(capacityLeftList)
        rateList = []
        for capacityLeft in capacityLeftList:
            rateList.append(round(capacityLeft / capacityLeftAll * 100))
        rateListSum = sum(rateList)
        if rateListSum > 100:
            bias = rateListSum - 100
            rateList[0] + bias
        elif rateListSum < 100:
            bias = 100 - rateListSum
            rateList[0] - bias
        randomIndex = getRandomIndex(rateList)

        bin1 = binList[randomIndex]
        largestItem1 = bin1.findLargestItem()

        itemList = []
        for bin in binList:
            if bin.getBinIndex() == bin1.getBinIndex():
                continue
            for item in bin.getItemList():
                itemList.append(item)

        newBin = Bin(len(binList), binList[0].getBinCapacity())
        newBin.addItem(largestItem1)

        selectedList = [largestItem1]
        for item in itemList:
            if newBin.getCapacityLeft() >= item.getItemSize():
                newBin.addItem(item)
                selectedList.append(item)

        for item in itemList:
            if item in selectedList:
                continue
            for binItem in newBin.getItemList():
                if newBin.getCapacityLeft() + binItem.getItemSize() - item.getItemSize() < newBin.getCapacityLeft() and newBin.getCapacityLeft() + binItem.getItemSize() - item.getItemSize() >= 0:
                    newBin.removeItem(binItem)
                    selectedList.remove(binItem)
                    newBin.addItem(item)
                    selectedList.append(item)

        for bin in binList:
            for item in bin.getItemList():
                if item in selectedList:
                    bin.removeItem(item)

        binList.append(newBin)

        bestNeighbor.setBinList(binList)
        return bestNeighbor 
    
    return bestNeighbor

def vns_shaking(solution, strength):
    # currentSolutionCopy = copy.deepcopy(solution)
    # shakeSolution = copy.deepcopy(solution)

    m = 0
    tryNum = 0

    binList = solution.getBinList()
    while m < strength and tryNum < 200:
        #binList = copy.deepcopy(solution.getBinList())

        randomIndex1 = random.randint(0, len(binList) - 1)
        randomIndex2 = random.randint(0, len(binList) - 1)
        while randomIndex1 == randomIndex2:
            randomIndex2 = random.randint(0, len(binList) - 1)

        bin1 = binList[randomIndex1]
        bin2 = binList[randomIndex2]

        # itemList = []
        # for item in bin1.getItemList():
        #     itemList.append(item)
        # for item in bin2.getItemList():
        #     itemList.append(item)
        
        # bin1.removeAllItem()
        # bin2.removeAllItem()

        # indicator = 1
        # counter = 0
        # avalability = 1
        # for item in itemList:
        #     if indicator == 1:
        #         if bin1.getCapacityLeft() < item.getItemSize():
        #             avalability = 0
        #             break
        #         else:
        #             bin1.addItem(item)
        #             counter += 1
                
        #         if counter % 4 == 1:
        #             indicator = 2
        #         elif counter % 4 == 2:
        #             indicator = 2
        #         elif counter % 4 == 3:
        #             indicator = 1
        #         elif counter % 4 == 0:
        #             indicator = 1
        #     elif indicator == 2:
        #         if bin2.getCapacityLeft() < item.getItemSize():
        #             avalability = 0
        #             break
        #         else:
        #             bin2.addItem(item)
        #             counter += 1

        #         if counter % 4 == 1:
        #             indicator = 2
        #         elif counter % 4 == 2:
        #             indicator = 2
        #         elif counter % 4 == 3:
        #             indicator = 1
        #         elif counter % 4 == 0:
        #             indicator = 1

        # if avalability == 0:
        #     m += 1
        # else:
        #     solution.setBinList(binList)
        #     m += 1

        largestItem1 = bin1.findLargestItem()
        largestItem2 = bin2.findLargestItem()

        if bin1.getCapacityLeft() + largestItem1.getItemSize() - largestItem2.getItemSize() >= 0 and bin2.getCapacityLeft() - largestItem1.getItemSize() + largestItem2.getItemSize() >= 0:
            bin1.removeItem(largestItem1)
            bin1.addItem(largestItem2)
            bin2.removeItem(largestItem2)
            bin2.addItem(largestItem1)
            m += 1

        tryNum += 1


def variable_neighbourhood_search(problem):
    timeStart = time.time()
    timeSpent = 0

    nbIndex = 1
    currentSolution = greedy_heuristic(problem)
    print("Greedy Search objective " + str(currentSolution.getObjective()))
    bestSolution = currentSolution

    while timeSpent < MAX_TIME:
        while nbIndex <= K:
            # print("Index " + str(nbIndex))
            neighborSolution = best_descent_vns(nbIndex, currentSolution)

            if neighborSolution.getObjective() < currentSolution.getObjective():
                print("Index " + str(nbIndex))
                print("Update better solution " + str(neighborSolution.getObjective()))

                bestSolution = neighborSolution
                currentSolution = neighborSolution
                nbIndex = 1
            else:
                nbIndex += 1

        # bestSolution = neighborSolution

        vns_shaking(currentSolution, SHAKE_STRENGTH)

        nbIndex = 1

        timeFinish = time.time()
        timeSpent = timeFinish - timeStart

    return bestSolution


problemList = loadProblem("binpack11.txt")
# itemList = problemList[0].getItemList()
# for item in itemList:
#     print([item.getItemIndex(), item.getItemSize()])

solution0 = greedy_heuristic(problemList[0])
#solution1 = best_descent_vns(0, solution0)
solution1 = variable_neighbourhood_search(problemList[0])
binList = solution1.getBinList()
print("Final objective " + str(len(binList)))

# for bin in binList:
#     itemList = bin.getItemList()
#     string = ""
#     for item in itemList:
#         string = string + str([item.getItemIndex(), item.getItemSize()]) + " "
#     print(string)

solutionList = []
solutionList.append(solution1)
printSolution("binpack11_sln_test.txt", solutionList)