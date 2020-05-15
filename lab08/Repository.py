class Repository:

    def __init__(self, filename):
        self.filename = filename
        self.points = []
        self.input = []
        self.output = []
        self.readfile()

    def readfile(self):
        file = open(self.filename, 'r')
        lines = file.readlines()
        index = 0
        for line in lines:
            if index % 2 == 0:
                f_list = [float(i) for i in line.split(" ")]
                self.points.append([float(f_list[0]), float(f_list[1]), float(f_list[2]), float(f_list[3]), float(f_list[4]), float(f_list[5])])
                self.input.append(
                    [float(f_list[0]), float(f_list[1]), float(f_list[2]), float(f_list[3]), float(f_list[4])])
                self.output.append([float(f_list[5])])
            index += 1
