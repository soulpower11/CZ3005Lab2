import sys
import time
import numpy as np
import random
from pyswip import Prolog

# return string for query, no need to concatenate everytime ;type-> string


def getquerystr(type, x, y):
    return type+'('+str(x)+','+str(y)+')'


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.1)


class Cell:
    def __init__(self, y=0, x=0):
        self.hidden = False
        self.agent = False
        self.agent_direction = "UP"
        self.glitter = False
        self.wumpus = False
        self.deadWumpus = False
        self.stench = False
        self.tingle = False
        self.confunded = False
        self.confundus = False
        self.breeze = False
        self.gold = False
        self.start = False
        self.bump = False
        self.wall = False
        self.empty = True
        self.scream = False
        self.visited = False
        self.safe = False
        self.x = x
        self.y = y
        self.printout = ''

    # returns a string for printing

    def __repr__(self):
        S = ""
        # edge case: wall & hidden
        if self.hidden:
            return "         "
        if self.wall:
            return "#########"
        # 1: Confounded
        if self.confunded == True:
            S += "%"
        else:
            S += "."
        # 2: Stench
        if self.stench == True:
            S += "="
        else:
            S += "."
        # 3: Tingle
        if self.tingle == True:
            S += "T"
        else:
            S += "."
        # 4: Agent or NPC
        if self.agent or self.wumpus:
            S += "-"
        else:
            S += " "
        # 5:
        if self.wumpus == True and self.confundus == True:
            S += "U"
        elif self.wumpus == True:
            S += "W"
        elif self.confundus == True:
            S += "O"
        elif self.agent == True:
            if self.agent_direction == "UP":
                S += "∧"
            if self.agent_direction == "DOWN":
                S += "∨"
            if self.agent_direction == "LEFT":
                S += "<"
            if self.agent_direction == "RIGHT":
                S += ">"
        elif self.safe:
            if self.visited:
                S += 'S'
            else:
                S += 's'
        else:
            S += '?'
        # 6: Agent or NPC
        if self.agent or self.wumpus:
            S += "-"
        else:
            S += " "
        # 7: Glitter
        if self.glitter:
            S += "*"
        else:
            S += '.'

     # S+=str(self.y)
     # S+=str(self.x)
        # 8: Bump
        if self.bump:
            S += "B"
        else:
            S += '.'
        # 9: Scream
        if self.scream:
            S += "@"
        else:
            S += '.'
       # S=("{0:4}".format(S))
        self.printout = S
        return S


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.startX = 2
        self.startY = 2
        self.agentX = 2
        self.agentY = 2
        self.agentD = "DOWN"
        self.resetWorld()
        self.solvable = False

    def makeWorld(self):

        for h in range(self.height):
            self.world.append([])
            for w in range(self.width):
                self.world[h].append([])
        for h in range(len(self.world)):
            for w in range(len(self.world[h])):
                # create a cell with coordinates
                cell = Cell(h, w)
                # absolute map will show all cell
                cell.visited = True
                # set wall around outer map
                if(h == 0 or h == self.height-1 or w == 0 or w == self.width-1):
                    cell.wall = True
                    cell.empty = False
                self.world[h][w] = cell
                # set agent start position
                if(h == self.startY and w == self.startX):
                    self.world[h][w].start = True
                    self.world[h][w].agent = True
                    self.world[h][w].agent_direction = "UP"
                    self.agentX = w
                    self.agentY = h

    # reset world
    def resetWorld(self):
        self.world = []
        self.startX = 1
        self.startY = 4
        self.agentX = 1
        self.agentY = 4
        self.agentD = "UP"
        self.makeWorld()
        self.putThings()

    def resetWorldRandom(self):
        self.world = []
        self.startX = 1
        self.startY = 4
        self.agentX = 1
        self.agentY = 4
        self.agentD = "UP"
        self.makeWorld()
        self.putThingsRandom()

    # set env
    def putThings(self):
        xm = [0, 1, 0, -1]
        ym = [-1, 0, 1, 0]
        wumpusx = 4
        wumpusy = 4
        goldx = 2
        goldy = 2

        ty = 1
        tx = 4
        self.world[ty][tx].confundus = True
        self.world[ty][tx].empty = False
        for i in range(4):
            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                self.world[ty+ym[i]][tx+xm[i]].tingle = True
                self.world[ty+ym[i]][tx+xm[i]].empty = False
        ty = 2
        tx = 3
        self.world[ty][tx].confundus = True
        self.world[ty][tx].empty = False
        for i in range(4):
            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                self.world[ty+ym[i]][tx+xm[i]].tingle = True
                self.world[ty+ym[i]][tx+xm[i]].empty = False
        ty = 4
        tx = 3
        self.world[ty][tx].confundus = True
        self.world[ty][tx].empty = False
        for i in range(4):
            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                self.world[ty+ym[i]][tx+xm[i]].tingle = True
                self.world[ty+ym[i]][tx+xm[i]].empty = False

        ty = wumpusy
        tx = wumpusx
        self.world[ty][tx].wumpus = True
        self.world[ty][tx].empty = False

        for i in range(4):
            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                self.world[ty+ym[i]][tx+xm[i]].stench = True
                self.world[ty+ym[i]][tx+xm[i]].empty = False

        ty = goldy
        tx = goldx
        self.world[ty][tx].gold = True
        self.world[ty][tx].glitter = True
        self.world[ty][tx].empty = False

    def putThingsRandom(self):
        x = 0
        xm = [0, 1, 0, -1]
        ym = [-1, 0, 1, 0]
        next = "P"
        checkPos = False

        while checkPos == False:
            tx = random.randint(0, self.width-1)
            ty = random.randint(0, self.height-1)
            if tx != self.startX and ty != self.startY:

                if next == "P":
                    if self.world[ty][tx].wall == False and self.world[ty][tx].confundus == False:
                        self.world[ty][tx].confundus = True
                        self.world[ty][tx].empty = False

                        for i in range(4):
                            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                                self.world[ty+ym[i]][tx+xm[i]].tingle = True
                                self.world[ty+ym[i]][tx+xm[i]].empty = False
                        x += 1
                        if x == 3:
                            next = "W"

                elif next == "W":
                    if self.world[ty][tx].wall == False and self.world[ty][tx].confundus == False:

                        self.world[ty][tx].wumpus = True
                        self.world[ty][tx].empty = False

                        for i in range(4):
                            if self.world[ty+ym[i]][tx+xm[i]].wall == False and self.world[ty+ym[i]][tx+xm[i]].confundus == False:
                                self.world[ty+ym[i]][tx+xm[i]].stench = True
                                self.world[ty+ym[i]][tx+xm[i]].empty = False
                        next = "G"

                elif next == "G":
                    if self.world[ty][tx].wall == False and self.world[ty][tx].confundus == False and self.world[ty][tx].wumpus == False:
                        self.world[ty][tx].gold = True
                        self.world[ty][tx].glitter = True
                        self.world[ty][tx].empty = False
                        checkPos = True


