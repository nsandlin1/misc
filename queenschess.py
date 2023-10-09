import operator

def is_val(board, n, x, y):
    '''
    returns if placement of queen is legal
    '''

    # Checks horizontal
    if 'Q' in board[x]:
        return False
    
    # Checks vertical
    for row in board:
        if row[y] == 'Q':
            return False

    # Checks diagonal


    def queen_blocking(board, n, x, y, dir):
        '''
        returns: whether a queen is blocking move
        '''

        operatorlookup = {
            '+': operator.add,
            '-': operator.sub
        }


        def reqs(dir, n):
            '''
            returns: constraints with respect to map size
            '''

            if dir == 'NE':
                return tempx > 0 and tempy < n
            if dir == 'SE':
                return tempx < n and tempy < n
            if dir == 'SW':
                return tempx < n and tempy > 0
            if dir == 'NW':
                return tempx > 0 and tempy > 0

        def get_ops(dir):
            '''
            returns: operations of x, y respectively through diagonal traversal
            '''

            if dir == 'NE':
                return ['-','+']
            if dir == 'SE':
                return ['+','+']
            if dir == 'SW':
                return ['+','-']
            if dir == 'NW':
                return ['-','-']

        
        tempx = x
        tempy = y

        ops = get_ops(dir)
        op1 = operatorlookup.get(ops[0])
        op2 = operatorlookup.get(ops[1])

        while reqs(dir, n):
            tempx = op1(tempx, 1)
            tempy = op2(tempy, 1)
            if board[tempx][tempy] == 'Q':
                return True


    if queen_blocking(board, n, x, y, 'NE'):
        return False
    if queen_blocking(board, n, x, y, 'SE'):
        return False
    if queen_blocking(board, n, x, y, 'SW'):
        return False
    if queen_blocking(board, n, x, y, 'NW'):
        return False
    
    return True


def gen_spots(board, n, num_queens=0):
    '''
    returns: board with queens positioned
    '''

    if num_queens == n+1:
        return True


    for row in range(len(board)):
        for col in range(len(board[row])):
            if is_val(board, n, row, col):
                board[row][col] = 'Q'
                num_queens += 1
                if gen_spots(board, n, num_queens):
                    return True
                
                board[row][col] = '-'
                num_queens -= 1
    return False
            

def printSolution(board):
    for r in board:
        print(str(r).replace(',', '').replace('\'', ''))
    print()


if __name__ == '__main__':
    bs = int(input("Enter a value n to generate n*n board: "))
    board = [['-' for _ in range(0, bs)] for _ in range(0, bs)]
    n = bs-1
    if gen_spots(board, n):
        printSolution(board)
