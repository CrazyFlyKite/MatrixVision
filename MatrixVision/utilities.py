import re
from enum import Enum
from os import PathLike
from typing import List, Dict, Tuple, Final, Unpack, Any, TypeAlias

import numpy as np
from customtkinter import CTkEntry
from pygame import Surface

# Custom types
Color: TypeAlias = Tuple[int, int, int]
PrerenderedCharacters: TypeAlias = Dict[Tuple[str, Color], Surface]
PathLikeString: TypeAlias = str | PathLike

# Window
TITLE: Final[str] = 'Matrix Vision'
WIDTH, HEIGHT = 250, 240
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
WINDOW_RESIZABLE: Final[bool] = False

# Matrix Vision
PYGAME_RESOLUTION = PYGAME_WIDTH, PYGAME_HEIGHT = 960, 720
NUMBER_OF_SPACES: Final[int] = 20
KATAKANA: Final[np.ndarray] = np.array(
	[chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for _ in range(NUMBER_OF_SPACES)])

# Defaults
DEFAULT_FONT_SIZE: Final[int] = 15
DEFAULT_FPS: Final[int] = 30
MIN_FONT_SIZE, MAX_FONT_SIZE = 3, 200
MIN_FPS, MAX_FPS = 5, 240

# Info
INFO_MESSAGE: Final[str] = '''
Matrix Vision is a Python-based application that allows you to create
dynamic matrix-style visualizations inspired by the iconic \"The Matrix\" movie.
With Matrix Vision, you can open camera feeds, images, or generate simulated rain displays,
all with customizable parameters to create unique visual experiences.

The app is inspired by code from CoderSpace\'s YouTube channel.

Version: 1.0
Developer: CrazyFlyKite
Copyright ©, CrazyFlyKite, All Rights Reserved
'''

# Fonts
MAIN_FONT: Final[PathLikeString] = '../assets/fonts/MS Mincho.ttf'

# Colors
BLACK: Final[Color] = 0, 0, 0


# Display type
class DisplayType(Enum):
	CAMERA: Final[str] = 'camera'
	IMAGE: Final[str] = 'image'
	RAIN: Final[str] = 'rain'


SUPPORTED_EXTENSIONS: Final[List[str]] = ['png', 'jpg', 'jpeg', 'bmp', 'gif']


# Classes
class CTkNumberEntry(CTkEntry):
	def __init__(self, master: Any, **kwargs: Unpack[Dict[str, Any]]) -> None:
		super().__init__(master, **kwargs)
		self.configure(validate='key', validatecommand=(self.register(self.on_validate), '%P'))

	@staticmethod
	def on_validate(new_value: str) -> bool:
		return new_value == "" or re.match(r'^\d*$', new_value) is not None
