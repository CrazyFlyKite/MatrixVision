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
WINDOW_TITLE: Final[str] = 'Matrix Vision Lobby'
WINDOW_WIDTH, WINDOW_HEIGHT = 250, 200
WINDOW_RESIZABLE: Final[bool] = False

# Matrix Vision
PYGAME_RESOLUTION = WIDTH, HEIGHT = 960, 720

# Defaults
DEFAULT_FONT_SIZE: Final[int] = 15
DEFAULT_FPS: Final[int] = 30
MIN_FONT_SIZE, MAX_FONT_SIZE = 3, 200
MIN_FPS, MAX_FPS = 5, 120

# Graphics
NUMBER_OF_SPACES: Final[int] = 20
KATAKANA: Final[np.ndarray] = np.array(
	[chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for _ in range(NUMBER_OF_SPACES)])


# Display type
class DisplayType(Enum):
	IMAGE: str = 'image'
	CAMERA: str = 'camera'
	RAIN: str = 'rain'


SUPPORTED_EXTENSIONS: Final[List[str]] = ['png', 'jpg', 'jpeg', 'bmp', 'gif']

# Fonts
MAIN_FONT: Final[PathLikeString] = '../assets/fonts/MS Mincho.ttf'

# Colors
BLACK: Final[Color] = 0, 0, 0


# Classes
class CTkNumberEntry(CTkEntry):
	def __init__(self, master: Any, **kwargs: Unpack[Dict[str, Any]]) -> None:
		super().__init__(master, **kwargs)
		self.configure(validate='key', validatecommand=(self.register(self.on_validate), '%P'))

	@staticmethod
	def on_validate(new_value: str) -> bool:
		return re.match(r'^\d*$', new_value) is not None
