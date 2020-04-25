from pprint import pprint

import pandas

from Controller import Controller

dataset = pandas.read_csv("C:/Users/Marius/Desktop/university 2/SEM2/ArtInt/Assignments/lab07/Files/database", sep=' ', header=None)


class UI:

    def printmenu(self):
        print("\t 1 - Do the thing")
        print("\t 0 - exit")

    def run(self):
        controller = Controller(len(dataset.columns), 0.001)
        choice = -1
        while choice != 0:
            self.printmenu()
            choice = int(input(">>"))

            if choice == 1:
                for x in range(1000):
                    controller.step()
                controller.print_weights()
                print("The total error: ", controller.total_error())
            elif choice == 0:
                print("Endgame")
            else:
                print("Not a valid option")
