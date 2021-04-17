import permutation
import kociemba
from RotoDNF import DNFanalyzer
import re
import pyperclip
from difflib import SequenceMatcher
import jellyfish


def ERROR_FUNC():
    print("unknown move: ")

class Cube:
    def __init__(self):
        self.dict_moves = {1: "U", 2: "U", 3: "U", 4: "U", 5: "U", 6: "U", 7: "U", 8: "U", 9: "U", 10: "R", 11: "R", 12: "R",
              13: "R", 14: "R", 15: "R", 16: "R", 17: "R", 18: "R", 19: "F", 20: "F", 21: "F", 22: "F", 23: "F",
              24: "F", 25: "F", 26: "F", 27: "F", 28: "D", 29: "D", 30: "D", 31: "D", 32: "D", 33: "D", 34: "D",
              35: "D", 36: "D", 37: "L", 38: "L", 39: "L", 40: "L", 41: "L", 42: "L", 43: "L", 44: "L", 45: "L",
              46: "B", 47: "B", 48: "B", 49: "B", 50: "B", 51: "B", 52: "B", 53: "B", 54: "B"}

        self.corners_numbers = [1, 3, 7, 9, 10, 12, 16, 18, 19, 21, 25, 27, 28, 30, 34, 36, 37, 39, 43, 45, 46, 48, 52, 54]
        self.edges_numbers = [2, 4, 6, 8, 11, 13, 15, 17, 20, 22, 24, 26, 29, 31, 33, 35, 38, 40, 42, 44, 47, 49, 51, 53]
        self.current_perm_list = []
        self.solved_edges = 0
        self.solved_corners = 0
        self.solved_perm = permutation.Permutation(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,54)
        self.solve_stats = []
        self.current_perm = self.solved_perm
        self.scramble = ""
        self.solve = ""
        self.solve_helper = ""
        self.url = ""
        self.current_max_perm_list = None
        self.parity = None
        self.max_edges = 12
        self.rotation = ['x', 'x\'', 'x2', 'z', 'z\'', 'z2', 'y', 'y\'', 'y2']

        self.current_facelet = ""
        self.R = permutation.Permutation(1, 2, 21, 4, 5, 24, 7, 8, 27, 16, 13, 10, 17, 14, 11, 18, 15, 12, 19, 20, 30, 22, 23, 33, 25, 26, 36, 28, 29, 52, 31, 32, 49, 34, 35, 46, 37, 38, 39, 40, 41,42, 43, 44, 45, 9, 47, 48, 6, 50, 51, 3, 53, 54).inverse()
        self.RP = self.R.inverse()
        self.R2 = self.R * self.R
        self.L = permutation.Permutation(54, 2, 3, 51, 5, 6, 48, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 1, 20, 21, 4,23, 24, 7, 26, 27, 19, 29, 30, 22, 32, 33, 25, 35, 36, 43, 40, 37, 44, 41, 38,45, 42, 39, 46, 47, 34, 49, 50, 31, 52, 53, 28).inverse()
        self.LP = self.L.inverse()
        self.L2 = self.L * self.L
        self.D = permutation.Permutation(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 25, 26, 27, 19, 20, 21, 22, 23, 24, 43, 44, 45, 34, 31, 28, 35, 32, 29, 36, 33, 30, 37, 38, 39, 40, 41, 42, 52, 53, 54, 46, 47, 48, 49, 50, 51, 16, 17, 18).inverse()
        self.DP = self.D.inverse()
        self.D2 = self.D * self.D
        self.B = permutation.Permutation(12, 15, 18, 4, 5, 6, 7, 8, 9, 10, 11, 36, 13, 14, 35, 16, 17, 34, 19, 20, 21,22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 40, 43, 3, 38, 39, 2, 41,42, 1, 44, 45, 52, 49, 46, 53, 50, 47, 54, 51, 48).inverse()
        self.BP = self.B.inverse()
        self.B2 = self.B * self.B
        self.U = permutation.Permutation(7, 4, 1, 8, 5, 2, 9, 6, 3, 46, 47, 48, 13, 14, 15, 16, 17, 18, 10, 11, 12, 22,23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 19, 20, 21, 40, 41, 42,43, 44, 45, 37, 38, 39, 49, 50, 51, 52, 53, 54).inverse()
        self.UP = self.U.inverse()
        self.U2 = self.U * self.U
        self.F = permutation.Permutation(1, 2, 3, 4, 5, 6, 45, 42, 39, 7, 11, 12, 8, 14, 15, 9, 17, 18, 25, 22, 19, 26,23, 20, 27, 24, 21, 16, 13, 10, 31, 32, 33, 34, 35, 36, 37, 38, 28, 40, 41, 29,43, 44, 30, 46, 47, 48, 49, 50, 51, 52, 53, 54).inverse()
        self.FP = self.F.inverse()
        self.F2 = self.F * self.F
        self.M = permutation.Permutation(1, 53, 3, 4, 50, 6, 7, 47, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 2, 21, 22, 5, 24, 25, 8, 27, 28, 20, 30, 31, 23, 33, 34, 26, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 35, 48, 49, 32, 51, 52, 29, 54).inverse()
        self.MP = self.M.inverse()
        self.M2 = self.M * self.M
        self.S = permutation.Permutation(1, 2, 3, 44, 41, 38, 7, 8, 9, 10, 4, 12, 13, 5, 15, 16, 6, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 17, 14, 11, 34, 35, 36, 37, 31, 39, 40, 32, 42, 43, 33, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54).inverse()
        self.SP = self.S.inverse()
        self.S2 = self.S * self.S
        self.E = permutation.Permutation(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 22, 23, 24, 16, 17, 18, 19, 20, 21, 40, 41, 42, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 49, 50, 51, 43, 44, 45, 46, 47, 48, 13, 14, 15, 52, 53, 54).inverse()
        self.EP = self.E.inverse()
        self.E2 = self.E * self.E





    def diff_states(self, perm_list):
        return SequenceMatcher(None, self.current_max_perm_list, perm_list).ratio()

        #return jellyfish.levenshtein_distance(self.current_max_perm_list, perm_list)



    def r(self):
        self.current_perm =  self.R * self.current_perm
    def rp(self):
        self.current_perm =  self.RP * self.current_perm

    def r2(self):
        self.current_perm = self.R2 * self.current_perm
    def l(self):
        self.current_perm =  self.L * self.current_perm
    def lp(self):
        self.current_perm = self.LP * self.current_perm
    def l2(self):
        self.current_perm =  self.L * self.L * self.current_perm
    def d(self):
        self.current_perm =  self.D * self.current_perm
    def dp(self):
        self.current_perm = self.DP * self.current_perm
    def d2(self):
        self.current_perm = self.D * self.D * self.current_perm
    def b(self):
        self.current_perm =  self.B * self.current_perm
    def bp(self):
        self.current_perm = self.BP * self.current_perm
    def b2(self):
        self.current_perm = self.B * self.B * self.current_perm
    def u(self):
        self.current_perm =  self.U * self.current_perm
    def up(self):
        self.current_perm = self.UP * self.current_perm
    def u2(self):
        self.current_perm = self.U * self.U * self.current_perm
    def f(self):
        self.current_perm =  self.F * self.current_perm
    def fp(self):
        self.current_perm = self.FP * self.current_perm
    def f2(self):
        self.current_perm = self.F * self.F * self.current_perm
    def m(self):
        self.current_perm = self.M * self.current_perm
    def mp(self):
        self.current_perm = self.MP * self.current_perm
    def m2(self):
        self.current_perm = self.M * self.M * self.current_perm
    def e(self):
        self.current_perm = self.E * self.current_perm
    def ep(self):
        self.current_perm = self.EP * self.current_perm
    def e2(self):
        self.current_perm = self.E * self.E * self.current_perm
    def s(self):
        self.current_perm = self.S * self.current_perm
    def sp(self):
        self.current_perm = self.SP * self.current_perm
    def s2(self):
        self.current_perm = self.S * self.S * self.current_perm
    def rw(self):
        self.current_perm = self.R * self.current_perm
        self.current_perm = self.MP * self.current_perm
    def rwp(self):
        self.current_perm = self.RP * self.current_perm
        self.current_perm = self.M * self.current_perm
    def rw2(self):
        self.current_perm = self.R * self.R * self.current_perm
        self.current_perm = self.MP * self.MP *  self.current_perm
    def lw(self):
        self.current_perm = self.L * self.current_perm
        self.current_perm = self.M * self.current_perm
    def lwp(self):
        self.current_perm = self.LP * self.current_perm
        self.current_perm = self.MP * self.current_perm
    def lw2(self):
        self.current_perm = self.L * self.L * self.current_perm
        self.current_perm = self.M * self.M *  self.current_perm
    def uw(self):
        self.current_perm = self.U * self.current_perm
        self.current_perm = self.EP * self.current_perm
    def uwp(self):
        self.current_perm = self.UP * self.current_perm
        self.current_perm = self.E * self.current_perm
    def uw2(self):
        self.current_perm = self.U * self.U * self.current_perm
        self.current_perm = self.EP * self.EP *  self.current_perm
    def dw(self):
        self.current_perm = self.D * self.current_perm
        self.current_perm = self.E * self.current_perm
    def dwp(self):
        self.current_perm = self.DP * self.current_perm
        self.current_perm = self.EP * self.current_perm
    def dw2(self):
        self.current_perm = self.D * self.D * self.current_perm
        self.current_perm = self.D * self.D *  self.current_perm
    def fw(self):
        self.current_perm = self.F * self.current_perm
        self.current_perm = self.S * self.current_perm
    def fwp(self):
        self.current_perm = self.FP * self.current_perm
        self.current_perm = self.SP * self.current_perm
    def fw2(self):
        self.current_perm = self.F * self.F * self.current_perm
        self.current_perm = self.S * self.S *  self.current_perm
    def bw(self):
        self.current_perm = self.B * self.current_perm
        self.current_perm = self.SP * self.current_perm
    def bwp(self):
        self.current_perm = self.BP * self.current_perm
        self.current_perm = self.S * self.current_perm
    def bw2(self):
        self.current_perm = self.B * self.B * self.current_perm
        self.current_perm = self.SP * self.SP *  self.current_perm
    def x(self):
        self.rw()
        self.lp()
    def xp(self):
        self.rwp()
        self.l()
    def x2(self):
        self.x()
        self.x()
    def y(self):
        self.uw()
        self.dp()
    def yp(self):
        self.uwp()
        self.d()
    def y2(self):
        self.y()
        self.y()
    def z(self):
        self.fw()
        self.bp()
    def zp(self):
        self.fwp()
        self.b()
    def z2(self):
        self.z()
        self.z()

    def singlemoveExecute(self, move):
        funcMoves = {
        'R': self.r,
        'R\'': self.rp,
        'R2': self.r2,
        'R2\'': self.r2,
        'L': self.l,
        'L\'': self.lp,
        'L2': self.l2,
        'L2\'': self.l2,
        'F': self.f,
        'F\'': self.fp,
        'F2': self.f2,
        'F2\'': self.f2,
        'B': self.b,
        'B\'': self.bp,
        'B2': self.b2,
        'B2\'': self.b2,
        'D': self.d,
        'D\'': self.dp,
        'D2': self.d2,
        'D2\'': self.d2,
        "U": self.u,
        'U\'': self.up,
        'U2': self.u2,
        'U2\'': self.u2,
        "S": self.s,
        'S\'': self.sp,
        'S2': self.s2,
        'S2\'': self.s2,
        "E": self.e,
        'E\'': self.ep,
        'E2': self.e2,
        'E2\'': self.e2,
        "M": self.m,
        'M\'': self.mp,
        'M2': self.m2,
        'M2\'': self.m2,
        "r": self.rw,
        'r\'': self.rwp,
        'r2': self.rw2,
        'r2\'': self.rw2,
        "Rw": self.rw,
        'Rw\'': self.rwp,
        'Rw2': self.rw2,
        'Rw2\'': self.rw2,
        "l": self.lw,
        'l\'': self.lwp,
        'l2': self.lw2,
        'l2\'': self.lw2,
        "Lw": self.lw,
        'Lw\'': self.lwp,
        'Lw2': self.lw2,
        'Lw2\'': self.lw2,
        "f": self.fw,
        'f\'': self.fwp,
        'f2': self.fw2,
        'f2\'': self.fw2,
        "Fw": self.fw,
        'Fw\'': self.fwp,
        'Fw2': self.fw2,
        'Fw2\'': self.fw2,
        "d": self.dw,
        'd\'': self.dwp,
        'd2': self.dw2,
        'd2\'': self.dw2,
        "Dw": self.dw,
        'Dw\'': self.dwp,
        'Dw2': self.dw2,
        'Dw2\'': self.dw2,
        "b": self.bw,
        'b\'': self.bwp,
        'b2': self.bw2,
        'b2\'': self.bw2,
        "Bw": self.bw,
        'Bw\'': self.bwp,
        'Bw2': self.bw2,
        'Bw2\'': self.bw2,
        "u": self.uw,
        'u\'': self.uwp,
        'u2': self.uw2,
        'u2\'': self.uw2,
        "Uw": self.uw,
        'Uw\'': self.uwp,
        'Uw2': self.uw2,
        'Uw2\'': self.uw2,
        'x': self.x,
        'x\'': self.xp,
        'x2': self.x2,
        'y': self.y,
        'y\'': self.yp,
        'y2': self.y2,
        'z': self.z,
        'z\'': self.zp,
        'z2': self.z2,

    }

        # funcMoves.get('R')()

        funcMoves.get(move)()



    def gen_url(self):
        self.url = "https://www.cubedb.net/?rank=3&title={}&scramble=".format("test")
        for move in self.scramble.split():
            if "\'" in move:
                move.replace("\'", "-")
            self.url += "{}_".format(move)
        self.url += "&alg="

        for move in self.solve_stats:
            if "\'" in move["move"]:
                move["move"].replace("\'", "-")
            self.url += "{}_".format(move["move"])
            if move["comment"] != "":
                self.url += move["comment"]
        pyperclip.copy(self.url)

    def perm_to_string(self, perm):
        perm_string = ""
        for i in range(1,55):
            perm_string += str(perm(i)) + " "
        return (perm_string)
    def count_solved_cor(self):
        solved_corners = 0

        if len(self.current_perm_list) <= 1:
            return 8
        for cor in self.corners_numbers:
            if str(cor) in self.current_perm_list:
                solved_corners += 1

        return 8 - int(solved_corners/3)

    def count_solve_edges(self):
        solved_edges = 0
        current_perm_list = self.perm_to_string(self.current_perm).split()
        # if len(self.current_perm_list) <= 1:
        #     return 12
        # print("prem : {}\nperm_str : {}\n current_perm_list : {}\n\n".format(self.current_perm, self.perm_to_string(self.current_perm), current_perm_list))
        # print(self.edges_numbers)
        for edge in self.edges_numbers:

            # if str(edge) in self.current_perm_list:
            #     solved_edges += 1
            if current_perm_list[edge - 1] == str(edge):
                # print("list : {} - edge : {}".format(current_perm_list[edge - 1], edge))
                solved_edges += 1

        return int(solved_edges/2)

    def exe_move(self, move):
        self.singlemoveExecute(move)
        facelet_str = self.current_perm.__str__()
        self.current_perm_list = []
        facelet = "0UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

        if facelet_str != "1":
            outer = re.compile(r'\((.*?)\)')
            matches = outer.findall(facelet_str)
            facelet = list(facelet)
            helper = facelet.copy()
            for p in matches:
                c = -1
                p = p.split()
                for i in p:
                    self.current_perm_list.append(i)
                    c += 1
                    temp1 = helper[int(p[c])]
                    facelet[int(p[(c + 1) % len(p)])] = temp1

        self.current_facelet = "{}{}".format("0",''.join(facelet[1:]))

    def y_rotation(self):
        solve = self.solve_helper.translate(str.maketrans('RrBbLlFfMz', 'BbLlFfRrSx'))
        solve.replace("S", "M'")
        solve.replace("x", "z'")
        solve.replace("''","")
        self.solve_helper = solve

    def y2_rotation(self):
        self.y_rotation()
        self.y_rotation()
    def yp_rotation(self):
        self.y2_rotation()
        self.y_rotation()
    def apply_rotation(self, rotation):
        funcMoves = {
            "y" : self.y_rotation,
            "yp" : self.yp_rotation,
            "y2" : self.y2_rotation
    }
        funcMoves.get(rotation)()

    def parse_rotations(self):

        solve_move_list = self.solve.split()
        for move in solve_move_list:
            if move in self.rotations:
                self.apply_rotation(move)

