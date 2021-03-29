import openpyxl
import keyboard
import webbrowser
from  algClass import Alg
import os
import subprocess
import pyautogui
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import cv2
import time

def url(Cube, scramble):#gen url of solve to algcubing
    sol = str(Cube.solution)
    scramble = str(scramble)
    scramble = scramble.replace('\'', "-")
    scramble = scramble.replace(" ", "_")
    newSol = "https://alg.cubing.net/?setup="
    newSol += scramble
    newSol += "%0A&alg="
    solWrong = ""
    allSol = sol.split(" ")
    count = 0
    if (Cube.moveWrong == 0):
        sol = sol.replace("\'", "-")
        sol = sol.replace(" ", "_")
        newSol += sol
    else:
        for x in allSol:

            x = x.replace("\'", "-")
            solWrong += x +"_"
            if(count == Cube.moveWrong):
                solWrong+="%2F%2Fmistake_from_here%0A"
            count+=1

        newSol+=solWrong

    newSol+="%0A"
    return newSol





def playVid(Cube):#play video of so;ve from the sec of mistake
    f = open('playVid.txt', 'w')
    f.write(str(Cube.secMistake))
    f.close()
    os.system('playVid.py')

### Setup!!! ###
exeOrder = "EdgesCorners"

class DNFanalyzer:
    alg = Alg("")
    scrambleToExe = ""
    scrambleApplied = ""
    scramble = True
    memo = False
    solving = False
    startMemoTime = time.time()
    memoTime = time.time()
    startExeTime = time.time()
    exeTime = time.time()
    Recon = ""
    secMistake = 0.0
    success = False
    solveTime = 0
    exeMoves = []#[move, time, cornersSolved, edgesSolved, index]
    scrambleRaw = 0
    parity = False
    solveNum = 0
    solution = ""
    moveWrong = 0

def saveSolve(Cube):#save results to excel
    memo = Cube.memoTime
    exce = Cube.exeTime
    all = memo + exce

    isSolved = Cube.alg.checkSolved()
    succsses = ""
    print("all: ", all, ", memo: ", memo, ", exe: ", exce)
    a = input("Solved? (y/n)")#make sure the result is right
    if(a == "y"):
        succsses = "yes"
        Cube.secMistake = 0.0
    else:
        succsses = "no"
    row = Cube.scrambleRaw

    wb = openpyxl.load_workbook(os.getcwd() + "\RotoDNFStats.xlsx", data_only="yes")
    ws = wb["RotoStats"]
    strRow = str(Cube.scrambleRaw)
    ws.cell(row, 3).value = round(memo,2)
    ws.cell(row, 4).value = round(exce,2)
    ws.cell(row, 5).value = round(all,2)
    ws.cell(row, 6).value = round(Cube.secMistake, 2)
    ws.cell(row, 7).value = succsses
    ws.cell(row,10).value = url(Cube,ws.cell(row,1).value)
    #ws.cell(row, 8).value = "=HYPERLINK(" + "\"C:\Python\PythonWork\BLD\RotoBLD\RotoDNF\\videos\solve" + strRow +".avi\""+", "+"\"solve"+strRow+"\")"
    ws.cell(row, 9).value =  Cube.solution
    wb.save(os.getcwd() + "\RotoDNFStats.xlsx")

def resetCube(Cube):
    Cube.solving = False
    Cube.moves = []
    Cube.moveNumber = 0
    Cube.alg.reset()
    Cube.moveNumber = 0
    Cube.exeMoves = []
    Cube.scrambleToExe = getScramble(Cube)
    Cube.scrambleApplied = ""
    Cube.scramble = True
    Cube.solving = False
    Cube.secMistake = 0.0
    Cube.startMemoTime = time.time()
    Cube.memoTime = time.time()
    Cube.startExeTime = time.time()
    Cube.exeTime = time.time()
    Cube.success = False
    Cube.rawSol = []
    Cube.mostPiecesSolved = 0
    Cube.solution = ""
    Cube.moveWrong = 0


