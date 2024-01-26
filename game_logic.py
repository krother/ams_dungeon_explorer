"""
the Dungeon Explorere game logic
"""
# REFACTOR: remove redundant classes
# REFACTOR: move all levels to extra module

# TODO: add stationary monster
# TODO: collect all coins to exit level and defeat all monsters
# TODO: create a few more levels
# TODO: add a bag for collecting coins
# TODO: show health bar
# TODO: show contents of bag
# REFACTOR: empty default arguments for DungeonExplorer

from pydantic import BaseModel

Level = [
    ".......$.#",
    ".##.#.#.##",
    ".#.....X.#",
    ".#..##.#.#",
    ".#.#...$.#",
    ".##.###..#",
    "......#.##",
    "..##..#..#",
    ".......$.#",
    "##########",
]


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

    def move_command(self, action: str) -> None:
        """handles player actions like 'left', 'right', 'jump', 'fireball'"""
        # remember old position
        old_x, old_y = self.player.x, self.player.y

        if action == "right" and self.player.x < 9:
            self.player.x += 1
        elif action == "left" and self.player.x > 0:
            self.player.x -= 1
        elif action == "up" and self.player.y > 0:
            self.player.y -= 1
        elif action == "down":
            if self.player.y < 9:
                self.player.y += 1
            else:
                self.player.y = 0  # wrap-around move

        elif action == "jump":
            self.player.x += 2

        # check for walls
        for wall in self.walls:
            if self.player.x == wall.x and self.player.y == wall.y:
                self.player.x, self.player.y = old_x, old_y

        # collect coin if there is any
        for coin in self.coins:
            if self.player.x == coin.x and self.player.y == coin.y:
                # we found a coin
                self.coins.remove(coin)  # remove the coin we found from the level
                self.player.coins += 10
                print("you now have", self.player.coins, "coins")
                break  # stop the loop because we modified coins

        # check for doors
        for door in self.doors:
            if self.player.x == door.x and self.player.y == door.y:
                self.event = "new level"
                start_level(dungeon=self, level=Level, start_position={"x": 0, "y": 0})

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
    player=Player(x=4, y=4),
    walls=[
       Position(x=0, y=0),
       Position(x=1, y=0),
       Position(x=2, y=0),
       Position(x=3, y=0),
       Position(x=4, y=6),
    ],
    coins=[
        Position(x=0, y=1),
        Position(x=2, y=5),
    ],
    doors=[
        Position(x=9, y=9),
    ],
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
