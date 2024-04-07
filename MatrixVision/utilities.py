from enum import Enum
from os import PathLike
from typing import Dict, Tuple, Final

import numpy as np
from pygame import Surface

# Custom types
type Color = Tuple[int, int, int]
type PrerenderedCharacters = Dict[Tuple[str, Color], Surface]
type PathLikeString = str | bytes | PathLike

# Window
RESOLUTION = WIDTH, HEIGHT = 960, 720
NAME: Final[str] = 'Matrix Vision'
FPS: Final[int] = 30

# Graphics
NUMBER_OF_SPACES: Final[int] = 10
KATAKANA: Final[np.ndarray] = np.array(
	[chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for _ in range(NUMBER_OF_SPACES)])
FONT_SIZE: Final[int] = 10
SIZE = ROWS, COLUMNS = HEIGHT // FONT_SIZE, WIDTH // FONT_SIZE


# Display type
class DisplayType(Enum):
	IMAGE: str = 'image'
	CAMERA: str = 'camera'


DISPLAY_TYPE: Final[DisplayType] = DisplayType.CAMERA
IMAGE_PATH: Final[PathLikeString] = '../assets/images/image 1.jpg'

# Fonts
MAIN_FONT: Final[PathLikeString] = '../assets/fonts/MS Mincho.ttf'

# Colors
BLACK: Final[Color] = 0, 0, 0
