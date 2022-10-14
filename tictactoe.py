"""
Tic Tac Toe Player
"""

X = "X"
O = "O"
EMPTY = None

player_value = {
    X: 1,
    O: -1,
    None: 0
}

opponent_dict = {
    X: O,
    O: X
}


winning_combinations = [
    # horizontal
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # vertical
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # diagonal
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum([
        row.count(X)
        for row in board
    ])

    o_count = sum([
        row.count(O)
        for row in board
    ])

    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result_list = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                result_list.append((i, j))

    return result_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def player_result(board, action, current_player):
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for comb in winning_combinations:
        if board[comb[0][0]][comb[0][1]] == board[comb[1][0]][comb[1][1]] == board[comb[2][0]][comb[2][1]]:
            return board[comb[0][0]][comb[0][1]]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return sum([
        row.count(EMPTY)
        for row in board
    ]) == 0 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return player_value[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    possible_actions = actions(board)
    actions_dict = {}

    for action in possible_actions:
        current_result_board = result(board, action)
        opponent_result_board = player_result(board, action, opponent_dict[current_player])

        current_player_value = utility(current_result_board)
        opponent_player_value = utility(opponent_result_board)

        add_value_to_set(actions_dict, current_player_value, action)
        add_value_to_set(actions_dict, opponent_player_value, action)

    return get_action(actions_dict, current_player)


def add_value_to_set(my_dict, key, value):
    if key in my_dict:
        my_dict[key].add(value)
    else:
        my_dict[key] = {value}


def get_action(actions_dict, current_player):
    # returns first actions if current user can win
    if player_value[current_player] in actions_dict:
        return actions_dict[player_value[current_player]].pop()
    # returns first actions if opponent can win
    elif player_value[opponent_dict[current_player]] in actions_dict:
        return actions_dict[player_value[opponent_dict[current_player]]].pop()
    # takes any other action
    else:
        return actions_dict[0].pop()
