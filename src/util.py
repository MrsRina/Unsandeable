from pyglet.gl import *;

import pyglet.gl as GL11;
import pyglet;
import math;

# Created by Rina, sim eu criei isso, na verdade, tudo que foi escrito nesse projeto e genuinamente meu.
class FontRenderer(object):
	def __init__(self, main, batch, font = None, size = None):
		self.path  = font;
		self.size  = size;
		self.font  = font;
		self.batch = batch;
		self.main  = main;

		self.cfont = None;

		try:
			self.cfont = pyglet.font.load(font, self.size);
		except:
			self.cfont = pyglet.font.load(self.path, self.size);

		self.text = None;

	def get_width(self, string):
		return pyglet.text.Label(string, font_name = self.font, font_size = self.size).content_width;

	def get_height(self, string):
		return pyglet.text.Label(string, font_name = self.font, font_size = self.size).content_height;

	def instance(self):
		return pyglet.text.Label("", font_name = self.font, font_size = self.size, batch = self.batch);

	def render(self, label, text, x, y, color):
		label.text = text;
		label.x = x;
		label.y = self.main.screen_height - y; # sei la e invertido aquik
		label.color = color;
		label.anchor_y = "bottom";
		label.draw();

class BatchHelper:
	def group_texture(surface):
		return surface;

	def remove_cube(batch_list, vertex_list):
		count = 0;

		for vertex in batch_list[vertex_list]:
			vertex.delete();

			count += 1;

		if count >= len(batch_list[vertex_list]):
			batch_list.pop(vertex_list);

	def apply_cube(batch, groups, textures, x, y, z, width, height, lenght, color):
		w, h, l = x + width, y + height, z + lenght;

		tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1));

		vertex_list = [
			#batch.add(4, GL_QUADS, groups["back"], ('v3f', (w, y, z,  x, y, z,  x, h, z,  w, h, z)), tex_coords), # back
			#batch.add(4, GL_QUADS, groups["front"], ('v3f', (x, y, l,  w, y, l,  w, h, l,  x, h, l)), tex_coords), # front
	
			#batch.add(4, GL_QUADS, groups["left"], ('v3f', (x, y, z,  x, y, l,  x, h, l,  x, h, z)), tex_coords),  # left
			#batch.add(4, GL_QUADS, groups["right"], ('v3f', (w, y, l,  w, y, z,  w, h, z,  w, h, l)), tex_coords),  # right
	
			#batch.add(4, GL_QUADS, groups["down"], ('v3f', (x, y, z,  w, y, z,  w, y, l,  x, y, l)), tex_coords),  # bottom
			batch.add(4, GL_QUADS, groups["up"], ('v3f', (x, h, l,  w, h, l,  w, h, z,  x, h, z)), tex_coords)  # top
		];

		return vertex_list;

class GameRenderGL:
	def position(x, y = None, z = None):
		if y is None and z is None:
			GL11.glTranslatef(x.x, x.y, x.z);
		else:
			GL11.glTranslatef(x, y, z);

	def rotate(angle, x, y, z):
		GL11.glRotatef(angle, x, y, z);

	def identity():
		GL11.glLoadIdentity();

	def push_matrix():
		GL11.glPushMatrix();

	def pop_matrix():
		GL11.glPopMatrix();

	def setup(main):
		GL11.glClearDepth(1);

		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MIN_FILTER, GL11.GL_NEAREST)
		GL11.glTexParameteri(GL11.GL_TEXTURE_2D, GL11.GL_TEXTURE_MAG_FILTER, GL11.GL_NEAREST)

		GL11.glEnable(GL11.GL_BLEND)
		GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA)

		GameRenderGL.world(main);

		GL11.glEnable(GL11.GL_CULL_FACE);
		GL11.glEnable(GL11.GL_DEPTH_TEST);

	def world(main):
		GL11.glViewport(0, 0, main.screen_width, main.screen_height);

		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();

		gluPerspective(main.fov, (main.screen_width / main.screen_height), 0.1, main.fog);
	
		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glLoadIdentity();

		GL11.glDisable(GL11.GL_CULL_FACE);
		GL11.glEnable(GL11.GL_DEPTH_TEST);

	def overlay(main):
		GL11.glDisable(GL11.GL_DEPTH_TEST);

		GL11.glViewport(0, 0, main.screen_width, main.screen_height);
		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();

		gluOrtho2D(0, main.screen_width, 0, main.screen_height);
	
		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glLoadIdentity();

	def clear(main):
		GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);
		GL11.glClearColor(float(main.background[0] / 255.0), float(main.background[1] / 255.0), float(main.background[2] / 255.0), 1.0);

