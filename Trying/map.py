from pyswip import Prolog
import random
from itertools import product
prolog = Prolog()
prolog.consult("Agent.pl")

walls = []
#RelativeWall = []
agent = {}

def GenerateMap():
    board = [[" " for a in range(6)] for b in range(7)]

    coord = list(product(range(2, 5), range(2, 4)))
    randcoord = random.sample(coord, 6)
    randcoord[0] = (1, 1)

    newMap = GenerateCell(board, randcoord)
    return newMap, randcoord

def GenerateCell(board, coor):
    for X in range(len(board)):
        for Y in range(len(board[X])):
            board[X][Y] = [["." for a in range(3)] for b in range(3)]
    for X in range(len(board)):
        for Y in range(len(board[X])):
            ChangeSymbol(board,X,Y, 4, " ")
            ChangeSymbol(board,X,Y, 5, "s")
            ChangeSymbol(board,X,Y, 6, " ")
            if(X == 0 or Y == 0 or X == len(board)-1 or Y == len(board[X])-1):
                SetWall(board, X, Y)
            
    agent.update({'direction': 'north', 'X': 1, 'Y': 1})
    ChangeSymbol(board, coor[1][0], coor[1][1], 7, "*")
    SetStartingCell(board, coor[0][0], coor[0][1])
    SetWumpusCell(board, coor[2][0], coor[2][1])
    SetPortalCell(board, coor[3][0], coor[3][1])
    SetPortalCell(board, coor[4][0], coor[4][1])
    SetPortalCell(board, coor[5][0], coor[5][1])

    return board
    
def ChangeSymbol(board,X,Y, symbolno, symbol):
    if f'{X},{Y}' not in walls:
        cell = board[X][Y]
        if(symbolno == 1):
            cell[0][0] = symbol
        elif(symbolno == 2):
            cell[1][0] = symbol
        elif(symbolno == 3):
            cell[2][0] = symbol
        elif(symbolno == 4):
            cell[0][1] = symbol
        elif(symbolno == 5):
            cell[1][1] = symbol
        elif(symbolno == 6):
            cell[2][1] = symbol
        elif(symbolno == 7):
            cell[0][2] = symbol
        elif(symbolno == 8):
            cell[1][2] = symbol
        elif(symbolno == 9):
            cell[2][2] = symbol

def RChangeSymbol(board,X,Y, symbolno, symbol):
    cell = board[X][Y]
    if(symbolno == 1):
        cell[0][0] = symbol
    elif(symbolno == 2):
        cell[1][0] = symbol
    elif(symbolno == 3):
        cell[2][0] = symbol
    elif(symbolno == 4):
        cell[0][1] = symbol
    elif(symbolno == 5):
        cell[1][1] = symbol
    elif(symbolno == 6):
        cell[2][1] = symbol
    elif(symbolno == 7):
        cell[0][2] = symbol
    elif(symbolno == 8):
        cell[1][2] = symbol
    elif(symbolno == 9):
        cell[2][2] = symbol


def SetStartingCell(board, X, Y):
    ChangeSymbol(board, X, Y, 4, "-")
    ChangeSymbol(board, X, Y, 5, "^")
    ChangeSymbol(board, X, Y, 6, "-")

def SetWumpusCell(board, X, Y):
    ChangeSymbol(board, X, Y, 4, "-")
    ChangeSymbol(board, X, Y, 5, "W")
    ChangeSymbol(board, X, Y, 6, "-")
    ChangeSymbol(board, X+1, Y, 2, "=")
    ChangeSymbol(board, X-1, Y, 2, "=")
    ChangeSymbol(board, X, Y+1, 2, "=")
    ChangeSymbol(board, X, Y-1, 2, "=")

def SetPortalCell(board, X, Y):
    ChangeSymbol(board, X, Y, 4, "-")
    ChangeSymbol(board, X, Y, 5, "O")
    ChangeSymbol(board, X, Y, 6, "-")
    ChangeSymbol(board, X+1, Y, 3, "T")
    ChangeSymbol(board, X-1, Y, 3, "T")
    ChangeSymbol(board, X, Y+1, 3, "T")
    ChangeSymbol(board, X, Y-1, 3, "T")