def getScramble(Cube):# returns Cube object of scramble

    wb = openpyxl.load_workbook(os.getcwd() + "\RotoDNFStats.xlsx", data_only="yes")
    ws = wb["RotoStats"]
    i=1
    while(ws.cell(i,2).value != "no"):
        i+=1
    ws.cell(i,2).value = "yes"
    wb.save(os.getcwd() + "\RotoDNFStats.xlsx")
    Cube.scrambleRaw = i
    numSolve = open('vidNum.txt', 'w')
    numSolve.write(str(Cube.scrambleRaw))
    numSolve.close()
    Cube.scrambleApplied = ws.cell(i,1).value
    return ws.cell(i,1).value



def findNewMoves(lastMoves, currentMoves):#get last moves done
    lastLen = len(lastMoves)
    if (lastLen != len(currentMoves)):
        return currentMoves[lastLen:]
    return []
def takeCorners(elem):
    return elem[2]

def takeEdges(elem):
    return elem[3]
def takeIndex(elem):
    return elem[4]
def takeTime(elem):
    return elem[1]
def initTimer(browser):# i use csTimer because the gan 356i is encrypted and i didn't managed to solve it in python, so i just use cs
    browser.get("https://cstimer.net")
    pyautogui.click(42, 160)  # options
    time.sleep(1)
    pyautogui.click(313, 400)  # timer
    time.sleep(1)
    pyautogui.click(436, 413)  # timer
    time.sleep(1)
    pyautogui.click(443, 511)  # giiker
    time.sleep(8)
    pyautogui.click(588, 146)  # GAN
    time.sleep(1)
    pyautogui.click(616, 487)  # OK
    time.sleep(12)
    pyautogui.click(431, 189)  # accecpt
    time.sleep(3)
    pyautogui.rightClick(431, 189)
    time.sleep(1)
    pyautogui.click(369, 420)
    time.sleep(2)
    pyautogui.click(664, 141)  # console
    time.sleep(2)
    pyautogui.click(539, 681)  # console
    pyautogui.write('console.clear()')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.write("giikerutil")
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.click(526, 265)
    time.sleep(0.5)
    pyautogui.click(540, 367)
    time.sleep(0.5)
    pyautogui.click(551, 496)
    time.sleep(0.5)
    pyautogui.click(560, 510)
    time.sleep(0.5)
    pyautogui.scroll(-500)
    time.sleep(0.5)
    pyautogui.rightClick(589, 584)
    time.sleep(0.5)
    pyautogui.click(500, 658)
    time.sleep(0.5)
    pyautogui.click(39, 113)
    time.sleep(0.5)
    return browser