def main():
    SOLVED = "0UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    MISTAKE_SOLVE_CORNERS = "D D U' R' U' D B2 U D' R' U D' D' U' D B' U D' R U' R' U' D B U2 D' U' R' L F R' L D2 R L' F R L' U D' F U' D R' U' R U D' F' U D R' L F R F B' D' D' F' B R F' L' R L' U L U' R' L F L' F' R R U2 R D R' U U R D' R' R' R U R D' R' U' R D R' R' R R R D D U' R'"
    # SOLVE = "D U' D R' U' D B B U D' R' D' U D' U' D B' U D' R U' R' U' D B U D' U U' R' L F R' L D' D' R L' F R L' U D' F U' D R' U' R U D' F' U D R' L F R F B' D' D' F' B R F' L' R L' U L U' R' L F L' F' R R U U R D R' U2 R D' R' R' R U R D' R' U' R D R' R' R' U D' R' D R U' R' D' R D R D' L' D L D' L' D R' D' L D L' D' L D R"
    # SCRAMBLE = "B2 F2 U2 F2 D R2 U' L2 D L2 F2 B' R' U B2 D R D' L B U'"

    SOLVE = "U L' L' R' R U' R' L F L' L' F' R L' R' L F R' F' L' R U R U' F B' U F' U' F' B L F L' U U' R' U' R' U' D B B D' U R' U R U' D F' U F U D' L' U' L D R L' F R' L D R L' F R' L R' U D' F U' F' U' D R U U' R' R' D' R U U R' D R U U R U U D' R U' R' D R U R' U' U D U R' D R U2 R' D' R D' U D R' D' R U' R' D R D' R U R' F' R U R' U' R' F R R U' R' U'"
    SCRAMBLE = "L2 U R2 F2 R2 B2 D2 U F2 U L2 R B L' F D L' D' L2 F2 U'"

    # SCRAMBLE = "B F2 U2 L2 R2 D B U2 F R' D U' B2 L D' R' D2 R2"
    # SOLVE = "y R2 D R2' D' R2 U' R2' D R2 D' R2' U L' D2' L U' L' D2' L U U' R' D R U2 R' D' R U' U' R D' R' U R D R' R' U' R' E  R U R' E' R2 l' U' L U r' R U' L' U L U L2 U' M' U L2 U' r' R F U' R' M' r U R U' R' M' r U R' F' L U L E' L' U' L E L2'"

    # SCRAMBLE = "U' B2 R2 D2 F2 U R2 D U' F R D B2 D2 L' F2 U R2 B2 D2 Rw'"
    # SOLVE = "x M' U' M' U' M U' M' U' M2' U' L' U' L' U L U L U L' l' U' l' E' l2' E' l' U l U' R' F' R S R' F R S' U D R' U R D' R' U2 R D R' U R D' U' R2' D' R U' R' D R U R U U' R U' R' D R U R' D' U U D' R' U' R D' R' U R D2 U'"

    cube = Cube()
    cube.scramble = SCRAMBLE
    cube.solve = SOLVE
    cube.solve_helper = SOLVE
    cube.current_facelet = SOLVED
    SCRAMBLE_LIST = SCRAMBLE.split()
    # cube.apply_rotation("y")
    print("here {}".format(cube.solve_helper))
    for move in SCRAMBLE_LIST:
        cube.exe_move(move)
    max_solved = cube.count_solve_edges()
    if not cube.current_perm.is_even:
        cube.parity = True
        cube.max_edges = 10

    count = 0
    cube.solve_stats.append({"count": count, "move": "", "ed": cube.count_solve_edges(), "cor": cube.count_solved_cor(), "comment": ""})
    cube.current_max_perm_list = cube.perm_to_string(cube.current_perm)

    for move in cube.solve.split():
        exe_move = cube.solve_helper.split()[count]
        cube.exe_move(exe_move)
        count += 1
        print("{} : {}".format(move, exe_move))
        # if move in cube.rotation:
        #     print("move : {}".format(move))
        #     cube.current_max_perm_list = cube.perm_to_string(cube.current_perm)
        solved_edges =  cube.count_solve_edges()
        solved_cor = cube.count_solved_cor()
        diff = cube.diff_states(cube.perm_to_string(cube.current_perm))
        # max_solved = solved_edges if
        # if diff > 0.8 or diff < 0.1: #sequence matcher
        if diff > 0.85 : #18:
            cube.current_max_perm_list = cube.perm_to_string(cube.current_perm)
            cube.solve_stats.append({"count" : count,"move": move, "ed" : solved_edges,"cor" :  solved_cor, "comment" : "//e : {}, c : {}%0A".format(solved_edges, solved_cor),  "diff" : diff, "perm" : cube.perm_to_string(cube.current_perm)})
        else:
            cube.solve_stats.append({"count" : count,"move": move, "ed" : solved_edges,"cor" :  solved_cor, "comment" : "" , "diff" : diff, "perm" : cube.perm_to_string(cube.current_perm)})

    cube.gen_url()
    print(*cube.solve_stats, sep="\n")
if __name__ == '__main__':
    main()
