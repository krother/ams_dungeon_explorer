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


class Door(BaseModel):
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
    doors: list[Door] = []
    running: bool = True

    # we define our own functions inside this class
    # function inside a class have a special parameter 'self'.
    # we also may define a return type
    def is_running(self) -> bool:
        """True as long as the game is not finished"""
        return self.running

    def move_command(self, action: str) -> None:
        """handles player actions like 'left', 'right', 'jump', 'fireball'"""
        # remember old position
        old_x, old_y = self.player.x, self.player.y

        if action == 'right' and self.player.x < 9:
            self.player.x += 1
        elif action == 'left' and self.player.x > 0:
            self.player.x -= 1
        elif action == 'up' and self.player.y > 0:
            self.player.y -= 1
        elif action == 'down':
            if self.player.y < 9:
                self.player.y += 1
            else:
                self.player.y = 0  # wrap-around move

        elif action == 'jump':
            self.player.x += 2

        # check for doors
        for door in self.doors:
            if self.player.x == door.x and self.player.y == door.y:
                self.running = False  # found the exit

        # check for walls
        for wall in self.walls:
            if self.player.x == wall.x and self.player.y == wall.y:
                self.player.x, self.player.y = old_x, old_y

        # collect coin if there is any
        for coin in self.coins:
            if self.player.x == coin.x and self.player.y == coin.y:
                # we found a coin
                self.coins.remove(coin)   # remove the coin we found from the level
                self.player.coins += coin.value
                print("you now have", self.player.coins, "coins")
                break  # stop the loop because we modified coins

    def get_objects(self) -> list[list[int, int, str]]:
        """
        returns everything inside the dungeon
        as a list of (x, y, object_type) items.
        """
        result = []
        result.append([self.player.x, self.player.y, "player"])
        for w in self.walls:
            result.append([w.x, w.y, "wall"])
        for c in self.coins:
            result.append([c.x, c.y, "coin"])
        for d in self.doors:
            result.append([d.x, d.y, "open_door"])        
        return result

    

# define the level we will play
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
    ],
    doors = [
        Door(x=9, y=9),
    ]
)

# TODO: removed boundaries of the dungeon