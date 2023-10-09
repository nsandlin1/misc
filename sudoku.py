# Uses backtracking

puzzle = [[0,0,3,0,0,0,0,0,8],
          [0,4,9,7,0,0,1,0,0],
          [0,0,0,6,5,0,0,0,0],
          [0,0,5,9,0,0,0,0,1],
          [7,8,0,0,0,0,0,3,2],
          [3,0,0,0,0,1,5,0,0],
          [0,0,0,0,6,7,0,0,0],
          [0,0,7,0,0,2,6,1,0],
          [4,0,0,0,0,0,3,0,0]]

def is_val(num, puzzle, x, y):
    '''
    Verifies validity of move
    '''

    # Check row
    if num in puzzle[x]:
        return False
    
    # Check column
    for row in puzzle:
        if row[y] == num:
            return False
    
    # Check in box
    box_row = (x//3)*3
    box_col = (y//3)*3
    for row in range(3):
        for col in range(3):
            if puzzle[box_row + row][box_col + col] == num:
                return False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     


    return True

def get_empty(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col
    return None

def solver(puzzle):

    empt = get_empty(puzzle)
    if empt:
        row, col = empt
    else:
        return True
    
    for num in range(1, 10):
        if is_val(num, puzzle, row, col):
            puzzle[row][col] = num
            if solver(puzzle):
                return True
            puzzle[row][col] = 0

    return False

if __name__ == '__main__':
    if solver(puzzle):
        for row in range(9):
            print(puzzle[row])
    else:
        print('nothing')
