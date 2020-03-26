import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *

from Evolutionary.Controller import EAController
from HillClimbing.Controller import HCController
from ParticleSwarm.PSOv2 import *
import threading
import time
from Evolutionary import *
from HillClimbing import *
from UI import UI


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.table = QLabel(self)
        self.table.move(150, 450)
        self.table.setFont(QFont('Rustico', 20))
        self.particle = 1000
        self.size = 3
        self.pop = 25
        self.iter = 500
        self.mut = 0.5
        self.w = 1.0
        self.c1 = 1.0
        self.c2 = 2.5
        self.message = "working on it..."
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 100, 800, 800)
        self.setWindowTitle('Artificial Intelligence')

        lbl1 = QLabel(self)
        lbl1.setText("SIZE OF THE SQUARE: ")
        lbl1.move(20, 10)
        size = QLineEdit(self)
        size.move(200, 10)
        size.textChanged[str].connect(self.setSize)

        lbl2 = QLabel(self)
        lbl2.setText("NUMBER OF ITERATIONS: ")
        lbl2.move(20, 50)
        iterations = QLineEdit(self)
        iterations.move(200, 50)
        iterations.textChanged[str].connect(self.setIteration)

        lbl3 = QLabel(self)
        lbl3.setText("POPULATION SIZE: ")
        lbl3.move(20, 90)
        pop = QLineEdit(self)
        pop.move(200, 90)
        pop.textChanged[str].connect(self.setPopulation)

        lbl4 = QLabel(self)
        lbl4.setText("PROBABILITY OF MUTATION: ")
        lbl4.move(20, 130)
        mutation = QLineEdit(self)
        mutation.move(200, 130)
        mutation.textChanged[str].connect(self.setMutation)

        lbl5 = QLabel(self)
        lbl5.setText("NUMBER OF PARTICLES:")
        lbl5.move(20, 170)
        particles = QLineEdit(self)
        particles.move(200, 170)
        particles.textChanged[str].connect(self.setParticle)

        lbl6 = QLabel(self)
        lbl6.setText("W (FOR PSO): ")
        lbl6.move(20, 210)
        w = QLineEdit(self)
        w.move(200, 210)
        w.textChanged[str].connect(self.setW)

        lbl7 = QLabel(self)
        lbl7.setText("C1 (FOR PSO): ")
        lbl7.move(20, 250)
        c1 = QLineEdit(self)
        c1.move(200, 250)
        c1.textChanged[str].connect(self.setC1)

        lbl8 = QLabel(self)
        lbl8.setText("C2 (FOR PSO): ")
        lbl8.move(20, 290)
        c2 = QLineEdit(self)
        c2.move(200, 290)
        c2.textChanged[str].connect(self.setC2)

        hc = QPushButton('HC', self)
        hc.setToolTip('This is a <b>QPushButton</b> widget')
        hc.setCheckable(True)
        hc.resize(hc.sizeHint())
        hc.move(400, 20)
        hc.clicked.connect(self.hillClimbing)

        ea = QPushButton('EA', self)
        ea.setToolTip('This is a <b>QPushButton</b> widget')
        ea.setCheckable(True)
        ea.resize(ea.sizeHint())
        ea.move(400, 70)
        ea.clicked[bool].connect(self.evolutionary)

        pso = QPushButton('PSO', self)
        pso.setToolTip('This is a <b>QPushButton</b> widget')
        pso.setCheckable(True)
        pso.resize(pso.sizeHint())
        pso.move(400, 120)
        pso.clicked[bool].connect(self.particleSwarm)

        stop = QPushButton('STOP', self)
        stop.setToolTip('Stop the application')
        stop.setCheckable(True)
        stop.resize(stop.sizeHint())
        stop.move(600, 70)
        stop.clicked.connect(self.close)
        self.show()

        # self.table.setFixedWidth(500)
        # self.table.setText(self.message)
        # self.table.hide()




    def setSize(self, text):
        self.size = int(text)

    def setPopulation(self, text):
        self.pop = int(text)

    def setMutation(self, text):
        self.mut = float(text)
        
    def setIteration(self, text):
        self.iter = int(text)
        
    def setParticle(self, text):
        self.particle = int(text)

    def setW(self, text):
        self.w = float(text)

    def setC1(self, text):
        self.c1 = float(text)

    def setC2(self, text):
        self.c2 = float(text)

    def hillClimbing(self):

        controller = HCController(self.size)
        # str1 = controller.solve(self.__iter, self.__size)

        pid = threading.Thread(target=controller.solve, args=(self.iter, self.size))
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
        controller = EAController(self.size)
        str1 = controller.solve(self.pop, self.iter, self.mut, self.size)
        # ea.solve()
        self.table.setWordWrap(True)

        string = str1
        self.table.setText(string)
        self.table.resize(300, 300)

    def particleSwarm(self):

        solvePSO(self.iter, self.particle, self.size, self.w, self.c1, self.c2)
        pid = threading.Thread(target=solvePSO, args=(self.iter, self.particle, self.size, self.w, self.c1, self.c2))
        pid.start()
        pid.join()
        while pid.is_alive():
            time.sleep(0.1)

        self.table.setWordWrap(True)

        matrix = ""
        for i in range(self.size):
            for j in range(self.size):
                matrix = matrix + str(outcome[0][i][j]) + " "
            matrix = matrix + "\n"
        string = "Detected minimum : " + str(outcomeFitness[0]) + "\n" + str(matrix)

        self.table.setText(string)
        self.table.resize(300, 300)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.excepthook = except_hook
    sys.exit(app.exec_())