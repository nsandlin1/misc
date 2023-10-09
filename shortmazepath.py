my_maze = [[1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
           [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
           [0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
           [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
           [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
           [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
           [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
           [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]]


traveled = [[False for col in row] for row in my_maze]


def is_val(move):
    '''
    takes: tile to move to e.g., [5,4]
    returns: validity of a move
    '''

    x = move[0]
    y = move[1]

    # Checks if on board
    if x < 0 or y < 0 or x > 9 or y > 9:
        return False

    # Checks if a 1
    if my_maze[x][y] == 0:
        return False

    # Checks if previously traveled
    if traveled[x][y] == True:
        return False

    return True

def poss_moves(curr):
    currx = curr[0]
    curry = curr[1]
    poss = []

    # Up
    poss.append((currx-1, curry))
    # Down
    poss.append((currx+1, curry))
    # Left
    poss.append((currx, curry-1))
    # Right
    poss.append((currx, curry+1))

    return poss

def printSolution(board):
    for r in board:
        print(str(r).replace(',', '').replace('True', 'True '))
    print()


def gen_path(curr, end, min=0): 
    
    traveled[curr[0]][curr[1]] = True

    if curr == end:
        return min

    up, down, left, right = poss_moves(curr)

    if is_val(up):
        min = gen_path(up, end, min+1)
    if is_val(down):
        min = gen_path(down, end, min+1)
    if is_val(left):
        min = gen_path(left, end, min+1)
    if is_val(right): 
        min = gen_path(right, end, min+1)
    
    return min




if __name__ == '__main__':
    print(gen_path((0,0), (7,5)))

    printSolution(traveled)