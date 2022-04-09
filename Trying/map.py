from pyswip import Prolog
import random
from itertools import product
prolog = Prolog()
prolog.consult("Agent.pl")


def GenerateCell(board, coor):
    for x in range(7):
        for y in range(6):
            board[x][y] = [["." for a in range(3)] for b in range(3)]

    (board[coor[0][0]][coor[0][1]])[1][0] = "−"  # characterPosition
    (board[coor[1][0]][coor[1][1]])[2][0] = "*"  # coinPosition
    (board[coor[2][0]][coor[2][1]])[1][1] = "W"  # wumpusPosition
    (board[coor[3][0]][coor[3][1]])[1][1] = "O"  # portalPosition
    (board[coor[4][0]][coor[4][1]])[1][1] = "O"  # portalPosition
    (board[coor[5][0]][coor[5][1]])[1][1] = "O"  # portalPosition

    return board


def GenerateMap():
    board = [["|   |" for a in range(6)] for b in range(7)]

    coord = list(product(range(1, 6), range(1, 5)))
    randcoord = random.sample(coord, 6)
    randcoord[0] = (0, 0)

    newMap = GenerateCell(board, randcoord)
    return newMap, randcoord


def localisation(absMap, coor):
    if(prolog.query(localisation(absMap[coor[0]][coor[1]]) == True)):
        return True
    else:
        return False


