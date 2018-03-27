class Board():
    board = []
    BOARD_LENGTH = 15

    # __init__ ??
    def init_board(self):
        for i in range(self.BOARD_LENGTH):
            self.board.append([])
            for j in range(self.BOARD_LENGTH):
                self.board[i].append(0)

    def insert_letter(self, letter, x, y):
        self.board[x][y] = letter

    def insert_word(self, word, x, y, vertical=False):
        if vertical:
            for i, letter in enumerate(word):
                self.insert_letter(letter, x, y+i)
        else:
            for i, letter in enumerate(word):
                self.insert_letter(letter, x+i, y)

    def init_test_bord(self):
        self.insert_word("troll", 7, 7)
        self.insert_word("kopfball", 9, 6, True)

    def get_letter(self, x, y):
        return self.board[x][y]