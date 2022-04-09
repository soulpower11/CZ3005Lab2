import random
from types import CellType
from pyswip import Prolog

prolog = Prolog()
prolog.consult('agent.pl')

### Generate a set of initial game map cells
def reset():
    ### Outer wall cells. Agent cannot exist here. Will cause bump
    r0c0 = [['#','#','#'],
            ['#','#','#'],
            ['#','#','#']]
    # All outer cells are wall cells
    r0c1 = r0c2 = r0c3 = r0c4 = r0c5 = r0c6 = r5c0 = r5c1 = r5c2 = r5c3 = r5c4 = r5c5 = r5c6 = r1c0 = r2c0 = r3c0 = r4c0 = r1c6 = r2c6 = r3c6 = r4c6 = r0c0

    ### Inner wall cells. Only cells not containing NPC can be initialized with agent during reset
    # Initialize all other cells to normal cells first
    r1c1 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r1c2 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r1c3 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r1c4 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r1c5 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r2c1 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r2c2 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r2c3 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r2c4 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r2c5 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
        
    r3c1 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r3c2 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r3c3 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r3c4 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r3c5 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r4c1 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]
    
    r4c2 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r4c3 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r4c4 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    r4c5 = [['.', '.', '.'],
            [' ', '?', ' '],
            ['.', '.', '.']]

    inner_wall = [r1c2, r1c3, r1c4, r1c5, r2c1, r2c2, r2c3, r2c4, r2c5, r3c1, r3c2, r3c3, r3c4, r3c5, r4c1, r4c2, r4c3, r4c4, r4c5, r1c1]

    wumpus_world = [[r0c0,r0c1,r0c2,r0c3,r0c4,r0c5,r0c6],
                    [r1c0,r1c1,r1c2,r1c3,r1c4,r1c5,r1c6],
                    [r2c0,r2c1,r2c2,r2c3,r2c4,r2c5,r2c6],
                    [r3c0,r3c1,r3c2,r3c3,r3c4,r3c5,r3c6],
                    [r4c0,r4c1,r4c2,r4c3,r4c4,r4c5,r4c6],
                    [r5c0,r5c1,r5c2,r5c3,r5c4,r5c5,r5c6]]

    # Randomize up to 3 Confundus portal
    i = 3
    while i > 0:
        tempx = random.randrange(1,6)
        tempy = random.randrange(1,5)
        (wumpus_world[tempy][tempx])[0][0] = '%'
        (wumpus_world[tempy][tempx])[1][0] = (wumpus_world[tempy][tempx])[1][2] = '-'
        i -= 1

    # Randomize 1 wumpus
    tempx = random.randrange(1,6)
    tempy = random.randrange(1,5)
    (wumpus_world[tempy][tempx])[0][0] = '.'
    (wumpus_world[tempy][tempx])[1][0] = (wumpus_world[tempy][tempx])[1][2] = '-'

    # Randomize 1 gold
    tempx = random.randrange(1,6)
    tempy = random.randrange(1,5)
    (wumpus_world[tempy][tempx])[0][0] = '.'
    (wumpus_world[tempy][tempx])[1][0] = (wumpus_world[tempy][tempx])[1][2] = '-'
    (wumpus_world[tempy][tempx])[2][0] = '*'

    # Fill in stench cells
    for i in range(1,5):
        for j in range(1,6):
            if (wumpus_world[i][j])[1][0] == '-' and (wumpus_world[i][j])[2][0] != '*' and (wumpus_world[i][j])[0][0] != '%':
                if wumpus_world[i+1][j] in inner_wall:
                    (wumpus_world[i+1][j])[0][1] = '='
                if wumpus_world[i-1][j] in inner_wall:
                    (wumpus_world[i-1][j])[0][1] = '='
                if wumpus_world[i][j+1] in inner_wall:
                    (wumpus_world[i][j+1])[0][1] = '='
                if wumpus_world[i][j-1] in inner_wall:
                    (wumpus_world[i][j-1])[0][1] = '='

    # Fill in tingle cells
    for i in range(1,5):
        for j in range(1,6):
            if (wumpus_world[i][j])[1][0] == '-' and (wumpus_world[i][j])[0][0] == '%':
                if wumpus_world[i+1][j] in inner_wall:
                    (wumpus_world[i+1][j])[0][2] = 'T'
                if wumpus_world[i-1][j] in inner_wall:
                    (wumpus_world[i-1][j])[0][2] = 'T'
                if wumpus_world[i][j+1] in inner_wall:
                    (wumpus_world[i][j+1])[0][2] = 'T'
                if wumpus_world[i][j-1] in inner_wall:
                    (wumpus_world[i][j-1])[0][2] = 'T'
    
    # Fill in initial agent location
    agentX, agentY = randomize_agent(wumpus_world)
    wumpus_world[agentY][agentX][1][0] = '-'
    wumpus_world[agentY][agentX][1][2] = '-'
    wumpus_world[agentY][agentX][1][1] = '^'     

    prolog.query("reborn.")
    # return the generated world, and the agents absolute position within world to begin analysis
    return wumpus_world, agentX, agentY
        
