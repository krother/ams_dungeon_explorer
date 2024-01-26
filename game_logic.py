"""
the Dungeon Explorere game logic
"""
# TODO: add stationary monster
# TODO: add fireball
# TODO: collect all coins to exit level and defeat all monsters
# TODO: add a bag for collecting coins
# TODO: show health bar
# TODO: show contents of bag
# REFACTOR: empty default arguments for DungeonExplorer

from pydantic import BaseModel
from levels import LEVELS

#
# define data model
#
class Position(BaseModel):
    x: int
    y: int


class Player(BaseModel):
    x: int
    y: int
    health: int = 100   # TODO: not used at the moment!!
    coins: int = 0


class DungeonExplorer(BaseModel):
    player: Player
    walls: list[Position]  # does not work for Python 3.8, not sure about 3.9
    coins: list[Position]
    doors: list[Position] = []
    event: str = ""
    level_number: int = 0


def move_command(dungeon, player, action: str) -> None:
    """handles player actions like 'left', 'right', 'jump', 'fireball'"""
    # remember old position
    old_x, old_y = player.x, player.y

    if action == "right" and player.x < 9:
        player.x += 1
    elif action == "left" and player.x > 0:
        player.x -= 1
    elif action == "up" and player.y > 0:
        player.y -= 1
    elif action == "down":
        if player.y < 9:
            player.y += 1
        else:
            player.y = 0  # wrap-around move

    elif action == "jump":
        player.x += 2

    # check for walls
    for wall in dungeon.walls:
        if player.x == wall.x and player.y == wall.y:
            player.x, player.y = old_x, old_y

    # collect coin if there is any
    for coin in dungeon.coins:
        if player.x == coin.x and player.y == coin.y:
            # we found a coin
            dungeon.coins.remove(coin)  # remove the coin we found from the level
            player.coins += 10
            print("you now have", player.coins, "coins")
            break  # stop the loop because we modified coins

    # check for doors
    for door in dungeon.doors:
        if player.x == door.x and player.y == door.y:
            dungeon.level_number += 1
            if dungeon.level_number == len(LEVELS):
                dungeon.event = "game over"
            else:
                dungeon.event = "new level"
                start_level(dungeon=dungeon,
                        level=LEVELS[dungeon.level_number],
                        start_position={"x": 0, "y": 0}
                        )


def get_objects(dungeon) -> list[list[int, int, str]]:
    """
    returns everything inside the dungeon
    as a list of (x, y, object_type) items.
    """
    result = []
    result.append([dungeon.player.x, dungeon.player.y, "player"])
    for w in dungeon.walls:
        result.append([w.x, w.y, "wall"])
    for c in dungeon.coins:
        result.append([c.x, c.y, "coin"])
    for d in dungeon.doors:
        result.append([d.x, d.y, "open_door"])
    return result


# define the level we will play
dungeon_explorer = DungeonExplorer(
    player=Player(x=4, y=4),
    walls=[],
    coins=[],
    doors=[],
)


def start_level(
    dungeon: DungeonExplorer, level: list[str], start_position: dict[str, int], **kwargs
) -> None:
    dungeon.player.x = start_position["x"]
    dungeon.player.y = start_position["y"]
    dungeon.walls = []
    dungeon.coins = []
    dungeon.doors = []
    for y, row in enumerate(level):  # y is a row number 0, 1, 2, ...
        for x, tile in enumerate(row):  # x is a column number 0, 1, 2, ...
            if tile == "#":
                wall = Position(x=x, y=y)
                dungeon.walls.append(wall)
            if tile == "X":
                door = Position(x=x, y=y)
                dungeon.doors.append(door)
            if tile == "$":
                coin = Position(x=x, y=y)
                dungeon.coins.append(coin)

start_level(dungeon_explorer, LEVELS[0], {"x" : 4, "y" : 4})