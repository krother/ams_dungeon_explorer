"""
the Dungeon Explorere game logic
"""
from pydantic import BaseModel

#
# define data model
#
class Wall(BaseModel):
    x: int
    y: int


class Coin(BaseModel):
    x: int
    y: int
    value: int = 10


class Player(BaseModel):
    x: int
    y: int
    health: int = 100
    coins: int = 0


class DungeonExplorer(BaseModel):
    player: Player
    walls: list[Wall]  # does not work for Python 3.8, not sure about 3.9
    coins: list[Coin]

    # we define our own functions inside this class
    # function inside a class have a special parameter 'self'.
    # we also may define a return type
    def is_running(self) -> bool:
        """True as long as the game is not finished"""
        ...

    def move_command(self, action: str) -> None:
        """handles player actions like 'left', 'right', 'jump', 'fireball'"""
        ...

    def get_objects(self) -> list[list[int, int, str]]:
        """
        returns everything inside the dungeon
        as a list of (x, y, object_type) items.
        """
        ...

    


dungeon_explorer = DungeonExplorer(
    player = Player(x=4, y=4),
    walls = [
        Wall(x=0, y=0),
        Wall(x=1, y=0),
        Wall(x=2, y=0),
        Wall(x=3, y=0),
        Wall(x=4, y=6),
    ],
    coins = [
        Coin(x=0, y=1, value=100),
        Coin(x=2, y=5),
    ]
)

# TODO: removed boundaries of the dungeon

def game_logic_temp():
    # remember old position
    old_x, old_y = player.x, player.y

    if key == 'd' and player.x < 9:
        player.x += 1
    elif key == 'a' and player.x > 0:
        player.x -= 1
    elif key == 'w' and player.y > 0:
        player.y -= 1
    elif key == 's':
        if player.y < 9:
            player.y += 1
        else:
            player.y = 0  # wrap-around move

    elif key == 'j':
        player.x += 2
    elif key == 'q':  # TODO: use ESCAPE instead
        exit_pressed = True

    # check for walls
    for wall in walls:
        if player.x == wall.x and player.y == wall.y:
            player.x, player.y = old_x, old_y

    # collect coin if there is any
    for coin in coins:
        if player.x == coin.x and player.y == coin.y:
            # we found a coin
            coins.remove(coin)   # remove the coin we found from the level
            player.coins += coin.value
            print("you now have", player.coins, "coins")
            break  # stop the loop because we modified coins
