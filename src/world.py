from util import GameRenderGL, Vec;
from api import Face, Data, log;

import pyglet.gl as GL11;
import pyglet;
import pygame;
import flag;
import os;

class Skybox:
	x = 0;
	y = 0;
	z = 0;

	w = 4096;
	h = 4096;
	l = 4096;

	def __init__(self, path):
		self.textures = {};
		self.no_render = False;

		for sides in flag.FACES:
			pass

		if self.no_render:
			return

		self.x = self.x - self.w / 2;
		self.y = self.y - self.h / 2;
		self.z = self.z - self.l / 2;

	def init(self):
		if self.no_render:
			return;

	def update(self):
		if self.no_render:
			return;

	def render(self):
		if self.no_render:
			return;

class Block:
	def __init__(self, x, y, z):
		self.flag = Data("Block");

		self.x = x;
		self.y = y;
		self.z = z;

		self.w = 1;
		self.h = 1;
		self.l = 1;

		self.color = [0, 0, 0, 100];
		self.textures = {};

	def init(self):
		self.flag.registry("type", "air");

	def set_type(self, type):
		loaded = True;

		for i in range(0, len(flag.FACES)):
			sides = flag.FACES[i];

			pass

	def get_type(self):
		return self.flag.get("type");

	def update(self):
		pass

	def render(self, batch):
		if self.get_type() == "air":
			GameRenderGL.render_block(batch, self.x, self.y, self.z, self.w, self.h, self.l, self.color);

			return;

class World:
	def __init__(self, main):
		self.main = main;

		self.entity_list = {};
		self.loaded_chunk = {};
		self.loaded_block = {};
		self.seed = 0;
		self.time = 0;

		self.batch = pyglet.graphics.Batch();

	def load_chunk_dirty(self, length, y):
		for x in range(-length, length):
			for z in range(-length, length):
				dirty = Block(x, y, z);

				dirty.init();
				dirty.set_type("dirty");

				GameRenderGL.render_block(self.batch, x, y, z, 1, 1, 1, 1);

				self.loaded_block[(z, y, z)] = dirty;
				self.loaded_chunk[dirty] = [x, y, z];

	def add(self, entity):
		self.entity_list[entity.id] = entity;

	def remove_entity(self, id):
		if self.entity_list.__contains__(id):
			del self.entity_list[id];

	def get_entity(self, id):
		if self.entity_list.__contains__(id):
			return self.entity_list[id];

		return None;

	def get_block(self, x, y, z):
		if (self.loaded_block.__contains__((x, y, z))):
			return self.loaded_block[(x, y, z)];

	def render(self, skybox):
		skybox.render();
		self.batch.draw();

	def update(self, skybox):
		delta_time = self.main.partial_ticks;

		for ids in self.entity_list:
			self.entity_list[ids].update(delta_time);

		for block_positions in self.loaded_block:
			self.loaded_block[block_positions].update();

		skybox.update();
