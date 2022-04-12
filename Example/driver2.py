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
        # edge case: wall
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
        self.startX = 1
        self.startY = 1
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

    # reset world
    def resetWorld(self):
        self.world = []
        self.makeWorld()

    # set env
    def putThings(self):
        x = 0
        xm = [0, 1, 0, -1]
        ym = [-1, 0, 1, 0]
        next = "P"
        checkPos = False
        while checkPos == False:
            tx = random.randint(self.startX, self.width-1)
            ty = random.randint(self.startY, self.height-1)

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
        self.mapHeight = 8
        self.mapWidth = 8
        self.resetAgent()

    def resetAgent(self):
        self.alive = True
        self.gold = False
        self.confunded = False
        self.direction = "DOWN"
        self.arrow = 1
        self.route = []
        self.xPos = 1
        self.yPos = 1
        self.startx = 1
        self.starty = 1
        self.makeMap()
        self.sense = ''
        self.percept = 'C-S-T-G-B-S'

    def randomAllocateAgent(self, world):
        self.alive = True
        self.direction = "DOWN"
        self.arrow = 1
        self.route = []
        self.confunded = False
        self.sense = ''
        self.percept = 'Confounded-S-T-G-B-S'
        checkPos = False
        while checkPos == False:
            tx = random.randint(1, world.width-1)
            ty = random.randint(1, world.height-1)
            if world.world[ty][tx].wall == False and world.world[ty][tx].confundus == False and world.world[ty][tx].wumpus == False:
                self.xPos = tx
                self.yPos = ty
                self.startx = tx
                self.starty = ty
                checkPos = True
        self.makeMap()

    # create relative map

    def makeMap(self):
        self.map = []
        for h in range(self.mapHeight):
            self.map.append([])
            for w in range(self.mapWidth):
                cell = Cell(h, w)

                if h == self.yPos and w == self.xPos:
                    cell.agent = True
                    cell.agent_direction = self.direction
                    cell.empty = False
                    cell.visited = True
                    cell.safe = True

                self.map[h].append(cell)

    # percepts: get the input for prolog
    def percepts(self, cell, event):

        print('percepts function')
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
                percepts += 'Glitter-'
                sense += 'on,'
            else:
                percepts += 'G-'
                sense += 'off,'
            if event == 'bump':
                percepts += 'Bump-'
                sense += 'on,'
                cell.bump = True
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

            if self.direction == "UP":
                direction = 0
            elif self.direction == "RIGHT":
                direction = 1
            elif self.direction == "DONW":
                direction = 2
            elif self.direction == "LEFT":
                direction = 3
        x = 0
        y = 0
        while hit == False:
            print('shoot function')
            print_slow(str(self.yPos+ym[direction]+y))
            print_slow(str(self.xPos+xm[direction]+x))
            world.world[self.yPos+ym[direction] +
                        y][self.xPos+xm[direction]+x].glitter = True
            if world.world[self.yPos+ym[direction]+y][self.xPos+xm[direction]+x].wumpus:
                hit = True
                print_slow('You killed the wumpus!')
                # remove wumpus & stench, add scream
                self.map[self.yPos][self.xPos].scream = True
                world.world[self.yPos+ym[direction] +
                            y][self.xPos+xm[direction]+x].wumpus = False
                wumpusY = self.yPos+ym[direction]+y
                wumpusX = self.xPos+xm[direction]+x
                for i in range(4):
                    world.world[wumpusY+ym[i]][wumpusX+xm[i]].stench = False
                self.percepts(self.map[self.yPos][self.xPos], 'scream')
            elif world.world[self.yPos+ym[direction]+y][self.xPos+xm[direction]+x].wall:
                hit = True
                print_slow('You missed!')
                self.percepts(self.map[self.yPos][self.xPos], 'nil')
            else:
                y += ym[direction]
                x += xm[direction]

    def updateMap(self):
        print('in update map')
        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])
        relativeD = (relative_pos[0]["D"])
        print(relativeX, relativeY, relativeD)
        absX = self.startx - relativeX
        absY = self.starty + relativeY
        print('newcell: '+str(self.map[absY][absX]))
        print('newcell: '+str(absY)+str(absX))
        self.map[absY][absX].agent = True
        self.map[absY][absX].empty = False
        self.map[absY][absX].agent_direction = self.direction
        print(bool(list(prolog.query(getquerystr('stench', relativeX, relativeY)))))

        self.map[absY][absX].stench = bool(
            list(prolog.query(getquerystr("stench", relativeX, relativeY))))
        self.map[absY][absX].tingle = bool(
            list(prolog.query(getquerystr("tingle", relativeX, relativeY))))
        self.map[absY][absX].glitter = bool(
            list(prolog.query(getquerystr("glitter", relativeX, relativeY))))
       # self.map[absY][absX].bump = bool(
        #  list(prolog.query(getquerystr("bump", relativeX, relativeY))))
        # self.map[absY][absX].safe = bool(
        #    list(prolog.query(getquerystr("safe", relativeX, relativeY))))
        self.map[absY][absX].stench = world.world[absY][absX].stench
        wumpus = list(prolog.query(
            getquerystr("wumpus", relativeX, relativeY)))
        print(wumpus)
        # iterate throught the list of maps to mark cells
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                relativeX = self.startx - j
                relativeY = i - self.starty
                self.map[i][j].wumpus = bool(
                    list(prolog.query(getquerystr("wumpus", relativeX, relativeY))))
                self.map[i][j].safe = bool(
                    list(prolog.query(getquerystr("safe", relativeX, relativeY))))
                self.map[i][j].confundus = bool(
                    list(prolog.query(getquerystr("confundus", relativeX, relativeY))))

              #  self.map[i][j].confoundus = bool(
              #  list(prolog.query(getquerystr("confundus", relativeX, relativeY))))

        # update position !!!!!!
        self.xPos = absX
        self.yPos = absY

    def move(self, world, action):

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
                relative_pos = list(prolog.query("current(X,Y,D)"))
                relativeX = (relative_pos[0]["X"])
                relativeY = (relative_pos[0]["Y"])
                relativeD = (relative_pos[0]["D"])
                absX = self.startx - relativeX
                absY = self.starty + relativeY
                self.map[absY][absX].agent = False
                self.map[absY][absX].empty = True
                self.map[absY][absX].scream = False
                # set new location

                # update agent position
              #  self.xPos = newx
              #  self.yPos = newy
                print(newx, newy)
                self.percepts(cell, 'nil')
                self.map[self.yPos][self.xPos].visited = True
            else:
                '''do nth, no update'''
                bump = True
                print_slow('You bump into a wall!')
                self.map[newy][newx].wall = True
                self.percepts(cell, 'bump')

        # change agent direction for turning

        if action == "turnleft":
            direction = self.direction
            if direction == "UP":
                self.direction = "LEFT"
            if direction == "DOWN":
                self.direction = "RIGHT"
            if direction == "LEFT":
                self.direction = "DOWN"
            if direction == "RIGHT":
                self.direction = "UP"
            self.map[self.yPos][self.xPos].agent_direction = self.direction
            self.map[self.yPos][self.xPos].scream = False
            cell = world.world[self.yPos][self.xPos]
            self.percepts(cell, 'nil')

        if action == "turnright":
            direction = self.direction
            if direction == "UP":
                self.direction = "RIGHT"
            if direction == "DOWN":
                self.direction = "LEFT"
            if direction == "LEFT":
                self.direction = "UP"
            if direction == "RIGHT":
                self.direction = "DOWN"
            self.map[self.yPos][self.xPos].agent_direction = self.direction
            self.map[self.yPos][self.xPos].scream = False
            cell = world.world[self.yPos][self.xPos]
            self.percepts(cell, 'nil')

        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])

    def pickup(self, world):
        relative_pos = list(prolog.query("current(X,Y,D)"))
        relativeX = (relative_pos[0]["X"])
        relativeY = (relative_pos[0]["Y"])
        absX = self.startx - relativeX
        absY = self.starty + relativeY
        if world.world[absY][absX].glitter:
            world.world[absY][absX].glitter = False
           # self.map[absY][absX].gold=True
            # self.gold=True
            print_slow('You found the gold!')
            self.percepts(world.world[absY][absX], 'nil')
        else:
            print_slow('nothing there...')
            self.percepts(world.world[absY][absX], 'nil')


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