def SetWall(board, X, Y):
    walls.append(f'{X},{Y}')
    board[X][Y] = [['#' for innerY in range(3)] for innerX in range(3)]

# def SetRelativeWall(board, X, Y):
#     RelativeWall.append(f'{X},{Y}')
#     board[X][Y] = [[' ' for innerY in range(3)] for innerX in range(3)]

def SetUnknownCell(board, X, Y):
    RChangeSymbol(board, X, Y, 4, " ")
    RChangeSymbol(board, X, Y, 5, "?")
    RChangeSymbol(board, X, Y, 6, " ")

def addDot(board, X, Y):
    for i in range(1, 10):
        RChangeSymbol(board, X, Y, i, ".")

def CellAroundCell(board, X, Y):
    if(board[X-1][Y][1][1] == " "):
        addDot(board, X-1, Y)
        SetUnknownCell(board, X-1, Y)
    if(board[X+1][Y][1][1] == " "):
        addDot(board, X+1, Y)
        SetUnknownCell(board, X+1, Y)
    if(board[X][Y+1][1][1] == " "):
        addDot(board, X, Y+1)
        SetUnknownCell(board, X, Y+1)
    if(board[X][Y-1][1][1] == " "):
        addDot(board, X, Y-1)
        SetUnknownCell(board, X, Y-1)


#------------------------------------------------------------------------------------

def localisation(absMap, coor):
    if(prolog.query(localisation(absMap[coor[0]][coor[1]] )== True)):
        return True
    else:
        return False

def create_relativeMap():
    relativeboard = [[" " for a in range(6)] for b in range(7)]
    for X in range(len(relativeboard)):
        for Y in range(len(relativeboard[X])):
            relativeboard[X][Y] = [[" " for a in range(3)] for b in range(3)]
    # for X in range(len(relativeboard)):
    #     for Y in range(len(relativeboard[X])):
    #         if(X == 0 or Y == 0 or X == len(relativeboard)-1 or Y == len(relativeboard[X])-1):
    #             SetRelativeWall(relativeboard, X, Y)
    return relativeboard


def Update_RelativeMap(RelativeMap, starting):
    if(starting == True):
        addDot(RelativeMap, 1, 1)
        SetStartingCell(RelativeMap, 1, 1)
        CellAroundCell(RelativeMap, 1, 1)
        Print_Map(RelativeMap)

def Print_Map(map):
    innerW = 3
    innerH = 3
    w = 7
    h = 6

    line = [["" for y in range(innerH)] for x in range(h)]

    for X in range(len(map)):
        for Y in range(len(map[X])):
            cell = map[X][Y]
            for innerX in range(len(cell)):

                for innerY in range(len(cell[innerX])):
                    if innerX == 2 and X != len(map)-1:
                        line[Y][innerY] += f" {cell[innerX][innerY]}  "
                    else:
                        line[Y][innerY] += f" {cell[innerX][innerY]}"

    for i in range(5, -1, -1):
        for j in range(3):
            print(line[i][j])
        print()

    #print action sequence
    #print realtive map
    #print sensory that is turn on
