w, h = 7, 6

# X row width
# Y column height

board = [[0 for y in range(h)] for x in range(w)]

innerW, innerH = 3, 3

for X in range(len(board)):
    for Y in range(len(board[X])):
        board[X][Y] = [['.' for x in range(innerW)] for y in range(innerH)]

board[0][0][0][1] = '-'

line = [["" for y in range(innerH)] for x in range(h)]

for X in range(len(board)):
    for Y in range(len(board[X])):
        cell = board[X][Y]
        for innerX in range(len(cell)):
            for innerY in range(len(cell[innerX])):
                if innerX == 2 and X != len(board)-1:
                    line[Y][innerY] += f" {cell[innerX][innerY]} "
                else:
                    line[Y][innerY] += f" {cell[innerX][innerY]}"

for i in range(h):
    for j in range(innerH):
        print(line[i][j])
    print()

# line = [["|" for y in range(innerH)] for x in range(h)]

# for X in range(len(board)):
#     for Y in range(len(board[X])):
#         cell = board[X][Y]
#         for innerX in range(len(cell)):

#             for innerY in range(len(cell[innerX])):
#                 if innerX == 2 and X != len(board)-1:
#                     line[Y][innerY] += f" {cell[innerX][innerY]} | |"
#                 else:
#                     line[Y][innerY] += f" {cell[innerX][innerY]} |"

# decorator = ""

# for i in range(w):
#     decorator += "+"

#     for j in range(innerW):
#         decorator += "---+"

#     decorator += " "

# for i in range(h):
#     print(decorator)
#     for j in range(innerH):
#         print(line[i][j])
#         print(decorator)
#     print()


# for X in range(len(board)):
#     for Y in range(len(board[X])):
#         cell = board[X][Y]
#         for innerX in range(len(cell)):
#             for innerY in range(len(cell[innerX])):
#                 if innerY == 2:
#                     print(cell[innerX][innerY], end="\n")
#                 else:
#                     print(cell[innerX][innerY], end=" ")

# board = [[0 for x in range(w)] for y in range(h)]

# innerW, innerH = 3, 3

# for Y in range(len(board)):
#     for X in range(len(board[Y])):
#         board[Y][X] = [['.' for x in range(innerW)] for y in range(innerH)]

# board[0][0][1][0] = '-'

# Iterate grid from it's Y axis
for Y in range(len(board)):

    # Iterate the 3x3 cell grid from it's Y axis
    for innerY in range(innerW):

        # Print out the cell row by row
        for X in range(len(board[Y])):

            cell = board[Y][X]

            for innerX in range(len(cell[innerY])):
                print(cell[innerY][innerX], end=" ")

            print(" ", end="")

        print("\n", end="")

    print("\n", end="")
