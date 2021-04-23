from decode_gan import aes128, decData
from bleak import BleakClient
import openpyxl
import keyboard
import websockets
import webbrowser
from  algClass import Alg
import os
import subprocess
import time
import asyncio
from trainer import Trainer, get_new_moves
import msvcrt as m
import pyperclip
import socket
import kociemba
from BLD_solve_parse import parse_solve


### Setup!!! ###
exeOrder = "EdgesCorners"
import json






class DNFanalyzer:
    def __init__(self):
        self.facelet_moves = ""
        self.fail_reason = ""
        self.frame_rate = 0
        self.url = ""
        self.alg = Alg("")
        self.scrambleToExe = ""
        self.scrambleApplied = ""
        self.scramble = True
        self.memo = False
        self.solving = False
        self.startMemoTime = time.time()
        self.memoTime = time.time()
        self.startExeTime = time.time()
        self.exeTime = time.time()
        self.Recon = ""
        self.secMistake = 0.0
        self.success = False
        self.solveTime = 0
        self.exeMoves = []#[move, time, cornersSolved, edgesSolved, index]
        self.scrambleRow = 0
        self.parity = False
        self.solveNum = 0
        self.solution = ""
        self.moveWrong = 0
        self.ws_rec = None
        self.ws_rec_ip = "127.0.0.1"
        self.ws_rec_port = 12345
        self.ws_play = None
        self.ws_play_ip = "127.0.0.1"
        self.ws_play_port = 12321
        self.ws_ui = None
        self.video_time = 0
        self.scramble_moves = []
        self.solve_moves = []

    def resetCube(self):
        self.solving = False
        self.moves = []
        self.moveNumber = 0
        self.alg.reset()
        self.moveNumber = 0
        self.exeMoves = []
        self.scrambleToExe = getScramble(self)
        self.scrambleApplied = ""
        self.scramble = True
        self.solving = False
        self.secMistake = 0.0
        self.startMemoTime = time.time()
        self.memoTime = time.time()
        self.startExeTime = time.time()
        self.exeTime = time.time()
        self.success = False
        self.rawSol = []
        self.mostPiecesSolved = 0
        self.solution = ""
        self.moveWrong = 0
        self.scramble_moves = []

    async def send_ui(self, field, msg):
        data_to_ui = json.dumps({field:msg})
        await self.ws_ui.send(data_to_ui)

    def wait(self):
        while(not keyboard.is_pressed(' ')):
            pass

def init_ws(ip, port):
    time.sleep(2)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    return client

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

    subprocess.Popen(["python", 'playVid.py'])

    Cube.ws_play = init_ws(Cube.ws_play_ip, Cube.ws_play_port)
    Cube.ws_play.recv(1024).decode('utf-8')
    Cube.ws_play.send(bytearray(str("{}:{}:{}:{}".format("%.2f"%Cube.secMistake, Cube.scrambleRow, Cube.frame_rate, Cube.video_time)), 'utf-8'))


    data = Cube.ws_play.recv(1024).decode('utf-8')
    if data != "finish":
        data_split = data.split(":")
        Cube.secMistake = int(float(data_split[0]))
        Cube.fail_reason = data_split[1]
def getScramble(Cube):# returns Cube object of scramble

    wb = openpyxl.load_workbook(os.getcwd() + "\RotoDNFStats.xlsx", data_only="yes")
    ws = wb["RotoStats"]
    i=1
    while(ws.cell(i,2).value != "no"):
        i+=1
    ws.cell(i,2).value = "yes"
    wb.save(os.getcwd() + "\RotoDNFStats.xlsx")
    Cube.scrambleRow = i
    Cube.scrambleApplied = ws.cell(i,1).value
    return ws.cell(i,1).value

