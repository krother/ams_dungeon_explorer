"""
the Dungeon Explorere game logic
"""
# TODO: left/right fireball moves

# any other monster
#   add a symbol to the level, to start_level and the dungeon data type

# TODO: collect all coins to exit level and defeat all monsters
# TODO: add a bag for collecting coins
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
    position: Position
    health: int = 100   # TODO: not used at the moment!!
    coins: int = 0
    last_direction: str = "up"

class Fireball(BaseModel):
    position: Position
    direction: str

class DungeonExplorer(BaseModel):
    player: Player
    walls: list[Position]  # does not work for Python 3.8, not sure about 3.9
    coins: list[Position]
    doors: list[Position] = []
    traps: list[Position] = []
    fireballs: list[Fireball]=[]

    event: str = ""
    level_number: int = 0


def move_command(dungeon, player, action: str) -> None:
    """handles player actions like 'left', 'right', 'jump', 'fireball'"""
    # remember old position
    old_position = player.position.model_copy()
    pos = player.position

    if action == "right" and pos.x < 9:
        pos.x += 1
        player.last_direction = action
    elif action == "left" and pos.x > 0:
        pos.x -= 1
        player.last_direction = action
    elif action == "up" and pos.y > 0:
        pos.y -= 1
        player.last_direction = action
    elif action == "down":
        player.last_direction = action
        if pos.y < 9:
            pos.y += 1
        else:
            pos.y = 0  # wrap-around move

    elif action == "jump":
        pos.x += 2
    elif action == "fireball":
        ball= Fireball(position=pos.copy(), direction=player.last_direction)
        dungeon.fireballs.append(ball)
    # check for walls
    for wall in dungeon.walls:
        if player.position == wall:
            player.position = old_position

    # collect coin if there is any
    for coin in dungeon.coins:
        if player.position == coin:
            # we found a coin
            dungeon.coins.remove(coin)  # remove the coin we found from the level
            player.coins += 10
            print("you now have", player.coins, "coins")
            break  # stop the loop because we modified coins

    # check for doors
    for door in dungeon.doors:
        if player.position == door:
            dungeon.level_number += 1
            if dungeon.level_number == len(LEVELS):
                dungeon.event = "game over"
            else:
                dungeon.event = "new level"
                start_level(dungeon=dungeon,
                        level=LEVELS[dungeon.level_number],
                        start_position=Position(x=0, y=0)
                        )
    # check for traps
    for trap in dungeon.traps:
        if player.position == trap:
            dungeon.event = "you died"


def get_objects(dungeon) -> list[list[int, int, str]]:
    """
    returns everything inside the dungeon
    as a list of (x, y, object_type) items.
    """
    result = []
    result.append([dungeon.player.position.x, dungeon.player.position.y, "player"])
    for w in dungeon.walls:
        result.append([w.x, w.y, "wall"])
    for c in dungeon.coins:
        result.append([c.x, c.y, "coin"])
    for d in dungeon.doors:
        result.append([d.x, d.y, "open_door"])
    for t in dungeon.traps:
        result.append([t.x, t.y, "trap"])
    for f in dungeon.fireballs:
        result.append([f.position.x, f.position.y, "fireball"])
    return result

def update(dungeon):
    new_balls = []
    for ball in dungeon.fireballs:
        if ball.direction == "up":
            ball.position.y -= 1
        elif ball.direction == "down":
            ball.position.y += 1
        active = True
        if (
            ball.position.y < 0 or
            ball.position.y > 9 or
            ball.position in dungeon.walls
        ):  # fireballs move until top border
            active = False
        for t in dungeon.traps:
            if ball.position == t:
                dungeon.traps.remove(t)
                active = False
        if active:
            new_balls.append(ball)  # keeps moving
    dungeon.fireballs = new_balls


    
# define the level we will play
dungeon_explorer = DungeonExplorer(
    player=Player(position=Position(x=4, y=4)),
    walls=[],
    coins=[],
    doors=[],
)


def start_level(
    dungeon: DungeonExplorer, level: list[str], start_position: Position, **kwargs
) -> None:
    dungeon.player.position = start_position
    dungeon.traps = []
    dungeon.walls = []
    dungeon.coins = []
    dungeon.doors = []
    for y, row in enumerate(level):  # y is a row number 0, 1, 2, ...
        for x, tile in enumerate(row):  # x is a column number 0, 1, 2, ...
            if tile == "T":
                traps = Position(x=x, y=y)
                dungeon.traps.append(traps)
            if tile == "#":
                wall = Position(x=x, y=y)
                dungeon.walls.append(wall)
            if tile == "X":
                door = Position(x=x, y=y)
                dungeon.doors.append(door)
            if tile == "$":
                coin = Position(x=x, y=y)
                dungeon.coins.append(coin)

start_level(dungeon_explorer, LEVELS[0], Position(x = 4, y = 4))
