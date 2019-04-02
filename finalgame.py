
import random
# The board is a list of numbers corresponding to each position in the game board. The numbers then will be replaced by
# either 'O' or 'X' as the game progresses.
board = [0,1,2,3,4,5,6,7,8,9]

# Initialize players and computer values
player = ''
computer = ''

# Corners, Center and Side Moves, respectively

corners = [1, 7, 3, 9]
center = [5]
sides = [2, 4, 6, 8]

# Winner combinations
winners = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

# Table
tab = range(1, 10)

def print_board():
    """
    This function prints the board. The board has 9 blank spaces in the beginning. As the game progresses, each blank
    space is filled with the user or computer inputted value (X or O)
    :return:
    """
    x = 1
    for i in board:
        end = ' | '
        if x % 3 == 0:
            end = ' \n'
            if i != 1:
                end += '---------\n'
        char = ' '
        if i in ('X', 'O'):
            char = i
        x += 1
        print(char, end=end)


def select_char():
    """
    This function randomly assigns X or O to the user, and consequently to the computer.
    :return:
    """
    chars = ('X', 'O')
    if random.randint(0, 1) == 0:
        return chars[::-1]
    return chars


def can_move(brd, player, move):
    """
    This function determines whether there is a move available to make. Basically, checks whether the board is full or not.
    Returns false if the space is already played, or if there is no more space left to play.
    :param brd: the board list
    :param player:
    :param move: The position in the board
    :return:
    """
    if move in tab and brd[move - 1] == move - 1:
        return True
    return False


def can_win(brd, player, move):
    """
    This function determines whether the player in question can potentially win. Returns true if the board has winning
    combinations as given in the 'winners' tuple.
    :param brd:
    :param player:
    :param move:
    :return:
    """
    places = []
    x = 0
    for i in brd:
        if i == player:
            places.append(x)
        x += 1
    win = True
    for tup in winners:
        win = True
        for ix in tup:
            if brd[ix] != player:
                win = False
                break
        if win == True:
            break
    return win


def make_move(brd, player, move, undo=False):
    """
    This will make the desired move by replacing the number in the board list by the player character, 'X' or 'O'. Returns
    a tuple with either (False, False) or (True, False) or (True, True)
    :param brd:
    :param player:
    :param move:
    :param undo:
    :return:
    """
    if can_move(brd, player, move):
        brd[move - 1] = player
        win = can_win(brd, player, move)
        if undo:
            brd[move - 1] = move - 1
        return (True, win)
    return (False, False)


# Bot
def computer_move():
    """
    This is the algorithm used by the bot to make a decision regarding where to play.
    :return:
    """
    move = -1
    # Step 1: Check if there is a winning move to play. If yes, play that move. If not, go to step 2.
    for i in range(1, 10):
        if make_move(board, computer, i, True)[1]:
            move = i
            break
    if move == -1:
        # Step 2: Check if player has the potential for a winning move. If yes, block that move by playing it.
        # If not, go to step 3.
        for i in range(1, 10):
            if make_move(board, player, i, True)[1]:
                move = i
                break
    if move == -1:
        # Step 3: If center is free, try to take the center.
        for mv in center:
            #for mv in tup:
            if move == -1 and can_move(board, computer, mv):
                move = mv
                break
    if move == -1:
        # Step 4: Check if the corners are free. Then take one of the corners.
        for mv in corners:
            #for mv in tup:
            if move == -1 and can_move(board, computer, mv):
                move = mv
                break
    return make_move(board, computer, move)


def space_exist():
    """
    Check whether there is space remaining in the board to play
    :return: True or False
    """
    return board.count('X') + board.count('O') != 9


# Game Start

# Ask user to select opponent
vschoice = input("Who is your opponent? 1.Computer 2.Another Player. Type (1/2) ")

# If user selects the computer
if int(vschoice)==1:

    # Ask user who goes first
    firstmove = input("Who goes first? 1.Player 2. Computer ")

    # When player goes first
    if int(firstmove)==1:
        player, computer = select_char()
        print('Player is [%s] and computer is [%s]' % (player, computer))
        result = 'Draw!'
        while space_exist():
            print_board()

            move = int(input('# Make your move ! [1-9] : '))
            moved, won = make_move(board, player, move)
            if not moved:
                print(' >> Invalid number ! Try again !')
                continue
            #
            if won:
                result = 'Congratulations ! You won !'
                break
            elif computer_move()[1]:
                result = 'You lose !'
                break

        print_board()
        print(result)

    # If computer goes first.
    if int(firstmove)==2:
        player, computer = select_char()
        print('Player is [%s] and computer is [%s]' % (player, computer))
        result = 'Draw!'
        while space_exist():
            if computer_move()[1]:
                result = 'You lose'
                break
            print_board()
            move = int(input('# Make your move ! [1-9] : '))

            moved, won = make_move(board, player, move)

            if not moved:
                print(' >> Invalid number ! Try again !')
                continue
            #
            if won:
                result = 'Congratulations ! You won !'
                break


        print_board()
        print(result)

# If player chooses another player as opponent
if int(vschoice) == 2:
    player, player2 = select_char()
    print('Player 1 is [%s] and Player 2 is [%s]' % (player, player2))
    result = 'Draw'
    while space_exist():
        print_board()

        move = int(input('# Make your move ! [1-9] : '))
        moved, won = make_move(board, player, move)
        if not moved:
            print(' >> Invalid number ! Try again !')
            continue
        #
        if won:
            result = 'Congratulations ! P1 won !'
            break

        print_board()
        move1 = int(input('# P2 Make your move ! [1-9] : '))
        moved1, won1 = make_move(board, player2, move1)
        if not moved1:
            print(' >> Invalid number ! Try again !')
            continue
        #
        if won1:
            result = 'Congratulations ! P2 won !'
            break

    print_board()
    print(result)