def saveSolve(Cube):#save results to excel
    memo = Cube.memoTime
    exce = Cube.exeTime
    all = memo + exce
    print("all: ", all, ", memo: ", memo, ", exe: ", exce)
    a = input("Solved? (y/n)")#make sure the result is right
    if(a == "y"):
        succsses = "yes"
        Cube.secMistake = 0.0
    else:
        succsses = "no"
    row = Cube.scrambleRow

    wb = openpyxl.load_workbook(os.getcwd() + "\RotoDNFStats.xlsx", data_only="yes")
    ws = wb["RotoStats"]
    strRow = str(Cube.scrambleRow)
    ws.cell(row, 3).value = round(memo,2)
    ws.cell(row, 4).value = round(exce,2)
    ws.cell(row, 5).value = round(all,2)
    ws.cell(row, 6).value = round(Cube.secMistake, 2)
    ws.cell(row, 7).value = succsses

    ws.cell(row,10).value = url(Cube,ws.cell(row,1).value)
    print(Cube.fail_reason)
    ws.cell(row,11).value = Cube.fail_reason
    Cube.url = ws.cell(row,10).value
    pyperclip.copy(Cube.url)
    #ws.cell(row, 8).value = "=HYPERLINK(" + "\"C:\Python\PythonWork\BLD\RotoBLD\RotoDNF\\videos\solve" + strRow +".avi\""+", "+"\"solve"+strRow+"\")"
    ws.cell(row, 9).value =  Cube.solution
    wb.save(os.getcwd() + "\RotoDNFStats.xlsx")
def takeCorners(elem):
    return elem[2]

def takeEdges(elem):
    return elem[3]
def takeIndex(elem):
    return elem[4]
def takeTime(elem):
    return elem[1]


def moves_to_string(moves):
    st = ""
    for m in moves:
        st += m + " "
    return st
async def reset_scramble(Cube, trainer):
    Cube.resetCube()
    Cube.alg.movesToExecute = Cube.scrambleToExe  # put scramble moves ready to execute
    Cube.alg.executeAlg()
    Cube.alg.reverseSelf()
    trainer.facelet_last_string = ""
    trainer.facelet_current_state = ""
    Cube.facelet_moves = ""

    await Cube.send_ui("msg", "press space when cube is solved")  # add this to websocket
    await trainer.set_cube_solved()
    # Cube.wait()
    while (not keyboard.is_pressed(' ')):
         pass
    # trainer.data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f5), trainer.decoder)
    # trainer.data_move_counter = trainer.data[12]
    await Cube.send_ui("msg", "scramble")
    await Cube.send_ui("scramble", Cube.scrambleToExe)  # add this to websocket
    Cube.scramble_moves = []
    await trainer.set_cube_solved()
def get_facelet_strnig(value):
    state = []
    for i in range(0, len(value) - 2, 3):
        face = value[i ^ 1] << 16 | value[i + 1 ^ 1] << 8 | value[i + 2 ^ 1]
        for j in range(21, -1, -3):
            state.append("URFDLB"[face >> j & 0x7])
            if (j == 12):
                state.append("URFDLB"[int(i / 3)])

    latestFacelet = "".join(state)
    return latestFacelet

async def get_state(Cube, trainer):
    trainer.state_data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f2), trainer.decoder)
    value = trainer.state_data
    # print(trainer.last_state_string)
    if value != trainer.last_state_data:
        current_state = get_facelet_strnig(value)
        Cube.facelet_moves += " " + kociemba.solve(trainer.last_state_string, current_state)
        await Cube.send_ui("facelet", Cube.facelet_moves)  # add this to websocket
        trainer.last_state_data = value
        trainer.last_state_string = current_state

async def scramble_cube(Cube, trainer):

    print("hereeee")
    trainer.facelet_last_string = ""
    trainer.facelet_current_state = ""
    Cube.facelet_moves = ""
    await Cube.send_ui("msg","press space when cube is solved")
    await Cube.send_ui("moves", "")
    while (not keyboard.is_pressed(' ')):
         pass
    await trainer.set_cube_solved()
    # trainer.data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f5), trainer.decoder)
    # trainer.data_move_counter = trainer.data[12]
    # trainer.state_data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f2), trainer.decoder)
    # trainer.last_state_string = get_facelet_strnig(trainer.state_data)

    await Cube.send_ui("msg", "scramble")
    await Cube.send_ui("scramble",Cube.scrambleToExe) # add this to websocket
    Cube.scramble_moves = []

    while (Cube.scramble):  # Scramble Cube
        if (keyboard.is_pressed('q')):
            await reset_scramble(Cube,trainer)
        # trainer.data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f5), trainer.decoder)
        # trainer.new_moves = get_new_moves(trainer.data, trainer.data_move_counter)
        # await get_state(Cube,trainer)
        await asyncio.sleep(0.1)
        # trainer.moves += trainer.new_moves
        if (len(trainer.new_moves) != trainer.data_move_counter):
            trainer.moves += trainer.new_moves
            newMoves = trainer.new_moves[trainer.data_move_counter: len(trainer.new_moves)]
            trainer.data_move_counter = len(trainer.new_moves)
            # trainer.new_moves.reverse()
            for move in newMoves:
                Cube.scramble_moves.append(move)
                await Cube.send_ui("moves",moves_to_string(Cube.scramble_moves))
                Cube.alg.movesToExecute = move
                Cube.alg.executeAlg()
                if (Cube.alg.checkSolved() == True):
                    Cube.scramble = False
            # trainer.new_moves = []
        # trainer.data_move_counter = trainer.data[12]
