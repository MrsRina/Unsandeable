from api import Gui;
from util import Math;

import pyglet;
import world;
import flag;

class GamePaused(Gui):
	def __init__(self, main):
		super().__init__("GamePaused");

		self.main = main;
		self.font_renderer = self.main.font_renderer.instance();

	def on_mouse_event(self, mx, my, button, state):
		self.do_close();

	def on_render(self, mx, my, partial_ticks):
		text = "Your game was paused!";

		x = (self.main.screen_width / 2) - (self.font_renderer.content_width / 2);
		y = (self.main.screen_height / 2) + (self.main.screen_height / 3);

		self.main.font_renderer.render(self.font_renderer, text, x, y, (255, 255, 255, 255 // 2));

class InitializingPosOpenGameGui(Gui):
	def __init__(self, main):
		super().__init__("InitializingPosOpenGame");

		# Nao coloquei na classe gui ja que isso e bem liberal mesmo fds.
		self.main = main;
		self.alpha = 255 // 2;
		self.start_close = False;
		self.font_renderer = self.main.font_renderer.instance();

	def process_game_join(self):
		self.main.world = world.load(self.main, "Eu Sou Trans e Linda", 24);

		self.start_close = True;

	def on_key_event(self, key, state):
		if key == pyglet.window.key.SPACE:
			self.process_game_join();

	def on_close(self):
		self.main.background = [190, 190, 190];
		self.main.no_render_world = False;

	def on_open(self):
		self.start_close = False;
		self.main.no_render_world = True;

	def on_render(self, mx, my, partial_ticks):
		text = "Press SPACE to continue!";

		x = (self.main.screen_width / 2) - (self.font_renderer.content_width / 2);
		y = (self.main.screen_height / 2) + (self.main.screen_height / 3);

		self.main.font_renderer.render(self.font_renderer, text, x, y, (255, 255, 255, self.alpha));

		if self.start_close:
			self.alpha = int(Math.interpolation_linear(self.alpha, 0, partial_ticks));

			if (self.alpha <= 1):
				self.do_close();