def move_forward(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']

    if direction == 'north':
        y1 = y+1
        if f'{x},{y1}' not in walls:
            ChangeSymbol(board, x, y, 6, ".")
            ChangeSymbol(board, x, y, 4, ".")
            ChangeSymbol(board, x, y, 8, ".")
            ChangeSymbol(board, x, y, 5, "S")
            ChangeSymbol(board, x, y1, 6, "-")
            ChangeSymbol(board, x, y1, 4, "-")
            ChangeSymbol(board, x, y1, 5, "∧")
            agent['Y'] = y1
        else:
            ChangeSymbol(board, x, y, 8, "B")
    elif direction == 'west':
        x1 = x-1
        if f'{x1},{y}' not in walls:
            ChangeSymbol(board, x, y, 6, ".")
            ChangeSymbol(board, x, y, 4, ".")
            ChangeSymbol(board, x, y, 8, ".")
            ChangeSymbol(board, x, y, 5, "S")
            ChangeSymbol(board, x1, y, 6, "-")
            ChangeSymbol(board, x1, y, 4, "-")
            ChangeSymbol(board, x1, y, 5, "<")
            agent['X'] = x1
        else:
            ChangeSymbol(board, x, y, 8, "B")
    elif direction == 'east':
        x1 = x+1
        if f'{x1},{y}' not in walls:
            ChangeSymbol(board, x, y, 6, ".")
            ChangeSymbol(board, x, y, 4, ".")
            ChangeSymbol(board, x, y, 8, ".")
            ChangeSymbol(board, x, y, 5, "S")
            ChangeSymbol(board, x1, y, 6, "-")
            ChangeSymbol(board, x1, y, 4, "-")
            ChangeSymbol(board, x1, y, 5, ">")
            agent['X'] = x1
        else:
            ChangeSymbol(board, x, y, 8, "B")
    elif direction == 'south':
        y1 = y-1
        if f'{x},{y1}' not in walls:
            ChangeSymbol(board, x, y, 6, ".")
            ChangeSymbol(board, x, y, 4, ".")
            ChangeSymbol(board, x, y, 8, ".")
            ChangeSymbol(board, x, y, 5, "S")
            ChangeSymbol(board, x, y1, 6, "-")
            ChangeSymbol(board, x, y1, 4, "-")
            ChangeSymbol(board, x, y1, 5, "∨")
            agent['Y'] = y1
        else:
            ChangeSymbol(board, x, y, 8, "B")


def turn_left(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']
    if direction == 'north':
        ChangeSymbol(board, x, y, 5, "<")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'west'
    elif direction == 'west':
        ChangeSymbol(board, x, y, 5, "∨")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'south'
    elif direction == 'east':
        ChangeSymbol(board, x, y, 5, "∧")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'north'
    elif direction == 'south':
        ChangeSymbol(board, x, y, 5, ">")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'east'


def turn_right(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']
    if direction == 'north':
        ChangeSymbol(board, x, y, 5, ">")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'east'
    elif direction == 'west':
        ChangeSymbol(board, x, y, 5, "∧")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'north'
    elif direction == 'east':
        ChangeSymbol(board, x, y, 5, "∨")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'south'
    elif direction == 'south':
        ChangeSymbol(board, x, y, 5, "<")
        ChangeSymbol(board, x, y, 8, ".")
        agent['direction'] = 'west'


def pickup(board):
    x = agent['X']
    y = agent['Y']
    ChangeSymbol(board, x, y, 7, ".")


def move_agent(board, action):
    if action == 'moveforward':
        move_forward(board)
    elif action == 'turnleft':
        turn_left(board)
    elif action == 'turnright':
        turn_right(board)
    elif action == 'pickup':
        pickup(board)

def main():
    AbsoluteMap, coor = GenerateMap()
    RelativeMap = create_relativeMap()
    Print_Map(AbsoluteMap)
    reset = True #prolog.query("reborn")
    Update_RelativeMap(RelativeMap, reset)
    reset = False
    while True:
        print("1) Move forward")
        print("2) Turn left")
        print("3) Turn right")
        print("4) Pick up")
        print("0) Exit")
        option = input("What option do you want to do? ")
        # print("Type: LA, LB, LC, LD, LE, LF")
        # status = input("What is the status of the cell? ")
        if option == '1':
            move_agent(AbsoluteMap, 'moveforward')
            Print_Map(AbsoluteMap)
            list(prolog.query("move(moveforward,[on,off,off,off,off,on])"))
                    # print_relative()
        elif option == '2':
            move_agent(AbsoluteMap, 'turnleft')
            list(prolog.query("move(turnleft,[on,off,off,off,off,on])"))
            Print_Map(AbsoluteMap)
                    # print_relative()
        elif option == '3':
            move_agent(AbsoluteMap, 'turnright')
            list(prolog.query("move(turnright,[on,off,off,off,off,on])"))
            Print_Map(AbsoluteMap)
                    # print_relative()
        elif option == '4':
            move_agent(AbsoluteMap, 'pickup')
            list(prolog.query("move(pickup,[on,off,off,off,off,on])"))
            Print_Map(AbsoluteMap)
                    # print_relative()
        elif option == '0':
            break

        prolog.query(move(action, status))

        #Print_RelativeMap(RelativeMap)

        break
    return

main()