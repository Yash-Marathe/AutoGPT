import pprint


def column(matrix: list, i: int) -> list:
    """Return the i-th column of the given matrix."""
    return [row[i] for row in matrix]


def check(lst: list) -> int | None:
    """Check if all elements in the list are the same and not zero.

    Returns the common element if true, otherwise None.
    """
    if len(set(lst)) <= 1 and lst[0] != 0:
        return lst[0]
    return None


def check_diag(board: list, offset: int = 0) -> int | None:
    """Check if the diagonal elements in the given board are the same and not zero.

    The offset parameter is used to check both diagonals.

    Returns the common element if true, otherwise None.
    """
    if (
        board[0][0 + offset] == board[1][1 + offset]
        and board[1][1 + offset] == board[2][2 + offset]
    ):
        if board[0][0 + offset] != 0:
            return board[0][0 + offset]
    return None


def place_item(row: int, column: int, board: list, current_player: int) -> None:
    """Place the current player's item on the given board at the specified row and column.

    If the position is already occupied, does nothing.
    """
    if board[row][column] != 0:
        return
    board[row][column] = current_player


def swap_players(player: int) -> int:
    """Swap the given player with the other player."""
    if player == 2:
        return 1
    return 2


def winner(board: list) -> int | None:
    """Check if there is a winner on the given board.

    Returns the winning player if true, otherwise None.
    """
    for row in board:
        if check(row) is not None:
            return check(row)

    for column_index in range(len(board[0])):
        if check(column(board, column_index)) is not None:
            return check(column(board, column_index))

    if check_diag(board) is not None:
        return check_diag(board)

    if check_diag(board, offset=-1) is not None:
        return check_diag(board, offset=-1)

    return 0


def get_location() -> tuple[int, int]:
    """Get the location for the next move as a tuple of row and column."""
    while True:
        location = input(
            "Choose where to play. Enter two numbers separated by a comma, for example: 1,1 "
        )
        print(f"\nYou picked {location}")
        try:
            coordinates = tuple(int(x) for x in location.split(","))
            if len(coordinates) != 2 or any(c < 0 or c > 2 for c in coordinates):
                raise ValueError
        except ValueError:
            print("You inputted a location in an invalid format")
            continue
        return coordinates


def game_play() -> None:
    """Play the tic-tac-toe game."""
    num_moves = 0
    pp = pprint.PrettyPrinter(width=20)
    current_player = 1
    board = [[0 for _ in range(3)] for _ in range(3)]

    while num_moves < 9 and winner(board) == 0:
        print("This is the current board: ")
        pp.pprint(board)
        coordinates = get_location()
        place_item(coordinates[0], coordinates[1], board, current_player)
        current_player = swap_players(current_player)