def Toprint(Absmap, coor):
    decorator = ""

    for i in range(7):
        decorator += "+"
        for j in range(3):
            decorator += "---+"
        decorator += " "

    line = [["|" for y in range(3)] for x in range(6)]

    for X in range(len(Absmap)):
        for Y in range(len(Absmap[X])):
            cell = Absmap[X][Y]
            for innerX in range(len(cell)):

                for innerY in range(len(cell[innerX])):
                    if innerX == 2 and X != len(Absmap)-1:
                        line[Y][innerY] += f" {cell[innerY][innerX]} | |"
                    else:
                        line[Y][innerY] += f" {cell[innerY][innerX]} |"

    for i in range(6):
        print(decorator)
        for j in range(3):
            print(line[i][j])
            print(decorator)
        print()

    # print(coor)
    # print(Absmap[0][0][0][0], Absmap[0][0][0][1], Absmap[0][0][0][2], " ", Absmap[1][0][0][0], Absmap[1][0][0][1], Absmap[1][0][0][2], " ", Absmap[2][0][0][0], Absmap[2][0][0][1], Absmap[2][0][0][2], " ", Absmap[3][0][0][0], Absmap[3]
    #       [0][0][1], Absmap[3][0][0][2], " ", Absmap[4][0][0][0], Absmap[4][0][0][1], Absmap[4][0][0][2], " ", Absmap[5][0][0][0], Absmap[5][0][0][1], Absmap[5][0][0][2], " ", Absmap[6][0][0][0], Absmap[6][0][0][1], Absmap[6][0][0][2])
    # print(Absmap[0][0][1][0], Absmap[0][0][1][1], Absmap[0][0][1][2], " ", Absmap[1][0][1][0], Absmap[1][0][1][1], Absmap[1][0][1][2], " ", Absmap[2][0][1][0], Absmap[2][0][1][1], Absmap[2][0][1][2], " ", Absmap[3][0][1][0], Absmap[3]
    #       [0][1][1], Absmap[3][0][1][2], " ", Absmap[4][0][1][0], Absmap[4][0][1][1], Absmap[4][0][1][2], " ", Absmap[5][0][1][0], Absmap[5][0][1][1], Absmap[5][0][1][2], " ", Absmap[6][0][1][0], Absmap[6][0][1][1], Absmap[6][0][1][2])
    # print(Absmap[0][0][2][0], Absmap[0][0][2][1], Absmap[0][0][2][2], " ", Absmap[1][0][2][0], Absmap[1][0][2][1], Absmap[1][0][2][2], " ", Absmap[2][0][2][0], Absmap[2][0][2][1], Absmap[2][0][2][2], " ", Absmap[3][0][2][0], Absmap[3]
    #       [0][2][1], Absmap[3][0][2][2], " ", Absmap[4][0][2][0], Absmap[4][0][2][1], Absmap[4][0][2][2], " ", Absmap[5][0][2][0], Absmap[5][0][2][1], Absmap[5][0][2][2], " ", Absmap[6][0][2][0], Absmap[6][0][2][1], Absmap[6][0][2][2])
    # print("")
    # print(Absmap[0][1][0][0], Absmap[0][1][0][1], Absmap[0][0][0][2], " ", Absmap[1][1][0][0], Absmap[1][1][0][1], Absmap[1][1][0][2], " ", Absmap[2][1][0][0], Absmap[2][1][0][1], Absmap[2][1][0][2], " ", Absmap[3][1][0][0], Absmap[3]
    #       [1][0][1], Absmap[3][1][0][2], " ", Absmap[4][1][0][0], Absmap[4][1][0][1], Absmap[4][1][0][2], " ", Absmap[5][1][0][0], Absmap[5][1][0][1], Absmap[5][1][0][2], " ", Absmap[6][1][0][0], Absmap[6][1][0][1], Absmap[6][1][0][2])
    # print(Absmap[0][1][1][0], Absmap[0][1][1][1], Absmap[0][1][1][2], " ", Absmap[1][1][1][0], Absmap[1][1][1][1], Absmap[1][1][1][2], " ", Absmap[2][1][1][0], Absmap[2][1][1][1], Absmap[2][1][1][2], " ", Absmap[3][1][1][0], Absmap[3]
    #       [1][1][1], Absmap[3][1][1][2], " ", Absmap[4][1][1][0], Absmap[4][1][1][1], Absmap[4][1][1][2], " ", Absmap[5][1][1][0], Absmap[5][1][1][1], Absmap[5][1][1][2], " ", Absmap[6][1][1][0], Absmap[6][1][1][1], Absmap[6][1][1][2])
    # print(Absmap[0][1][2][0], Absmap[0][1][2][1], Absmap[0][1][2][2], " ", Absmap[1][1][2][0], Absmap[1][1][2][1], Absmap[1][1][2][2], " ", Absmap[2][1][2][0], Absmap[2][1][2][1], Absmap[2][1][2][2], " ", Absmap[3][1][2][0], Absmap[3]
    #       [1][2][1], Absmap[3][1][2][2], " ", Absmap[4][1][2][0], Absmap[4][1][2][1], Absmap[4][1][2][2], " ", Absmap[5][1][2][0], Absmap[5][1][2][1], Absmap[5][1][2][2], " ", Absmap[6][1][2][0], Absmap[6][1][2][1], Absmap[6][1][2][2])
    # print("")
    # print(Absmap[0][2][0][0], Absmap[0][2][0][1], Absmap[0][2][0][2], " ", Absmap[1][2][0][0], Absmap[1][2][0][1], Absmap[1][2][0][2], " ", Absmap[2][2][0][0], Absmap[2][2][0][1], Absmap[2][2][0][2], " ", Absmap[3][2][0][0], Absmap[3]
    #       [2][0][1], Absmap[3][2][0][2], " ", Absmap[4][2][0][0], Absmap[4][2][0][1], Absmap[4][2][0][2], " ", Absmap[5][2][0][0], Absmap[5][2][0][1], Absmap[5][2][0][2], " ", Absmap[6][2][0][0], Absmap[6][2][0][1], Absmap[6][2][0][2])
    # print(Absmap[0][2][1][0], Absmap[0][2][1][1], Absmap[0][2][1][2], " ", Absmap[1][2][1][0], Absmap[1][2][1][1], Absmap[1][2][1][2], " ", Absmap[2][2][1][0], Absmap[2][2][1][1], Absmap[2][2][1][2], " ", Absmap[3][2][1][0], Absmap[3]
    #       [2][1][1], Absmap[3][2][1][2], " ", Absmap[4][2][1][0], Absmap[4][2][1][1], Absmap[4][2][1][2], " ", Absmap[5][2][1][0], Absmap[5][2][1][1], Absmap[5][2][1][2], " ", Absmap[6][2][1][0], Absmap[6][2][1][1], Absmap[6][2][1][2])
    # print(Absmap[0][2][2][0], Absmap[0][2][2][1], Absmap[0][2][2][2], " ", Absmap[1][2][2][0], Absmap[1][2][2][1], Absmap[1][2][2][2], " ", Absmap[2][2][2][0], Absmap[2][2][2][1], Absmap[2][2][2][2], " ", Absmap[3][2][2][0], Absmap[3]
    #       [2][2][1], Absmap[3][2][2][2], " ", Absmap[4][2][2][0], Absmap[4][2][2][1], Absmap[4][2][2][2], " ", Absmap[5][2][2][0], Absmap[5][2][2][1], Absmap[5][2][2][2], " ", Absmap[6][2][2][0], Absmap[6][2][2][1], Absmap[6][2][2][2])
    # print("")
    # print(Absmap[0][3][0][0], Absmap[0][3][0][1], Absmap[0][3][0][2], " ", Absmap[1][3][0][0], Absmap[1][3][0][1], Absmap[1][3][0][2], " ", Absmap[2][3][0][0], Absmap[2][3][0][1], Absmap[2][3][0][2], " ", Absmap[3][3][0][0], Absmap[3]
    #       [3][0][1], Absmap[3][3][0][2], " ", Absmap[4][3][0][0], Absmap[4][3][0][1], Absmap[4][3][0][2], " ", Absmap[5][3][0][0], Absmap[5][3][0][1], Absmap[5][3][0][2], " ", Absmap[6][3][0][0], Absmap[6][3][0][1], Absmap[6][3][0][2])
    # print(Absmap[0][3][1][0], Absmap[0][3][1][1], Absmap[0][3][1][2], " ", Absmap[1][3][1][0], Absmap[1][3][1][1], Absmap[1][3][1][2], " ", Absmap[2][3][1][0], Absmap[2][3][1][1], Absmap[2][3][1][2], " ", Absmap[3][3][1][0], Absmap[3]
    #       [3][1][1], Absmap[3][3][1][2], " ", Absmap[4][3][1][0], Absmap[4][3][1][1], Absmap[4][3][1][2], " ", Absmap[5][3][1][0], Absmap[5][3][1][1], Absmap[5][3][1][2], " ", Absmap[6][3][1][0], Absmap[6][3][1][1], Absmap[6][3][1][2])
    # print(Absmap[0][3][2][0], Absmap[0][3][2][1], Absmap[0][3][2][2], " ", Absmap[1][3][2][0], Absmap[1][3][2][1], Absmap[1][3][2][2], " ", Absmap[2][3][2][0], Absmap[2][3][2][1], Absmap[2][3][2][2], " ", Absmap[3][3][2][0], Absmap[3]
    #       [3][2][1], Absmap[3][3][2][2], " ", Absmap[4][3][2][0], Absmap[4][3][2][1], Absmap[4][3][2][2], " ", Absmap[5][3][2][0], Absmap[5][3][2][1], Absmap[5][3][2][2], " ", Absmap[6][3][2][0], Absmap[6][3][2][1], Absmap[6][3][2][2])
    # print("")
    # print(Absmap[0][4][0][0], Absmap[0][4][0][1], Absmap[0][4][0][2], " ", Absmap[1][4][0][0], Absmap[1][4][0][1], Absmap[1][4][0][2], " ", Absmap[2][4][0][0], Absmap[2][4][0][1], Absmap[2][4][0][2], " ", Absmap[3][4][0][0], Absmap[3]
    #       [4][0][1], Absmap[3][4][0][2], " ", Absmap[4][4][0][0], Absmap[4][4][0][1], Absmap[4][4][0][2], " ", Absmap[5][4][0][0], Absmap[5][4][0][1], Absmap[5][4][0][2], " ", Absmap[6][4][0][0], Absmap[6][4][0][1], Absmap[6][4][0][2])
    # print(Absmap[0][4][1][0], Absmap[0][4][1][1], Absmap[0][4][1][2], " ", Absmap[1][4][1][0], Absmap[1][4][1][1], Absmap[1][4][1][2], " ", Absmap[2][4][1][0], Absmap[2][4][1][1], Absmap[2][4][1][2], " ", Absmap[3][4][1][0], Absmap[3]
    #       [4][1][1], Absmap[3][4][1][2], " ", Absmap[4][4][1][0], Absmap[4][4][1][1], Absmap[4][4][1][2], " ", Absmap[5][4][1][0], Absmap[5][4][1][1], Absmap[5][4][1][2], " ", Absmap[6][4][1][0], Absmap[6][4][1][1], Absmap[6][4][1][2])
    # print(Absmap[0][4][2][0], Absmap[0][4][2][1], Absmap[0][4][2][2], " ", Absmap[1][4][2][0], Absmap[1][4][2][1], Absmap[1][4][2][2], " ", Absmap[2][4][2][0], Absmap[2][4][2][1], Absmap[2][4][2][2], " ", Absmap[3][4][2][0], Absmap[3]
    #       [4][2][1], Absmap[3][4][2][2], " ", Absmap[4][4][2][0], Absmap[4][4][2][1], Absmap[4][4][2][2], " ", Absmap[5][4][2][0], Absmap[5][4][2][1], Absmap[5][4][2][2], " ", Absmap[6][4][2][0], Absmap[6][4][2][1], Absmap[6][4][2][2])
    # print("")
    # print(Absmap[0][5][0][0], Absmap[0][5][0][1], Absmap[0][5][0][2], " ", Absmap[1][5][0][0], Absmap[1][5][0][1], Absmap[1][5][0][2], " ", Absmap[2][5][0][0], Absmap[2][5][0][1], Absmap[2][5][0][2], " ", Absmap[3][5][0][0], Absmap[3]
    #       [5][0][1], Absmap[3][5][0][2], " ", Absmap[4][5][0][0], Absmap[4][5][0][1], Absmap[4][5][0][2], " ", Absmap[5][5][0][0], Absmap[5][5][0][1], Absmap[5][5][0][2], " ", Absmap[6][5][0][0], Absmap[6][5][0][1], Absmap[6][5][0][2])
    # print(Absmap[0][5][1][0], Absmap[0][5][1][1], Absmap[0][5][1][2], " ", Absmap[1][5][1][0], Absmap[1][5][1][1], Absmap[1][5][1][2], " ", Absmap[2][5][1][0], Absmap[2][5][1][1], Absmap[2][5][1][2], " ", Absmap[3][5][1][0], Absmap[3]
    #       [5][1][1], Absmap[3][5][1][2], " ", Absmap[4][5][1][0], Absmap[4][5][1][1], Absmap[4][5][1][2], " ", Absmap[5][5][1][0], Absmap[5][5][1][1], Absmap[5][5][1][2], " ", Absmap[6][5][1][0], Absmap[6][5][1][1], Absmap[6][5][1][2])
    # print(Absmap[0][5][2][0], Absmap[0][5][2][1], Absmap[0][5][2][2], " ", Absmap[1][5][2][0], Absmap[1][5][2][1], Absmap[1][5][2][2], " ", Absmap[2][5][2][0], Absmap[2][5][2][1], Absmap[2][5][2][2], " ", Absmap[3][5][2][0], Absmap[3]
    #       [5][2][1], Absmap[3][5][2][2], " ", Absmap[4][5][2][0], Absmap[4][5][2][1], Absmap[4][5][2][2], " ", Absmap[5][5][2][0], Absmap[5][5][2][1], Absmap[5][5][2][2], " ", Absmap[6][5][2][0], Absmap[6][5][2][1], Absmap[6][5][2][2])
    # print("")

    # print action sequence
    # print realtive map
    # print sensory that is turn on


def main():
    AbsoluteMap, coor = GenerateMap()
    Toprint(AbsoluteMap, coor)
    while True:

        break
    return


main()
