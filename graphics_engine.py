"""
graphics engine for 2D games
"""
import numpy as np
import cv2
from game_logic import dungeon_explorer

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64

# define a function that doubles image size
size2x = lambda a: np.kron(a, np.ones((2, 2, 1), dtype=a.dtype))

# load image and extract square tiles from it
wall_img = size2x(cv2.imread('tiles/wall.png'))
coin_img = size2x(cv2.imread('tiles/gold.png'))
open_door_img = size2x(cv2.imread('tiles/open_door.png'))
player_img = size2x(cv2.imread('tiles/deep_elf_high_priest.png'))


def draw(obj):
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    for x, y, name in obj:
        # calculate screen positions
        xpos, ypos = x * TILE_SIZE, y * TILE_SIZE
        if name == "player":
            image = player_img
        elif name == "wall":
            image = wall_img
        elif name == "coin":
            image = coin_img
        elif name == "open_door":
            image = open_door_img

        frame[ypos:ypos + TILE_SIZE, xpos:xpos + TILE_SIZE] = image

    cv2.imshow('Dungeon Explorer', frame)



exit_pressed = False
while not exit_pressed and dungeon_explorer.is_running():

    # draw
    obj = dungeon_explorer.get_objects()
    draw(obj)

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == 'q':  # TODO: use ESCAPE instead
        exit_pressed = True
    if key == "a":
        dungeon_explorer.move_command("left")
    if key == "d":
        dungeon_explorer.move_command("right")
    if key == "w":
        dungeon_explorer.move_command("up")
    if key == "s":
        dungeon_explorer.move_command("down")
    if key == "j":
        dungeon_explorer.move_command("jump")

cv2.destroyAllWindows()
