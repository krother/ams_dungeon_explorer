"""
graphics engine for 2D games
"""
import numpy as np
import cv2
from game_logic import dungeon_explorer, get_objects, move_command
from cutscene import cutscene


# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "j": "jump",
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = 640, 640
TILE_SIZE = 64


def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    assert img is not None
    img = np.kron(img, np.ones((2, 2, 1), dtype=img.dtype))  # double image size
    return img


IMAGES = {
    "player": read_image("tiles/deep_elf_high_priest.png"),
    "wall": read_image("tiles/wall.png"),
    "coin": read_image("tiles/gold.png"),
    "open_door": read_image("tiles/open_door.png"),
}


def draw(obj):
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
    for x, y, name in obj:
        # calculate screen positions
        xpos, ypos = x * TILE_SIZE, y * TILE_SIZE
        image = IMAGES[name]
        frame[ypos : ypos + TILE_SIZE, xpos : xpos + TILE_SIZE] = image
    cv2.imshow("Dungeon Explorer", frame)


exit_game = False
while not exit_game:
    # draw
    obj = get_objects(dungeon_explorer)
    draw(obj)

    # handle keyboard input
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":  # TODO: use ESCAPE instead
        exit_game = True
    if key in MOVES:
        move_command(dungeon_explorer, dungeon_explorer.player, MOVES[key])
    if dungeon_explorer.event == "new level":
        dungeon_explorer.event = ""  # delete the event
        cutscene(
            text="Congratulations Warrior, you just completed the level. Now the real challenge starts.",
            songfile="song18.mp3",
            imagefile="title.png",
        )
        cutscene(
            text="Welcome To The New Level ",
            wait=5,
            songfile="song18.mp3",
            imagefile="title.png",
        )
    elif dungeon_explorer.event == "game over":
        cutscene(
            text="Congratulations! You finished all levels.",
            wait=5,
            songfile="song18.mp3",
            imagefile="title.png",
        )
        exit_game = True


cv2.destroyAllWindows()
