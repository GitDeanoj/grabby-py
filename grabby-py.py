
import requests
import shutil
import os
import sys
import time

exit = False
downloading = False
count = 0

def ImageDwnLoop(strFilename, charDelim):
    strProg = ""

    file1 = open(strFilename, 'r')
    Lines = file1.readlines()

    intProgCount = 0
    intTotalCount = Lines.count


    for line in Lines:
        listImages =  str(line).split(charDelim) # char to split images
        
        for s in listImages:
            if(intProgCount <= intTotalCount):
                strProg = "Progress: " + str(intProgCount) + "/" + str(intTotalCount)
                print (strProg, end="\r")

            r = requests.get(s, stream=True, headers={'User-agent': 'Mozilla/5.0'}) # "headers=" fixes issue downloading large amounts of images(zero disk space images)
            if r.status_code == 200:
                with open(str(count) + strFilename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        
        intProgCount+=1
    print(strProg + "\nDone.")

def PrintDwnLoop(strFilename, charDelim):
    file1 = open(strFilename, 'r')
    Lines = file1.readlines()
    listImages = [];
    listAllImages = [];

    for line in Lines:
        listImages =  str(line).split(charDelim) # char to split images
        
        for s in listImages:
            listAllImages.append(s)
            
    count=1
    for strTemp in listAllImages:
        if(count < 6):
            print ("Item " + str(count) + ": " + strTemp)
            count +=1

def SetDestination(strDirectory):
    if not os.path.exists(strDirectory):
        inputDir = input('\"' + strDirectory + '\" not found, create a new directory? (type y or n):')
        if(inputDir == "y" or inputDir == "Y"):
            os.makedirs(strDirectory)
        else:
            return False
    return True

def checkInputFile(inputFile):
    file_exists = os.path.exists(inputFile)
    return(file_exists)

def startFunc(boolInputFound):
    print("   ____           _     _             ____ \n"+
    "  / ___|_ __ __ _| |__ | |__  _   _  |  _ \ _   _ \n"+
    " | |  _| '__/ _` | '_ \| '_ \| | | | | |_) | | | |\n"+
    " | |_| | | | (_| | |_) | |_) | |_| | |  __/| |_| |\n"+
    "  \____|_|  \__,_|_.__/|_.__/ \__, | |_|    \__, |\n"+
    "                              |___/         |___/ \n\n\n")
    boolOutputReady = False

    while(boolInputFound == False):
        inputFile = input('Enter your input:')
        
        if(inputFile == "--exit"):
            sys.exit()

        if(checkInputFile(inputFile)):
            boolInputFound = True
           
    while(boolOutputReady == False):
        inputChar = input('Enter your split char:')
        PrintDwnLoop(inputFile, inputChar)

        inputContinue = input('Does this look correct? (type y or n):')
        if(inputContinue == "y" or inputContinue == "Y"):
            boolOutputReady = True
    
    boolReadyDownload = False
    while(boolReadyDownload == False):
        inputLoc = input('Output location:')
        if(SetDestination(inputLoc)):
            boolReadyDownload = True

    inputDwn = input('Start Download? (type y or n):')
    if(inputDwn == "y" or inputDwn == "Y"):
        ImageDwnLoop(inputLoc, inputChar)

boolInputFound = False
startFunc(boolInputFound)
