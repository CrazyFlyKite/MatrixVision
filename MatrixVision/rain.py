from typing import List

import pygame

from utilities import *


class MatrixVision:
	def __init__(self) -> None:
		# Pygame
		pygame.init()
		self.screen = pygame.display.set_mode(RESOLUTION)
		self.surface = pygame.Surface(RESOLUTION)
		self.clock = pygame.time.Clock()
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
			pygame.display.set_caption(f'{NAME} | FPS: {self.clock.get_fps():.0f}')
			self.clock.tick(FPS)


class Matrix:
	def __init__(self, matrix_vision: MatrixVision) -> None:
		self.app = matrix_vision
		self.font = pygame.font.Font(MAIN_FONT, FONT_SIZE)

		self.matrix = np.random.choice(KATAKANA, SIZE)
		self.character_intervals = np.random.randint(25, 50, size=SIZE)
		self.column_speed = np.random.randint(100, 250, size=SIZE)
		self.prerendered_characters = self.get_prerendered_characters()

	def get_prerendered_characters(self) -> PrerenderedCharacters:
		character_colors: List[Color] = [(0, green, 0) for green in range(256)]
		prerendered_characters: PrerenderedCharacters = {}

		for character in KATAKANA:
			prerendered_character: Dict[Tuple[str, Color], pygame.Surface] = {
				(character, color): self.font.render(character, True, color) for color in character_colors
			}
			prerendered_characters.update(prerendered_character)

		return prerendered_characters

	def draw(self) -> None:
		for y, row in enumerate(self.matrix):
			for x, character in enumerate(row):
				self.app.surface.blit(
					self.prerendered_characters[(character, (0, 170, 0))],
					(x * FONT_SIZE, y * FONT_SIZE)
				)

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
