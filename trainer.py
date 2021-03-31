import asyncio
from bleak import BleakClient
from decode_gan import aes128
from decode_gan import get_moves
from decode_gan import decData
import time
from algClass import Alg
import pickle
from datetime import datetime
import shutil
from algs_dict_init import load_pkl
import websockets
import json


class Trainer:
    def __init__(self):
        self.key = [59, 18, 93, 222, 120, 218, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]
        self.decoder = aes128(self.key)
        self.data_send = {}
        self.data = None
        self.data_move_counter = None
        self.fail_times = 0
        self.success = False
        self.letter = ""
        self.new_moves = []
        self.moves = []
        self.use_recognize = True
        self.recognize_time_finished = False
        self.recognize_time = None
        self.algStartTime = 0
        self.algEndTime = None
        self.countTraining = 0
        self.start_practice_time = time.time()
        self.training_time_per_alg = 10
        self.action = ""
        self.index_train = 500
        self.save_timer_diff = 300
        self.save_timer = time.time()
        self.pkl_path = "algs_dict.pkl"
        self.pkl_path_backup = "dicts_backup.pkl"
        self.algs_dict = load_pkl(self.pkl_path)
        self.lp_2_index_edges = load_pkl("lp_2_index_edges.pkl")
        self.lp_2_corners_dict = load_pkl("lp_2_index_corners.pkl")
        self.websocket = None
        self.current_alg = Alg(self.algs_dict[self.index_train].alg_string)
        self.reset_alg()  # initialize alg
        self.solve_time = None
        self.ble_server = None
        self.addr = "F8:30:02:08:FB:FE"
        self.timesUp = False
        self.finish_training = False
        self.try_again_before_string = 3
        self.train_times_per_alg = 3
        if self.train_times_per_alg != 1:
            self.use_recognize = False
        self.all_train_time = 15
        self.finish_training_time = time.time() + self.all_train_time * 15
        self.string_moves = ""
        self.solve_times_alg = ""
        self.timer_show_interval = 10
        self.chrct_uuid_f5 = '0000fff5-0000-1000-8000-00805f9b34fb'
        self.chrct_uuid_f2 = "0000fff2-0000-1000-8000-00805f9b34fb"
        self.state_data = None
        self.last_state_data = None
        self.last_state_string = ""
    def reset_alg(self):

        if self.use_recognize:
            self.recognize_time = time.time()
            self.recognize_time_finished = False
        self.current_alg.algString = self.algs_dict[self.index_train].alg_string
        self.current_alg.reset()
        self.current_alg.movesToExecute = self.current_alg.algString
        self.current_alg.executeAlg()
        self.current_alg.reverseSelf()
        self.moves = []
        self.algStartTime = 0
        self.data_send["moves"] = ""
        # print(self.algs_dict[self.index_train])

    def moves_to_string(self):
        st = ""
        for m in self.moves:
            st += m + " "
        return st

    def move_alg_action_data_send(self):
        self.data_send["lp"] = self.algs_dict[self.index_train].letter_pair
        self.data_send["solve"] = ""
        self.data_send["add"] = ""
        self.data_send["alg"] = ""
        self.data_send["save"] = ""
        self.solve_times_alg = ""

    def next_alg_action(self):
        self.index_train = (self.index_train + 1) % len(self.algs_dict)
        self.move_alg_action_data_send()
        self.reset_alg()
        self.fail_times = 0
        self.start_practice_time = time.time()

    def last_alg_action(self):
        self.index_train = (self.index_train - 1) % len(self.algs_dict)
        self.move_alg_action_data_send()
        self.reset_alg()
        self.fail_times = 0
        self.countTraining = 0
        self.start_practice_time = time.time()

    def failed_alg_action(self):
        self.reset_alg()
        self.fail_times += 1
        if self.fail_times == self.try_again_before_string:
            self.data_send["alg"] = self.current_alg.algString

    def train_add_action(self):
        self.algs_dict[self.index_train].train_alg = True
        self.reset_alg()
        self.data_send["add"] = "added"

    def finish_training_action(self):
        self.finish_training = True
        self.save_solves()
        shutil.copy(self.pkl_path, self.pkl_path_backup)
        self.data_send["save"] = "saved!"

    def add_solve_to_dict(self):
        solve_time = float("%.2f" % (time.time() - self.algStartTime))
        if self.use_recognize:
            self.recognize_time = float("%.2f" % self.recognize_time)
            self.algs_dict[self.index_train].solves_times.append(((solve_time, self.recognize_time), datetime.now()
                                                                  .strftime("%Y-%m-%d %H:%M:%S")))
        else:
            self.algs_dict[self.index_train].solves_times.append((solve_time, datetime.now()
                                                                  .strftime("%Y-%m-%d %H:%M:%S")))
        self.solve_time = solve_time

    def exec_alg_action(self):
        if len(self.moves) > 0 and self.algStartTime == 0:
            self.algStartTime = time.time()

        if self.use_recognize and len(self.moves) > 0 and not self.recognize_time_finished:
            self.recognize_time = time.time() - self.recognize_time
            self.recognize_time_finished = True
        self.new_moves.reverse()
        for move in self.new_moves:
            self.current_alg.movesToExecute = move
            self.current_alg.executeAlg()

        if self.current_alg.isSolved:
            self.countTraining += 1
            self.add_solve_to_dict()
            if self.countTraining == self.train_times_per_alg:
                self.next_alg_action()
            else:
                self.solve_times_alg += "{}, ".format(str(self.solve_time))
                self.data_send["solve"] = self.solve_times_alg
                self.reset_alg()
        else:
            string_moves = self.moves_to_string()
            if string_moves != self.string_moves:
                self.string_moves = string_moves
                self.data_send["moves"] = self.moves_to_string()

    def exec_action(self):

        self.action = self.check_next_action()
        action = self.action

        if action == "Last":
            self.last_alg_action()
        if action == "Next":
            self.next_alg_action()
        if action == "Exec":
            self.exec_alg_action()
        if action == "Fail":
            self.failed_alg_action()
        if action == "Train_add":
            self.train_add_action()
        if action == "Finish":
            self.finish_training_action()

    def check_next_action(self):
        if self.check_times_up():
            return "Next"
        if len(self.moves) < 2:
            return "Exec"
        last_two_moves = self.moves[len(self.moves) - 2:len(self.moves)]
        if ('L' in last_two_moves) and ("L'" in last_two_moves):
            return "Fail"
        if ('F' in last_two_moves) and ("F'" in last_two_moves):
            return "Next"
        if ('B' in last_two_moves) and ("B'" in last_two_moves):
            return "Last"
        if ('D' in last_two_moves) and ("D'" in last_two_moves):
            return "Train_add"
        if len(self.moves) >= 4:
            last_four_moves = self.moves[len(self.moves) - 4: len(self.moves)]
            if last_four_moves.count("D'") == 4 or last_four_moves.count("D") == 4:
                return "Finish"
        return "Exec"

    def save_solves(self):
        if (time.time() - self.save_timer > self.save_timer_diff) or self.finish_training:
            with open(self.pkl_path, "wb") as f:
                pickle.dump(self.algs_dict, f)
                print("saved!")
            self.save_timer = time.time()

    def check_times_up(self):
        if time.time() - self.start_practice_time > self.training_time_per_alg:
            return True
        return False

    def print_solves(self, index):
        for solve in self.algs_dict[index].solves_times:
            print(solve)


