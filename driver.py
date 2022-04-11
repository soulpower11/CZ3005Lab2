from pyswip import Prolog
rm ast import While

# X row width
# Y column height

w, h = 7, 6
innerW, innerH = 3, 3

prolog = Prolog()
prolog.consult("agent.pl")

walls = []
wampus = []
portals = []
has_arrow = True
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
    change_symbol(board, X, Y, 4, "-")
    change_symbol(board, X, Y, 5, "W")
    change_symbol(board, X, Y, 6, "-")
    if f'{X},{Y}' not in wampus:
        wampus.append(f'{X},{Y}')
    change_symbol(board, X+1, Y, 2, "=")
    change_symbol(board, X-1, Y, 2, "=")
    change_symbol(board, X, Y+1, 2, "=")
    change_symbol(board, X, Y-1, 2, "=")


def set_portal_cell(board, X, Y):
    change_symbol(board, X, Y, 4, "-")
    change_symbol(board, X, Y, 5, "O")
    change_symbol(board, X, Y, 6, "-")
    portals.append(f'{X},{Y}')
    change_symbol(board, X+1, Y, 3, "T")
    change_symbol(board, X-1, Y, 3, "T")
    change_symbol(board, X, Y+1, 3, "T")
    change_symbol(board, X, Y-1, 3, "T")


def kill_wampus(board, X, Y):
    change_symbol(board, X, Y, 4, " ")
    change_symbol(board, X, Y, 5, "s")
    change_symbol(board, X, Y, 6, " ")
    wampus.remove(f'{X},{Y}')
    change_symbol(board, X+1, Y, 2, ".")
    change_symbol(board, X-1, Y, 2, ".")
    change_symbol(board, X, Y+1, 2, ".")
    change_symbol(board, X, Y-1, 2, ".")


def set_visited_cell(board, X, Y):
    change_symbol(board, X, Y, 1, ".")
    change_symbol(board, X, Y, 4, " ")
    change_symbol(board, X, Y, 5, "S")
    change_symbol(board, X, Y, 6, " ")
    change_symbol(board, X, Y, 8, ".")
    change_symbol(board, X, Y, 9, ".")


def set_agent_cell(board, X, Y, direction):
    change_symbol(board, X, Y, 1, ".")
    change_symbol(board, X, Y, 4, "-")
    change_symbol(board, X, Y, 6, "-")
    change_symbol(board, X, Y, 8, ".")
    change_symbol(board, X, Y, 9, ".")
    if direction == 'north':
        change_symbol(board, X, Y, 5, "∧")
    elif direction == 'west':
        change_symbol(board, X, Y, 5, "<")
    elif direction == 'east':
        change_symbol(board, X, Y, 5, ">")
    elif direction == 'south':
        change_symbol(board, X, Y, 5, "∨")


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