class TimerStamp:
	def __init__(self):
		self.ms = -1;

	def reset(self):
		self.ms = pygame.time.get_ticks();

	def current_ms(self):
		return pygame.time.get_ticks() - self.ms;

	def is_passed(self, ms):
		return pygame.time.get_ticks() - self.ms >= ms;

	def count(self, ms_div):
		return (pygame.time.get_ticks() - self.ms) / ms_div;

class Vec:
	def __init__(self, x, y, z):
		self.x = x;
		self.y = y;
		self.z = z;

	def get_x(self):
		return self.x;

	def get_y(self):
		return self.y;

	def get_z(self):
		return self.z;

	def get(self):
		return [self.x, self.y, self.z];

	def length(self):
		return sqrt(self.x * self.x + self.y * self.y + self.z * self.z);

	def __add__(self, num):
		if type(num) is Vec:
			return Vec(self.x + num.x, self.y + num.y, self.z + num.z);

		return Vec(self.x + num, self.y + num, self.z + num);

	def __sub__(self, num):
		if type(num) is Vec:
			return Vec(self.x - num.x, self.y - num.y, self.z - num.z);

		return Vec(self.x - num, self.y - num, self.z - num);

	def __mul__(self, num):
		if type(num) is Vec:
			return Vec(self.x * num.x, self.y * num.y, self.z * num.z);

		return Vec(self.x * num, self.y * num, self.z * num);

	def __div__(self, num):
		return Vec(self.x / num, self.vec.y / num, self.z / num);

	def __neg__(self):
		return Vec(-self.x, -self.y, -self.z);

class Rect:
	def __init__(self, tag):
		self.x, self.y, self.w, self.h = 0, 0, 0, 0;

		self.tag = tag;

class AABB:
	def __init__(self):
		self.min = Vec(0, 0, 0);
		self.max = Vec(0, 0, 0);

	def get(self):
		return [self.min.get(), self.max.get()];

	def collide(self, aabb):
		return (self.min.x >= aabb.min.x and self.max.x <= aabb.max.x) and \
			   (self.min.y >= aabb.min.y and self.max.y <= aabb.max.y) and \
			   (self.min.z >= aabb.min.z and self.max.z <= aabb.max.z);

class String:
	def vec_to_string(vec):
		return String.position_to_string(vec.x, vec.y, vec.z);

	def position_to_string(x, y, z):
		return "x: " + str((x)) + " y: " + str((y)) + " z: " + str(int(z));

	def len_to_string(list):
		return str(len(list));

	def object_tagged_to_string(object):
		try:
			return object.tag;
		except:
			return "";

class Math:
	def move_x(angle):
		return math.sin(math.radians(angle));

	def move_z(angle):
		return math.cos(math.radians(angle));

	def clamp(value, minimum, maximum):
		return (value if value <= maximum else maximum) if value >= minimum else minimum;

	def interpolation_linear(last, value, ticks):
		return last + (value - last) * ticks;

	def block_collide(block, x, y, z):
		return x >= block.x and y >= block.y and z >= block.z and x <= block.x + block.w and y <= block.y + block.h and z <= block.z + block.l;

	def block_distance(block, x, y, z):
		diff_x = (block.x + block.w) - x;
		diff_y = (block.y + block.h) - y;
		diff_z = (block.z + block.l) - z;

		return math.sqrt(diff_x * diff_x + diff_y * diff_y + diff_z * diff_z);

	def object_distance(obj_x, obj_y, obj_z, obj_w, obj_h, obj_l, x, y, z):
		diff_x = (obj_x + obj_w / 2) - x;
		diff_y = (obj_y + obj_h) - y;
		diff_z = (obj_z + obj_l / 2) - z;

		return math.sqrt(diff_x * diff_x + diff_y * diff_y + diff_z * diff_z);