"""
graphics engine for 2D games
"""
import numpy as np
import cv2
from pydantic import BaseModel


#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64


def draw_dungeon(player, walls, coins, player_img, wall_img, coin_img):
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)

    # TODO: we should organize the image drawing in a smarter way
    # objects = [player] + walls + coins  # list concatenation

    # draw player
    xpos, ypos = player.x * TILE_SIZE, player.y * TILE_SIZE
    frame[ypos:ypos + TILE_SIZE, xpos:xpos + TILE_SIZE] = player_img

    # draw walls
    for wall in walls:
        xpos, ypos = wall.x * TILE_SIZE, wall.y * TILE_SIZE
        frame[ypos:ypos + TILE_SIZE, xpos:xpos + TILE_SIZE] = wall_img

    # draw coins
    for coin in coins:
        xpos, ypos = coin.x * TILE_SIZE, coin.y * TILE_SIZE
        frame[ypos:ypos + TILE_SIZE, xpos:xpos + TILE_SIZE] = coin_img

    cv2.imshow('Dungeon Explorer', frame)


# define a function that doubles image size
size2x = lambda a: np.kron(a, np.ones((2, 2, 1), dtype=a.dtype))

# load image and extract square tiles from it
wall_img = size2x(cv2.imread('tiles/wall.png'))
coin_img = size2x(cv2.imread('tiles/gold.png'))
player_img = size2x(cv2.imread('tiles/deep_elf_high_priest.png'))


exit_pressed = False
while not exit_pressed:

    draw_dungeon(player, walls, coins, player_img, wall_img, coin_img)

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)

    game_logic_temp(key)
    
cv2.destroyAllWindows()
