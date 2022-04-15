import random
from pyswip import Prolog

# X row width
# Y column height
# Rows correspond to the second coordinate of the absolute position and the columns to the first coordinate of the absolute position.

w, h = 7, 6

innerW, innerH = 3, 3

prolog = Prolog()
prolog.consult("agent.pl")


walls = []
wampus = []
portals = []
agent = {}
origin = {}
coins = []

rwalls = []
rwalls_map = []
visited_map = []
visited = []
safe_map = []
safe = []
rcurrent = ''
rcurrent_map = ''
rh = h*2
rw = w*2

dead = False
teleported = False
gameend = False


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
    if f'{X},{Y}' not in portals:
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


def change_rsymbol(board, X, Y, symbolno, symbol):
    if f'{X},{Y}' not in rwalls:
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


def set_ragent_cell(absmap, board, X, Y, direction):
    cell = absmap[agent['X']][agent['Y']]

    confounded = False
    stench = False
    tingle = False
    glitter = False
    bump = False
    scream = False

    if cell[0][0] == '%':
        confounded = True
    if cell[1][0] == '=':
        stench = True
    if cell[2][0] == 'T':
        tingle = True
    if cell[0][2] == '*':
        glitter = True
    if cell[1][2] == 'B':
        bump = True
    if cell[2][2] == '@':
        scream = True

    if confounded:
        change_rsymbol(board, X, Y, 1, "%")
    else:
        change_rsymbol(board, X, Y, 1, ".")
    if stench:
        change_rsymbol(board, X, Y, 2, "=")
    else:
        change_rsymbol(board, X, Y, 2, ".")
    if tingle:
        change_rsymbol(board, X, Y, 3, "T")
    else:
        change_rsymbol(board, X, Y, 3, ".")
    if glitter:
        change_rsymbol(board, X, Y, 7, "*")
    else:
        change_rsymbol(board, X, Y, 7, ".")
    if bump:
        change_rsymbol(board, X, Y, 8, "B")
    else:
        change_rsymbol(board, X, Y, 8, ".")
    if scream:
        change_rsymbol(board, X, Y, 9, "@")
    else:
        change_rsymbol(board, X, Y, 9, ".")

    change_rsymbol(board, X, Y, 4, "-")
    change_rsymbol(board, X, Y, 6, "-")
    if direction == 'rnorth':
        change_rsymbol(board, X, Y, 5, "∧")
    elif direction == 'rwest':
        change_rsymbol(board, X, Y, 5, "<")
    elif direction == 'reast':
        change_rsymbol(board, X, Y, 5, ">")
    elif direction == 'rsouth':
        change_rsymbol(board, X, Y, 5, "∨")


def set_rwumpus_cell(board, X, Y):
    change_rsymbol(board, X, Y, 4, "-")
    change_rsymbol(board, X, Y, 5, "W")
    change_rsymbol(board, X, Y, 6, "-")


def set_rportal_cell(board, X, Y):
    change_rsymbol(board, X, Y, 4, "-")
    change_rsymbol(board, X, Y, 5, "O")
    change_rsymbol(board, X, Y, 6, "-")


def kill_rwampus(board, X, Y):
    change_rsymbol(board, X, Y, 4, " ")
    change_rsymbol(board, X, Y, 5, "s")
    change_rsymbol(board, X, Y, 6, " ")


def set_rvisited_cell(board, X, Y):
    change_rsymbol(board, X, Y, 1, ".")
    change_rsymbol(board, X, Y, 4, " ")
    change_rsymbol(board, X, Y, 5, "S")
    change_rsymbol(board, X, Y, 6, " ")
    change_rsymbol(board, X, Y, 8, ".")
    change_rsymbol(board, X, Y, 9, ".")


def set_rsafe_cell(board, X, Y):
    change_rsymbol(board, X, Y, 1, ".")
    change_rsymbol(board, X, Y, 4, " ")
    change_rsymbol(board, X, Y, 5, "s")
    change_rsymbol(board, X, Y, 6, " ")
    change_rsymbol(board, X, Y, 8, ".")
    change_rsymbol(board, X, Y, 9, ".")


