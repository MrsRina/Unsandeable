from api import Overlay;
from util import String;

import pyglet;

# Todos os HUDs do jogo, so para a gente renderizalos!
class Debug(Overlay):
	def __init__(self, main):
		super().__init__("Debug");

		self.main = main;
		self.font_renderer = self.main.font_renderer.instance();

	def draw(self, partial_ticks):
		text = ["All Chunks: " + String.len_to_string(self.main.world.loaded_chunk),
				"Update Chunks: " + String.len_to_string(self.main.world.chunk_update_list),
				String.vec_to_string(self.main.camera.position),
				"FPS: " + str(pyglet.clock.get_fps())];
		cache_position_y = 1;

		for texts in text:
			self.main.font_renderer.render(self.font_renderer, texts, 1, cache_position_y, (255, 255, 255, 255));

			cache_position_y += self.font_renderer.content_height;