reset = True
play = True
quitgame = False


while not quitgame:

    if reset:
        world.resetWorld()
        world.putThings()
        agent = Agent(world)
        reset = False
        play = True

    if play:
        quitgame = False
        askTry = False
        while agent.alive == True and agent.gold == False and play:

           # print absolute map, print cell row by row
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

            # print relative map
            print("relative map:\n")
            for i in range(len(agent.map)):
                for j in range(len(agent.map[i])):
                    print(" ".join(repr(agent.map[i][j])[0:3]), end="  ")
                print("\n", end="")
                for j in range(len(agent.map[i])):
                    print(" ".join(repr(agent.map[i][j])[3:6]), end="  ")
                print("\n", end="")
                for j in range(len(agent.map[i])):
                    print(" ".join(repr(agent.map[i][j])[6:9]), end="  ")
                print("\n")

            # print agent info
            print("agent absolute location: X:" +
                  str(agent.yPos)+" Y: "+str(agent.xPos))
            print("agent absolute direction:"+str(agent.direction))
            print('agent relative location: ' +
                  str(list(prolog.query("current(X,Y,_)"))))
            print("agent relative direction:" +
                  str(list(prolog.query("current(_,_,D)"))))

            print('agent sense: '+agent.percept)

            print('visited: ' + str(list(prolog.query("visited(X,Y)"))))
            print('stench: ' + str(list(prolog.query("stench(X,Y)"))))
            print('tingle: ' + str(list(prolog.query("tingle(X,Y)"))))

            # actions=list(prolog.query("explore(L)"))
            # if(len(actions)==0) :
            #   print("\n\n")
            #   print("no actions available, try again?")
           # else:
          #      print('explore: ' + str(actions[0]['L']))
            # print('safe: ' + str(list(prolog.query("safe(X,Y)"))))
            # print('sense: '+agent.sense)

            try:
                movement = input("Enter direction: ")
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

                elif agent.confunded:
                    print_slow('you stepped into a portal!')
                    print_slow('relocate to another cell...')
                    agent.randomAllocateAgent(world)
                    agent.percepts(
                        world.world[agent.starty][agent.startx], 'confounded')
                    print('test')
                    strs = "reposition("+agent.sense+")"
                    print(strs)
                    bool(list(prolog.query(strs)))

                else:
                    strs = "move("+movement+","+agent.sense+")"
                    print('str: '+strs)
                    print((list(prolog.query(strs))))

                agent.updateMap()

                print_slow('moving')
            except Exception as e:
                # ... PRINT THE ERROR MESSAGE ... #
                print(e)
                print('awww snap!')
                pass

            # print thank you for playing message character by character

string = "thank you for playing"
for i in range(len(string)):
    print(string[i], end="")
    time.sleep(0.05)
    sys.stdout.flush()
