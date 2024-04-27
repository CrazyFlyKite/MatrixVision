from tkinter.filedialog import askopenfile
from tkinter.messagebox import showwarning
from typing import Optional, IO

from customtkinter import CTk, CTkFont, CTkButton, CTkLabel, CTkFrame, IntVar, LEFT, CENTER

from matrix_rain import MatrixRain
from matrix_vision import MatrixVision
from utilities import *


class Main:
	def __init__(self) -> None:
		self.root = CTk()
		self.font_size_var = IntVar(value=DEFAULT_FONT_SIZE)
		self.fps_var = IntVar(value=DEFAULT_FPS)

	def setup_window(self) -> None:
		self.root.wm_title(WINDOW_TITLE)
		self.root.wm_geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
		self.root.wm_resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)
		self.root.eval('tk::PlaceWindow . center')

	def setup_ui(self) -> None:
		# Title font
		title_font: CTkFont = CTkFont(size=17, weight='bold')
		preferences_font: CTkFont = CTkFont(size=13, weight='bold')

		# Open
		CTkLabel(self.root, text='Open Matrix Vision', font=title_font).pack(pady=(2, 5))

		open_frame: CTkFrame = CTkFrame(self.root)
		open_frame.pack()

		CTkButton(open_frame, text='Camera', width=10, command=lambda: self.open(DisplayType.CAMERA)
		          ).pack(padx=3, side=LEFT)
		CTkButton(open_frame, text='Image', width=10, command=lambda: self.open(DisplayType.IMAGE)
		          ).pack(padx=3, side=LEFT)
		CTkButton(open_frame, text='Rain', width=10, command=lambda: self.open(DisplayType.RAIN)
		          ).pack(padx=3, side=LEFT)

		# Preferences
		CTkLabel(self.root, text='Preferences', font=title_font).pack(pady=5)

		# Font Size
		font_size_frame: CTkFrame = CTkFrame(self.root)
		font_size_frame.pack(pady=3)

		CTkLabel(font_size_frame, text='Font Size', font=preferences_font).pack(padx=5, side=LEFT)
		CTkNumberEntry(font_size_frame, width=50, justify=CENTER, textvariable=self.font_size_var
		               ).pack(padx=5, side=LEFT)

		# DEFAULT_FPS
		fps_frame: CTkFrame = CTkFrame(self.root)
		fps_frame.pack(pady=3)

		CTkLabel(fps_frame, text='FPS', font=preferences_font).pack(padx=5, side=LEFT)
		CTkNumberEntry(fps_frame, width=50, justify=CENTER, textvariable=self.fps_var).pack(padx=5, side=LEFT)

	def open(self, display_type: DisplayType) -> None:
		if MIN_FONT_SIZE < self.font_size_var.get() > MAX_FONT_SIZE:
			showwarning('Invalid Font Size', 'The font size must be in range from 3 to 200.')
			return

		if MIN_FPS < self.fps_var.get() > MAX_FPS:
			showwarning('Invalid FPS', 'The DEFAULT_FPS must be in range from 5 to 120.')
			return

		match display_type:
			case DisplayType.CAMERA:
				self.open_camera()
			case DisplayType.IMAGE:
				self.open_image()
			case DisplayType.RAIN:
				self.open_rain()

	def open_camera(self) -> None:
		MatrixVision(display_type=DisplayType.CAMERA, font_size=self.font_size_var.get(), fps=self.fps_var.get()).run()

	def open_image(self) -> None:
		image: Optional[IO] = askopenfile(
			filetypes=(
				('png files', ' '.join(f'*.{extension.lower()}' for extension in SUPPORTED_EXTENSIONS)),
				('all file', '*.*')
			)
		)

		if image is None:
			self.root.focus_force()
			return

		MatrixVision(display_type=DisplayType.IMAGE, font_size=self.font_size_var.get(), fps=self.fps_var.get(),
		             image=image.name).run()

	def open_rain(self) -> None:
		MatrixRain(font_size=self.font_size_var.get(), fps=self.fps_var.get()).run()

	def run(self) -> None:
		self.setup_window()
		self.setup_ui()
		self.root.mainloop()


if __name__ == '__main__':
	main: Main = Main()
	main.run()
