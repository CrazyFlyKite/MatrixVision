from contextlib import redirect_stdout

with redirect_stdout(None):
	import pygame

from utilities import *


class MatrixRain:
	def __init__(self, *, font_size: int, fps: int) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode(PYGAME_RESOLUTION)
		pygame.display.set_caption('Matrix Rain')
		self.surface = pygame.Surface(PYGAME_RESOLUTION)
		self.clock = pygame.time.Clock()
		self.matrix = Matrix(self, font_size=font_size, fps=fps)

		self.font_size = font_size
		self.fps = fps

	def draw(self) -> None:
		self.surface.fill(BLACK)
		self.matrix.run()
		self.screen.blit(self.surface, (0, 0))

	def run(self) -> None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

			self.draw()
			pygame.display.flip()
			self.clock.tick(self.fps)


class Matrix:
	def __init__(self, matrix_rain: MatrixRain, /, *, font_size: int, fps: int) -> None:
		self.app = matrix_rain
		self.font_size = font_size
		self.fps = fps
		self.font = pygame.font.Font(MAIN_FONT, font_size)

		size: Tuple[int, int] = HEIGHT // font_size, WIDTH // font_size
		self.matrix = np.random.choice(KATAKANA, size)
		self.character_intervals = np.random.randint(25, 50, size=size)
		self.column_speed = np.random.randint(100, 250, size=size)
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
					(x * self.font_size, y * self.font_size)
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
