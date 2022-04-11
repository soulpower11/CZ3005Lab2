from pyswip import Prolog
from ast import While

# X row width
# Y column height

w, h = 7, 6
innerW, innerH = 3, 3

prolog = Prolog()
prolog.consult("agent.pl")

walls = []

agent = {}


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


def generate_cell():
    cell = [['.' for innerY in range(innerH)] for innerX in range(innerW)]
    cell[0][1] = " "
    cell[1][1] = "?"
    cell[2][1] = " "

    return cell


def generate_map():
    board = [[generate_cell() for y in range(h)] for x in range(w)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            if Y == 0 or Y == len(board[X])-1 or X == 0 or X == len(board) - 1:
                set_wall_cell(board, X, Y)
            else:
                change_symbol(board, X, Y, 5, "s")

    change_symbol(board, 2, 1, 6, "-")
    change_symbol(board, 2, 1, 4, "-")
    change_symbol(board, 2, 1, 5, "∧")
    agent.update({'direction': 'north', 'X': 1, 'Y': 1})
    change_symbol(board, 3, 2, 7, "*")
    set_wumpus_cell(board, 2, 4)
    set_portal_cell(board, 4, 3)

    return board


def move_forward(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']

    if direction == 'north':
        y1 = y+1
        if f'{x},{y1}' not in walls:
            change_symbol(board, x, y, 6, ".")
            change_symbol(board, x, y, 4, ".")
            change_symbol(board, x, y, 8, ".")
            change_symbol(board, x, y, 5, "S")
            change_symbol(board, x, y1, 6, "-")
            change_symbol(board, x, y1, 4, "-")
            change_symbol(board, x, y1, 5, "∧")
            agent['Y'] = y1
        else:
            change_symbol(board, x, y, 8, "B")
    elif direction == 'west':
        x1 = x-1
        if f'{x1},{y}' not in walls:
            change_symbol(board, x, y, 6, ".")
            change_symbol(board, x, y, 4, ".")
            change_symbol(board, x, y, 8, ".")
            change_symbol(board, x, y, 5, "S")
            change_symbol(board, x1, y, 6, "-")
            change_symbol(board, x1, y, 4, "-")
            change_symbol(board, x1, y, 5, "<")
            agent['X'] = x1
        else:
            change_symbol(board, x, y, 8, "B")
    elif direction == 'east':
        x1 = x+1
        if f'{x1},{y}' not in walls:
            change_symbol(board, x, y, 6, ".")
            change_symbol(board, x, y, 4, ".")
            change_symbol(board, x, y, 8, ".")
            change_symbol(board, x, y, 5, "S")
            change_symbol(board, x1, y, 6, "-")
            change_symbol(board, x1, y, 4, "-")
            change_symbol(board, x1, y, 5, ">")
            agent['X'] = x1
        else:
            change_symbol(board, x, y, 8, "B")
    elif direction == 'south':
        y1 = y-1
        if f'{x},{y1}' not in walls:
            change_symbol(board, x, y, 6, ".")
            change_symbol(board, x, y, 4, ".")
            change_symbol(board, x, y, 8, ".")
            change_symbol(board, x, y, 5, "S")
            change_symbol(board, x, y1, 6, "-")
            change_symbol(board, x, y1, 4, "-")
            change_symbol(board, x, y1, 5, "∨")
            agent['Y'] = y1
        else:
            change_symbol(board, x, y, 8, "B")


def turn_left(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']
    if direction == 'north':
        change_symbol(board, x, y, 5, "<")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'west'
    elif direction == 'west':
        change_symbol(board, x, y, 5, "∨")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'south'
    elif direction == 'east':
        change_symbol(board, x, y, 5, "∧")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'north'
    elif direction == 'south':
        change_symbol(board, x, y, 5, ">")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'east'


def turn_right(board):
    direction = agent['direction']
    x = agent['X']
    y = agent['Y']
    if direction == 'north':
        change_symbol(board, x, y, 5, ">")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'east'
    elif direction == 'west':
        change_symbol(board, x, y, 5, "∧")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'north'
    elif direction == 'east':
        change_symbol(board, x, y, 5, "∨")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'south'
    elif direction == 'south':
        change_symbol(board, x, y, 5, "<")
        change_symbol(board, x, y, 8, ".")
        agent['direction'] = 'west'


def pickup(board):
    x = agent['X']
    y = agent['Y']
    change_symbol(board, x, y, 7, ".")


def move_agent(board, action):
    if action == 'moveforward':
        move_forward(board)
    elif action == 'turnleft':
        turn_left(board)
    elif action == 'turnright':
        turn_right(board)
    elif action == 'pickup':
        pickup(board)


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


def print_relative():
    board = [[[['.' for innerY in range(innerH)] for innerX in range(innerW)]
              for y in range(h)] for x in range(w)]

    visited = []
    for soln in prolog.query("visited(X,Y)"):
        visited.append(f'{soln["X"]},{soln["Y"]}')

    current = list(prolog.query("current(X,Y,D)"))[0]

    print(visited)
    print(current)

    line = [["" for y in range(innerH)] for x in range(h)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            if f'{X},{Y}' in visited:
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
    print_relative()
    while True:
        print("1. Testing Mode")
        print("0. Exit")
        option = input()
        if option == '1':
            while True:
                print('Actions')
                print('1. Move Forward')
                print('2. Turn Left')
                print('3. Turn Right')
                print('4. Pick Up')
                print("0. Exit")
                option = input()
                if option == '1':
                    move_agent(board, 'moveforward')
                    print_map(board)
                    list(prolog.query(
                        "move(moveforward,[on,off,off,off,off,on])"))
                    # print_relative()
                elif option == '2':
                    move_agent(board, 'turnleft')
                    list(prolog.query(
                        "move(turnleft,[on,off,off,off,off,on])"))
                    print_map(board)
                    # print_relative()
                elif option == '3':
                    move_agent(board, 'turnright')
                    list(prolog.query(
                        "move(turnright,[on,off,off,off,off,on])"))
                    print_map(board)
                    # print_relative()
                elif option == '4':
                    move_agent(board, 'pickup')
                    list(prolog.query(
                        "move(pickup,[on,off,off,off,off,on])"))
                    print_map(board)
                    # print_relative()
                elif option == '0':
                    break
        elif option == '0':
            break


main()
