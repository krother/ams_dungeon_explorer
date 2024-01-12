"""
Tests for the DungeonExplorer game

To execute the tests, do:

   pip install pytest

   pytest

"""
from game_logic import DungeonExplorer, Player, Wall, Coin, Door

def test_move():
    # three steps in every automated test:
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(x=4, y=4),
        walls = [],
        coins = [],
    )
    # 2. execute the code that we test
    d.move_command("right")
    obj = d.get_objects()
    # 3. check whether the result is what we expect (assertion)
    assert obj == [
        [5, 4, "player"]
    ]


def test_wall():
    """Player cannot move through a wall"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(x=4, y=4),
        walls = [Wall(x=5, y=4)],
        coins = [],
    )
    # 2. execute the code that we test
    d.move_command("right")
    obj = d.get_objects()
    # 3. check whether the result is what we expect (assertion)
    assert obj == [
        [4, 4, "player"],
        [5, 4, "wall"],
    ]


def test_coin():
    """Player can collect coins"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(x=4, y=4),
        walls = [],
        coins = [
            Coin(x=7, y=3, value=777),
        ],
    )
    # 2. execute the code that we test
    d.move_command("right")
    d.move_command("right")
    d.move_command("right")
    d.move_command("up")
    obj = d.get_objects()
    # 3. check whether the result is what we expect (assertion)
    assert d.player.coins == 777
    assert obj == [
        [7, 3, "player"],
    ]

def test_exit():
    """Player can walk through an open door"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(x=4, y=4),
        walls = [],
        coins = [],
        doors = [Door(x=3, y=4)]
    )
    # 2. execute the code that we test
    d.move_command("left")
    obj = d.get_objects()
    # 3. check whether the result is what we expect (assertion)
    assert d.is_running() == False
    assert obj == [
        [3, 4, "player"],
        [3, 4, "open_door"],
    ]
