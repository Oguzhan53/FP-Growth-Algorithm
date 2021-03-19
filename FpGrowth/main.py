# OGUZHAN SEZGIN 
# DATA MINING - HOMEWORK 

import pandas as pd
from anytree import Node, RenderTree, ContRoundStyle, findall
from texttable import Texttable


def isNaN(num):
    return num != num


def addElement(freq_array, element):
    for i in range(len(freq_array)):
        if freq_array[i][0] == element:
            freq_array[i][1] += 1
            return
    freq_array.append([element, 1])


def mergeSort(arr):
    if len(arr) > 1:

        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        mergeSort(L)
        mergeSort(R)
        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i][1] > R[j][1]:
                arr[k] = L[i]
                i += 1
            elif L[i][1] == R[j][1]:
                i1 = 0
                fl = True
                while i1 < len(L[i][0]) and i1 < len(R[j][0]):
                    a = ord(L[i][0][i1])
                    b = ord(R[j][0][i1])
                    if ord(L[i][0][i1]) < ord(R[j][0][i1]):
                        arr[k] = L[i]
                        i += 1
                        fl = False
                        break
                    elif ord(L[i][0][i1]) != ord(R[j][0][i1]):
                        break
                    i1 += 1
                if fl:
                    arr[k] = R[j]
                    j += 1

            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def isCotains(array, element):
    for i in range(len(array)):
        if (array[i][0] == element):
            return i
    return -1


def createOrderedSet(dataArray, freqArray):
    new_array = [[]]
    flag = False
    index = 0
    for i in range(len(dataArray)):
        if flag:
            mergeSort(new_array[index])
            index += 1
            flag = False
            new_array.append([])
        for j in range(len(dataArray[i])):
            ti = isCotains(freqArray, dataArray[i][j])
            if ti != -1:
                new_array[index].append(freqArray[ti])
                flag = True
    mergeSort(new_array[-1])
    return new_array


def removeElement(freqArray, min_sup):
    new_array = []
    for i in range(len(freqArray)):
        if freqArray[i][1] >= min_sup:
            new_array.append(freqArray[i])

    return new_array


def createDataArray():
    data = pd.read_csv("small_data.csv")
    dataArray = data.values
    # dataArray = [["E", "K", "M", "N", "O", "Y"], ["D", "E", "K", "N", "O", "Y"], ["A", "E", "K", "M"],
    #              ["C", "K", "M", "U", "Y"], ["C", "E", "I", "K", "O"]]

    freqArray = [[0 for x in range(2)] for y in range(1)]

    for i in range(len(dataArray)):
        for j in range(len(dataArray[i])):
            var = dataArray[i][j]
            if not isNaN(var):
                addElement(freqArray, var)
    freqArray.pop(0)
    return dataArray, freqArray


def createFTree(orderedSet):
    root = Node("root", num=0)
    temp = root
    for i in range(len(orderedSet)):
        temp = temp.root
        nameArray = []
        for j in range(len(orderedSet[i])):
            nameArray.append(orderedSet[i][j][0])
        path = findall(root, filter_=lambda node: node.name in nameArray)
        if path != ():
            temp = root
            j = 0
            while j < len(nameArray):
                if temp.name == nameArray[j]:
                    temp.num += 1
                    j += 1
                    if j == len(nameArray):
                        break
                fl = True
                for j1 in range(len(temp.children)):
                    if temp.children[j1].name == nameArray[j]:
                        temp = temp.children[j1]
                        # if j == len(nameArray) - 1:
                        #     temp.num += 1
                        fl = False
                        break
                if fl:
                    while j < len(nameArray):
                        chl = Node(nameArray[j], parent=temp, num=1)
                        temp = chl
                        j += 1
                    break


        else:
            for j in range(len(orderedSet[i])):
                chl = Node(orderedSet[i][j][0], parent=temp, num=1)
                temp = chl
    return root


def createConditionalPattern(root, freqArray):
    cPBase = [[[]]]
    for i in range(len(freqArray)):
        path = findall(root, filter_=lambda node: node.name in freqArray[-1 - i][0])
        cPBase[i].append(freqArray[-1 - i][0])
        cPBase.append([[]])
        for j in range(len(path)):
            num = path[j].num

            name = []
            temp = path[j].parent
            while temp.name != "root":
                name.append(temp.name)
                temp = temp.parent
            if name != []:
                cPBase[i][0].append(num)
                cPBase[i][0].append(name)

    cPBase.pop()
    return cPBase


