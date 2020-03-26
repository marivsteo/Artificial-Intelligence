import sys

from GUI import Example, QApplication
from UI import UI


def main():
    # ui = UI()
    # ui.run()

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

main()
