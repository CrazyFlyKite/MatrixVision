from contextlib import redirect_stdout
from typing import List

import cv2

with redirect_stdout(None):
	import pygame

from utilities import *


class MatrixVision:
	def __init__(self) -> None:
		# Pygame
		pygame.init()
		self.screen = pygame.display.set_mode(RESOLUTION)
		self.surface = Surface(RESOLUTION)
		self.clock = pygame.time.Clock()

		self.camera = cv2.VideoCapture(0)
		if not self.camera.isOpened():
			raise RuntimeError('Unable to open the camera')

		self.matrix = Matrix(self)

	def draw(self) -> None:
		self.surface.fill(BLACK)
		self.matrix.run()
		self.screen.blit(self.surface, (0, 0))

	def run(self) -> None:
		while True:
			[exit() for event in pygame.event.get() if event.type == pygame.QUIT]
			self.draw()
			pygame.display.flip()
			pygame.display.set_caption(f'{NAME} | FPS: {self.clock.get_fps():,.0f}')
			self.clock.tick(FPS)


class Matrix:
	def __init__(self, matrix_vision: MatrixVision) -> None:
		self.app = matrix_vision
		self.font = pygame.font.Font(MAIN_FONT, FONT_SIZE)

		self.matrix = np.random.choice(KATAKANA, SIZE)
		self.character_intervals = np.random.randint(25, 50, size=SIZE)
		self.column_speed = np.random.randint(100, 250, size=SIZE)
		self.prerendered_characters = self.get_prerendered_characters()

	def get_camera_frame(self) -> pygame.pixelarray.PixelArray:
		ret, frame = self.app.camera.read()

		if not ret:
			raise RuntimeError('Unable to capture frame from the camera')

		frame = cv2.flip(frame, 1)
		frame_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		return pygame.PixelArray(pygame.image.frombuffer(frame_rgb.flatten(), frame_rgb.shape[:2][::-1], 'RGB'))  # NOQA

	def get_image(self, path: PathLikeString) -> pygame.pixelarray.PixelArray:
		return pygame.pixelarray.PixelArray(pygame.transform.scale(pygame.image.load(path), RESOLUTION))

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
		match DISPLAY_TYPE:
			case DisplayType.CAMERA:
				image: pygame.pixelarray.PixelArray = self.get_camera_frame()
			case DISPLAY_TYPE.IMAGE:
				image: pygame.pixelarray.PixelArray = self.get_image(IMAGE_PATH)
			case _:
				raise NameError('Provided display type is unavailable')

		for y, row in enumerate(self.matrix):
			for x, character in enumerate(row):
				if character:
					position: Tuple[int, int] = x * FONT_SIZE, y * FONT_SIZE
					_, red, green, blue = pygame.Color(image[position])  # NOQA

					if red and green and blue:
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


if __name__ == '__main__':
	app: MatrixVision = MatrixVision()
	app.run()
