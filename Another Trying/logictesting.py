
unvisitedlist = [(1, 0),  (-1, 0),  (0, 1),  (0, -1)]
stench = [[0, 2], [-1, 3]]
safe = [[0, 0], [1, 0], [1, 1], [1, 2], [
    2, 2], [3, 2], [-1, 0], [0, 1], [0, -1]]
print(stench)
print(unvisitedlist)


def checkwumpus():
    start = stench[0]
    end = stench[1]

    if (start[0]+1 == end[0] or start[0]-1 == end[0]):
        print(f'wumpus at {end[0]},{start[1]}')
    if (start[1]+1 == end[1] or start[1]-1 == end[1]):
        print(f'wumpus at {start[0]},{end[1]}')

    # Moving forward
    # rnorth Y+1
    # rwest X-1
    # reast X+1
    # rsouth Y-1

    # (1,0) -> (0,1)
tempcurrentlocation = {
    'X': -1,
    'Y': 2,
    'D': 'reast'
}


def movetolocation(coor):
    print(tempcurrentlocation['X'], tempcurrentlocation['Y'])
    i = 0
    while coor[0] != tempcurrentlocation['X'] or coor[1] != tempcurrentlocation['Y']:
        moveX(tempcurrentlocation['X'], coor[0])
        print(
            f"After MoveX: X: {tempcurrentlocation['X']} Y: {tempcurrentlocation['Y']}")
        moveY(tempcurrentlocation['Y'], coor[1])
        print(
            f"After MoveY: X: {tempcurrentlocation['X']} Y: {tempcurrentlocation['Y']}")

    print(tempcurrentlocation['X'], tempcurrentlocation['Y'])


def changedirection(G):
    if tempcurrentlocation['D'] != G:
        if tempcurrentlocation['D'] == 'rnorth':
            tempcurrentlocation['D'] = 'reast'
        elif tempcurrentlocation['D'] == 'rwest':
            tempcurrentlocation['D'] = 'rnorth'
        elif tempcurrentlocation['D'] == 'reast':
            tempcurrentlocation['D'] = 'rsouth'
        elif tempcurrentlocation['D'] == 'rsouth':
            tempcurrentlocation['D'] = 'rwest'
        changedirection(G)


def moveX(start, end):
    # print(f'moveX start: {start}, end: {end}')
    X = end - start
    if start < end:
        # if X > 0:
        # print(tempcurrentlocation['D'])
        changedirection('reast')
        # print(tempcurrentlocation['D'])
        for i in range(start+1, end+1):
            if [i, tempcurrentlocation['Y']] in safe:
                tempcurrentlocation['X'] = i
            else:
                break
    elif start > end:
        # elif X < 0:
        # print(tempcurrentlocation['D'])
        changedirection('rwest')
        # print(tempcurrentlocation['D'])
        for i in range(start, end-1, - 1):
            if [i, tempcurrentlocation['Y']] in safe:
                tempcurrentlocation['X'] = i
            else:
                break


def moveY(start, end):
    # print(f'moveY start: {start}, end: {end}')
    Y = end - start
    # if Y > 0:
    if start < end:
        # print(tempcurrentlocation['D'])
        changedirection('rnorth')
        # print(tempcurrentlocation['D'])
        for i in range(start+1, end+1):
            if [tempcurrentlocation['X'], i] in safe:
                tempcurrentlocation['Y'] = i
            else:
                break

    # elif Y < 0:
    elif start > end:
        # print(tempcurrentlocation['D'])
        changedirection('rsouth')
        # print(tempcurrentlocation['D'])
        for i in range(start, end-1, - 1):
            if [tempcurrentlocation['X'], i] in safe:
                tempcurrentlocation['Y'] = i
            else:
                break


# movetolocation([-2, 1])
# print(-2 > -1)
# print(-2 > -1)
# Start < End
# print(-4 < -1)

# print(-1 > -4)

# def test():
#     for i in range(1, -1-1, - 1):
#         print(i)


# test()

checkwumpus()