def generate_abs_map():
    board = [[generate_cell() for Y in range(h)] for X in range(w)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            if Y == 0 or Y == len(board[X])-1 or X == 0 or X == len(board) - 1:
                set_wall_cell(board, X, Y)
            else:
                change_symbol(board, X, Y, 5, "s")

    set_agent_cell(board, 2, 1, 'north')
    change_symbol(board, 2, 1, 1, "%")
    agent.update({'direction': 'north', 'X': 2, 'Y': 1})
    global has_arrow
    has_arrow = True
    change_symbol(board, 3, 2, 7, "*")
    set_wumpus_cell(board, 2, 4)
    set_portal_cell(board, 4, 3)

    return board


def reset_map(board):
    for X in range(len(board)):
        for Y in range(len(board[X])):
            if f'{X},{Y}' not in wampus and f'{X},{Y}' not in walls and f'{X},{Y}' not in portals:
                change_symbol(board, X, Y, 5, "s")

    set_agent_cell(board, 2, 1, 'north')
    change_symbol(board, 2, 1, 1, "%")
    agent['direction'] = 'north'
    agent['X'] = 2
    agent['Y'] = 1
    global has_arrow
    has_arrow = True
    change_symbol(board, 3, 2, 7, "*")
    set_wumpus_cell(board, 2, 4)


def teleport(board):
    for X in range(len(board)):
        for Y in range(len(board[X])):
            if f'{X},{Y}' not in wampus and f'{X},{Y}' not in walls and f'{X},{Y}' not in portals:
                change_symbol(board, X, Y, 5, "s")

    set_agent_cell(board, 5, 4, 'north')
    change_symbol(board, 5, 4, 1, "%")
    agent['direction'] = 'north'
    agent['X'] = 5
    agent['Y'] = 4


def move_forward(board):
    direction = agent['direction']
    X = agent['X']
    Y = agent['Y']

    if direction == 'north':
        Y1 = Y+1
        if f'{X},{Y1}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
        elif f'{X},{Y1}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
        elif f'{X},{Y1}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X, Y1, direction)
            agent['Y'] = Y1
    elif direction == 'west':
        X1 = X-1
        if f'{X1},{Y}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
        elif f'{X1},{Y}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
        elif f'{X1},{Y}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X1, Y, direction)
            agent['X'] = X1
    elif direction == 'east':
        X1 = X+1
        if f'{X1},{Y}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
        elif f'{X1},{Y}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
        if f'{X1},{Y}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X1, Y, direction)
            agent['X'] = X1
    elif direction == 'south':
        Y1 = Y-1
        if f'{X},{Y1}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
        elif f'{X},{Y1}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
        elif f'{X},{Y1}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X, Y1, direction)
            agent['Y'] = Y1


def turn_left(board):
    direction = agent['direction']
    X = agent['X']
    Y = agent['Y']
    if direction == 'north':
        set_agent_cell(board, X, Y, 'west')
        agent['direction'] = 'west'
    elif direction == 'west':
        set_agent_cell(board, X, Y, 'south')
        agent['direction'] = 'south'
    elif direction == 'east':
        set_agent_cell(board, X, Y, 'north')
        agent['direction'] = 'north'
    elif direction == 'south':
        set_agent_cell(board, X, Y, 'east')
        agent['direction'] = 'east'


def turn_right(board):
    direction = agent['direction']
    X = agent['X']
    Y = agent['Y']
    if direction == 'north':
        set_agent_cell(board, X, Y, 'east')
        agent['direction'] = 'east'
    elif direction == 'west':
        set_agent_cell(board, X, Y, 'north')
        agent['direction'] = 'north'
    elif direction == 'east':
        set_agent_cell(board, X, Y, 'south')
        agent['direction'] = 'south'
    elif direction == 'south':
        set_agent_cell(board, X, Y, 'west')
        agent['direction'] = 'west'


def pickup(board):
    X = agent['X']
    Y = agent['Y']
    change_symbol(board, X, Y, 7, ".")


def shoot(board):
    direction = agent['direction']
    X = agent['X']
    Y = agent['Y']
    global has_arrow

    if has_arrow:
        if direction == 'north':
            for Y1 in range(Y+1, h-1):
                cell = board[X][Y1]
                if cell[1][1] == 'W':
                    kill_wampus(board, X, Y1)
                    change_symbol(board, X, Y, 9, "@")
            has_arrow = False
        elif direction == 'west':
            for X1 in range(X-1, 0, -1):
                cell = board[X1][Y]
                if cell[1][1] == 'W':
                    kill_wampus(board, X1, Y)
                    change_symbol(board, X, Y, 9, "@")
        elif direction == 'east':
            for X1 in range(X+1, w-1):
                cell = board[X1][Y]
                if cell[1][1] == 'W':
                    has_arrow = False
                    kill_wampus(board, X1, Y)
                    change_symbol(board, X, Y, 9, "@")
            has_arrow = False
        elif direction == 'south':
            for Y1 in range(Y-1, 0, -1):
                cell = board[X][Y1]
                if cell[1][1] == 'W':
                    has_arrow = False
                    kill_wampus(board, X, Y1)
                    change_symbol(board, X, Y, 9, "@")
            has_arrow = False


def move_agent(board, action):
    if action == 'moveforward':
        move_forward(board)
    elif action == 'turnleft':
        turn_left(board)
    elif action == 'turnright':
        turn_right(board)
    elif action == 'pickup':
        pickup(board)
    elif action == 'shoot':
        shoot(board)


def get_indicator(board):
    indicators = []
    X = agent['X']
    Y = agent['Y']
    cell = board[X][Y]

    if cell[0][0] == '%':
        indicators.append('on')
    else:
        indicators.append('off')
    if cell[1][0] == '=':
        indicators.append('on')
    else:
        indicators.append('off')
    if cell[2][0] == 'T':
        indicators.append('on')
    else:
        indicators.append('off')
    if cell[0][2] == '*':
        indicators.append('on')
    else:
        indicators.append('off')
    if cell[1][2] == 'B':
        indicators.append('on')
    else:
        indicators.append('off')
    if cell[2][2] == '@':
        indicators.append('on')
    else:
        indicators.append('off')

    return indicators


def print_map_with_border(board):
    line = [["|" for Y in range(innerH)] for X in range(h)]

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


def print_abs_map(board):

    line = [["" for Y in range(innerH)] for X in range(h)]

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


def print_relative_map():
    board = [[generate_cell() for Y in range(h)] for X in range(w)]

    current = list(prolog.query("current(X,Y,D)"))[0]
    print(current)

    direction = current['D']
    X = current['X']
    Y = current['Y']

    set_agent_cell(board, X, Y, 'north')

    visited = []
    for soln in prolog.query("visited(X,Y)"):
        visited.append(f'{soln["X"]},{soln["Y"]}')

    print(visited)

    line = [["" for Y in range(innerH)] for X in range(h)]

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
    board = generate_abs_map()
    print_abs_map(board)
    # print_relative()
    while True:
        print("1. Testing Mode")
        print("0. Exit")
        option = input()
        if option == '1':
            print_abs_map(board)
            while True:
                print('Actions')
                print('1. Move Forward')
                print('2. Turn Left')
                print('3. Turn Right')
                print('4. Pick Up')
                print('5. Shoot')
                print("0. Exit")
                option = input()
                if option == '1':
                    move_agent(board, 'moveforward')
                    print_abs_map(board)
                    indicators = ','.join(map(str, get_indicator(board)))
                    list(prolog.query(
                        f"move(moveforward,[{indicators}])"))
                    print_relative_map()
                elif option == '2':
                    move_agent(board, 'turnleft')
                    list(prolog.query(
                        f"move(turnleft,[{indicators}])"))
                    print_relative_map()
                elif option == '3':
                    move_agent(board, 'turnright')
                    list(prolog.query(
                        f"move(turnright,[{indicators}])"))
                    print_relative_map()
                elif option == '4':
                    move_agent(board, 'pickup')
                    list(prolog.query(
                        f"move(pickup,[{indicators}])"))
                    print_relative_map()
                elif option == '5':
                    move_agent(board, 'shoot')
                    list(prolog.query(
                        f"move(shoot,[{indicators}])"))
                    print_relative_map()
                elif option == '0':
                    X = agent['X']
                    Y = agent['Y']
                    set_visited_cell(board, X, Y)
                    reset_map(board)
                    break
        elif option == '0':
            break


main()
