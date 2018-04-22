import json
from urllib.request import Request, urlopen
import board


def play_hands_on_board(board, hand, max_results, duden):
    prev_dict = analyze_board(board)
    result = {}
    for key in prev_dict.keys():
        parts = key.split("-")
        x = int(parts[0])
        y = int(parts[1])
        result[key] = validate_hand(prev_dict[key], hand, board[x][y])
        if duden:
            result[key] = validate_online(result[key])
        result[key] = get_top_x_words(result[key], max_results)
    return result


def analyze_board(board):
    result = {}
    for i, row in enumerate(board):
        for j, letter in enumerate(row):
            if letter == 0:
                continue
            key_string = str(i) + "-" + str(j)
            vertical = check_vertical(board, i, j)
            horizontal = check_horizontal(board, i, j)
            if vertical:
                result[key_string] = find_words(letter, vertical[0], vertical[1])
            if horizontal:
                result[key_string] = find_words(letter, horizontal[0], horizontal[1])
            else:
                continue
    return result


def check_horizontal(board, x, y):
    # is free?
    if y+1 > 14:
        if board[x][y-1] != 0:
            return False
    elif y-1 < 0:
        if board[x][y+1] != 0:
            return False
    elif board[x][y+1] != 0 or board[x][y-1] != 0:
        return False
    # has neighbours right ?
    i = 1
    while True:
        if x+1 > 14 or x-1 < 0 or y+i > 14:
            break
        if board[x+1][y+i] == 0 and board[x-1][y+i] == 0:
            i = i + 1
        else:
            break
    result_right = i - 1
    # has neighbouts left ?
    i = 1
    while True:
        if x + 1 > 14 or x - 1 < 0 or y - i < 0:
            break
        elif board[x+1][y-i] == 0 and board[x-1][y-i] == 0:
            i = i + 1
        else:
            break
    result_left = i - 1
    if result_left == 0 and result_right == 0:
        return False
    return result_left, result_right


def check_vertical(board, x, y):
    # is free?
    if x+1 > 14:
        if board[x-1][y] != 0:
            return False
    elif x-1 < 0:
        if board[x+1][y] != 0:
            return False
    if board[x+1][y] != 0 or board[x-1][y] != 0:
        return False
    # has neighbours up ?
    i = 1
    while True:
        if x+i > 14 or y-1 < 0 or y+1 > 14:
            break
        if board[x+i][y+1] == 0 and board[x+i][y-1] == 0:
            i = i + 1
        else:
            break
    result_up = i - 1
    # has neighbouts down ?
    i = 1
    while True:
        if y+1 > 14 or y-1 < 0 or x-i < 0:
            break
        if board[x-i][y+1] == 0 and board[x-i][y-1] == 0:
            i = i + 1
        else:
            break
    result_down = i - 1
    if result_up == 0 and result_down == 0:
        return False
    return result_up, result_down


def find_words(letter, sbl, sal):
    results = []
    with open("lists/german.dic", "r") as f:
        for line in f.readlines():
            line = line.lower().strip()
            if letter in line:
                pos = 0
                for o in range(line.count(letter)):
                    if o != 0:
                        pos = line.find(letter, pos + 1)
                    else:
                        pos = line.find(letter, pos)
                    if pos <= sbl:
                        # print(line + str(pos))
                        if len(line) - (pos + 1) <= sal:
                            results.append(line)
    # print(results)
    return results


def validate_hand(words, hand, board_letter):
    results = []
    for word in words:
        found = True
        hand_copy = list(hand)
        board_letter_copy = board_letter
        for letter in word:
            if letter not in hand_copy and letter != board_letter_copy:
                found = False
                break
            elif letter in hand_copy:
                hand_copy.remove(letter)
            elif letter == board_letter_copy:
                board_letter_copy = ""
            else:
                raise Exception("This should never be reached")
        if found:
            results.append(word)
    return results


def get_top_x_words(words, x):
    return sorted(words, key=len, reverse=True)[:x]


def validate_online(words):
    url = "https://www.duden.de/suchen/dudenonline/"
    for word in words:
        req = Request(url + str(word), headers={'User-Agent': 'Mozilla/5.0'})
        try:
            site = urlopen(req)
            data = json.loads(site.read().decode())
            print(data)
            i = "af"
        except:
            print(url + str(word))
    return words

# DEPRECATED:
def test():
    b = board.Board()
    b.init_board()
    b.init_test_bord()
    my_letter = b.get_letter(11, 7)

    # print(letter)
    #
    # words = find_words(letter, 6, 6)
    # print(len(words))
    # print(wor,ds)
    my_hand = ["i", "u", "i" "u", "a", "r", "c"]
    my_words = find_words("p", 2, 2)
    result = validate_hand(my_words, my_hand, "p")
    result.sort(key=len, reverse=True)
    print(result)

    # print(w)
    # print(len(words))
    # print(words)
