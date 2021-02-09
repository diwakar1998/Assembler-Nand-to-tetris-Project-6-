import sys
import finalTranslator as ftr
import methodsRequired as mr

#opening the file
filename = sys.argv[1]
file = open(filename+".asm",'r') 
#file = open('Rect.asm','r') 
spoiledCodeList = file.readlines()

hackCode = ftr.Assembler(spoiledCodeList)

#Cleaning the code checks for comments, new lines and comments inline of code
print(hackCode)
file = open(filename+".hack",'w')
file.writelines(hackCode)
