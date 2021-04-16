import permutation
import kociemba
from RotoDNF import DNFanalyzer
import re


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

        self.current_perm = self.solved_perm
        self.scramble = ""
        self.solve = ""
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

    def count_solved_cor(self):
        solved_corners = 0

        if len(self.current_perm_list) <= 1:
            return 8
        for cor in self.corners_numbers:
            if str(cor) in self.current_perm_list:
                print(str(cor))
                solved_corners += 1

        return 8 - solved_corners/3

    def count_solve_edges(self):
        print(self.current_perm)
        print(self.current_perm_list)
        solved_edges = 0
        if len(self.current_perm_list) <= 1:
            return 12
        for edge in self.edges_numbers:
            if str(edge) in self.current_perm_list:
                print(str(edge))
                solved_edges += 1
        return 12 - solved_edges/2

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
    }

        # funcMoves.get('R')()

        funcMoves.get(move)()



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


def main():
    SOLVED = "0UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    MISTAKE_SOLVE_CORNERS = "D D U' R' U' D B2 U D' R' U D' D' U' D B' U D' R U' R' U' D B U2 D' U' R' L F R' L D2 R L' F R L' U D' F U' D R' U' R U D' F' U D R' L F R F B' D' D' F' B R F' L' R L' U L U' R' L F L' F' R R U2 R D R' U U R D' R' R' R U R D' R' U' R D R' R' R R R D D U' R'"
    SOLVE = "D U' D R' U' D B B U D' R' D' U D' U' D B' U D' R U' R' U' D B U D' U U' R' L F R' L D' D' R L' F R L' U D' F U' D R' U' R U D' F' U D R' L F R F B' D' D' F' B R F' L' R L' U L U' R' L F L' F' R R U U R D R' U2 R D' R' R' R U R D' R' U' R D R' R' R' U D' R' D R U' R' D' R D R D' L' D L D' L' D R' D' L D L' D' L D R"
    SCRAMBLE = "B2 F2 U2 F2 D' R2 U' L2 D L2 F2 B' R' U B2 R D' L B U'"
    cube = Cube()
    cube.scramble = SCRAMBLE
    cube.solve = SOLVE
    cube.current_facelet = SOLVED
    SCRAMBLE_LIST = SCRAMBLE.split()
    for move in SCRAMBLE_LIST:
        cube.exe_move(move)
    print(cube.current_perm)
    print(cube.current_facelet)
    print("corners : {}, edges : {}".format(cube.count_solved_cor(), cube.count_solve_edges()))
    print(kociemba.solve(cube.current_facelet[1:], SOLVED[1:]))

if __name__ == '__main__':
    main()