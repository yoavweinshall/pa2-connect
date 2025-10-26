from typing import Callable, Tuple, List, Set

from connectx.game import ConnectX

DIRECTIONS = ((1,0), (0,-1), (0,1), (-1,0), (1,1), (-1, 1), (1, -1), (-1,-1))

def compute_sequence(board: List[List[str]],
                     color: str,
                     start: Tuple[int, int],
                     direction: Tuple[int, int],
                     calculated_sequences: Set[Tuple[Tuple[int, int]]]
                     ) -> int:
        if (not (0 <= start[0] + 3 * direction[0] < len(board))) or (not (0 <= start[1] + 3 * direction[1] < len(board[0]))):
            return 0
        score = 0
        loc = list(start)
        this_seq = [start]
        for i in range(1,4):
            loc = [loc[0] + direction[0], loc[1] + direction[1]]
            if board[loc[0]][loc[1]] == color:
                score += 1
                this_seq.append((loc[0], loc[1]))
            elif board[loc[0]][loc[1]] is not None:
                return 0
        tuple_seq = tuple(this_seq)
        if tuple_seq in calculated_sequences:
            return 0
        calculated_sequences.add(tuple_seq)
        return score**score


def evaluate(g: ConnectX):
    board = g.board
    value = 0
    calculated_sequences = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'R':
                for direction in DIRECTIONS:
                    value += compute_sequence(board, board[row][col], (row, col), direction, calculated_sequences)
            elif board[row][col] == 'Y':
                for direction in DIRECTIONS:
                    value -= compute_sequence(board, board[row][col], (row, col), direction, calculated_sequences)
    return value



def minmax_min_component(game: ConnectX, depth: int, evaluator: Callable) -> Tuple[int, float]:
    """
    Calculate a min component of the minimax algorithm. The AI's move
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :return: The move that gives the lowest score and the score
    """
    best_value = float('inf')
    best_play = None
    for move in game.legal_actions():
        new_game = game.clone()
        new_game.play(move)
        if new_game.is_terminal() or depth == 1:
            return move, evaluator(new_game)
        else:
            play, value = minmax_max_component(new_game, depth - 1, evaluator)
        if value < best_value:
            best_play, best_value = move, value
    return best_play, best_value


def minmax_max_component(game: ConnectX, depth: int, evaluator: Callable) -> Tuple[int, float]:
    """
    Calculate a max component of the minimax algorithm. The Player's move
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :return: The move that gives the highest score and the score
    """
    best_value = -float('inf')
    best_play = None
    for move in game.legal_actions():
        new_game = game.clone()
        new_game.play(move)
        if new_game.is_terminal() or depth == 1:
            return move, evaluator(new_game)
        else:
            play, value = minmax_min_component(new_game, depth - 1, evaluator)
        if value > best_value:
            best_play, best_value = move, value
    return best_play, best_value


def minimax(game: ConnectX, depth: int, evaluator: Callable) -> int:
    """
    Calculate the best possible move using minimax algorithm.
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :return:number between 0 and 6 that represents an optimal move
    """
    best_play, best_value =  minmax_min_component(game, depth, evaluator)
    return best_play


def alpha_beta_min_component(
        game: ConnectX,
        depth: int,
        evaluator: Callable,
        alpha: float = -float('inf'),
        beta: float = float('inf'),
        ) -> Tuple[int, float]:
    """
    Calculate a min component of the minimax algorithm. The AI's move
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :param alpha: upper bound of the search space
    :param beta: lower bound of the search space
    :return: The move that gives the lowest score and the score
    """
    best_value = float('inf')
    best_play = None
    for move in game.legal_actions():
        new_game = game.clone()
        new_game.play(move)
        if new_game.is_terminal() or depth == 1:
            return move, evaluator(new_game)
        else:
            play, value = alpha_beta_max_component(new_game, depth - 1, evaluator, alpha, beta)
        if value < best_value:
            best_play, best_value = move, value
            beta = min(beta, best_value)
            if alpha > beta:
                return best_play, best_value
    return best_play, best_value


def alpha_beta_max_component(game: ConnectX, depth: int, evaluator: Callable,
                             alpha: float = -float('inf'), beta: float = float('inf')) -> Tuple[int, float]:
    """
    Calculate a max component of the minimax algorithm. The Player's move
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :param alpha: upper bound of the search space
    :param beta: lower bound of the search space
    :return: The move that gives the highest score and the score
    """
    best_value = -float('inf')
    best_play = None
    for move in game.legal_actions():
        new_game = game.clone()
        new_game.play(move)
        if new_game.is_terminal() or depth == 1:
            return move, evaluator(new_game)
        else:
            play, value = alpha_beta_min_component(new_game, depth - 1, evaluator, alpha, beta)
        if value > best_value:
            best_play, best_value = move, value
            alpha = max(alpha, best_value)
            if alpha > beta:
                return best_play, best_value
    return best_play, best_value


def alpha_beta_pruning(game: ConnectX, depth: int, evaluator: Callable) -> int:
    """
    Calculate the best possible move using alpha beta pruning algorithm.
    :param game: ConnectX game
    :param depth: how many moves further we're going to explore
    :param evaluator: heuristic function that estimates how good is a state
    :return:number between 0 and 6 that represents an optimal move
    """
    best_play, best_value =  alpha_beta_min_component(game, depth, evaluator)
    return best_play


def best_move(game: ConnectX, depth:int = 3, use_alpha_beta: bool = True, evaluator: Callable=evaluate) -> int:
    """
    Calculating the best move for our AI agent
    :param game: The connect game board
    :param depth: how many moves farther to explore
    :param use_alpha_beta: binary switch that determines whether to use alpha-beta (True) or minimax (False)
    :param evaluator:
    :return: where to place the best move
    """
    return alpha_beta_pruning(game.clone(), depth, evaluator) if use_alpha_beta else (
        minimax(game.clone(), depth, evaluator))
