from util import GameRenderGL, Vec, BatchHelper, Math;
from api import Face, Data, log;

import pyglet.gl as GL11;
import pyglet;
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

		self.w = 0.5;
		self.h = 0.5;
		self.l = 0.5;

		self.color = [0, 0, 0, 100];
		self.textures = {};
		self.groups = {};

		self.render = True;

	def init(self):
		self.flag.registry("type", "air");
		self.flag.registry("texture", "air");

	def set_type(self, type):
		if self.flag.get("type") != type:
			self.flag.set("type", type);

	def set_texture(self, texture):
		self.flag.set("texture", texture);

	def get_type(self):
		return self.flag.get("type");

	def get_texture(self):
		return self.flag.get("texture");

	def set_render(self):
		self.render = True;

	def unset_render(self):
		self.render = False;

	def refresh(self, texture_manager):
		if self.get_type() == "air":
			return;

		self.textures = {};
		self.groups = {};

		for faces in flag.FACES:
			data = texture_manager.get("block_" + self.get_type() + "_" + faces);

			texture = data[0];
			group = data[1];

			if texture is not None and group is not None:
				self.textures[faces] = texture;
				self.groups[faces] = group;

	def update(self, camera, chunk_update_distance):
		if Math.block_collide(self, camera.x, camera.y, camera.z) < chunk_update_distance:
			self.set_render();
		else:
			self.unset_render();

class Chunk:
	def __init__(self, world):
		self.world = world;
		self.position = Vec(0, 0, 0);
		self.extend = Vec(6, 6, 6);

		self.loaded_block = {};

	def add(self, block):
		if self.loaded_block.__contains__(block) is False:
			self.loaded_block[block] = block;

	def remove(self, block):
		if self.loaded_block.__contains__(block):
			self.loaded_block.pop(block);

class World:
	def __init__(self, main):
		self.main = main;

		self.loaded_chunk = {}; # Vou usar pra salvar todos os blocos do mundo.
		self.loaded_block = {}; # Todos os chunks do jogo...

		self.seed = 0;
		self.time = 0;

		self.batch = pyglet.graphics.Batch();
		self.group = pyglet.graphics.Group();

		self.batch_list = {};
		self.entity_list = {};
		self.chunk_update_list = {}; # O que fica na memoria ram!

	def load_chunk_dirty(self, r, l):
		length = int(r);
		y = int(l);

		chunk_size = 24;
		chunk = None;

		count_x = 0;
		count_z = 0;

		for x in range(-length, length):
			count_x += 1;

			for z in range(-length, length):
				count_z += 1;

				dirty = Block(x - 0.5, y, z - 0.5);
				dirty.init();
				dirty.set_type("dirty");
				dirty.refresh(self.main.texture_manager);
	
				self.add_block(dirty);

				if chunk is None or count_x >= chunk_size or count_z >= chunk_size:
					if count_x >= chunk_size:
						count_x = 0;

					if count_z >= chunk_size:
						count_z = 0;

					chunk = Chunk(self);

					chunk.position.x = x - 0.5;
					chunk.position.z = z - 0.5;

					chunk.extend.x = chunk_size;
					chunk.extend.y = chunk_size;
					chunk.extend.z = chunk_size;

					self.add_chunk(chunk);
					self.chunk_block(dirty, chunk, flag.ADD);

				self.change_block(dirty, "set_vertex");

	def add_block(self, block):
		self.loaded_block[(block.x, block.y, block.z)] = block;

	def add_chunk(self, chunk):
		self.loaded_chunk[chunk] = chunk;

	def chunk_block(self, block, chunk, mode):
		if mode is flag.ADD and chunk is not None and chunk.loaded_block.__contains__(block) is False:
			chunk.add(block);

		if mode is flag.REMOVE and chunk is not None and chunk.loaded_block.__contains__(block):
			chunk.remove(block);

	def change_block(self, block, action):
		if action is "unset_vertex" and self.batch_list.__contains__(block):
			BatchHelper.remove_cube(self.batch_list, block);

		if action is "set_vertex" and self.batch_list.__contains__(block) is False:
			self.batch_list[block] = BatchHelper.apply_cube(self.batch, block.groups, block.textures, block.x, block.y, block.z, block.w, block.h, block.l, (255, 255, 255, 255));

		if action is "destroy":
			self.loaded_block.pop(block);

	def refresh_chunk(self, chunk, action):
		if action is "remove" and self.chunk_update_list.__contains__(chunk):
			log("Detected removed chunk update!");

			for blocks in chunk.loaded_block:
				self.change_block(blocks, "unset_vertex");

			self.chunk_update_list.pop(chunk);

		if action is "add" and self.chunk_update_list.__contains__(chunk) is False:
			log("Detected added chunk update!");

			for blocks in chunk.loaded_block:
				self.change_block(blocks, "set_vertex");

			self.chunk_update_list[chunk] = chunk;

	def get_block(self, x, y, z):
		block = None;

		for blocks in self.loaded_chunk:
			if Math.block_collide(blocks, x, y, z):
				block = blocks;

				break;

		return block;

	def add_entity(self, entity):
		self.entity_list[entity.id] = entity;

	def remove_entity(self, id):
		if self.entity_list.__contains__(id):
			self.entity_list.pop(id);

	def get_entity(self, id):
		if self.entity_list.__contains__(id):
			return self.entity_list[id];

		return None;

	def render(self, skybox):
		skybox.render();
		self.batch.draw();

	def update(self, skybox):
		delta_time = self.main.partial_ticks;

		for ids in self.entity_list:
			self.entity_list[ids].update(delta_time);

		chunk_update_distance = self.main.game_settings.setting_render.value("chunk-distance");
		camera = self.main.camera.position;

		for (x, y, z) in self.loaded_block:
			blocks = self.loaded_block[(x, y, z)];

		for chunks in self.loaded_chunk:
			if Math.object_distance(chunks.position.x, chunks.position.y, chunks.position.z, chunks.extend.x, chunks.extend.y, chunks.extend.z, camera.x, camera.y, camera.z) > chunk_update_distance:
				self.refresh_chunk(chunks, "remove");
			else:
				self.refresh_chunk(chunks, "add");

				log("nigger");

		for chunks in self.chunk_update_list:
			for blocks in chunks.loaded_block:
				if blocks.get_type() is not blocks.get_texture():
					if blocks.get_type() is not "air":
						blocks.refresh(self.main.texture_manager);
						self.change_block(blocks, "set_vertex");
	
					blocks.set_texture(blocks.get_type());

		skybox.update();