def randomize_agent(world):
    # Initialise agent in a location without the gold and in a safe square (ie. without any NPCs)
    flag = False
    while flag == False:
        tempx = random.randrange(1,6)
        tempy = random.randrange(1,5) 
        if world[tempy][tempx][1][0] == ' ':
             flag = True           
    return tempx,tempy

def update_map(curworld, action, newX, newY):
    # Update the current wumpus world map with the new X and Y coordinates if changed, and the action taken
    pass
    # return updated_wumpus_world

### Pass in the current square from the wumpus world map to analyse the symbols within the square.
# Update the knowledge base with new facts using the add_ rules if there are any relevant facts to add
# Return the action decision and new current square
def analyse_sq(world, currentX, currentY):
    if world[currentY][currentX][0][1] == "=":
        prolog.query("add_stench.")
    if world[currentY][currentX][0][2] == "T":
        prolog.query("add_tingle.")

    world[currentY][currentX][1][1]

    if world[currentY][currentX][1][0] == '-':
        if world[currentY][currentX][2][0] == "*":
            prolog.query("add_glitter.")
            # pick up the gold
        elif world[currentY][currentX][0][0] == "%":
            prolog.query("add_confundus.")
            # reposition    
        else:
            # encounter wumpus, break loop 
            return None, None, None 
    # Symbol 8: Bump indicator. "B" is printed if the indicator is on and a dot otherwise. Caution: Bump indicator is transitory. That is, it will appear only if the agent tried to go forward and met a Wall.
    world[currentY][currentX][2][1]
    # Symbol 9: Scream indicator. "@" is printed if the indicator is on and a dot otherwise. Caution: Scream indicator is transitory. That is, it will appear only if the agent shot its Arrow and the Wumpus was killed/removed.
    world[currentY][currentX][2][2]

    # return action, newX, newY

### Print out the current map
def printout(world):
    for i in range(0,6):
        print('\n')
        temp_array = []
        for j in range(0,7):
            temp_array.append(world[i][j])
        a = []
        for k in range(0,7):
            a.append(temp_array[k][0])
        print(a)
        a = []
        for k in range(0,7):
            a.append(temp_array[k][1])
        print(a)
        a = []
        for k in range(0,7):
            a.append(temp_array[k][2])
        print(a)



#### Main Driver Code ####
print("----------------------- Welcome to Wumpus World. This is the initial map -----------------------")

completed = False
while True:
    world, curX, curY = reset()
    # printout(world)
    while True:
        chosenaction, curX, curY = analyse_sq(world, curX, curY)
        # If wumpus is encountered then reset
        if chosenaction == None:
            break
        updated_world = update_map(world, chosenaction, curX, curY)
        # printout(updated_world)
        # if gold has been found and safe path to relative origin 0,0 is reached:
        #   break loop and set completed = True
    if completed == True:
        break

print("------------------------------------ Wumpus World game ended ------------------------------------")