import time
import asyncio
from bleak import BleakClient
import struct
import math
import numpy
import os
import sys
import collections


class aes128:
    def __init__(self, key):
        self.sbox = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250,
                     89, 71,
                     240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229,
                     241, 113,
                     216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26,
                     27, 110,
                     90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57,
                     74, 76,
                     88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143,
                     146, 157,
                     56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126,
                     61, 100,
                     93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58,
                     10, 73, 6,
                     36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244,
                     234, 101,
                     122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62,
                     181, 102,
                     72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30,
                     135,
                     233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

        self.sboxI = [0] * 256
        self.shiftTabI = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]
        self.xtime = [0] * 256
        self.xtime_init = False
        self.init()
        self.initial_bool = False
        self.initial = None
        exKey = [0] * 176
        for i in range(len(key)):
            exKey[i] = key[i]
        Rcon = 1
        self.tmp = [0] * 200

        for i in range(16, 176, 4):
            try:
                self.tmp = exKey[i - 4: i]
                if (i % 16 == 0):
                    self.tmp = [self.sbox[self.tmp[1]] ^ Rcon, self.sbox[self.tmp[2]], self.sbox[self.tmp[3]],
                                self.sbox[self.tmp[0]]]
                    Rcon = self.xtime[Rcon]
                for j in range(4):
                    exKey[i + j] = exKey[i + j - 16] ^ self.tmp[j]
            except Exception as e:
                pass
        self.key = exKey

    def decrypt(self, block):
        rkey = self.key[160: 176]
        for i in range(16):
            block[i] ^= rkey[i]
        for i in range(144, 15, -16):
            block = self.shiftSubAdd(block, self.key[i: i + 16])
            for j in range(0, 16, 4):
                s0 = block[j + 0]
                s1 = block[j + 1]
                s2 = block[j + 2]
                s3 = block[j + 3]
                h = s0 ^ s1 ^ s2 ^ s3
                xh = self.xtime[h]
                h1 = self.xtime[self.xtime[xh ^ s0 ^ s2]] ^ h
                h2 = self.xtime[self.xtime[xh ^ s1 ^ s3]] ^ h
                block[j + 0] ^= h1 ^ self.xtime[s0 ^ s1]
                block[j + 1] ^= h2 ^ self.xtime[s1 ^ s2]
                block[j + 2] ^= h1 ^ self.xtime[s2 ^ s3]
                block[j + 3] ^= h2 ^ self.xtime[s3 ^ s0]
        block = self.shiftSubAdd(block, self.key[0:16])
        return block

    def shiftSubAdd(self, state, rkey):
        state0 = state[:]

        for i in range(16):
            state[i] = self.sboxI[state0[self.shiftTabI[i]]] ^ rkey[i]
        return state

    def init(self):
        if (self.xtime_init == True):
            return
        for i in range(256):
            self.sboxI[self.sbox[i]] = i
        for i in range(128):
            self.xtime[i] = i << 1
            self.xtime[128 + i] = (i << 1) ^ 0x1b
        self.xtime_init = True


decoder = None


def decData(value, decoder):
    if (decoder == None):
        return value
    decoded = [0] * len(value)
    for i in range(len(value)):
        decoded[i] = value[i]

    if (len(decoded) > 16):
        decoded = decoded[0:len(decoded) - 16] + decoder.decrypt(decoded[len(decoded) - 16:])
    decoded = decoder.decrypt(decoded)
    return decoded


def toEuler(w, x, y, z):
    sp = 2 * (w * y - z * x)
    eu = {
        "x": math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)),
        "y": math.asin(sp) if abs(sp) < 1 else numpy.sign(sp) * math.pi / 2,
        "z": math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))}

    return eu


def faceRotation(r):
    if (r < -3 * math.pi / 4):
        return 0
    if (r < -math.pi / 4):
        return 1
    if (r > 3 * math.pi / 4):
        return 0
    if (r > math.pi / 4):
        return 3
    return 2


def get_battery(value, decoder):
    value = decoder.decrypt(value)
    return value[7]


def timesOff(f6val, decoder):
    f6val = decoder.decrypt(f6val)
    timeOffs = collections.deque()
    for i in range(9):
        off = f6val[i * 2 + 1] | f6val[i * 2 + 2] << 8
        timeOffs.appendleft((math.floor(off / 0.95)))
    return timeOffs


def get_moves(value):

    twists = ["U", "?", "U'", "R", "?", "R'", "F", "?", "F'", "D", "?", "D'", "L", "?", "L'", "B", "?", "B'"]
    moves = []
    for i in range(13, 19):
        moves.append(twists[value[i]])
    return moves
