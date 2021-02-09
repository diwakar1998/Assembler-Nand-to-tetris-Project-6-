import tables as tb

#CodeCleaner
def cleanCode(spoiledList):
# Cleans comments '//blablabla' outside code and '\n' this is newline
    size = len(spoiledList)
    finalIndex = size-1
    while finalIndex != -1 :
        currentLine = spoiledList[finalIndex]
        forCommentsOutside = currentLine[:2]
        if currentLine == '\n':
            spoiledList.remove(currentLine)
        if forCommentsOutside == '//':
            spoiledList.remove(currentLine)    
        finalIndex = finalIndex -1
    #the obtained code here is devoid of comments and empty spaces

# Removes '\n' , '   ' empty space , inline comments  
    sizecodeCleaned = len(spoiledList)
    finalIndexcodeCleaned = sizecodeCleaned-1  
    subStringCheck1 = '\n'
    stringCheck = '/'
    finalCode = []
    while finalIndexcodeCleaned != -1 :
        currentLinecode = str(spoiledList[finalIndexcodeCleaned])
        if currentLinecode.endswith(subStringCheck1):
            currentLinecode = currentLinecode[:-len(subStringCheck1)]
        indextoremove = currentLinecode.find(stringCheck)
        if (indextoremove != -1):
            currentLinecode = currentLinecode[0:indextoremove] 
        for eachChar in currentLinecode:
            if eachChar == " ":
                currentLinecode = currentLinecode.replace(eachChar,"")           
        finalCode.append(currentLinecode)
        finalIndexcodeCleaned = finalIndexcodeCleaned -1
    finalCode.reverse()
    return finalCode

#Assembler
def assembler(cleanCode):
    size = len(cleanCode)
    finalIndex = size-1
    hackCode = []
#Main loop
    while finalIndex != -1 :
        ins = str(cleanCode[finalIndex])
#takes care of A Instruction
        if (ins[0] == "@"):        
            ins = str(bin(int(ins[1:])).replace("0b",""))
            ins = lengthFixer(ins,16)
            hackCode.append(ins+'\n')

#takes care of c instruction        
        if (ins.find("=") != -1):            
            #to find destination part
            indexofeq = ins.find("=")
            destString = ins[0:indexofeq] 
            desBin = getEqDestString(destString)            
            #to find operation part
            opString = ins[indexofeq+1:]
            compBin = getEqOpString(opString)  
            tempIns = "111" + compBin+desBin + "000"+'\n'
            hackCode.append(tempIns)
#takes care of jump instruction
        if(ins.find(";") != -1):
            #operation part
            indexofjmp = ins.find(";")+1
            opString = ins[:indexofjmp-1]
            opPart = getEqOpString(opString)
            #jump part
            jmpString = ins[indexofjmp:]
            jmpBin = getEqJmpString(jmpString)
            tempIns = "111" + opPart + "000"+jmpBin+'\n'
            hackCode.append(tempIns)
        finalIndex = finalIndex-1

    hackCode.reverse()
    return hackCode


def lengthFixer(ins,size):
    while (len(ins) < size):
        ins = '0'+ ins 
    return ins

def getEqDestString(destStr):
    desBinValue = tb.dest_table.get(destStr)
    return desBinValue

def getEqOpString(opString):
    compBinValue = tb.comp_table.get(opString)
    return compBinValue
    
def getEqJmpString(jmpString):
    jmpBinValue = tb.jump_table.get(jmpString)
    return jmpBinValue
