"""
A Tic-Tac-Toe checker with a test
"""
TRIPLES = [('O', 'O', 'O'), ('X', 'X', 'X')]

COMBINATIONS = [
    #y1 x1 y2 x2 y3 x3
    [0, 0, 1, 1, 2, 2],  # first diagonal
    [2, 0, 1, 1, 0, 2],  # second diagonal
    [0, 0, 0, 1, 0, 2],  # first row
    [1, 0, 1, 1, 1, 2],  # second row
    [2, 0, 2, 1, 2, 2],  # third row
    [0, 0, 1, 0, 2, 0],  # first column
    [0, 1, 1, 1, 2, 1],  # second column
    [0, 2, 1, 2, 2, 2],  # third column
]

def check(field) -> str:
    for y1, x1, y2, x2, y3, x3 in COMBINATIONS:  # every row of COMBINATIONS gets distributed to 6 variables
        if (field[y1][x1], field[y2][x2], field[y3][x3]) in TRIPLES:
            return field[y1][x1] + " won"
    return "draw"


def test_check():
    field =  [
        ['X', 'O', 'X'],
        ['.', 'X', 'O'],
        ['X', 'O', 'O']
    ]
    assert check(field) == str('X won')


def test_check2():
    field =  [
        ['O', 'O', 'X'],
        ['.', 'O', 'O'],
        ['X', 'O', 'O']
    ]
    assert check(field) == str('O won')


def test_draw():
    field = [
        ['X', 'O', 'O'],
        ['.', 'X', 'X'],
        ['X', 'O', 'O']
    ]
    assert check(field) == str('draw')


def test_draw2():
    field = [
        ['.', 'O', '.'],
        ['.', '.', '.'],
        ['X', '.', '.']
    ]
    assert check(field) == str('draw')