def initCube():
    browser1 = webdriver.Chrome(ChromeDriverManager().install())
    browser = initTimer(browser1)
    movesList = ["U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'", "D", "D2", "D'", "L", "L2", "L'", "B", "B2", "B'"]
    lastMoves = []
    script = "return temp1"
    Cube = DNFanalyzer()

    while(True):
        print("\n")
        resetCube(Cube)
        Cube.alg.move(Cube.scrambleToExe)  # put scramble moves ready to execute
        Cube.alg.executeAlg()
        Cube.alg.reverseSelf()

        print("press space when cube is solved")
        while(keyboard.is_pressed(' ') == False):
            pass
        moves = browser.execute_script(script)
        newMoves = findNewMoves(lastMoves, moves)
        lastMoves = moves
        print(Cube.scrambleToExe)
        while(Cube.scramble == True):#Scramble Cube
            moves = browser.execute_script(script)
            newMoves = findNewMoves(lastMoves, moves)
            lastMoves = moves
            for move in newMoves:
                #print(" ",movesList[move], end="", flush=True)
                Cube.alg.executeAlgWithMoves(movesList[move])
                if(Cube.alg.checkSolved() == True):
                    Cube.scramble = False

        flagSpace =False
        c = 0
        print("\npress space to start memo")
        while(flagSpace == False):
            if(keyboard.is_pressed(' ') == True):
                c+=1
            if(c==3):
                flagSpace = True
                c=0
        f= open('boolVid.txt', 'w')#used txt file bool because i didn't managed to figure out how to do it in one file....
        f.write('T')
        f.close()
        subprocess.Popen(["python","recordVid.py"])#record video while solving
        while(open('StartRec.txt').read(1) != 'T'):
            pass
        Cube.solveTime = time.time()
        print("press s to start solve")
        while (keyboard.is_pressed('s') == False):
            pass
        print("Solve!")
        Cube.memoTime = time.time()- Cube.solveTime
        moveCount = 0
        Cube.exeTime = time.time()
        exeMoves = []
        moves = []
        while (keyboard.is_pressed(' ') == False):  #While you are solving the cube
            moves = browser.execute_script(script)
            newMoves = findNewMoves(lastMoves, moves)
            lastMoves = moves

            for move in newMoves:
                exeMoves.append([movesList[move],time.time(), 0, 0, moveCount])
                moveCount+=1
        Cube.exeTime = time.time()- Cube.exeTime
        a = open('boolVid.txt','w')
        a.write('F')
        a.close()

        #finished solve
        Cube.alg.reset()
        Cube.alg.executeAlgWithMoves(Cube.scrambleToExe)
        Cube.alg.reverseSelf()
        if(Cube.alg.cornerEven() == True):
            Cube.parity = False
            print("no parity")
        else:
            Cube.parity = True
            print("parity")
        #Cube.alg.printState()
        for move in exeMoves:
            Cube.alg.movesToExecute = move[0]
            Cube.alg.reverseSelf()
            Cube.alg.executeAlg()
            Cube.alg.reverseSelf()
            #print("move is :", move[0]," moveNum ", move[4])
            #Cube.alg.printState()#correct  s
            m = move[0]
            t = move[1]
            moveC = move[4]
            corSol = Cube.alg.countSolvedCor()#correct
            edSol = Cube.alg.countSolveEdges()#correct
            Cube.exeMoves.append([m,t,corSol,edSol,moveC])#correct
        sortedByIndex = Cube.exeMoves.copy()
        sortedByIndex.reverse()
        Cube.exeMoves.sort(key=takeEdges, reverse=True)
        sortedByEdges = Cube.exeMoves.copy()  # works
        Cube.exeMoves.sort(key=takeCorners, reverse=True)
        sortedByCorners =  Cube.exeMoves.copy()
        Cube.solution = sortedByIndex.copy()

        print("sortedByEdges ", *sortedByEdges, sep="\n")
        print("sortedByCorners ", *sortedByCorners, sep="\n")
        print("sortedByIndex ", *sortedByIndex, sep="\n")

        solve = ""
        sortedByIndex.reverse()
        for x in sortedByIndex:
            solve += " " + x[0]

        Cube.solution = solve
        sortedByIndex.reverse()
        if(exeOrder == "EdgesCorners"):
            if(sortedByIndex[0][2] == 8 and sortedByIndex[0][3] == 12):

                print("Solved!")
            elif((sortedByEdges[0][3] == 12 and Cube.parity == False) or (sortedByEdges[0][3] >=10 and Cube.parity == True)):# if there is parity' and max edges >= 10 then it means edges are good
                print("you solved all edges correctly")
                # corners are wrong
                maxCornersFullEdges = []
                for x in sortedByCorners:
                    if((x[3] == 12 and Cube.parity == False) or (x[3] >= 10 and Cube.parity == True)):
                        maxCornersFullEdges.append(x)

                tempSortedIndex = sortedByIndex.copy()
                maxCornersFullEdges.sort(key=takeTime, reverse=True)
                print("maxCornersFullEdges ", *maxCornersFullEdges, sep="\n")
                if(tempSortedIndex[0][3] != 12):#if all edges are not right at the final state, then take the last time all edges were good( mistake in excecution
                    mistakeMove =  maxCornersFullEdges[0]
                else:#take the first time all edges were good (did the wrong Alg)
                    maxCornersFullEdges.reverse()
                    mistakeMove = maxCornersFullEdges[0]
                Cube.moveWrong = mistakeMove[4]
                Cube.secMistake = round(mistakeMove[1]-Cube.solveTime,2) #the time of the first time you had max corners solved with full edges
                print("mistake time was ",Cube.secMistake  , " seconds from the begining")
                print("the last move right  ", mistakeMove[4], "move, which was ", mistakeMove[0][0])
                playVid(Cube)

            else: #not all edges are good find the most edges solved
                max = sortedByEdges[0][3]
                maxEdgesSolved = []
                for move in sortedByEdges:
                    if (move[3] == max):
                        maxEdgesSolved.append(move)
                maxEdgesSolved.sort(key=takeTime)
                sortedByMaxEdgesTime = maxEdgesSolved.copy()
                Cube.moveWrong = sortedByMaxEdgesTime[0][4]
                Cube.secMistake = round(sortedByMaxEdgesTime[0][1]-Cube.solveTime, 2) # max edges solved first time
                print("mistake time was ",Cube.secMistake, " seconds from the begining")
                print("the last move right  ", sortedByMaxEdgesTime[0][4], "move, which was ", sortedByMaxEdgesTime[0][0])
                playVid(Cube)

        else:
            if (sortedByIndex[0][2] == 8 and sortedByIndex[0][3] == 12):
                print("Solved!")

            elif ((sortedByCorners[0][2] == 8 and Cube.parity == False) or (sortedByCorners[0][2] >=6 and Cube.parity == True)):
                print("you solved all corners correctly")
                #not all edges are good

                maxEdgesFullCorners = []#edges are wrong

                for x in sortedByEdges:
                    if ((x[2] == 8 and Cube.parity == False) or (x[2] >= 6 and Cube.parity == True)):
                        maxEdgesFullCorners.append(x)
                maxEdgesFullCorners.sort(key = takeEdges, reverse=True)  # all moves that edges was max
                max = maxEdgesFullCorners[0][2]
                maxEdgesSolved = []

                maxEdgesFullCorners.sort(key=takeTime, reverse=True)
                tempSortedIndex = sortedByIndex.copy()
                if (tempSortedIndex[0][3] != 8):  # if all edges are not right at the final state, then take the last time all edges were good
                    mistakeMove = maxEdgesFullCorners[0]
                else:  # take the first time all edges were good
                    maxEdgesFullCorners.reverse()
                    mistakeMove = maxEdgesFullCorners[0]
                Cube.moveWrong = mistakeMove[4]
                sortedByMaxEdgesTime = maxEdgesFullCorners.copy()
                Cube.secMistake =round(mistakeMove[1]-Cube.solveTime ,2)# the time of the first time you had max corners solved
                print("mistake time was ", Cube.secMistake, " seconds from the begining")
                print("last move right ", mistakeMove[4], "move, which was ",
                      mistakeMove[0])

                playVid(Cube)
            else:  # not all corners are good
                max = sortedByCorners[0][2]
                maxCornersSolved = []
                for move in sortedByEdges:
                    if (move[2] == max):
                        maxCornersSolved.append(move)
                maxCornersSolved.sort(key=takeTime)
                sortedByMaxCornersTime = maxCornersSolved.copy()
                Cube.moveWrong = sortedByMaxCornersTime[0][4]
                Cube.secMistake = round(sortedByMaxCornersTime[0][1]-Cube.solveTime, 2) # the time of the first time you had max corners solved
                print("mistake time was ", Cube.secMistake , " seconds from the begining")
                print("last move right ", sortedByMaxCornersTime[0][4], "move, which was ", sortedByMaxCornersTime[0][4])
                playVid(Cube)
        saveSolve(Cube)
initCube()
