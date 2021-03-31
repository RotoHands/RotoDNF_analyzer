from bleak import BleakClient
import bleak
import asyncio
from bleak import BleakScanner

def parse_move(msgLen, value):

    axisPerm = [5, 2, 0, 3, 1, 4]
    facePerm = [0, 1, 2, 5, 8, 7, 6, 3]
    faceOffset = [0, 0, 6, 2, 0, 0]
    curBatteryLevel = -1
    for i in range(0,msgLen,2):

        axis = axisPerm[value[3 + i] >> 1]
        power =[0, 2][value[3 + i] & 1]
        m = axis * 3 + power
        print('move', "URFDLB"[axis] + " 2'"[power])


def parseData(value):
    if (len(value) < 4) :
        return None
    if value[0] != 0x2a or value[len(value) - 2] != 0x0d or value[len(value) - 1] != 0x0a:
        return None
    msgType = value[2]
    msgLen = len(value) - 6
    if (msgType == 1):
        parse_move(msgLen, value)
def toHexVal(value):
    valhex = []
    for i in range(len(value)):
        valhex.append(value[i] >> 4 & 0xf)
        valhex.append(value[i] & 0xf)
    return valhex

def callback(sender: int, data: bytearray):
    data = parseData(data)


async def connect_to_device(address):
    print("starting", address, "loop")
    notify_uuid = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'

    async with BleakClient(address, timeout=15.0) as client:
        print("connect to", address)

        try:
            await client.start_notify(notify_uuid, callback)
            await client.start_notify()
            await asyncio.sleep(30.0)
            await client.stop_notify(notify_uuid)
        except Exception as e:
            print(e)
    print("disconnect from", address)
async def main(addr):
    addrs = "ec:6a:31:5b:17:2d"
    addr = "DA:82:22:7A:A8:82"
    UUID_SUFFIX = '-b5a3-f393-e0a9-e50e24dcca9e'
    SERVICE_UUID = '6e400001' + UUID_SUFFIX
    CHRCT_UUID_WRITE = '6e400002' + UUID_SUFFIX
    CHRCT_UUID_READ = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
    client = BleakClient(addr)
    await client.pair()
    print(await client.connect())
    print("here")
    await client.start_notify(CHRCT_UUID_READ, callback)
    while True:
        pass
    # model_number = await client.read_gatt_char(CHRCT_UUID_READ)

    # await client.start_notify()



loop = asyncio.get_event_loop()
loop.run_until_complete(connect_to_device("DA:82:22:7A:A8:82"))