class Agent:

    def __init__(self, world):
        self.mapHeight = 9
        self.mapWidth = 11
        self.resetAgent()

    def resetAgent(self):
        self.alive = True
        self.gold = False
        self.foundgold = False
        self.confunded = False
        self.direction = "UP"
        self.arrow = 1
        self.route = []
        self.xPos = 5
        self.yPos = 4
        self.startx = 5
        self.starty = 4
        self.makeMap()
        self.sense = ''
        self.percept = 'C-S-T-G-B-S'

    def randomAllocateAgent(self, world):
        self.alive = True
        self.direction = "DOWN"
        self.arrow = 1
        self.route = []
        self.startx = 5
        self.starty = 4
        self.xPos = 5
        self.yPos = 4
        self.makeMap()
        self.confunded = False
        self.sense = ''
        self.percept = 'Confounded-S-T-G-B-S'
        checkPos = False
        while checkPos == False:
            world.world[world.agentY][world.agentX].agent = False
            tx = random.randint(1, world.width-1)
            ty = random.randint(1, world.height-1)
            if world.world[ty][tx].wall == False and world.world[ty][tx].confundus == False and world.world[ty][tx].wumpus == False:

                world.agentX = tx
                world.agentY = ty
                world.agentD = "UP"
                world.world[world.agentY][world.agentX].agent = True
                world.world[world.agentY][world.agentX].agent_direction = "UP"
                world.world[world.agentY][world.agentX].confunded = True
                checkPos = True
        print("Agent is at: ", world.agentX, world.agentY)
        print(world.world[world.agentY][world.agentX])
        cell = world.world[world.agentY][world.agentX]
        self.percepts(cell, 'confounded')

    # create relative map

    def makeMap(self):
        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])
        relativeD = (relative_pos[0]["D"])
        absX = self.startx + relativeX
        absY = self.starty + relativeY
        self.map = []
        for h in range(self.mapHeight):
            self.map.append([])
            for w in range(self.mapWidth):
                cell = Cell(h, w)
                cell.hidden = True

                if h == absY and w == absX:
                    cell.agent = True
                    cell.empty = False
                    cell.visited = True
                    cell.safe = True
                    cell.hidden = False

                    if relativeD == "rnorth":
                        cell.agent_direction = "UP"
                    elif relativeD == "rsouth":
                        cell.agent_direction = "DOWN"
                    elif relativeD == "reast":
                        cell.agent_direction = "RIGHT"
                    elif relativeD == "rwest":
                        cell.agent_direction = "LEFT"
                self.map[h].append(cell)

    # percepts: get the input for prolog

    def percepts(self, cell, event):

        print('percepts function')
        print(cell)
        sense = '['
        percepts = ''
        if cell.wumpus:
            '''do reset'''
            self.alive = False
            pass
        elif cell.confundus:
            '''reset postion'''
            self.confunded = True
            pass
        else:
            if event == 'confounded':
                percepts += 'Confounded-'
                sense += 'on,'
            else:
                percepts += 'C-'
                sense += 'off,'
            if cell.stench == True:
                percepts += 'Stench-'
                sense += 'on,'
            else:
                percepts += 'S-'
                sense += 'off,'

            if cell.tingle == True:
                percepts += 'Tingle-'
                sense += 'on,'
            else:
                percepts += 'T-'
                sense += 'off,'

            if cell.glitter == True:
                self.foundgold = True
                percepts += 'Glitter-'
                sense += 'on,'
            else:
                self.foundgold = False
                percepts += 'G-'
                sense += 'off,'
            if event == 'bump':
                percepts += 'Bump-'
                sense += 'on,'

            else:
                percepts += 'B-'
                sense += 'off,'
            if event == 'scream':
                percepts += 'Scream'
                sense += 'on]'
            else:
                percepts += 'S'
                sense += 'off]'

            self.sense = sense
            self.percept = percepts

    # implements shoot action

    def shoot(self, world):
        xm = [0, 1, 0, -1]
        ym = [-1, 0, 1, 0]
        hit = False
        direction = 1
        if self.arrow > 0:
            self.arrow -= 1

        if world.agentD == "UP":
            direction = 0
        elif world.agentD == "RIGHT":
            direction = 1
        elif world.agentD == "DOWN":
            direction = 2
        elif world.agentD == "LEFT":
            direction = 3

        x = 0
        y = 0
        while hit == False:
            print('shoot function')
            print_slow(str(world.agentY+ym[direction]+y))
            print_slow(str(world.agentX+xm[direction]+x))
            if world.world[world.agentY+ym[direction]+y][world.agentX+xm[direction]+x].wumpus:
                hit = True
                print_slow('You killed the wumpus!')
                # remove wumpus & stench, add scream
                world.world[world.agentY][world.agentX].scream = True
                world.world[world.agentY+ym[direction] +
                            y][world.agentX+xm[direction]+x].wumpus = False
                wumpusY = world.agentY+ym[direction]+y
                wumpusX = world.agentX+xm[direction]+x
                for i in range(4):
                    world.world[wumpusY+ym[i]][wumpusX+xm[i]].stench = False
                self.percepts(world.world[world.agentY]
                              [world.agentX], 'scream')
            elif world.world[world.agentY+ym[direction]+y][world.agentX+xm[direction]+x].wall:
                hit = True
                print_slow('You missed!')
                self.percepts(world.world[world.agentY][world.agentX], 'nil')
            else:
                y += ym[direction]
                x += xm[direction]

    def updateMap(self, world):
        print('in update map')
        self.makeMap()
        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])
        relativeD = (relative_pos[0]["D"])
        print(relativeX, relativeY, relativeD)
        absX = self.startx + relativeX
        absY = self.starty + relativeY
        print(absX, absY)
        print('newcell: '+str(self.map[absY][absX]))
        print('newcell: '+str(absY)+str(absX))

        print(bool(list(prolog.query(getquerystr('stench', relativeX, relativeY)))))

        self.map[absY][absX].stench = bool(
            list(prolog.query(getquerystr("stench", relativeX, relativeY))))
        self.map[absY][absX].tingle = bool(
            list(prolog.query(getquerystr("tingle", relativeX, relativeY))))
        self.map[absY][absX].glitter = bool(
            list(prolog.query(getquerystr("glitter", relativeX, relativeY))))
        self.map[absY][absX].scream = world.world[world.agentY][world.agentX].scream
        self.map[absY][absX].bump = world.world[world.agentY][world.agentX].bump
        self.map[absY][absX].confunded = world.world[world.agentY][world.agentX].confunded
       # self.map[absY][absX].bump = bool(
        #  list(prolog.query(getquerystr("bump", relativeX, relativeY))))
        # self.map[absY][absX].safe = bool(
        #    list(prolog.query(getquerystr("safe", relativeX, relativeY))))
      #  self.map[absY][absX].stench = world.world[absY][absX].stench
       # wumpus = list(prolog.query(
        #   getquerystr("wumpus", relativeX, relativeY)))

        # iterate throught the list of maps to mark cells
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                relativeX = j - self.startx
                relativeY = i - self.starty

                self.map[i][j].tingle = bool(
                    list(prolog.query(getquerystr("tingle", relativeX, relativeY))))
                self.map[i][j].glitter = bool(
                    list(prolog.query(getquerystr("glitter", relativeX, relativeY))))
                self.map[i][j].stench = bool(
                    list(prolog.query(getquerystr("stench", relativeX, relativeY))))
                self.map[i][j].wumpus = bool(
                    list(prolog.query(getquerystr("wumpus", relativeX, relativeY))))
                self.map[i][j].safe = bool(
                    list(prolog.query(getquerystr("safe", relativeX, relativeY))))
                self.map[i][j].visited = bool(
                    list(prolog.query(getquerystr("visited", relativeX, relativeY))))
                self.map[i][j].confundus = bool(
                    list(prolog.query(getquerystr("confundus", relativeX, relativeY))))
                self.map[i][j].wall = bool(
                    list(prolog.query(getquerystr("wall", relativeX, relativeY))))
                self.map[i][j].glitter = bool(
                    list(prolog.query(getquerystr("glitter", relativeX, relativeY))))

                if(self.map[i][j].safe or self.map[i][j].wumpus or self.map[i][j].glitter or self.map[i][j].tingle or self.map[i][j].stench or self.map[i][j].visited or self.map[i][j].confundus or self.map[i][j].wall):
                    self.map[i][j].hidden = False

                if(i == absY and j == absX):
                    self.map[i][j].agent = True
                    self.map[i][j].empty = False
                    if relativeD == "rnorth":
                        self.map[i][j].agent_direction = "UP"
                    elif relativeD == "rsouth":
                        self.map[i][j].agent_direction = "DOWN"
                    elif relativeD == "reast":
                        self.map[i][j].agent_direction = "RIGHT"
                    elif relativeD == "rwest":
                        self.map[i][j].agent_direction = "LEFT"
              #  self.map[i][j].confoundus = bool(
              #  list(prolog.query(getquerystr("confundus", relativeX, relativeY))))

        # update position !!!!!!
        self.xPos = absX
        self.yPos = absY

    def move(self, world, action):

        x = world.agentX
        y = world.agentY
        # remove scream&bump if it is there
        world.world[y][x].scream = False
        world.world[y][x].bump = False
        world.world[y][x].confunded = False
        if action == "moveforward":
            print('move')
            direction = self.direction
            relative_pos = list(prolog.query("current(X,Y,D)"))
            relativeX = (relative_pos[0]["X"])
            relativeY = (relative_pos[0]["Y"])
            relativeD = (relative_pos[0]["D"])
            # get absolute cell position by doing transposition:starting(x,y) + relative(x,y)
            absX = self.startx - relativeX
            absY = self.starty + relativeY

            # get the resultant cell location
            newx = absX
            newy = absY
            direction = world.agentD
            newx = world.agentX
            newy = world.agentY
            if direction == "UP":
                newy = newy-1
            if direction == "DOWN":
                newy = newy+1
            if direction == "LEFT":
                newx = newx-1
            if direction == "RIGHT":
                newx = newx+1
            cell = world.world[newy][newx]
            print('abscell')
            print(cell)
            print(relativeX, relativeY, relativeD)
            print(self.map[self.yPos][self.xPos])

            if cell.wall == False:
                # clear previous location
                world.world[world.agentY][world.agentX].agent = False
                world.world[world.agentY][world.agentX].empty = True
                world.world[world.agentY][world.agentX].agent_direction = None

                # set new location
                world.world[newy][newx].agent = True
                world.world[newy][newx].empty = False
                world.world[newy][newx].agent_direction = direction
                # update agent position
                world.agentY = newy
                world.agentX = newx
                print(newx, newy)
                self.percepts(cell, 'nil')
                self.map[self.yPos][self.xPos].visited = True
            else:
                '''do nth, no update'''
                print_slow('You bump into a wall!')

                cell = world.world[world.agentY][world.agentX]
                cell.bump = True
                self.percepts(cell, 'bump')

        # change agent direction for turning

        if action == "turnleft":
            direction = world.agentD
            if direction == "UP":
                world.agentD = "LEFT"
            if direction == "DOWN":
                world.agentD = "RIGHT"
            if direction == "LEFT":
                world.agentD = "DOWN"
            if direction == "RIGHT":
                world.agentD = "UP"
            # absolute
            world.world[y][x].agent_direction = world.agentD
            # relative
          #  self.map[self.yPos][self.xPos].agent_direction = world.agentD
          #  self.map[self.yPos][self.xPos].scream = False
            cell = world.world[y][x]
            self.percepts(cell, 'nil')

        if action == "turnright":
            direction = world.agentD
            if direction == "UP":
                world.agentD = "RIGHT"
            if direction == "DOWN":
                world.agentD = "LEFT"
            if direction == "LEFT":
                world.agentD = "UP"
            if direction == "RIGHT":
                world.agentD = "DOWN"
            # absolute
            world.world[y][x].agent_direction = world.agentD
            # relative
           # self.map[self.yPos][self.xPos].agent_direction = world.agentD
          #  self.map[self.yPos][self.xPos].scream = False
            cell = world.world[y][x]
            self.percepts(cell, 'nil')

        if action == 'pickup':
            cell = world.world[y][x]
            if cell.glitter == True:
                print_slow('You picked up a gold!')
                cell.glitter = False
                self.percepts(cell, 'nil')

            else:
                print_slow('nothing there...')
                self.percepts(cell, 'nil')

        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])

    def pickup(self, world):
        x = world.agentX
        y = world.agentY
        cell = world.world[y][x]
        if cell.glitter == True:
            print_slow('You picked up a gold!')
            cell.glitter = False
            self.percepts(cell, 'nil')

        else:
            print_slow('nothing there...')
            self.percepts(cell, 'nil')


