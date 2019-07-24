import copy   

class Puzzle:
    '''
    Fields:
            size: Nat 
            board: (listof (listof (anyof Str Nat Guess))
            constraints: (listof (list Str Nat (anyof '+' '-' '*' '/' '='))))
    '''
    
    def __init__(self, size, board, constraints):
        self.size=size
        self.board=board
        self.constraints=constraints
        
    def __eq__(self, other):
        return (isinstance(other,Puzzle)) and \
            self.size==other.size and \
            self.board == other.board and \
            self.constraints == other.constraints
    
    def __repr__(self):
        s='Puzzle(\nSize='+str(self.size)+'\n'+"Board:\n"
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.board[i][j],Guess):
                    s=s+str(self.board[i][j])+' '
                else:
                    s=s+str(self.board[i][j])+' '*7
            s=s+'\n'
        s=s+"Constraints:\n"
        for i in range(len(self.constraints)):
            s=s+'[ '+ self.constraints[i][0] + '  ' + \
                str(self.constraints[i][1]) + '  ' + self.constraints[i][2]+ \
                ' ]'+'\n'
        s=s+')'
        return s    

class Guess:
    '''
    Fields:
            symbol: Str 
            number: Nat
    '''        
    
    def __init__(self, symbol, number):
        self.symbol=symbol
        self.number=number
        
    def __repr__(self):
        return "('{0}',{1})".format(self.symbol, self.number)
    
    def __eq__(self, other):
        return (isinstance(other, Guess)) and \
            self.symbol==other.symbol and \
            self.number == other.number        

class Posn:
    '''
    Fields:
            y: Nat 
            y: Nat
    '''         
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)
    
    def __eq__(self,other):
        return (isinstance(other, Posn)) and \
            self.x==other.x and \
            self.y == other.y 
    


# unstr(con) returns a mutated con where the number in position 1 is changed
#    from a str to int
# Effects: mutates con
# unstr: (listof Str) -> (listof Str Int)
# requires: con to be non-empty and con[1] to be a string of integer 

def unstr(con):
    con[1] = int(con[1])
    return con


## read_puzzle(fname) reads information from fname file and returns the info as 
## Puzzle value.
## read_puzzle: Str -> Puzzle
# requires: fname to have at least 1 line of text

def read_puzzle(fname):
    kenken = open(fname, "r")
    n = int(kenken.readline())
    pos = 1
    board = []
    while pos <= n:
        board.append(kenken.readline())
        pos += 1
    constraints = kenken.readlines()
    kenken.close()
    board = list(map(lambda k: k.split(), board))
    constraints = list(map(lambda k: k.split(), constraints))
    constraints = list(map(lambda n: unstr(n) , constraints))
    return Puzzle(n, board, constraints)



## print_sol(puz, fname) prints the Puzzle puz in fname file
# Effects: prints Puzzle puz in fname file
## print_sol: Puzzle Str -> None

def print_sol(puz, fname):
    board = puz.board
    sboard = ""
    for b in board:
        pos = 0
        while pos < len(b):
            sboard += (str(b[pos]) + "  ")
            pos += 1
        sboard += "\n"
    outfile = open(fname, "w")
    outfile.write(sboard)
    outfile.close()



## find_blank(puz) returns the position of the first blank
## space in puz, or False if no cells are blank.  If the first constraint has
## only guesses on the board, find_blank returns 'guess'.  
## find_blank: Puzzle -> (anyof Posn False 'guess')
## Examples:
## find_blank(puzzle1) => Posn(0 0)
## find_blank(puzzle3partial) => 'guess'
## find_blank(puzzle2soln) => False

def find_blank(puz):
    board = puz.board
    constraints = puz.constraints
    if constraints == []:
        return False
    first_fill = constraints[0][0]
    pos = 0
    while pos <= len(board):
        if pos == len(board):
            return "guess"
        elif first_fill not in board[pos]:
            pos += 1
        elif first_fill in board[pos]:
            break
    y = 0
    for row in board:
        x = 0
        for n in row: 
            if n == first_fill:
                return Posn(x, y)
            else:
                x += 1
        y += 1
        



## used_in_row(puz, pos) returns a list of numbers used in the same 
## row as (x,y) position, pos, in the given puz.  
## used_in_row: Puzzle Posn -> (listof Nat)
# requires pos to be within the range of puz
## Example: 
## used_in_row(puzzle1,Posn(1,1)) => []
## used_in_row(puzzle1partial2,Posn(0,1)) => [1,2,4]

def used_in_row(puz,pos):
    board = puz.board
    if len(board) < 1: 
        board = [board]
    row = board[pos.y]
    used_num = []
    for n in row:
        if type(n) == Guess:
            used_num.append(n.number)
        elif type(n) == int:
            used_num.append(n)
    return sorted(used_num)



## used_in_col(puz, pos) returns a list of numbers used in the same 
## column as (x,y) position, pos, in the given puz.  
## used_in_col: Puzzle Posn -> (listof Nat)
## Examples:
## used_in_col(puzzle1partial2,Posn(1,0)) => [2,3]
## used_in_col(puzzle2soln,Posn(3,5)) => [1,2,3,4,5,6]

def used_in_col(puz,pos):
    x = pos.x
    board = puz.board
    n = puz.size
    column = []
    row = 0
    if len(board) == 0:
        return []
    while row < n:
        if type(board[row][x]) == Guess:
            column.append(board[row][x].number)
        elif type(board[row][x]) == int:
            column.append(board[row][x])
        row += 1
    return sorted(column)
 
 

