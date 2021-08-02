import permutation

class Alg:
    UCor = permutation.Permutation(2, 3, 4, 1, 17, 18, 7, 8, 5, 6, 11, 12, 9, 10, 15, 16, 13, 14, 19, 20, 21, 22, 23, 24)
    DCor = permutation.Permutation(1, 2, 3, 4, 5, 6, 11, 12, 9, 10, 15, 16, 13, 14, 19, 20, 17, 18, 7, 8, 22, 23, 24, 21)
    RCor = permutation.Permutation(1, 20, 17, 4, 5, 6, 7, 8, 9, 2, 3, 12, 14, 15, 16, 13, 21, 18, 19, 24, 11, 22, 23, 10)
    LCor = permutation.Permutation(9,2,3,12,6,7,8,5,23,10,11,22,13,14,15,16,17,4,1,20,21,18,19,24)
    BCor = permutation.Permutation(8,5,3,4,22,6,7,21,9,10,11,12,13,1,2,16,18,19,20,17,14,15,23,24)
    FCor = permutation.Permutation(1,2,16,13,5,3,4,8,10,11,12,9,24,14,15,23,17,18,19,20,21,22,6,7)

    UEdge = permutation.Permutation(2,3,4,1,17,6,7,8,5,10,11,12,9,14,15,16,13,18,19,20,21,22,23,24)
    DEdge = permutation.Permutation(1,2,3,4,5,6,11,8,9,10,15,12,13,14,19,16,17,18,7,20,22,23,24,21)
    REdge = permutation.Permutation(1,20,3,4,5,6,7,8,9,2,11,12,14,15,16,13,17,18,19,24,21,22,23,10)
    LEdge = permutation.Permutation(1,2,3,12,6,7,8,5,9,10,11,22,13,14,15,16,17,4,19,20,21,18,23,24)
    FEdge = permutation.Permutation(1,2,16,4,5,3,7,8,10,11,12,9,13,14,15,23,17,18,19,20,21,22,6,24)
    BEdge = permutation.Permutation(8,2,3,4,5,6,7,21,9,10,11,12,13,1,15,16,18,19,20,17,14,22,23,24)

    MEdge = permutation.Permutation(9,2,11,4,5,6,7,8,23,10,21,12,13,14,15,16,3,18,1,20,17,22,19,24)
    SEdge = permutation.Permutation(1,15,3,13,2,6,4,8,9,10,11,12,24,14,22,16,17,18,19,20,21,5,23,7)
    EEdge = permutation.Permutation(1,2,3,4,5,10,7,12,9,14,11,16,13,18,15,20,17,6,19,8,21,22,23,24)

    MCenter = permutation.Permutation(2,6,3,4,1,5)
    SCenter = permutation.Permutation(4,2,1,6,5,3)
    ECenter = permutation.Permutation(1,4,2,5,3,6)

    def __init__(self, algString):
        self.algString = algString
        self.corenerState = permutation.Permutation(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        self.edgeState = permutation.Permutation()
        self.centerState = permutation.Permutation()
        self.isSolved = False
        self.movesToExecute = ""
    def reverseSelf(self):
        self.corenerState = self.corenerState.inverse()
        self.edgeState = self.edgeState.inverse()
        self.centerState = self.centerState.inverse()
    def move(self, string):

        self.movesToExecute = string
    def corOrder(self):
        return self.corenerState.order

    def edgesOrder(self):
        return self.edgeState.order
    def edgeEven(self):
        return self.edgeState.is_even
    def cornerEven(self):
        return self.corenerState.is_even
    def countSolvedCor(self):
        solvedCorners = 0
        c = self.corenerState
        for i in range (1,25):
            if(c(i) == i):
                solvedCorners+=1
        return  solvedCorners/3

    def countSolveEdges(self):
        edgesSolved = 0
        c = self.edgeState
        for i in range (1,25):
            if(c(i) == i):
                edgesSolved+=1
        return  edgesSolved/2

    def checkSolvedByRotation(self):
        movesToDo = ['x','y','z']
        for rotation in movesToDo:

            self.movesToExecute = rotation
            self.executeAlg()

            self.Solved()
            if(self.isSolved == True):
                return True
            self.movesToExecute = rotation +"\'"
            self.executeAlg()


        movesToDo = ['x\'', 'y\'', 'z\'']
        for rotation in movesToDo:

            self.movesToExecute = rotation
            self.executeAlg()

            self.Solved()
            if(self.isSolved == True):
                return True
            self.movesToExecute = rotation[0]
            self.executeAlg()


        movesToDo = ['x2', 'y2', 'z2']
        for rotation in movesToDo:

            self.movesToExecute = rotation
            self.executeAlg()

            self.Solved()
            if (self.isSolved == True):
                return True
            self.movesToExecute = rotation
            self.executeAlg()



        return False
    def checkSolved(self):

        a = self.centerState.__bool__()
        b = self.corenerState.__bool__()
        c = self.edgeState.__bool__()

        if(a == False and b == False and c == False):
            return True
        else:
            return  False
    def Solved(self):

        a = self.centerState.__bool__()
        b = self.corenerState.__bool__()
        c = self.edgeState.__bool__()

        if(a == False and b == False and c == False):
            self.isSolved = True
        else:
            self.isSolved = False
    def copyAlg(self, alg):
        self.algString = alg.algString
        self.corenerState = alg.corenerState
        self.edgeState = alg.edgeState
        self.centerState = alg.centerState
    def printState(self):
        print("corner cycels;: " , self.corenerState.to_cycles())
        print("edges cycels;: ", self.edgeState.to_cycles())
        print("center cycels;: ", self.centerState.to_cycles())

    def reset(self):
        self.corenerState = permutation.Permutation()
        self.edgeState = permutation.Permutation()
        self.centerState = permutation.Permutation()
    def unkonwnFunction(self):
        print("unknown move: ")

    def printAlg(self):
        alg = self.algString
        print(alg)

    def U (self):
       self.corenerState =  self.UCor * self.corenerState
       self.edgeState = self.UEdge * self.edgeState

    def UPrime(self):
        self.corenerState =  self.UCor.inverse() * self.corenerState
        self.edgeState =   self.UEdge.inverse() * self.edgeState
    def U2(self):
        self.corenerState =  self.UCor * self.UCor * self.corenerState
        self.edgeState = self.UEdge * self.UEdge* self.edgeState

    def D(self):
        self.corenerState = self.DCor * self.corenerState
        self.edgeState =  self.DEdge * self.edgeState
    def DPrime(self):
        self.corenerState = self.DCor.inverse() * self.corenerState
        self.edgeState =  self.DEdge.inverse() * self.edgeState
    def D2(self):
        self.corenerState = self.DCor * self.DCor * self.corenerState
        self.edgeState =  self.DEdge * self.DEdge * self.edgeState

    def R(self):
        self.corenerState =  self.RCor * self.corenerState
        self.edgeState = self.REdge * self.edgeState
    def RPrime(self):
        self.corenerState =  self.RCor.inverse() * self.corenerState
        self.edgeState =  self.REdge.inverse() * self.edgeState
    def R2(self):
        self.corenerState = self.RCor * self.RCor * self.corenerState
        self.edgeState =  self.REdge * self.REdge * self.edgeState

    def L(self):
        self.corenerState =  self.LCor * self.corenerState
        self.edgeState =  self.LEdge * self.edgeState
    def LPrime(self):
        self.corenerState =  self.LCor.inverse() * self.corenerState
        self.edgeState =  self.LEdge.inverse() * self.edgeState
    def L2(self):
        self.corenerState =  self.LCor * self.LCor * self.corenerState
        self.edgeState =  self.LEdge * self.LEdge * self.edgeState

    def F(self):
        self.corenerState =  self.FCor * self.corenerState
        self.edgeState =  self.FEdge * self.edgeState
    def FPrime(self):
        self.corenerState =  self.FCor.inverse() * self.corenerState
        self.edgeState =  self.FEdge.inverse() * self.edgeState
    def F2(self):
        self.corenerState =  self.FCor * self.FCor * self.corenerState
        self.edgeState =  self.FEdge * self.FEdge * self.edgeState

    def B(self):
        self.corenerState =  self.BCor * self.corenerState
        self.edgeState = self.BEdge * self.edgeState
    def BPrime(self):
        self.corenerState =  self.BCor.inverse() * self.corenerState
        self.edgeState =  self.BEdge.inverse() * self.edgeState
    def B2(self):
        self.corenerState = self.BCor * self.BCor * self.corenerState
        self.edgeState =  self.BEdge * self.BEdge * self.edgeState

    def E (self):
       self.edgeState = self.EEdge * self.edgeState
       self.centerState =  self.ECenter * self.centerState

    def EPrime(self):
        self.edgeState =  self.EEdge.inverse() * self.edgeState
        self.centerState =  self.ECenter.inverse() * self.centerState
    def E2(self):
        self.edgeState = self.EEdge * self.EEdge * self.edgeState
        self.centerState =  self.ECenter * self.ECenter * self.centerState

    def M (self):
       self.edgeState = self.MEdge * self.edgeState
       self.centerState =  self.MCenter * self.centerState
    def MPrime(self):
        self.edgeState =  self.MEdge.inverse() * self.edgeState
        self.centerState = self.MCenter.inverse() * self.centerState
    def M2(self):
        self.edgeState =  self.MEdge * self.MEdge * self.edgeState
        self.centerState = self.MCenter * self.MCenter * self.centerState

    def S (self):
       self.edgeState = self.SEdge * self.edgeState
       self.centerState =  self.SCenter * self.centerState
    def SPrime(self):
        self.edgeState =  self.SEdge.inverse() * self.edgeState
        self.centerState = self.SCenter.inverse() * self.centerState
    def S2(self):
        self.edgeState =  self.SEdge * self.SEdge * self.edgeState
        self.centerState =  self.SCenter * self.SCenter * self.centerState
    def x(self):
        self.r()
        self.LPrime()
    def xprime(self):
        self.rPrime()
        self.L()
    def x2(self):
        self.x()
        self.x()

    def y(self):
        self.u()
        self.DPrime()
    def yprime(self):
        self.uPrime()
        self.D()
    def y2(self):
        self.y()
        self.y()

    def z(self):
        self.f()
        self.BPrime()
    def zprime(self):
        self.fPrime()
        self.B()
    def z2(self):
        self.z()
        self.z()

    def u (self):
        self.U()
        self.EPrime()

    def uPrime (self):
        self.UPrime()
        self.E()

    def u2 (self):
        self.u()
        self.u()

    def f (self):
        self.F()
        self.S()

    def fPrime(self):
        self.FPrime()
        self.SPrime()

    def f2(self):
        self.f()
        self.f()

    def r(self):
        self.R()
        self.MPrime()

    def rPrime(self):
        self.RPrime()
        self.M()

    def r2(self):
        self.r()
        self.r()

    def l(self):
        self.L()
        self.M()

    def lPrime(self):
        self.LPrime()
        self.MPrime()

    def l2(self):
        self.l()
        self.l()

    def d(self):
        self.D()
        self.E()

    def dPrime(self):
        self.DPrime()
        self.EPrime()

    def d2(self):
        self.d()
        self.d()

    def b(self):
        self.B()
        self.SPrime()

    def bPrime(self):
        self.BPrime()
        self.S()

    def b2(self):
        self.b()
        self.b()

    def singlemoveExecute(self, move):


        funcMoves = {
            'R': self.R,
            'R\'': self.RPrime,
            'R2': self.R2,
            'R2\'': self.R2,
            'L': self.L,
            'L\'': self.LPrime,
            'L2': self.L2,
            'L2\'': self.L2,
            'F': self.F,
            'F\'': self.FPrime,
            'F2': self.F2,
            'F2\'': self.F2,
            'B': self.B,
            'B\'': self.BPrime,
            'B2': self.B2,
            'B2\'': self.B2,
            'D': self.D,
            'D\'': self.DPrime,
            'D2': self.D2,
            'D2\'': self.D2,
            "U": self.U,
            'U\'': self.UPrime,
            'U2': self.U2,
            'U2\'': self.U2,
            'S': self.S,
            'S\'': self.SPrime,
            'S2': self.S2,
            'S2\'': self.S2,
            'E': self.E,
            'E\'': self.EPrime,
            'E2': self.E2,
            'E2\'': self.E2,
            'M': self.M,
            'M\'': self.MPrime,
            'M2': self.M2,
            'M2\'': self.M2,
            'r': self.r,
            'r\'': self.rPrime,
            'r2': self.r2,
            'l': self.l,
            'l\'': self.lPrime,
            'l2': self.l2,
            'd': self.d,
            'd\'': self.dPrime,
            'd2': self.d2,
            'u': self.u,
            'u\'': self.uPrime,
            'u2': self.u2,
            'f': self.f,
            'f\'': self.fPrime,
            'f2': self.f2,
            'b': self.b,
            'b\'': self.bPrime,
            'b2': self.b2,
            'x': self.x,
            'x\'' : self.xprime,
            'x2': self.x2,
            'y': self.y,
            'y\'': self.yprime,
            'y2': self.y2,
            'z': self.z,
            'z\'': self.zprime,
            'z2': self.z2,
        }
        funcMoves.get(move, self.unkonwnFunction)()
    def executeAlg(self):
        algMoves = self.movesToExecute.split()
        for move in algMoves:
            self.singlemoveExecute(move)
        self.Solved()

    def executeAlgWithMoves(self, moves):
        self.movesToExecute = moves
        algMoves = self.movesToExecute.split()
        for move in algMoves:
            self.singlemoveExecute(move)
        self.Solved()
        print("moves apllied: ", *algMoves, sep = " ")
