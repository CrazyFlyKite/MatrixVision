from contextlib import redirect_stdout
from typing import Optional

import cv2

with redirect_stdout(None):
	import pygame

from utilities import *


class MatrixVision:
	def __init__(self, *, display_type: DisplayType, font_size: int, fps: int,
	             image: Optional[PathLikeString] = None) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode(PYGAME_RESOLUTION)
		pygame.display.set_caption('Matrix Vision')
		self.surface = Surface(PYGAME_RESOLUTION)
		self.clock = pygame.time.Clock()
		self.camera = cv2.VideoCapture(0)

		if not self.camera.isOpened():
			raise RuntimeError('Unable to open the camera')

		self.matrix = Matrix(self, display_type=display_type, font_size=font_size, image=image)

		self.display_type = display_type
		self.fps = fps
		self.image = image

	def draw(self) -> None:
		self.surface.fill(BLACK)
		self.matrix.run()
		self.screen.blit(self.surface, (0, 0))

	def run(self) -> None:
		if self.display_type == DisplayType.IMAGE and self.image is None:
			raise TypeError('Please, provide the image path')

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

			self.draw()
			pygame.display.flip()
			self.clock.tick(self.fps)


class Matrix:
	def __init__(self, matrix_vision: MatrixVision, /, *, display_type: DisplayType, font_size: int,
	             image: Optional[PathLikeString] = None) -> None:
		self.app = matrix_vision
		self.font = pygame.font.Font(MAIN_FONT, font_size)

		size: Tuple[int, int] = HEIGHT // font_size, WIDTH // font_size
		self.matrix = np.random.choice(KATAKANA, size)
		self.character_intervals = np.random.randint(25, 50, size=size)
		self.column_speed = np.random.randint(100, 250, size=size)
		self.prerendered_characters = self.get_prerendered_characters()

		self.display_type = display_type
		self.font_size = font_size
		self.image = image

	def get_camera_frame(self) -> pygame.pixelarray.PixelArray:
		ret, frame = self.app.camera.read()

		if not ret:
			raise RuntimeError('Unable to capture frame from the camera')

		frame = cv2.flip(frame, 1)
		frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		return pygame.PixelArray(pygame.image.frombuffer(frame_rgb.flatten(), frame_rgb.shape[:2][::-1], 'RGB'))  # NOQA

	def get_image(self, image: PathLikeString) -> pygame.pixelarray.PixelArray:
		return pygame.pixelarray.PixelArray(pygame.transform.scale(pygame.image.load(image), PYGAME_RESOLUTION))

	def get_prerendered_characters(self) -> PrerenderedCharacters:
		character_colors: List[Color] = [(0, green, 0) for green in range(256)]
		prerendered_characters: PrerenderedCharacters = {}

		for character in KATAKANA:
			prerendered_character: Dict[Tuple[str, Color], Surface] = {
				(character, color): self.font.render(character, True, color) for color in character_colors
			}
			prerendered_characters.update(prerendered_character)

		return prerendered_characters

	def draw(self) -> None:
		match self.display_type:
			case DisplayType.CAMERA:
				image: pygame.pixelarray.PixelArray = self.get_camera_frame()
			case DisplayType.IMAGE:
				image: pygame.pixelarray.PixelArray = self.get_image(self.image)
			case _:
				raise NameError('Provided display type is unavailable')

		for y, row in enumerate(self.matrix):
			for x, character in enumerate(row):
				if character:
					position: Tuple[int, int] = x * self.font_size, y * self.font_size
					_, red, green, blue = pygame.Color(image[position])  # NOQA

					if all([red, green, blue]):
						color: int = (red + green + blue) // 3
						color = 220 if 160 < color < 220 else color
						rendered_character: Surface = self.prerendered_characters[(character, (0, color, 0))]
						rendered_character.set_alpha(color + 60)
						self.app.surface.blit(rendered_character, position)

	def shift_columns(self, frames: int) -> None:
		number_columns: np.ndarray = np.unique(np.argwhere(frames % self.column_speed == 0)[:, 1])
		self.matrix[:, number_columns] = np.roll(self.matrix[:, number_columns], shift=1, axis=0)

	def change_characters(self, frames: int) -> None:
		mask: np.ndarray = np.argwhere(frames % self.character_intervals == 0)
		self.matrix[mask[:, 0], mask[:, 1]] = np.random.choice(KATAKANA, mask.shape[0])

	def run(self) -> None:
		frames: int = pygame.time.get_ticks()

		self.change_characters(frames)
		self.shift_columns(frames)
		self.draw()