def findSubArrays(arr, start, end, subs):
    if end == len(arr):
        return
    elif start > end:
        return findSubArrays(arr, 0, end + 1, subs)
    else:
        subs.append(arr[start:end + 1])
        return findSubArrays(arr, start + 1, end, subs)


def findCommon(list):
    if list != []:
        i = 1
        minArr = list[1]
        minLen = len(list[1])

        while i < (len(list)):
            if minLen > len((list[i])):
                minLen = len(list[i])
                minArr = list[i]
            i += 2
        subArr = []
        findSubArrays(minArr, 0, 0, subArr)

        comArr = []
        first = True
        for j in range(len(subArr)):
            num = 0
            fl = True
            i = 1
            while i < (len(list)):
                if not all(elem in list[i] for elem in subArr[j]):
                    fl = False
                    break
                else:
                    num += list[i - 1]

                i += 2
            if fl and first:
                first = False
                comArr.append(subArr[j])
                comArr.append(num)
            elif fl and len(subArr[j]) > len(comArr[0]):
                comArr[0] = subArr[j]
                comArr[1] = num

        return comArr
    else:
        return []


def createConditionalPatternTree(cPBase):
    cpTree = []
    for i in range(len(cPBase)):
        cpTree.append(findCommon(cPBase[i][0]))
        cpTree[i].append(cPBase[i][1])
    return cpTree


def generateFrequentPattern(cFPTree):
    fPGen = [[[]]]
    i1 = 0
    for i in range(len(cFPTree)):
        if len(cFPTree[i]) != 1:
            tempArr = cFPTree[i][0].copy()
            tempArr.append(cFPTree[i][-1])
            if len(tempArr) > 2:
                subs = []
                findSubArrays(tempArr, 0, 0, subs)
                j1 = 0
                for j in range(len(subs)):
                    if len(subs[j]) > 1:
                        fPGen[i1][j1].append(subs[j])
                        fPGen[i1][j1].append(cFPTree[i][1])
                        fPGen[i1].append([])
                        j1 += 1
                fPGen[i1].pop()

            else:
                fPGen[i1][0].append(tempArr)
                fPGen[i1][0].append(cFPTree[i][1])
            fPGen[i1].append(cFPTree[i][-1])
            fPGen.append([[]])
            i1 += 1
    fPGen.pop()
    return fPGen


def printResults(cPBase, cFPTree, fPGen):
    t = Texttable()
    t.add_row(["ITEM", "CONDITIONAL PATTERN BASE"])
    for i in range(len(cPBase)):
        t.add_row([cPBase[i][-1], cPBase[i][0]])

    t2 = Texttable()
    t2.add_row(["ITEM", "CONDITIONAL FP TREE"])

    for i in range(len(cFPTree)):
        if len(cFPTree[i]) > 1:
            temp = []
            for j in range(len(cFPTree[i]) - 1):
                temp.append(cFPTree[i][j])
            t2.add_row([cFPTree[i][-1], temp])

        else:
            t2.add_row([cFPTree[i][0], " "])

    t3 = Texttable()
    t3.add_row(["ITEM", "FREQUENT PATTERN GENERATED"])
    for i in range(len(fPGen)):
        temp = []
        for j in range(len(fPGen[i]) - 1):
            temp.append(fPGen[i][j])
        t3.add_row([fPGen[i][-1], temp])
    print(t.draw())
    print(t2.draw())
    print(t3.draw())


minSup = 2
dataArray, freqArray = createDataArray()
mergeSort(freqArray)
freqArray = removeElement(freqArray, minSup)
orderedSet = createOrderedSet(dataArray, freqArray)
root = createFTree(orderedSet)
print(RenderTree(root, style=ContRoundStyle()))
cPBase = createConditionalPattern(root, freqArray)
cFPTree = createConditionalPatternTree(cPBase)
fPGen = generateFrequentPattern(cFPTree)
printResults(cPBase, cFPTree, fPGen)
print("END")
