import methodsRequired as mr
import tables as tb
import finalTranslator as ftr

def Assembler(spoiledCode):
    #method takes care of all method callings
    cleanCodeWithLabels = mr.cleanCode(spoiledCode)
    cleanCodeWithVariables = ftr.removeLabels(cleanCodeWithLabels)
    cleanCode = ftr.removeVariables(cleanCodeWithLabels)
    hackCode = mr.assembler(cleanCode)
    return hackCode

def removeVariables(codeWithVariables): 
    size = len(codeWithVariables)
    x=0
    variableList = []   
    while(x<size-1):
        currentIns = codeWithVariables[x]
        if(currentIns[0]=="@"):
            checkforVariable = currentIns[1:]
            try:
                ifint = int(checkforVariable)
            except ValueError:
                if(checkforVariable not in variableList):
                    variableList.append(checkforVariable)
        x=x+1
    #print(variableList)

    size = len(variableList)
    x=0
    startaddressvariable = 16
    variableAddressList = []
    
    while(x<size):
        variableAddressList.append(str(startaddressvariable))
        startaddressvariable = startaddressvariable + 1
        x=x+1
    #print(variableAddressList)
    variabledict = {}

    for i in variableList:
        variabledict[i] = variableAddressList[variableList.index(i)]

    #print(variabledict)

    size = len(codeWithVariables)
    x=0
    variableList = []   
    temp=""
    while(x<size-1):
        currentIns = codeWithVariables[x]
        if(currentIns[0]=="@"):
            checkforVariable = currentIns[1:]
            if(checkforVariable in variabledict):
                temp = "@"+str(variabledict[checkforVariable])
                codeWithVariables[x]= temp
        x=x+1
    #print(codeWithVariables)
    return codeWithVariables

def removeLabels(codeWithLabels):
    size = len(codeWithLabels)
    x=0
    #print(codeWithLabels)
    templist = codeWithLabels
    #takes care of all @ ins. in the predef table
    while (x < size-1):        
        currentIns = codeWithLabels[x]  
        toreplace = ""
        if(currentIns[0]=="@"):
            checkVal = currentIns[1:]
            if(checkVal in tb.predef_table):
                toreplace = "@" +str(tb.predef_table[checkVal])
                templist[x] = toreplace     
        x= x+1     
    
    #creating code address list
    tempaddress = []
    address = 0
    x=0
    size = len(templist)
    while (x < size-1):
        currentIns = templist[x]
        tempaddress.insert(x,address)                 
        if(currentIns[0]=="("):
            tempaddress[x]=address
            address = address - 1
        address = address +1
        x=x+1
    # print(tempaddress)
    # print(templist)

    #taking all labels into a list and mark their indexes
    labelList =[]
    labelIndexList=[]
    x=0
    size = len(templist)
    while (x < size-1):
        currentIns = templist[x]
        currentInsAdd = tempaddress[x]
        length = len(currentIns)
        if(currentIns[0] == "("):
            labelList.insert(x,currentIns[1:length-1])
            labelIndexList.insert(x,currentInsAdd)
        x=x+1
    # print(labelList)
    # print(labelIndexList)
    #construct label table
    labelDict = {}

    for i in labelList:
        labelDict[i] = labelIndexList[labelList.index(i)]
    #print(labelDict)
    ######################################
    #up until here the label table is prepared

    #to replace labels in the code
    x=0
    size = len(templist)
    temp2list = templist

    while (x < size-1):
        currentIns = temp2list[x]
        toreplace = ""
        if(currentIns[0]=="@"):
            checklabel = currentIns[1:]
            if(checklabel in labelDict):
                toreplace = "@" +str(labelDict[checklabel])
                temp2list[x] = toreplace     
        x= x+1  
    
    #removes labels
    x=0
    size = len(temp2list)
    temp3list = temp2list
    for ins in temp3list:
        if(ins[0]=="("):
            temp3list.remove(ins)
    return temp3list