def get_new_moves(data, counter):
    moves = get_moves(data)
    new_counter = data[12]
    new_moves = []

    for i in range((new_counter - counter) % 256):
        try:
            new_moves.append(moves[5 - i])
        except Exception as e:
            print(e)
            print("{} : {} : {} : {}".format(i, new_counter, counter, new_moves))
    return new_moves


async def connect(websocket, path):

    uuid_suffix = '-0000-1000-8000-00805f9b34fb'
    # chrct_uuid_f3 = '0000fff3' + uuid_suffix  # // prev moves
    chrct_uuid_f5 = '0000fff5' + uuid_suffix  # // gyro state, move counter, premoves
    chrct_uuid_f7 = '0000fff7' + uuid_suffix

    trainer = Trainer()
    trainer.ble_server = BleakClient(trainer.addr)
    await trainer.ble_server.connect()
    key = [59, 18, 93, 222, 120, 218, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]
    decoder = aes128(key)
    batt = await trainer.ble_server.read_gatt_char(chrct_uuid_f7)
    print(batt[7])
    trainer.websocket = websocket
    trainer.data = decData(await trainer.ble_server.read_gatt_char(chrct_uuid_f5), decoder)
    trainer.data_move_counter = trainer.data[12]
    while not trainer.finish_training:
        if int(trainer.finish_training_time - time.time()) % trainer.timer_show_interval == 0:
            minutes= str(int(trainer.finish_training_time - time.time()) // 60)
            sec = str(int(trainer.finish_training_time - time.time()) % 60)
            trainer.data_send["timer"] = "{}:{}".format(minutes, sec)
        trainer.data = decData(await trainer.ble_server.read_gatt_char(chrct_uuid_f5), decoder)
        trainer.new_moves = get_new_moves(trainer.data, trainer.data_move_counter)
        trainer.moves += trainer.new_moves
        trainer.data_move_counter = trainer.data[12]
        trainer.exec_action()
        if trainer.data_send:
            await trainer.websocket.send(json.dumps(trainer.data_send))
        trainer.data_send = {}
    await trainer.ble_server.disconnect()

    for i in range(500, 504):
        print(trainer.algs_dict[i])
        trainer.print_solves(i)

def main():
    start_server = websockets.serve(connect, "10.0.0.12", 5678)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()

if __name__ == '__main__':
    main()
