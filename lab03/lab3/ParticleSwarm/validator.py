class Validator:
    def __init__(self, n):
        self.n = n

    def lineCheck(self, board):
        s = []
        t = []
        for i in board:
            s.clear()
            t.clear()
            for j in i:
                s.append(j[0])
                t.append(j[1])

            try:
                for j in range(1, self.n + 1):
                    s.remove(j)
                    t.remove(j)
                return True
            except:
                return False
        return True

    def columnCheck(self, board):
        t = []
        s = []
        cnt = 0
        for i in board:
            s.append([])
            t.append([])
            cnt = cnt + 1
            for j in i:
                s[cnt - 1].append(j[0])
                t[cnt - 1].append(j[1])

        for i in range(len(s)):
            sOnColumn = []
            for j in range(len(s)):
                # print (i , j)
                if s[j][i] in sOnColumn:
                    return False
                else:
                    sOnColumn.append(s[j][i])

        for i in range(len(t)):
            tOnColumn = []
            for j in range(len(s)):
                if t[j][i] in tOnColumn:
                    return False
                else:
                    tOnColumn.append(t[j][i])

        return True

    def dublicatesCheck(self, board):
        visited = []
        for i in board:
            for j in i:
                if j in visited:
                    # print("on dublicates")
                    # print (board)
                    return False
                else:
                    visited.append(j)
        return True