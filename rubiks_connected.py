from bleak import BleakClient
# from bleak import B
import bleak
import asyncio
from bleak import BleakScanner

def parseData(value):
    axisPerm = [5, 2, 0, 3, 1, 4]
    facePerm = [0, 1, 2, 5, 8, 7, 6, 3]
    faceOffset = [0, 0, 6, 2, 0, 0]
    curBatteryLevel = -1

    if (len(value) < 4) :
        return None
    if value[0] != 0x2a or value[len(value) - 2] != 0x0d or value[len(value) - 1] != 0x0a:
        return None
    msgType = value[2]
    msgLen = len(value) - 6
    if (msgType == 1):
        # await client.write_gatt_char(write_uuid, bytearray([0x33]))

        for i in range(0, msgLen, 2):
            axis = axisPerm[value[3 + i] >> 1]
            power = [0, 2][value[3 + i] & 1]
            m = axis * 3 + power
            s = ("URFDLB"[axis] + " 2'"[power])
            return (s)
    elif (msgType == 2):
        facelet =[""]*54
        for a in range (6):
            axis = axisPerm[a] * 9
            aoff = faceOffset[a]
            facelet[axis + 4] = "BFUDRL"[value[3 + a * 9]]
            for i in range (8):
                facelet[axis + facePerm[(i + aoff) % 8]] = "BFUDRL"[value[(3 + a * 9 + i + 1)]]
        newFacelet = ''.join(facelet)
        return newFacelet
    elif (msgType == 5):
        return "battery level : {}".format(toHexVal(value)[3])

    elif (msgType == 7):
        return 'offline stats : {}'.format(toHexVal(value))
    elif (msgType == 8):
        return('cube type : {}'.format(toHexVal(value)))
    else:
        return("msgType : {}".format(msgType))
def toHexVal(value):
    valhex = []
    for i in range(len(value)):
        valhex.append(value[i] >> 4 & 0xf)
        valhex.append(value[i] & 0xf)
    return valhex

def callback(sender: int, data: bytearray):
    parseData(data)
async def check():
    while True:
        pass

async def connect_to_device(address):
    notify_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
    write_uuid = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
    service = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
    async with bleak.BleakClient(address, timeout=20.0) as client:
        try:
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print(e)

    print("disconnect from", address)
addr = "ec:6a:31:5b:17:2d"
addrs = "DA:82:22:7A:A8:82"
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_device(addr))