###########################################################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
prolog = Prolog()
print("\n\n")
print("wumpus world")
print("absolute map:\n")

prolog.consult('agent.pl')


# need to add list for query to work
list(prolog.query("reborn"))


# create world
world = Map(6, 7)
world.putThings()
agent = Agent(world)
agent.updateMap(world)
reset = True
play = True
quitgame = False


def printabs():
    print("absolute map:\n")
    for i in range(len(world.world)):
        for j in range(len(world.world[i])):
            print(" ".join(repr(world.world[i][j])[0:3]), end="  ")
        print("\n", end="")
        for j in range(len(world.world[i])):
            print(" ".join(repr(world.world[i][j])[3:6]), end="  ")
        print("\n", end="")
        for j in range(len(world.world[i])):
            print(" ".join(repr(world.world[i][j])[6:9]), end="  ")
        print("\n")


def printrel():
    print("relative map:\n")
    for i in range(len(agent.map)-1, -1, -1):
        for j in range(len(agent.map[i])):
            print(" ".join(repr(agent.map[i][j])[0:3]), end="  ")
        print("\n", end="")
        for j in range(len(agent.map[i])):
            print(" ".join(repr(agent.map[i][j])[3:6]), end="  ")
        print("\n", end="")
        for j in range(len(agent.map[i])):
            print(" ".join(repr(agent.map[i][j])[6:9]), end="  ")
        print("\n")


