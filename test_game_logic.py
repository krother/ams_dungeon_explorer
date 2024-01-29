"""
Tests for the DungeonExplorer game

To execute the tests, do:

   pip install pytest

   pytest

"""
from game_logic import DungeonExplorer, Player, Position, start_level, get_objects, move_command


def test_move():
    # three steps in every automated test:
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(position=Position(x=4, y=4)),
        walls=[],
        coins=[],
    )
    # 2. execute the code that we test
    move_command(d, d.player, "right")
    obj = get_objects(d)
    # 3. check whether the result is what we expect (assertion)
    assert obj == [[5, 4, "player"]]


def test_wall():
    """Player cannot move through a wall"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(position=Position(x=4, y=4)),
        walls=[Position(x=5, y=4)],
        coins=[],
    )
    # 2. execute the code that we test
    move_command(d, d.player, "right")
    obj = get_objects(d)
    # 3. check whether the result is what we expect (assertion)
    assert obj == [
        [4, 4, "player"],
        [5, 4, "wall"],
    ]


def test_coin():
    """Player can collect coins"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(position=Position(x=4, y=4)),
        walls=[],
        coins=[
            Position(x=7, y=3),
        ],
    )
    # 2. execute the code that we test
    move_command(d, d.player, "right")
    move_command(d, d.player, "right")
    move_command(d, d.player, "right")
    move_command(d, d.player, "up")
    obj = get_objects(d)
    # 3. check whether the result is what we expect (assertion)
    assert d.player.coins == 10
    assert obj == [
        [7, 3, "player"],
    ]


def test_exit():
    """Player can walk through an open door"""
    # 1. create data for testing (fixture)
    d = DungeonExplorer(
        player=Player(position=Position(x=4, y=4)), walls=[], coins=[], doors=[Position(x=3, y=4)]
    )
    # 2. execute the code that we test
    move_command(d, d.player, "left")
    obj = get_objects(d)
    # 3. check whether the result is what we expect (assertion)
    assert d.event == "new level"
    assert [0, 0, "player"] in obj


def test_start_level():
    d = DungeonExplorer(
        player=Player(position=Position(x=4, y=4)), walls=[], coins=[], doors=[]
    )  # add necessary parameters but they can be empty
    level = [
        "########",
        "#.#....#",
        "#.#.##.#",
        "#.#..#.#",
        "#.##.#.#",
        "#....#x#",
        "########",
    ]
    start_level(d, level=level, start_position=Position(x=1, y=1))
    assert [1, 1, "player"] in get_objects(d)  # change if your interface is different
    assert [4, 2, "wall"] in get_objects(d)  # an example wall
