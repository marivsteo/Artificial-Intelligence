from DecisionTree.Controller import Controller
import pandas as pd

dataset = pd.read_csv("C:/Users/Marius/Desktop/university 2/SEM2/ArtInt/Assignments/lab6/DECISION/balance-scale.data", sep=',', header=None)

class UI():

    def printTheMenu(self):
        print("\t 1 - Do the thing")
        print("\t 0 - exit")

    def run(self):
        controller = Controller(dataset)
        choice = -1
        while choice != 0:
            self.printTheMenu()
            choice = int(input(">>"))

            if choice == 1:
                controller.main()
            elif choice == 0:
                print("Endgame")
            else:
                print("Not a valid option")