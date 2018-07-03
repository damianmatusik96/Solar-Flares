import sys
import math as m
import random
from collections import Counter

class Node(object):
	def __init__(self, parent = None, children = []):
		self.children = []
		self.parent = parent
		self.height = 0
		self.splitValue = None
		self.testedAttributeIndex = None
		self.is_leaf = None
		self.classValue = None


def dataBase(filename):
    file = open(filename)
    rawFile = file.read()
    rowSplitData = rawFile.splitlines()
    data = list()
    for rows in rowSplitData:
        rowData = rows.split(' ')
        data.append(rowData)
    return data


testQualities = [1.12,1.59,2.34,2.11,0.845]

def roullette(testsQualities):
    revertValue = []
    weight = []

    for n in range(0,len(testsQualities)):
        revertValue.append(1/float(testsQualities[n]))
    suma = sum(revertValue)
    for n in range(0, len(revertValue)):
        weight.append(revertValue[n]/suma)
    rand = random.uniform(0,1)

    for n in range(0,len(weight) - 1):
        weight[n+1] = weight[n+1] + weight[n]

    for n in range(0, len(weight) - 1):
        if (rand < weight[0]):
            indexTest = 0
        elif (rand > weight[n] and rand < weight[n+1]):
            indexTest = n + 1
        else :
            continue

    return indexTest

tests = [['A', 'B', 'C', 'D', 'E', 'F', 'H'],
         ['X', 'R', 'S', 'A', 'H', 'K'],
         ['X', 'O', 'I', 'C'],
         ['1' , '2'],
         ['1', '2', '3'],
         ['1', '2', '3'],
         ['1', '2'],
         ['1', '2'],
         ['1', '2'],
         ['1', '2']]
testList = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'X', 'R', 'S', 'A', 'H', 'K','X', 'O', 'I', 'C', '1' , '2', '1', '2', '3', '1', '2', '3', '1', '2','1', '2', '1', '2', '1', '2' ]
def splitData(data, singleTest, testedColumn):
    left = list()
    right = list()
    root = []
    for row in data:
        if row[testedColumn] == singleTest:
            left.append(row)
        else:
            right.append(row)

    return left, right

def sumOfSquare(testData, tests):
    left = []
    right = []
    error = 99999
    tempError = 0
    testedColumn = 0
    totalQuality = list()
    qualityOfTests = list()
    finalTestedColumn = None
    finalTestIndex = None

    for wiersz in [tests[n] for n in range(0, len(tests))]:
        testIndex = 0

        for singleTest in [wiersz[n] for n in range(0, len(wiersz))]:
            left, right = splitData(testData, singleTest, testedColumn)

            if len(left) and len(right):
                tempError = singleSumOfSquare(left, right) + 0.00001
                qualityOfTests.append(tempError)

                index = roullette(qualityOfTests)
                splitTest = testList[index];
                if tempError < error:
                    error = tempError
                    finalTestIndex = testIndex
                    finalTestedColumn = testedColumn
                    testIndex += 1
                else:
                    testIndex += 1

            else:
                testIndex += 1
                qualityOfTests.append(99999)
        testedColumn += 1
    if finalTestedColumn == None:
        return None, None

    bestTest = tests[finalTestedColumn][finalTestIndex]
    return splitTest, finalTestedColumn

def singleSumOfSquare(left, right):
    leftSum = sum(float(row[-1]) for row in left)
    rightSum = sum(float(row[-1]) for row in right)
    leftAvg = leftSum / len(left)
    rightAvg = rightSum / len(right)

    leftError = 0
    rightError = 0

    for row in left:
        leftError += m.pow((float(row[-1]) - leftAvg), 2)
    for row in left:
        rightError += m.pow((float(row[-1]) - rightAvg), 2)
    singleError = leftError + rightError
    return singleError

def classifyLeaf(node, value):
    pass
def buildTree(dataSet, parent, tests, depth):
    node = Node(parent = parent)

    if parent == None:
        node.height = 0
    else:
        node.height = parent.height + 1

    classValue = [row[-1] for row in dataSet]
    counter = Counter(classValue)
    if len(dataSet) == 0:
        node.is_leaf = True
        node.classValue = 0
        return node
    if len(dataSet) == counter.most_common()[0][1]:
        node.is_leaf = True
        node.classValue = counter.most_common()[0][0]
        return node
    bestTest, testedAttr = sumOfSquare(dataSet, tests)
    if bestTest == None:
        node.is_leaf = True
        node.classValue = counter.most_common()[0][0]
        return node
    if node.height >= depth:
        node.is_leaf = True
        node.classValue = counter.most_common()[0][0]
        return node
    left, right = splitData(dataSet, bestTest, testedAttr)

    node.testedAttributeIndex = testedAttr
    node.splitValue = bestTest
    node.children.append(buildTree(left, node, tests,depth))
    node.children.append(buildTree(right, node, tests, depth))

    return  node
def printTree(node, tabIndex):
    if(node.is_leaf):
        print((tabIndex * '\t') +  " VALUE = ", node.classValue, "depth = ", node.height)
        return
    else:
        print((tabIndex * '\t') + "Tested by attr nr: ", node.testedAttributeIndex)

    tabIndex += 1

    for ch in node.children:
        printTree(ch, tabIndex)

def fitTree(node, example):
    if(node.is_leaf):
        return node.classValue

    currentTestedAttrIndex = node.testedAttributeIndex
    exampleValue = example[currentTestedAttrIndex]


    if(exampleValue == node.splitValue):
        classif = fitTree(node.children[0], example)
    else:
        classif = fitTree(node.children[1], example)

    return classif
def testTree(node, dtset):
    correctAnsw = 0
    for ex in dtset:
        ex_data = ex[:-1]
        realClassValue = ex[-1]
        treeClassif = fitTree(node, ex_data)

        if(treeClassif == realClassValue):
            correctAnsw += 1

    return correctAnsw/len(dtset)

def main():

    argv = sys.argv
    dataRatio = float(argv[3])
    daaata = dataBase(argv[1])
    print(argv[1])
    newData = [[row[index] for index in range(0, int(argv[4]))] for row in daaata]

    allExamples = len(newData)
    trainDataIndex = random.sample(range(0,allExamples), int(allExamples * dataRatio))
    trainData = [newData[index] for index in trainDataIndex]

    testData = [ex for ex in newData]
    root = buildTree(trainData, None, tests, int(argv[2]))


    print(testTree(root, testData))
if __name__ == "__main__":
    main()