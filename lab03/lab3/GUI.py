import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

from Evolutionary.Controller import EAController
from HillClimbing.Controller import HCController
from ParticleSwarm.PSOv2 import *
import threading
import time
from Evolutionary import *
from HillClimbing import *
from UI import UI


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.particle = 1000
        self.size = 3
        self.pop = 25
        self.iter = 500
        self.mut = 0.5
        # self.number = 0
        # self.prob = -1
        self.message = "working on it..."
        self.initUI()

    def initUI(self):
        lbl = QLabel(self)
        lbl.setText("input n = ")
        lbl.move(20, 10)
        n = QLineEdit(self)

        n.move(100, 10)

        # lbl = QLabel(self)
        # lbl.setText("probability =  = ")
        # lbl.move(20, 30)
        # p = QLineEdit(self)

        # # p.move(100, 30)
        n.textChanged[str].connect(self.getN)
        # p.textChanged[str].connect(self.getP)

        self.setGeometry(600, 600, 600, 440)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        hc = QPushButton('Hill Climbing', self)
        hc.setToolTip('This is a <b>QPushButton</b> widget')
        hc.setCheckable(True)
        hc.resize(hc.sizeHint())
        hc.move(50, 80)
        hc.clicked[bool].connect(self.hillClimbing)

        ea = QPushButton('EA', self)
        ea.setToolTip('This is a <b>QPushButton</b> widget')
        ea.setCheckable(True)
        ea.resize(ea.sizeHint())
        ea.move(50, 120)
        ea.clicked[bool].connect(self.evolutionary)

        pso = QPushButton('PSO', self)
        pso.setToolTip('This is a <b>QPushButton</b> widget')
        pso.setCheckable(True)
        pso.resize(pso.sizeHint())
        pso.move(50, 160)
        pso.clicked[bool].connect(self.particleSwarm)



        self.table = QLabel(self)
        # self.table.setFixedWidth(500)
        # self.table.setText(self.message)
        # self.table.hide()
        self.table.move(150, 150)
        self.show()

    # def sayHi(self):
    #     print(self.number, self.prob)

    def getN(self, text):
        self.size = int(text)

    def getP(self, text):
        self.mut = float(text)

    def hillClimbing(self):

        controller = HCController(self.__size)
        # str1 = controller.solve(self.__iter, self.__size)

        pid = threading.Thread(target=controller.solve, args=(self.__iter, self.__size))
        pid.start()
        pid.join()
        while pid.is_alive():
            #  print(pid.is_alive())
            time.sleep(0.1)
        # ui.solve(int(1))

        str1 = controller.result
        self.table.setWordWrap(True)

        string = str(str1)
        self.table.setText(string)
        self.table.resize(300, 300)

    def evolutionary(self):

        # ea = EA(int(self.number))
        controller = EAController(self.__size)
        str1 = controller.solve(self.__pop, self.__iter, self.__mut, self.__size)
        # ea.solve()
        self.table.setWordWrap(True)

        string = "Result is: " + str1
        self.table.setText(string)
        self.table.resize(300, 300)

    def particleSwarm(self):

        solvePSO(self.__iter, self.__particle, self.__size)
        pid = threading.Thread(target=solvePSO, args=(self.__iter, self.__particle, self.__size))
        pid.start()
        self.table.setWordWrap(True)
        matrix = ""
        for i in range(self.number):
            for j in range(self.number):
                matrix = matrix + str(outcome[0][i][j]) + " "
            matrix = matrix + "\n"
        string = "detected minimum : " + str(outcomeFitness[0]) + "\n" + str(matrix)
        self.table.setText(string)
        self.table.resize(300, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())