async def initCube(websocket, path):

    Cube = DNFanalyzer()
    Cube.ws_ui = websocket
    Cube.resetCube()
    Cube.alg.movesToExecute = Cube.scrambleToExe  # put scramble moves ready to execute
    Cube.alg.executeAlg()
    Cube.alg.reverseSelf()
    trainer = Trainer()
    trainer.ble_server = BleakClient(trainer.rubiks1_addr)
    async with BleakClient(trainer.rubiks1_addr, timeout=20.0) as trainer.ble_server:
        if trainer.rubiks == True:
            await trainer.ble_server.start_notify(14, trainer.callback)

        while True:

            Cube.resetCube()
            Cube.alg.movesToExecute = Cube.scrambleToExe  # put scramble moves ready to execute
            Cube.alg.executeAlg()
            Cube.alg.reverseSelf()
            await scramble_cube(Cube,trainer)
            await Cube.send_ui("msg","press enter to start memo") # add to websocket
            Cube.wait()
            Cube.solveTime = time.time()
            subprocess.Popen(["python","recordVid.py"])#record video while solving
            Cube.ws_rec = init_ws(Cube.ws_rec_ip, Cube.ws_rec_port)
            Cube.ws_rec.send(bytearray(str(Cube.scrambleRow), 'utf-8'))
            started = Cube.ws_rec.recv(1024).decode('utf-8')
            diff = time.time() - Cube.solveTime

            print("time difff : {}".format(diff))
            await Cube.send_ui("msg","press enter to start solve") # add to websocket
            while(len(trainer.new_moves) == trainer.data_move_counter):
                await asyncio.sleep(0.1)
            await Cube.send_ui("msg","Solve!")
            Cube.memoTime = time.time() - Cube.solveTime
            moveCount = 0
            Cube.exeTime = time.time() - diff
            exeMoves = []
            moves = []

            while not keyboard.is_pressed(' '):  #While you are solving the cube
                # trainer.data = decData(await trainer.ble_server.read_gatt_char(trainer.chrct_uuid_f5), trainer.decoder)
                # trainer.new_moves = get_new_moves(trainer.data, trainer.data_move_counter)
                await asyncio.sleep(0.1)
                if (len(trainer.new_moves) != trainer.data_move_counter):
                    trainer.moves += trainer.new_moves
                    newMoves = trainer.new_moves[trainer.data_move_counter : len(trainer.new_moves)]
                    trainer.data_move_counter = len(trainer.new_moves)

                    for move in newMoves:
                        Cube.solve_moves.append(move)
                        exeMoves.append([move, int(time.time() - Cube.solveTime - diff), 0, 0, moveCount])
                        moveCount += 1
                        moves.append(move)
                        await Cube.send_ui("moves",moves_to_string(moves))
                # trainer.data_move_counter = trainer.data[12]

            await Cube.send_ui("msg","finish")
            Cube.exeTime = time.time()- Cube.exeTime
            Cube.ws_rec.send(bytearray('STOP', 'utf-8'))
            Cube.frame_rate = round(float(Cube.ws_rec.recv(1024).decode('utf-8')))
            Cube.video_time = round(float(Cube.ws_rec.recv(1024).decode('utf-8')))

            scramble = Cube.scrambleToExe
            solve = " ".join(Cube.solve_moves)
            stats = parse_solve(scramble, solve)

            playVid(Cube)
            saveSolve(Cube)

def main():
    start_server = websockets.serve(initCube, "127.0.0.1", 56789)
    #TODO: fix parity,  use ffmpeg to add metadata of mistakes, trace alg solved and theit times --> to trainer,
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == '__main__':
    main()