##available_vals(puz,pos) returns a list of valid entries for the (x,y)  
## position, pos, of the consumed puzzle, puz.  
## available_vals: Puzzle Posn -> (listof Nat)
## Examples:
## available_vals(puzzle1partial, Posn(2,2)) => [2,4]
## available_vals(puzzle1partial2, Posn(0,1)) => [3]

def available_vals(puz,pos):
    n = puz.size
    used_row = used_in_row(puz,pos)
    used_col = used_in_col(puz, pos)
    used = used_row + used_col
    num = 1
    avail_num = []
    while num <= n:
        if num not in used:
            avail_num.append(num)
        num += 1
    return avail_num

             

## place_guess(brd,pos,val) fills in the (x,y) position, pos, of the board, brd, 
## with the a guess with value, val
## place_guess: (listof (listof (anyof Str Nat Guess))) Posn Nat 
##              -> (listof (listof (anyof Str Nat Guess)))
#  requires: pos of the the brd contains a symbol
## Examples:
## See provided tests

def place_guess(brd,pos,val):
    res=copy.deepcopy(brd)  # a copy of brd is assigned to res without any 
                            # aliasing to avoid mutation of brd. 
                            #  You should update res and return it
    res[pos.y][pos.x] = Guess(res[pos.y][pos.x], val)
    return res 



# fill_in_guess(puz, pos, val) fills in the pos Position of puz's board with 
# a guess with value val
# fill_in_guess: Puzzle Posn Nat -> Puzzle
# Examples: See provided tests


def fill_in_guess(puz, pos, val):
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    tmp=copy.deepcopy(res.board)
    res.board=place_guess(tmp, pos, val)
    return res


## guess_valid(puz) determines if the guesses in puz satisfy their constraint
## guess_valid: Puzzle -> Bool
## Examples: See provided tests

def guess_valid(puz):
    op = puz.constraints[0][2]
    op_num = puz.constraints[0][1]
    op_sym = puz.constraints[0][0]
    guess_num = []
    board = copy.deepcopy(puz.board) # so the puz.board is not mutated 
    row = 0
    for y in board: # generates a list of Nat that are all Guess of op_sym
        col = 0     #  and they are place at valid positions 
        for x in y:
            if type(x) == Guess and x.symbol == op_sym:
                avail_guess_sym = board[row][col].symbol # as if no guess was 
                board[row][col] = avail_guess_sym        # placed
                if x.number in available_vals(Puzzle(puz.size, board, 
                                                     puz.constraints), 
                                              Posn(col, row)):
                    guess_num.append(x.number)
            col += 1
        row += 1
    if op == '+' and sum(guess_num)==op_num:
        return True
    elif op == '*':
        pos = 0
        mult = 1
        while pos < len(guess_num):
            mult *= guess_num[pos]
            pos += 1
        if mult == op_num:
            return True
    elif op == '-':
        if guess_num[0] - guess_num[1] == op_num or \
        guess_num[1] - guess_num[0] == op_num:
            return True
    elif op == '/':
        if guess_num[0] // guess_num[1] == op_num or \
        guess_num[1] // guess_num[0] == op_num:
            return True
    elif op == '=' and len(guess_num) > 0 and guess_num[0] == op_num:
        return True
    else: return False



## apply_guess(puz) converts all guesses in puz into their corresponding numbers
## and removes the first contraint from puz's list of contraints
## apply_guess:  Puzzle -> Puzzle
# requires puz.constraints to be non empty
## Examples: See provided tests

def apply_guess(puz):
    # a copy of puz is assigned to res without any 
    # aliasing to avoid mutation of puz. 
    #  You should update res and return it    
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    board = res.board
    row = 0
    for rows in board:
        column = 0
        for x in rows:
            if type(x) == Guess:
                board[row][column] = x.number
            column += 1
        row += 1
    res.constraints = res.constraints[1:]
    return res                                         



## neighbours(puz) returns a list of next puzzles after puz in
## the implicit graph
## neighbours: Puzzle -> (listof Puzzle)
## Examples: See provided tests

def neighbours(puz):
    # a copy of puz is assigned to tmp without any 
    # aliasing to avoid mutation of puz. 
    tmp=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    
    if find_blank(tmp) == False:
        return []
    elif find_blank(tmp) == 'guess':
        if guess_valid(tmp):
            return [apply_guess(tmp)]
        elif not guess_valid(tmp):
            return []
    n = puz.size
    board = puz.board
    cons = puz.constraints
    con_sym = cons[0][0]
    pos = find_blank(tmp) # returns the first available Posn
    avail_val = available_vals(tmp, pos)
    lst_guess = []
    for val in avail_val:
        lst_guess.append(Puzzle(n, place_guess(board,pos,val), cons))
    return lst_guess
    


## solve_kenken(orig) finds the solution to a KenKen puzzle,
## orig, or returns False if there is no solution.  
## solve-kenken: Puzzle -> (anyof Puzzle False)
## Examples: See provided tests

def solve_kenken(orig):
    to_visit=[]
    visited=[]
    to_visit.append(orig)
    while to_visit!=[] :
        if find_blank(to_visit[0])==False:
            return to_visit[0]
        elif to_visit[0] in visited:
            to_visit.pop(0)
        else:
            nbrs = neighbours(to_visit[0])
            new = list(filter(lambda x: x not in visited, nbrs))
            new_to_visit=new + to_visit[1:] 
            new_visited= [to_visit[0]] + visited
            to_visit=new_to_visit
            visited=new_visited     
    return False
