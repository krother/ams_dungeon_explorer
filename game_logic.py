"""
the Dungeon Explorere game logic
"""
# TODO: Dragon shooting fireballs
# TODO: get rid of key repeat  
# TODO: collect all coins to exit level and defeat all monsters
# TODO: add a bag for collecting coins
# TODO: show contents of bag

from textwrap import wrap
from pydantic import BaseModel
from levels import LEVELS
import random 

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

class Dragon(BaseModel):
    health: int = 5
    position: Position
    direction: str = "up"

class DungeonExplorer(BaseModel):
    player: Player
    walls: list[Position] = [] # does not work for Python 3.8, not sure about 3.9
    coins: list[Position] = []
    doors: list[Position] = []
    traps: list[Position] = []
    fireballs: list[Fireball] = []
    giants : list[Position] = []
    dragons : list[Dragon] = []

    event: str = ""
    level_number: int = 0




def get_next_position(position: Position, direction: str, occupied: list[Position], wraparound=False) -> Position:
    new = Position(x=position.x, y=position.y)
    if direction == "right" and new.x < 9:
        new.x += 1
    elif direction == "left" and new.x > 0:
        new.x -= 1
    elif direction == "up" and new.y > 0:
        new.y -= 1
    elif direction == "down":
        if new.y < 9:
            new.y += 1
        elif wraparound:
            new.y = 0  # wrap-around move
    if new in occupied:
        return position
    else:
        return new


def move_command(dungeon, player, action: str) -> None:
    """handles player actions like 'left', 'right', 'jump', 'fireball'"""
    # remember old position
    old_position = player.position.model_copy()
    pos = player.position

    if action in ["up", "down", "left", "right"]:
        new = get_next_position(player.position, action, dungeon.walls, wraparound=True)
        player.last_direction = action
        player.position = new

    elif action == "jump":
        pos.x += 2
    elif action == "fireball":
        ball = Fireball(position=pos.copy(), direction=player.last_direction)
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
    # check for giants
    for giant in dungeon.giants:
        if player.position == giant:
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
    for g in dungeon.giants:
        result.append([g.x, g.y, "giant"])
    for f in dungeon.fireballs:
        result.append([f.position.x, f.position.y, "fireball"])
    for d in dungeon.dragons:
        result.append([d.position.x, d.position.y, "dragon"])
    return result

def update(dungeon):
    new_balls = []
    for ball in dungeon.fireballs:
        # move the fireball
        new = get_next_position(ball.position, ball.direction, occupied=dungeon.walls)
        if new == ball.position:  # hit a wall
            active = False
        else:
            active = True
            ball.position = new
        # check for collision with traps
        for t in dungeon.traps:
            if ball.position == t:
                dungeon.traps.remove(t)
                active = False
         
         #check for collision with giants
        for g in dungeon.giants:
            if ball.position == g:
                dungeon.giants.remove(g)
                active = False  
         #check for collision with dragons
        for d in dungeon.dragons:
            if ball.position == d.position:
                d.health -= 1
                if d.health == 0:
                    dungeon.dragons.remove(d)
                active = False        
        if active:
            new_balls.append(ball)  # keeps moving
    dungeon.fireballs = new_balls
        
    
    for g in dungeon.giants:
        direction = random.choice(["up","down","left","right","wait","wait","wait","wait"])
        new = get_next_position(g, direction, occupied = dungeon.walls + dungeon.giants + dungeon.dragons)
        g.x = new.x 
        g.y = new.y
        if g == dungeon.player.position: 
            dungeon.event = "you died"

    for d in dungeon.dragons:
        direction = random.choice(["up","down","left","right"])
        new = get_next_position(d.position, direction, occupied = dungeon.walls + dungeon.giants + dungeon.dragons)
        d.position = new
        if d.position == dungeon.player.position: 
            dungeon.event = "you died"

# define the level we will play
dungeon_explorer = DungeonExplorer(
    player=Player(position=Position(x=4, y=4)),
)


def start_level(
    dungeon: DungeonExplorer, level: list[str], start_position: Position, **kwargs
) -> None:
    dungeon.player.position = start_position
    dungeon.traps = []
    dungeon.walls = []
    dungeon.coins = []
    dungeon.doors = []
    dungeon.fireballs = []
    dungeon.giants = []
    dungeon.dragons = []
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
            if tile == "G":
                giant = Position(x=x, y=y)
                dungeon.giants.append(giant)
            if tile == "D":
                dragon = Dragon(position = Position(x=x, y=y))
                dungeon.dragons.append(dragon)

start_level(dungeon_explorer, LEVELS[0], Position(x = 4, y = 4))
