from pyswip import Prolog

# X row width
# Y column height

w, h = 7, 6
innerW, innerH = 3, 3

prolog = Prolog()
prolog.consult("agent.pl")

walls = []


def change_symbol(board, X, Y, symbolno, symbol):
    if f'{X},{Y}' not in walls:
        cell = board[X][Y]
        if symbolno == 1:
            cell[0][0] = symbol
        elif symbolno == 2:
            cell[1][0] = symbol
        elif symbolno == 3:
            cell[2][0] = symbol
        elif symbolno == 4:
            cell[0][1] = symbol
        elif symbolno == 5:
            cell[1][1] = symbol
        elif symbolno == 6:
            cell[2][1] = symbol
        elif symbolno == 7:
            cell[0][2] = symbol
        elif symbolno == 8:
            cell[1][2] = symbol
        elif symbolno == 9:
            cell[2][2] = symbol


def set_wumpus_cell(board, X, Y):
    change_symbol(board, X, Y, 5, "W")
    change_symbol(board, X, Y, 6, "-")
    change_symbol(board, X, Y, 4, "-")
    change_symbol(board, X+1, Y, 2, "=")
    change_symbol(board, X-1, Y, 2, "=")
    change_symbol(board, X, Y+1, 2, "=")
    change_symbol(board, X, Y-1, 2, "=")


def set_portal_cell(board, X, Y):
    change_symbol(board, X, Y, 5, "O")
    change_symbol(board, X, Y, 6, "-")
    change_symbol(board, X, Y, 4, "-")
    change_symbol(board, X+1, Y, 3, "T")
    change_symbol(board, X-1, Y, 3, "T")
    change_symbol(board, X, Y+1, 3, "T")
    change_symbol(board, X, Y-1, 3, "T")


def set_wall_cell(board, X, Y):
    walls.append(f'{X},{Y}')
    board[X][Y] = [['#' for innerY in range(
        innerH)] for innerX in range(innerW)]


def generate_map():
    board = [[[['.' for innerY in range(innerH)] for innerX in range(innerW)]
              for y in range(h)] for x in range(w)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            if Y == 0 or Y == len(board[X])-1 or X == 0 or X == len(board) - 1:
                set_wall_cell(board, X, Y)
            else:
                change_symbol(board, X, Y, 5, "s")

    change_symbol(board, 2, 1, 6, "-")
    change_symbol(board, 2, 1, 4, "-")
    change_symbol(board, 2, 1, 5, "^")
    change_symbol(board, 3, 2, 7, "*")
    set_wumpus_cell(board, 2, 4)
    set_portal_cell(board, 4, 3)

    return board


def print_map_with_border(board):
    line = [["|" for y in range(innerH)] for x in range(h)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            cell = board[X][Y]
            for innerX in range(len(cell)):
                for innerY in range(len(cell[innerX])):
                    if innerX == 2 and X != len(board)-1:
                        line[Y][innerY] += f" {cell[innerX][innerY]} | |"
                    else:
                        line[Y][innerY] += f" {cell[innerX][innerY]} |"

    decorator = ""

    for i in range(w):
        decorator += "+"

        for j in range(innerW):
            decorator += "---+"

        decorator += " "

    for i in range(h-1, -1, -1):
        print(decorator)
        for j in range(3):
            print(line[i][j])
            print(decorator)
        print()


def print_map(board):

    line = [["" for y in range(innerH)] for x in range(h)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            cell = board[X][Y]
            for innerX in range(len(cell)):

                for innerY in range(len(cell[innerX])):
                    if innerX == 2 and X != len(board)-1:
                        line[Y][innerY] += f" {cell[innerX][innerY]}  "
                    else:
                        line[Y][innerY] += f" {cell[innerX][innerY]}"

    for i in range(h-1, -1, -1):
        for j in range(innerH):
            print(line[i][j])
        print()


def main():
    board = generate_map()
    print_map(board)


main()
