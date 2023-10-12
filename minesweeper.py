import random

class Board:
    def __init__(self, dimSize, numBombs):
        self.dimSize = dimSize
        self.numBombs = numBombs

        self.board = makeNewBoard() #plant the bombs
        self.assignValueToBoard()

        #we'll save (row, cols) to this set
        self.dug = set() #if we dig at 0,0 then self.dug = {(0,0)}

    def makeNewBoard(self):
        board = [[None for _ in range(self.dimSize)] for _ in range(self.dimSize)]

        bombsPlanted = 0
        while bombsPlanted < self.numBombs :
            loc = random.randint(0, self.dimSize**2 - 1)
            row = loc // self.dimSize
            col = loc % self.dimSize

            if board[row][col] == '*':  #if there is already a bomb, pass
                continue
            board[row][col] = '*'
            bombsPlanted += 1
        return board

    def assignValueToBoard(self):
        for r in range(self.dimSize):
            for c in range(self.dimSize):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.getNumNeighboringBombs(r,c)
    
    def getNumNeighboringBombs(self, row, col):
        numNeighboringBombs = 0
        for r in range(max(0, row-1), min(self.dimSize-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimSize-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    numNeighboringBombs += 1
        return numNeighboringBombs

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dimSize-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimSize-1, col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True
    
    def __str__(self):
        visibleBoard = [[None for _ in range(self.dimSize)] for _ in range(self.dimSize)]
        for row in range(self.dimSize):
            for col in range(self.dimSize):
                if (row,col) in self.dug:
                    visibleBoard[row][col] = str(self.board[row][col])
                else:
                    visibleBoard[row][col] = ' '

        stringRep = ' '
        #get max column widths for printing
        widths = []
        for idx in range(self.dimSize):
            columns = map(lambda x: x[idx], visibleBoard)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )
        
        #print the csv strings
        indices = [i for i in range(self.dimSize)]
        indicesRow = ' '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-'+str(widths[idx])+ "s"
            cells.append(format% (col))
        indicesRow += ' '.join(cells)
        indicesRow += ' \n'

        for i in range(len(visibleBoard)):
            row = visibleBoard[i]
            stringRep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-'+str(widths[idx])+ "s"
                cells.append(format% (col))
            stringRep += ' |'.join(cells)
            stringRep += ' |\n'

        strLen = int(len(stringRep) / self.dimSize)
        stringRep = indicesRow + '-'*strLen + '\n' + stringRep + '-'*strLen

        return stringRep



def play(dimSize = 10, numBombs = 10):
    #step 1 : create the board and plant the bombs
    board = Board(dimSize, numBombs)
    #step 2 : show the user the board and ask where they want to dig

    #step 3a : if location is a bomb, show game over message
    #step 3b : if location is not a bomb, dig recursively until each square is at least next to a bomb
    #step 4 : repeat steps 2 and 3a,b until there are no places to dig => VICTORY !
    pass