def printinfo():
    print("agent absolute location: X:" +
          str(world.agentX)+" Y: "+str(world.agentY))
    print("agent absolute direction:"+str(world.agentD))
    print('agent relative location: ' +
          str(list(prolog.query("current(X,Y,_)"))))
    print("agent relative direction:" +
          str(list(prolog.query("current(_,_,D)"))))

    print('agent sense: '+agent.percept)

    print('visited: ' + str(list(prolog.query("visited(X,Y)"))))
    print('stench: ' + str(list(prolog.query("stench(X,Y)"))))
    print('tingle: ' + str(list(prolog.query("tingle(X,Y)"))))


printabs()
printrel()


while not quitgame:
    print("1.  Correctness of Agent's localisation and mapping abilities")
    print("2.  Correctness of Agent's sensory inference")
    print("3.  Correctness of Agent's memory management in response to stepping though a Confundus Portal")
    print("4.  Correctness of Agent's exploration capabilities")
    print("5.  Correctness of the Agent's end-game reset in a manner similar to that of Confundus Portal reset.")
    print("6.  Free Roam Mode")
    print("7.  Bonus stage: Free Roam with random map")
    print("8.  Hidden stage: Explore with random map")
    print("0.  Quit")

    option = input()

    if option == '1':
        list(prolog.query("reborn"))

        action_sequence = ['turnleft', 'moveforward', 'turnright', 'moveforward', 'moveforward', 'moveforward', 'moveforward', 'turnright', 'moveforward', 'moveforward', 'turnright', 'turnright', 'moveforward', 'turnleft', 'moveforward', 'moveforward', 'moveforward',
                           'moveforward', 'moveforward', 'turnleft', 'turnleft', 'moveforward', 'turnright', 'moveforward', 'moveforward', 'moveforward', 'moveforward', 'turnright', 'moveforward', 'turnright', 'turnright', 'moveforward', 'moveforward', 'moveforward', 'moveforward']

        print(action_sequence)
        for movement in action_sequence:
            printabs()
            printrel()
            printinfo()
            agent.move(world, movement)
            if agent.alive == False:
                print_slow('you died!')
                print_slow('respawning...:' +
                           str(bool(list(prolog.query("reborn")))))
                agent.resetAgent()
                world.resetWorld()

            elif agent.confunded:
                print_slow('you stepped into a portal!')
                print_slow('relocate to another cell...')
                agent.randomAllocateAgent(world)

                print('test'+agent.sense)
                strs = "reposition("+agent.sense+")"
                print(strs)
                bool(list(prolog.query(strs)))

            else:
                strs = "move("+movement+","+agent.sense+")"
                print('str: '+strs)
                print((list(prolog.query(strs))))
            agent.updateMap(world)
            print_slow('moving')
            print()

    if option == '2':
        list(prolog.query("reborn"))

        action_sequence = ['turnright', 'moveforward', 'turnleft', 'moveforward', 'moveforward', 'turnright', 'turnright', 'moveforward', 'turnleft',
                           'moveforward', 'moveforward', 'moveforward', 'moveforward', 'moveforward', 'turnleft', 'moveforward', 'turnleft', 'moveforward']

        print(action_sequence)
        for movement in action_sequence:
            printabs()
            printrel()
            printinfo()
            agent.move(world, movement)
            if agent.alive == False:
                print_slow('you died!')
                print_slow('respawning...:' +
                           str(bool(list(prolog.query("reborn")))))
                agent.resetAgent()
                world.resetWorld()

            elif agent.confunded:
                print_slow('you stepped into a portal!')
                print_slow('relocate to another cell...')
                agent.randomAllocateAgent(world)

                print('test'+agent.sense)
                strs = "reposition("+agent.sense+")"
                print(strs)
                bool(list(prolog.query(strs)))

            else:
                strs = "move("+movement+","+agent.sense+")"
                print('str: '+strs)
                print((list(prolog.query(strs))))
            agent.updateMap(world)
            print_slow('moving')
            print()
            printabs()
            printrel()
            printinfo()

    if option == '3':
        list(prolog.query("reborn"))

        action_sequence = ['turnleft', 'moveforward', 'turnright', 'moveforward', 'moveforward',
                           'moveforward', 'moveforward', 'turnright', 'moveforward', 'moveforward', 'turnright', 'moveforward']

        print(action_sequence)
        for movement in action_sequence:
            printabs()
            printrel()
            printinfo()
            agent.move(world, movement)
            if agent.alive == False:
                print_slow('you died!')
                print_slow('respawning...:' +
                           str(bool(list(prolog.query("reborn")))))
                agent.resetAgent()
                world.resetWorld()

            elif agent.confunded:
                print_slow('you stepped into a portal!')
                print_slow('relocate to another cell...')
                agent.randomAllocateAgent(world)

                print('test'+agent.sense)
                strs = "reposition("+agent.sense+")"
                print(strs)
                bool(list(prolog.query(strs)))

            else:
                strs = "move("+movement+","+agent.sense+")"
                print('str: '+strs)
                print((list(prolog.query(strs))))
            agent.updateMap(world)
            print_slow('moving')
            print()
            printabs()
            printrel()
            printinfo()

    if option == '4':
        list(prolog.query("reborn"))

        while True:
            if agent.foundgold:
                actions = ['pickup']
            else:
                actions = []
                L = list(prolog.query("explore(L)"))
                if len(L) == 0:
                    print_slow('Exploration Stops\n')
                    break
                actions = L[0]['L']
            print('explore: ' + str(actions))

            for movement in actions:
                printabs()
                printrel()
                printinfo()
                agent.move(world, movement)

                if agent.alive == False:
                    print_slow('you died!')
                    print_slow('respawning...:' +
                               str(bool(list(prolog.query("reborn")))))
                    agent.resetAgent()
                    world.resetWorld()

                elif agent.confunded:
                    print_slow('you stepped into a portal!')
                    print_slow('relocate to another cell...')
                    agent.randomAllocateAgent(world)

                    print('test'+agent.sense)
                    strs = "reposition("+agent.sense+")"
                    print(strs)
                    bool(list(prolog.query(strs)))

                else:
                    strs = "move("+movement+","+agent.sense+")"
                    print('str: '+strs)
                    print((list(prolog.query(strs))))
                agent.updateMap(world)
                print_slow('moving')
                print()
                printabs()
                printrel()
                printinfo()

    if option == '5':
        list(prolog.query("reborn"))

        action_sequence = ['turnleft', 'moveforward', 'turnright', 'moveforward', 'moveforward', 'moveforward', 'moveforward', 'turnright',
                           'moveforward', 'turnright', 'moveforward', 'moveforward', 'turnleft', 'moveforward', 'moveforward', 'turnright', 'moveforward']

        print(action_sequence)
        for movement in action_sequence:
            printabs()
            printrel()
            printinfo()
            agent.move(world, movement)
            if agent.alive == False:
                print_slow('you died!')
                print_slow('respawning...:' +
                           str(bool(list(prolog.query("reborn")))))
                agent.resetAgent()
                world.resetWorld()

            elif agent.confunded:
                print_slow('you stepped into a portal!')
                print_slow('relocate to another cell...')
                agent.randomAllocateAgent(world)

                print('test'+agent.sense)
                strs = "reposition("+agent.sense+")"
                print(strs)
                bool(list(prolog.query(strs)))

            else:
                strs = "move("+movement+","+agent.sense+")"
                print('str: '+strs)
                print((list(prolog.query(strs))))
            agent.updateMap(world)
            print_slow('moving')
            print()
            printabs()
            printrel()
            printinfo()
    elif option == '6':
        quitgame = False
        askTry = False
        while agent.alive == True and agent.gold == False and play:

           # print absolute map, print cell row by row
            printabs()
            agent.updateMap(world)
            # print relative map
            printrel()

            # print agent info
            printinfo()

            actions = list(prolog.query("explore(L)"))
            if(len(actions) == 0):
                print("\n\n")
                print("no actions available, try again?")
            else:
                print('explore: ' + str(actions[0]['L']))
            print('safe: ' + str(list(prolog.query("safe(X,Y)"))))
            # print('sense: '+agent.sense)

            try:
                print('Actions')
                print('1. Move Forward')
                print('2. Turn Left')
                print('3. Turn Right')
                print('4. Pick Up')
                print('5. Shoot')
                print("0. Back to Main Menu")
                option = input("Enter action: ")
                if option == '1':
                    movement = 'moveforward'
                elif option == '2':
                    movement = 'turnleft'
                elif option == '3':
                    movement = 'turnright'
                elif option == '4':
                    movement = 'pickup'
                elif option == '5':
                    movement = 'shoot'
                elif option == '0':
                    break
                if(movement == "moveforward"):
                    agent.move(world, movement)

                if(movement == "turnleft"):
                    agent.move(world, movement)
                if(movement == "turnright"):
                    agent.move(world, movement)
                if(movement == "shoot"):
                    agent.shoot(world)
                if(movement == "pickup"):
                    agent.pickup(world)

                if agent.alive == False:
                    print_slow('you died!')
                    print_slow('respawning...:' +
                               str(bool(list(prolog.query("reborn")))))
                    agent.resetAgent()
                    world.resetWorld()

                elif agent.confunded:
                    print_slow('you stepped into a portal!')
                    print_slow('relocate to another cell...')
                    agent.randomAllocateAgent(world)

                    print('test'+agent.sense)
                    strs = "reposition("+agent.sense+")"
                    print(strs)
                    bool(list(prolog.query(strs)))

                else:
                    strs = "move("+movement+","+agent.sense+")"
                    print('str: '+strs)
                    print((list(prolog.query(strs))))

                agent.updateMap(world)

                print_slow('moving')
            except Exception as e:
                # ... PRINT THE ERROR MESSAGE ... #
                print(e)
                print('awww snap!')
                pass

    elif option == '7':

        world.resetWorldRandom()
        list(prolog.query("reborn"))
        quitgame = False
        askTry = False
        print_slow('good luck have fun')
        while agent.alive == True and agent.gold == False and play:

           # print absolute map, print cell row by row
            printabs()

            # print relative map
            printrel()

            # print agent info
            printinfo()

            actions = list(prolog.query("explore(L)"))
            if(len(actions) == 0):
                print("\n\n")
                print("no actions available, try again?")
            else:
                print('explore: ' + str(actions[0]['L']))
            print('safe: ' + str(list(prolog.query("safe(X,Y)"))))
            # print('sense: '+agent.sense)

            try:
                print('Actions')
                print('1. Move Forward')
                print('2. Turn Left')
                print('3. Turn Right')
                print('4. Pick Up')
                print('5. Shoot')
                print("0. Back to Main Menu")
                option = input("Enter action: ")
                if option == '1':
                    movement = 'moveforward'
                elif option == '2':
                    movement = 'turnleft'
                elif option == '3':
                    movement = 'turnright'
                elif option == '4':
                    movement = 'pickup'
                elif option == '5':
                    movement = 'shoot'
                elif option == '0':
                    break
                if(movement == "moveforward"):
                    agent.move(world, movement)

                if(movement == "turnleft"):
                    agent.move(world, movement)
                if(movement == "turnright"):
                    agent.move(world, movement)
                if(movement == "shoot"):
                    agent.shoot(world)
                if(movement == "pickup"):
                    agent.pickup(world)

                if agent.alive == False:
                    print_slow('you died!')
                    print_slow('respawning...:' +
                               str(bool(list(prolog.query("reborn")))))
                    agent.resetAgent()
                    world.resetWorld()

                elif agent.confunded:
                    print_slow('you stepped into a portal!')
                    print_slow('relocate to another cell...')
                    agent.randomAllocateAgent(world)

                    print('test'+agent.sense)
                    strs = "reposition("+agent.sense+")"
                    print(strs)
                    bool(list(prolog.query(strs)))

                else:
                    strs = "move("+movement+","+agent.sense+")"
                    print('str: '+strs)
                    print((list(prolog.query(strs))))

                agent.updateMap(world)

                print_slow('moving')
            except Exception as e:
                # ... PRINT THE ERROR MESSAGE ... #
                print(e)
                print('awww snap!')
                pass

    elif option == '8':
        world.resetWorldRandom()
        list(prolog.query("reborn"))
        printabs()
        print_slow('this is the absolute map\n')
        print_slow('begin exploration')
        while True:
            if agent.foundgold:
                actions = ['pickup']
            else:
                actions = []
                L = list(prolog.query("explore(L)"))
                if len(L) == 0:
                    print_slow('Exploration Stops\n')
                    break
                actions = L[0]['L']
            print('explore: ' + str(actions))

            for movement in actions:
                printabs()
                printrel()
                printinfo()
                agent.move(world, movement)

                if agent.alive == False:
                    print_slow('you died!')
                    print_slow('respawning...:' +
                               str(bool(list(prolog.query("reborn")))))
                    agent.resetAgent()
                    world.resetWorld()

                elif agent.confunded:
                    print_slow('you stepped into a portal!')
                    print_slow('relocate to another cell...')
                    agent.randomAllocateAgent(world)

                    print('test'+agent.sense)
                    strs = "reposition("+agent.sense+")"
                    print(strs)
                    bool(list(prolog.query(strs)))

                else:
                    strs = "move("+movement+","+agent.sense+")"
                    print('str: '+strs)
                    print((list(prolog.query(strs))))
                agent.updateMap(world)
                print_slow('moving')
                print()
                printabs()
                printrel()
                printinfo()
    elif option == '0':
        play = False
        quitgame = True
        print_slow('Goodbye!')
        break
    world = Map(6, 7)
    world.putThings()
    agent = Agent(world)
    list(prolog.query("reborn"))


string = "Thank you for playing"
for i in range(len(string)):
    print(string[i], end="")
    time.sleep(0.05)
    sys.stdout.flush()
