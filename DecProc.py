import xml.etree.ElementTree
from decimal import Decimal
import re
decTreeXmlFilePath = "./decTreeSample.xml"
nameArray = ("speed","height","enemy","mach","sideslip")
valueArray = (1.5,1001,5,100,700)
def expressProc(express,value):
    expressList = re.findall(r"[\[\(](?:-?\d+(?:\.\d+)?)?,(?:-?\d+(?:\.\d+)?)?[\]\)]|-?\d+(?:\.\d+)?",express)
    print expressList
    for i in expressList:
        if i.find(",") == -1:
            if Decimal(i) == Decimal(value):
                return True
            else:
                continue
        else:
            leftNumStr = re.search(r"(?:-?\d+(?:\.\d+)?)?,",i).group(0)
            rightNumStr = re.search(r",(?:-?\d+(?:\.\d+)?)?",i).group(0)
            leftNum = None
            rightNum = None
            leftSign = i[0]
            rightSign = i[len(i)-1]
            if len(leftNumStr) !=  1:
                leftNum = Decimal(leftNumStr[:len(leftNumStr)-1])
            if len(rightNumStr) !=  1:
                rightNum = Decimal(rightNumStr[1:])
            if leftNum == None and rightNum !=  None:
                if rightSign == ')' and value < rightNum:
                    return True
                if rightSign == ']' and value<=rightNum:
                    return True
            if rightNum == None and leftNum !=  None:
                if leftSign == '(' and value > leftNum:
                    return True
                if leftSign == '[' and value >=rightNum:
                    return True
            if rightNum !=  None and leftNum != None:
                if value<rightNum and value>leftNum:
                    return True
                if value == rightNum and rightSign == ']':
                    return True
                if value == leftNum and leftSign == '[':
                    return True
            continue
    return False

def singleCondProc(cond,nameArray,valueArray):
    if cond.tag == "and":
        for subCond in cond:
            if singleCondProc(subCond,nameArray,valueArray) == False:
                return False
        return True
    if cond.tag == "or":
        for subCond in cond:
            if singleCondProc(subCond,nameArray,valueArray) == True:
                return True
        return False
       
    for index in range(len(nameArray)):
        if nameArray[index] == cond.tag:
            return expressProc(cond.text,valueArray[index])
    return False
def condsProc(node,nameArray,valueArray):
    for cond in node.findall("./"):
        if cond.tag !=  "name" and cond.tag !=  "node":
            if singleCondProc(cond,nameArray,valueArray) is False:
                return False
    return True


def nodeProc(node,nameArray,valueArray):
    if len(node.findall("./node")) == 0:
        return node.find("./name").text
    for subNode in node.findall("./node"):
        if condsProc(subNode,nameArray,valueArray) == True:
            return nodeProc(subNode,nameArray,valueArray)
    return "not in this tree" 


def decProc(decTreeXmlFile, nameArray,valueArray):
    root = xml.etree.ElementTree.parse(decTreeXmlFile).getroot()
    return nodeProc(root,nameArray,valueArray)
 
ans = decProc(decTreeXmlFilePath,nameArray,valueArray)
print  ans
   