def set_rwall_cell(board, X, Y, direction):
    if direction == 'rnorth':
        Y = Y+1
    elif direction == 'rwest':
        X = X-1
    elif direction == 'reast':
        X = X+1
    elif direction == 'rsouth':
        Y = Y-1

    if f'{X},{Y}' not in rwalls:
        rwalls.append(f'{X},{Y}')
        rwalls_map.append(f'{w+X},{h+Y}')

    board[w+X][h+Y] = [['#' for innerY in range(
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
    origin.update({'X': 2, 'Y': 1})
    coins.clear()
    change_symbol(board, 5, 4, 7, "*")
    coins.append('3,2')
    set_wumpus_cell(board, 2, 4)
    set_portal_cell(board, 4, 3)
    set_portal_cell(board, 4, 2)
    set_portal_cell(board, 4, 1)

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
    coins.clear()
    change_symbol(board, 3, 2, 7, "*")
    coins.append('3,2')
    set_wumpus_cell(board, 2, 4)


def teleport(board):
    for X in range(len(board)):
        for Y in range(len(board[X])):
            if f'{X},{Y}' not in wampus and f'{X},{Y}' not in walls and f'{X},{Y}' not in portals:
                change_symbol(board, X, Y, 5, "s")

    randY = random.randint(0, h-1)
    randX = random.randint(0, w-1)
    while f'{randX},{randY}' in wampus or f'{randX},{randY}' in walls or f'{randX},{randY}' in portals or f'{randX+1},{randY}' in portals or f'{randX-1},{randY}' in portals or f'{randX+1},{randY}' in wampus or f'{randX-1},{randY}' in wampus or f'{randX},{randY+1}' in portals or f'{randX},{randY-1}' in portals or f'{randX},{randY+1}' in wampus or f'{randX},{randY-1}' in wampus:
        randY = random.randint(0, h-1)
        randX = random.randint(0, w-1)

    set_agent_cell(board, randX, randY, 'north')
    change_symbol(board, randX, randY, 1, "%")
    agent['direction'] = 'north'
    agent['X'] = randX
    agent['Y'] = randY

    # set_agent_cell(board, 5, 4, 'north')
    # change_symbol(board, 5, 4, 1, "%")
    # agent['direction'] = 'north'
    # agent['X'] = 5
    # agent['Y'] = 4


def move_forward(board):
    global dead, teleported, gameend
    direction = agent['direction']
    X = agent['X']
    Y = agent['Y']

    # print(f'Actual Agent Location ({X},{Y}) facing {direction}')
    change_symbol(board, X, Y, 1, ".")

    if direction == 'north':
        Y1 = Y+1
        if X == origin['X'] and Y1 == origin['Y'] and len(coins) == 0:
            set_visited_cell(board, X, Y)
            reset_map(board)
            gameend = True
        elif f'{X},{Y1}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
            dead = True
        elif f'{X},{Y1}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
            teleported = True
        elif f'{X},{Y1}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X, Y1, direction)
            agent['Y'] = Y1
    elif direction == 'west':
        X1 = X-1
        if X1 == origin['X'] and Y == origin['Y'] and len(coins) == 0:
            set_visited_cell(board, X, Y)
            reset_map(board)
            gameend = True
        elif f'{X1},{Y}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
            dead = True
        elif f'{X1},{Y}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
            teleported = True
        elif f'{X1},{Y}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X1, Y, direction)
            agent['X'] = X1
    elif direction == 'east':
        X1 = X+1
        if X1 == origin['X'] and Y == origin['Y'] and len(coins) == 0:
            set_visited_cell(board, X, Y)
            reset_map(board)
            gameend = True
        elif f'{X1},{Y}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
            dead = True
        elif f'{X1},{Y}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
            teleported = True
        elif f'{X1},{Y}' in walls:
            change_symbol(board, X, Y, 8, "B")
        else:
            set_visited_cell(board, X, Y)
            set_agent_cell(board, X1, Y, direction)
            agent['X'] = X1
    elif direction == 'south':
        Y1 = Y-1
        if X == origin['X'] and Y1 == origin['Y'] and len(coins) == 0:
            set_visited_cell(board, X, Y)
            reset_map(board)
            gameend = True
        elif f'{X},{Y1}' in wampus:
            set_visited_cell(board, X, Y)
            reset_map(board)
            dead = True
        elif f'{X},{Y1}' in portals:
            set_visited_cell(board, X, Y)
            teleport(board)
            teleported = True
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
    has_arrow = bool(list(prolog.query('hasarrow')))
    change_symbol(board, X, Y, 1, '.')
    change_symbol(board, X, Y, 8, ' ')
    if has_arrow:
        if direction == 'north':
            for Y1 in range(Y+1, h-1):
                cell = board[X][Y1]
                if cell[1][1] == 'W':
                    kill_wampus(board, X, Y1)
                    change_symbol(board, X, Y, 9, "@")
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
                    kill_wampus(board, X1, Y)
                    change_symbol(board, X, Y, 9, "@")
        elif direction == 'south':
            for Y1 in range(Y-1, 0, -1):
                cell = board[X][Y1]
                if cell[1][1] == 'W':
                    kill_wampus(board, X, Y1)
                    change_symbol(board, X, Y, 9, "@")


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
    indicator_string = []

    if cell[0][0] == '%':
        indicators.append('on')
        indicator_string.append('Confounded')
    else:
        indicators.append('off')
        indicator_string.append('C')
    if cell[1][0] == '=':
        indicators.append('on')
        indicator_string.append('Stench')
    else:
        indicators.append('off')
        indicator_string.append('S')
    if cell[2][0] == 'T':
        indicators.append('on')
        indicator_string.append('Tingle')
    else:
        indicators.append('off')
        indicator_string.append('T')
    if cell[0][2] == '*':
        indicators.append('on')
        indicator_string.append('Glitter')
    else:
        indicators.append('off')
        indicator_string.append('G')
    if cell[1][2] == 'B':
        indicators.append('on')
        indicator_string.append('Bump')
    else:
        indicators.append('off')
        indicator_string.append('B')
    if cell[2][2] == '@':
        indicators.append('on')
        indicator_string.append('Scream')
    else:
        indicators.append('off')
        indicator_string.append('S')

    print(*indicator_string, sep="-")

    return indicators


def hit_wall(board):
    X = agent['X']
    Y = agent['Y']
    cell = board[X][Y]

    if cell[1][2] == 'B':
        return True

    return False


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


def generate_relative_map(absmap):
    # (0,0) == (7,6)
    global rcurrent_map, rcurrent
    board = [[generate_cell() for Y in range(rh)] for X in range(rw)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            change_rsymbol(board, X, Y, 5, "?")

    # for soln in prolog.query("visited(X,Y)"):
    #     if f'{soln["X"]},{soln["Y"]}' not in visited:
    #         visited.append(f'{soln["X"]},{soln["Y"]}')
    #         visited_map.append(f'{w + soln["X"]},{h + soln["Y"]}')
    #     set_rvisited_cell(board, w + soln["X"], h + soln["Y"])

    # print(visited)

    for soln in prolog.query("safe(X,Y)"):
        if f'{soln["X"]},{soln["Y"]}' not in safe:
            safe.append(f'{soln["X"]},{soln["Y"]}')
            safe_map.append(f'{w + soln["X"]},{h + soln["Y"]}')
        set_rsafe_cell(board, w + soln["X"], h + soln["Y"])

    rcurrent = '0,0'
    rcurrent_map = f'{w},{h}'

    current = list(prolog.query("current(X,Y,D)"))[0]
    # print(current)

    direction = current['D']
    X = current['X']
    Y = current['Y']

    # print(f'Agent is at {X},{Y} facing {direction}')

    set_ragent_cell(absmap, board, w+X, h+Y, direction)

    return board


def update_relative_map(absmap, board):
    global rcurrent_map, rcurrent

    for soln in prolog.query("safe(X,Y)"):
        if f'{soln["X"]},{soln["Y"]}' not in safe:
            safe.append(f'{soln["X"]},{soln["Y"]}')
            safe_map.append(f'{w + soln["X"]},{h + soln["Y"]}')
        set_rsafe_cell(board, w + soln["X"], h + soln["Y"])

    for soln in prolog.query("visited(X,Y)"):
        if f'{soln["X"]},{soln["Y"]}' not in visited:
            visited.append(f'{soln["X"]},{soln["Y"]}')
            visited_map.append(f'{w + soln["X"]},{h + soln["Y"]}')
        set_rvisited_cell(board, w + soln["X"], h + soln["Y"])

    # print(visited)

    current = list(prolog.query("current(X,Y,D)"))[0]
    # print(current)

    direction = current['D']
    X = current['X']
    Y = current['Y']

    # print(f'Agent is at {X},{Y} facing {direction}')

    rcurrent = f'{X},{Y}'
    rcurrent_map = f'{w + X},{h + Y}'

    set_ragent_cell(absmap, board, w+X, h+Y, direction)

    cell = absmap[agent['X']][agent['Y']]

    bump = False

    if cell[1][2] == 'B':
        bump = True

    # bump = bool(list(prolog.query('bump')))

    if bump:
        set_rwall_cell(board, X, Y, direction)

    for soln in prolog.query("wumpus(X,Y)"):
        if f'{soln["X"]},{soln["Y"]}' not in visited and f'{soln["X"]},{soln["Y"]}' not in rwalls:
            set_rwumpus_cell(board, w + soln["X"], h + soln["Y"])

    for soln in prolog.query("confundus(X,Y)"):
        if f'{soln["X"]},{soln["Y"]}' not in visited and f'{soln["X"]},{soln["Y"]}' not in rwalls:
            set_rportal_cell(board, w + soln["X"], h + soln["Y"])


def print_relative_map(board):
    global rcurrent_map, rcurrent
    line = [["" for Y in range(innerH)] for X in range(rh)]

    for X in range(len(board)):
        for Y in range(len(board[X])):
            cell = board[X][Y]
            if f'{X},{Y}' in visited_map:
                for innerX in range(len(cell)):
                    for innerY in range(len(cell[innerX])):
                        if innerX == 2 and X != len(board)-1:
                            line[Y][innerY] += f" {cell[innerX][innerY]}  "
                        else:
                            line[Y][innerY] += f" {cell[innerX][innerY]}"
            # elif f'{X-1},{Y}' in visited_map or f'{X+1},{Y}' in visited_map or f'{X},{Y-1}' in visited_map or f'{X},{Y+1}' in visited_map:
            #     for innerX in range(len(cell)):
            #         for innerY in range(len(cell[innerX])):
            #             if innerX == 2 and X != len(board)-1:
            #                 line[Y][innerY] += f" {cell[innerX][innerY]}  "
            #             else:
            #                 line[Y][innerY] += f" {cell[innerX][innerY]}"
            elif f'{X-1},{Y}' in visited_map or f'{X+1},{Y}' in visited_map or f'{X-1},{Y+1}' in visited_map or f'{X},{Y+1}' in visited_map or f'{X+1},{Y+1}' in visited_map or f'{X-1},{Y-1}' in visited_map or f'{X},{Y-1}' in visited_map or f'{X+1},{Y-1}' in visited_map:
                for innerX in range(len(cell)):
                    for innerY in range(len(cell[innerX])):
                        if innerX == 2 and X != len(board)-1:
                            line[Y][innerY] += f" {cell[innerX][innerY]}  "
                        else:
                            line[Y][innerY] += f" {cell[innerX][innerY]}"
            elif f'{X},{Y}' == rcurrent_map:
                for innerX in range(len(cell)):
                    for innerY in range(len(cell[innerX])):
                        if innerX == 2 and X != len(board)-1:
                            line[Y][innerY] += f" {cell[innerX][innerY]}  "
                        else:
                            line[Y][innerY] += f" {cell[innerX][innerY]}"
            # elif f'{X-1},{Y}' == rcurrent_map or f'{X+1},{Y}' == rcurrent_map or f'{X},{Y-1}' == rcurrent_map or f'{X},{Y+1}' == rcurrent_map:
            #     for innerX in range(len(cell)):
            #         for innerY in range(len(cell[innerX])):
            #             if innerX == 2 and X != len(board)-1:
            #                 line[Y][innerY] += f" {cell[innerX][innerY]}  "
            #             else:
            #                 line[Y][innerY] += f" {cell[innerX][innerY]}"
            elif f'{X-1},{Y}' == rcurrent_map or f'{X+1},{Y}' == rcurrent_map or f'{X-1},{Y+1}' == rcurrent_map or f'{X},{Y+1}' == rcurrent_map or f'{X+1},{Y+1}' == rcurrent_map or f'{X-1},{Y-1}' == rcurrent_map or f'{X},{Y-1}' == rcurrent_map or f'{X+1},{Y-1}' == rcurrent_map:
                for innerX in range(len(cell)):
                    for innerY in range(len(cell[innerX])):
                        if innerX == 2 and X != len(board)-1:
                            line[Y][innerY] += f" {cell[innerX][innerY]}  "
                        else:
                            line[Y][innerY] += f" {cell[innerX][innerY]}"
            else:
                for innerX in range(len(cell)):
                    for innerY in range(len(cell[innerX])):
                        if innerX == 2 and X != len(board)-1:
                            line[Y][innerY] += f"    "
                        else:
                            line[Y][innerY] += f"  "

    for i in range(rh-1, -1, -1):
        for j in range(innerH):
            print(line[i][j])
        print()


def relative_teleport(board):
    global rcurrent_map, rcurrent
    for coor in rwalls_map:
        X = int(coor.split(',')[0])
        Y = int(coor.split(',')[1])
        board[X][Y] = generate_cell()

    for coor in visited_map:
        X = int(coor.split(',')[0])
        Y = int(coor.split(',')[1])
        change_rsymbol(board, X, Y, 1, '.')
        change_rsymbol(board, X, Y, 2, '.')
        change_rsymbol(board, X, Y, 3, '.')

        change_rsymbol(board, X, Y, 8, '.')
        change_rsymbol(board, X, Y, 9, '.')

    for coor in safe_map:
        X = int(coor.split(',')[0])
        Y = int(coor.split(',')[1])
        change_rsymbol(board, X, Y, 1, '.')
        change_rsymbol(board, X, Y, 2, '.')
        change_rsymbol(board, X, Y, 3, '.')
        change_rsymbol(board, X, Y, 8, '.')
        change_rsymbol(board, X, Y, 9, '.')

    X = int(rcurrent_map.split(',')[0])
    Y = int(rcurrent_map.split(',')[1])
    change_rsymbol(board, X, Y, 1, '.')
    change_rsymbol(board, X, Y, 2, '.')
    change_rsymbol(board, X, Y, 3, '.')
    change_rsymbol(board, X, Y, 8, '.')
    change_rsymbol(board, X, Y, 9, '.')

    for X in range(len(board)):
        for Y in range(len(board[X])):
            change_rsymbol(board, X, Y, 5, "?")

    return board


def check_localisation():
    print("Visited:", end=" ")
    for soln in prolog.query("visited(X,Y)"):
        print(f'visited({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Wumpus:", end=" ")
    for soln in prolog.query("wumpus(X,Y)"):
        print(f'wumpus({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Confundus:", end=" ")
    for soln in prolog.query("confundus(X,Y)"):
        print(f'confundus({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Tingle:", end=" ")
    for soln in prolog.query("tingle(X,Y)"):
        print(f'tingle({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Glitter:", end=" ")
    for soln in prolog.query("glitter(X,Y)"):
        print(f'glitter({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Stench:", end=" ")
    for soln in prolog.query("stench(X,Y)"):
        print(f'stench({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Safe:", end=" ")
    for soln in prolog.query("safe(X,Y)"):
        print(f'safe({soln["X"]},{soln["Y"]})', end=" ")
    print()
    print("Wall:", end=" ")
    for soln in prolog.query("wall(X,Y)"):
        print(f'wall({soln["X"]},{soln["Y"]})', end=" ")
    print()
    current = list(prolog.query("current(X,Y,D)"))[0]

    direction = current['D']
    X = current['X']
    Y = current['Y']

    print(f'Agent is at ({X},{Y}) facing {direction}')


def clear_driver_variables():
    global rcurrent, rcurrent_map
    visited.clear()
    visited_map.clear()
    rwalls.clear()
    rwalls_map.clear()
    rcurrent = ''
    rcurrent_map = ''
    safe_map.clear()
    safe.clear()


def main():
    global dead, teleported, gameend, rcurrent, rcurrent_map
    list(prolog.query("reborn"))
    board = generate_abs_map()
    rmap = generate_relative_map(board)
    print_abs_map(board)
    print_relative_map(rmap)
    while True:
        print("1. Test Case 1: Correctness of Agent's localisation and mapping abilities")
        print("2. Test Case 2: Correctness of Agent's sensory inference")
        print("3. Test Case 3: Correctness of Agent's memory management in response to stepping though a Confundus Portal")
        print("4. Test Case 4: Correctness of Agent's exploration capabilities")
        print("5. Test Case 5: Correctness of the Agent's end-game reset in a manner similar to that of Confundus Portal reset.")
        print("6. Testing Mode")
        print("0. Exit")
        option = input()
        if option == '1':
            # Explore the whole map to test localisation and mapping abilities
            # Action Sequence ['turnright', 'turnright', 'moveforward', 'turnright', 'moveforward',
            #    'moveforward', 'turnleft', 'moveforward', 'turnleft', 'turnleft', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward',
            #    'turnright', 'turnright', 'moveforward', 'turnleft', 'moveforward',
            #    'turnright', 'moveforward', 'moveforward',
            #    'turnleft', 'moveforward',
            #    'turnright', 'moveforward', 'turnleft',
            #    'turnleft',  'moveforward', 'moveforward', 'moveforward', 'moveforward',
            #    'turnright', 'moveforward', 'turnleft', 'moveforward',
            #    'turnright', 'moveforward', 'turnleft', 'moveforward',
            #    'turnright', 'moveforward', 'turnright', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward',
            #    'turnleft', 'moveforward', 'turnright', 'moveforward']
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            print_abs_map(board)
            print_relative_map(rmap)
            action_sequence = ['turnright', 'turnright', 'moveforward', 'turnright', 'moveforward',
                               'moveforward', 'turnleft', 'moveforward', 'turnleft', 'turnleft', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward',
                               'turnright', 'turnright', 'moveforward', 'turnleft', 'moveforward',
                               'turnright', 'moveforward', 'moveforward',
                               'turnleft', 'moveforward',
                               'turnright', 'moveforward', 'turnleft',
                               'turnleft',  'moveforward', 'moveforward', 'moveforward', 'moveforward',
                               'turnright', 'moveforward', 'turnleft', 'moveforward',
                               'turnright', 'moveforward', 'turnleft', 'moveforward',
                               'turnright', 'moveforward', 'turnright', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward',
                               'turnleft', 'moveforward', 'turnright', 'moveforward']
            print(action_sequence)
            for action in action_sequence:
                move_agent(board, action)
                print_abs_map(board)
                list(prolog.query(
                    f"move({action},{get_indicator(board)})"))
                update_relative_map(board, rmap)
                print_relative_map(rmap)
                check_localisation()
            clear_driver_variables()
        elif option == '2':
            # Action Sequence ['turnright', 'moveforward', 'turnleft', 'moveforward', 'pickup', 'moveforward', 'moveforward', 'moveforward']
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            print_abs_map(board)
            print_relative_map(rmap)
            action_sequence = ['shoot', 'turnright', 'moveforward', 'turnleft',
                               'moveforward', 'pickup', 'moveforward', 'moveforward', 'moveforward']
            print(action_sequence)
            for action in action_sequence:
                move_agent(board, action)
                print_abs_map(board)
                list(prolog.query(
                    f"move({action},{get_indicator(board)})"))
                update_relative_map(board, rmap)
                print_relative_map(rmap)
                check_localisation()
            clear_driver_variables()
        elif option == '3':
            # Action Sequence ['moveforward', 'turnright', 'moveforward', 'turnleft', 'moveforward', 'moveforward', 'turnright', 'moveforward', 'turnright', 'moveforward']
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            print_abs_map(board)
            print_relative_map(rmap)
            action_sequence = ['moveforward', 'turnright', 'moveforward', 'turnleft',
                               'moveforward', 'moveforward', 'turnright', 'moveforward', 'turnright', 'moveforward']
            print(action_sequence)
            for action in action_sequence:
                move_agent(board, action)
                print_abs_map(board)
                if teleported:
                    list(prolog.query(
                        "reposition([on,off,off,off,off,off])"))
                    rmap = generate_relative_map(board)
                    clear_driver_variables()
                    teleported = False
                else:
                    list(prolog.query(
                        f"move({action},{get_indicator(board)})"))
                update_relative_map(board, rmap)
                print_relative_map(rmap)
                check_localisation()
            clear_driver_variables()
        elif option == '4':
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            i = 0
            while True:
                actions = []
                for soln in prolog.query("explore(L)"):
                    # print(soln)
                    try:
                        actions = [action for action in soln['L']]
                    except:
                        break

                print(f'actions: {actions}')
                current = list(prolog.query("current(X,Y,D)"))[0]

                if (len(actions) == 0 and current['X'] == 0 and current['Y'] == 0) or i == 2:
                    print('Exploration Stops')
                    X = agent['X']
                    Y = agent['Y']
                    set_visited_cell(board, X, Y)
                    reset_map(board)
                    list(prolog.query("reborn"))
                    clear_driver_variables()
                    rmap = generate_relative_map(board)
                    break
                elif len(actions) == 0:
                    i += 1

                for action in actions:
                    move_agent(board, action)
                    print_abs_map(board)
                    if dead:
                        list(prolog.query("reborn"))
                        clear_driver_variables()
                        rmap = generate_relative_map(board)
                        dead = False
                    if teleported:
                        list(prolog.query(
                            "reposition([on,off,off,off,off,off])"))
                        rmap = generate_relative_map(board)
                        clear_driver_variables()
                        teleported = False
                    else:
                        list(prolog.query(
                            f"move({action},{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                    if hit_wall(board):
                        break

        elif option == '5':
            # Action Sequence ['moveforward', 'turnright', 'moveforward','pickup', 'turnright', 'moveforward', 'turnright', 'moveforward']
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            print_abs_map(board)
            print_relative_map(rmap)
            action_sequence = ['moveforward',
                               'moveforward', 'moveforward']
            print(action_sequence)
            for action in action_sequence:
                move_agent(board, action)
                print_abs_map(board)
                if dead:
                    list(prolog.query("reborn"))
                    clear_driver_variables()
                    rmap = generate_relative_map(board)
                    dead = False
                else:
                    list(prolog.query(
                        f"move({action},{get_indicator(board)})"))
                update_relative_map(board, rmap)
                print_relative_map(rmap)
                check_localisation()
            clear_driver_variables()
        elif option == '6':
            list(prolog.query("reborn"))
            board = generate_abs_map()
            rmap = generate_relative_map(board)
            print_abs_map(board)
            print_relative_map(rmap)
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
                    if dead:
                        list(prolog.query("reborn"))
                        clear_driver_variables()
                        rmap = generate_relative_map(board)
                        dead = False
                    elif teleported:
                        list(prolog.query(
                            "reposition([on,off,off,off,off,off])"))
                        rmap = generate_relative_map(board)
                        clear_driver_variables()
                        teleported = False
                    else:
                        list(prolog.query(
                            f"move(moveforward,{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                elif option == '2':
                    move_agent(board, 'turnleft')
                    print_abs_map(board)
                    list(prolog.query(
                        f"move(turnleft,{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                elif option == '3':
                    move_agent(board, 'turnright')
                    print_abs_map(board)
                    list(prolog.query(
                        f"move(turnright,{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                elif option == '4':
                    move_agent(board, 'pickup')
                    print_abs_map(board)
                    list(prolog.query(
                        f"move(pickup,{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                elif option == '5':
                    move_agent(board, 'shoot')
                    print_abs_map(board)
                    list(prolog.query(
                        f"move(shoot,{get_indicator(board)})"))
                    update_relative_map(board, rmap)
                    print_relative_map(rmap)
                    check_localisation()
                elif option == '0':
                    clear_driver_variables()
                    break
        elif option == '0':
            break


main()
