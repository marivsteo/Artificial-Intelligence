class Board:
    board = None
    def __init__(self, n):
        # print(n)
        self.board = [[(0, 0) for x in range(n)] for y in range(n)]
        # self.visited = [[0 for x in range(n)] for y in range(n)] 