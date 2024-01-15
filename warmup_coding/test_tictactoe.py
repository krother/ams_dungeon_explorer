"""
A Tic-Tac-Toe checker with a test
"""

def check(field) -> str:
    if field[2][0] == field[1][1] == field[0][2] == 'O':
        return "O won"
    elif field[2][0] == field[1][1] == field[0][2] == 'X':
        return "X won"
    elif field[0][0]== field[1][1] == field[2][2] == 'O':
        return "O won"
    elif field[0][0]== field[1][1] == field[2][2] == 'X':
        return "X won"
    elif field[1][0] == field[1][1] == field[1][2] == 'O':
        return "O won"
    elif field[1][0] == field[1][1] == field[1][2] == 'X':
        return "X won"
    else:
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
