from api import Gui;

import pygame;
import flag;

class InitializingPosOpenGameGui(Gui):
	def __init__(self, main):
		super().__init__("InitializingPosOpenGame");

		# Nao coloquei na classe gui ja que isso e bem liberal mesmo fds.
		self.main = main;

	def on_key_event(self, key, state):
		if key == pygame.K_r and state == flag.KEYUP:
			print("r in keyup!");

		if key == pygame.K_r and state == flag.KEYDOWN:
			print("r in keydown!");