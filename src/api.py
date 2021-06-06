from util import Vec, GameRenderGL, Math;
from pyglet.window import key;

import pyglet;
import math;

# Shows problem on game, infos or warings using log system.
def log(type, txt = None):
	if txt is None:
		txt = type;
		type = "Main";

	print("[" + type + "] " + txt);

class TextureManager:
	def __init__(self, main):
		self.textures = {};
		self.groups = {};

		self.main = main;

	def init(self):
		self.load("block_dirty_up", "textures/blocks/dirty/dirty_up.png");
		self.load("block_dirty_down", "textures/blocks/dirty/dirty_down.png");
		self.load("block_dirty_back", "textures/blocks/dirty/dirty_sides.png");
		self.load("block_dirty_front", "textures/blocks/dirty/dirty_sides.png");
		self.load("block_dirty_left", "textures/blocks/dirty/dirty_sides.png");
		self.load("block_dirty_right", "textures/blocks/dirty/dirty_sides.png");

		self.load("skybox_up", "NOT_DONE");

	def load(self, tag, path):
		texture_data = None;

		try:
			texture_data = pyglet.image.load(path);
		except Exception as exc:
			log("TextureManager", "Exception on load texture: " + str(exc));

			return;

		self.textures[tag] = texture_data;
		self.groups[tag] = pyglet.graphics.TextureGroup(texture_data.get_texture());

	def get(self, tag):
		texture = None;
		group = None;

		if self.textures.__contains__(tag) and self.groups.__contains__(tag):
			texture = self.textures[tag];
			group = self.groups[tag];

		return [texture, group];

class Data:
	def __init__(self, context):
		self.context = context;
		self.data = {};

	def registry(self, name, value):
		self.data[name] = value;

	def set(self, name, value):
		if self.data.__contains__(name):
			self.data[name] = value;

	def get(self, name):
		if self.data.__contains__(name):
			return self.data[name];

	def remove(self, value_name):
		if self.data.__contains__(value_name):
			self.data.pop(value_name);

class Setting:
	def __init__(self, name):
		self.name = name;
		self.data = {};

	def value(self, value_name, value = None):
		if value is not None:
			self.data[value_name] = value;
		else:
			if self.data.__contains__(value_name):
				return self.data[value_name];

	def remove(self, value_name):
		if self.data.__contains__(value_name):
			self.data.pop(value_name);

class GameSetting:
	def __init__(self, main):
		self.main = main;
		self.settings = [];

		# All settings.
		self.setting_fullscreen = Setting("fullscreen");
		self.setting_fov = Setting("fov");
		self.setting_in_game = Setting("ingame");
		self.setting_render = Setting("render");

	def init(self):
		# Basic fullscreen stuff setting.
		self.setting_fullscreen.value("active", False);
		self.setting_fullscreen.value("width", 1280);
		self.setting_fullscreen.value("height", 720);

		# The fov handler setting.
		self.setting_fov.value("amount", 90);

		# In game settings.
		self.setting_in_game.value("mouse-sensivity", 0.1);

		# Movement stuffs.
		self.setting_in_game.value("move-forward", key.W);
		self.setting_in_game.value("move-backward", key.S);
		self.setting_in_game.value("move-left", key.A);
		self.setting_in_game.value("move-right", key.D);
		self.setting_in_game.value("move-jump", key.SPACE);
		self.setting_in_game.value("move-crouch", key.LSHIFT);

		# Render settings.
		self.setting_render.value("chunk-distance", 12);

		# Registry all settings.
		self.registry(self.setting_fullscreen);
		self.registry(self.setting_fov);
		self.registry(self.setting_in_game);
		self.registry(self.setting_render);

	def registry(self, setting):
		self.settings.append(setting);

	def on_save(self):
		pass

	def on_load(self):
		pass

class Gui:
	def __init__(self, tag):
		self.tag = tag;
		self.active = False;

	def do_close(self):
		if self.active:
			self.on_close();
			self.active = False;

	def do_open(self):
		if self.active is not True:
			self.on_open();
			self.active = True;

	def on_close(self):
		pass

	def on_open(self):
		pass

	def on_key_event(self, key, state):
		pass

	def on_key(self, keys):
		pass

	def on_mouse_event(self, mx, my, button, state):
		pass

	def on_render(self, mx, my, partial_ticks):
		pass

class GameGui:
	def __init__(self, main):
		self.main = main;
		self.guis = [];

		self.current_gui = None;

	def init(self):
		self.current_gui = None;

	def registry(self, gui):
		self.guis.append(gui);

	def get(self, gui_tag):
		for gui in self.guis:
			if gui.tag == gui_tag:
				return gui;

		return None;

	def open(self, gui_tag):
		gui = self.get(gui_tag);

		if gui is not None:
			if self.current_gui is not None:
				self.current_gui.do_close();

			self.current_gui = gui;
			self.current_gui.do_open();		

	def process_key_event(self, key, state):
		if self.current_gui is not None:
			self.current_gui.on_key_event(key, state);

	def process_mouse_event(self, mx, my, button, state):
		if self.current_gui is not None:
			self.current_gui.on_mouse_event(mx, my, button, state);

	def process_render(self, mx, my, partial_ticks):
		if self.current_gui is not None:
			self.current_gui.on_render(mx, my, partial_ticks);

class Controller:
	def __init__(self, main, entity, camera):
		self.main = main;
		self.entity = entity;
		self.speed = 1000;
		self.camera = camera;

	def keyboard(self, keys):
		if keys[self.main.game_settings.setting_in_game.value("move-forward")]:
			self.entity.position_linear.x -= Math.moveX(self.camera.yaw) * ((self.speed / 1000) * 0.1);
			self.entity.position_linear.z -= Math.moveZ(self.camera.yaw) * ((self.speed / 1000) * 0.1);

		if keys[self.main.game_settings.setting_in_game.value("move-backward")]:
			self.entity.position_linear.x += Math.moveX(self.camera.yaw) * ((self.speed / 1000) * 0.1);
			self.entity.position_linear.z += Math.moveZ(self.camera.yaw) * ((self.speed / 1000) * 0.1);

		if keys[self.main.game_settings.setting_in_game.value("move-left")]:
			self.entity.position_linear.x += Math.moveX(self.camera.yaw - 90) * ((self.speed / 1000) * 0.1);
			self.entity.position_linear.z += Math.moveZ(self.camera.yaw - 90) * ((self.speed / 1000) * 0.1);

		if keys[self.main.game_settings.setting_in_game.value("move-right")]:
			self.entity.position_linear.x -= Math.moveX(self.camera.yaw - 90) * ((self.speed / 1000) * 0.1);
			self.entity.position_linear.z -= Math.moveZ(self.camera.yaw - 90) * ((self.speed / 1000) * 0.1);

		if keys[self.main.game_settings.setting_in_game.value("move-jump")]:
			self.entity.do_jump();

		if keys[self.main.game_settings.setting_in_game.value("move-crouch")]:
			self.entity.do_crouch();

	def update(self):
		self.camera.position.x = self.entity.position.x;
		self.camera.position.y = self.entity.position.y + self.entity.height;
		self.camera.position.z = self.entity.position.z;

		self.entity.yaw = self.camera.yaw;
		self.entity.pitch = self.camera.pitch;

class Face:
	def __init__(self, name):
		self.name = name;
		self.face = util.Vec(0, 0, 0);

class Camera:
	def __init__(self, main):
		self.main = main;
		self.speed_mouse_sensivity = 0;
		self.focus = False;

		self.yaw = 0;
		self.pitch = 0;

		self.position = Vec(0, 0, 0);

	def update(self):
		GameRenderGL.identity();
		GameRenderGL.rotate(self.pitch, 1, 0, 0)
		GameRenderGL.rotate(360 - self.yaw, 0, 1, 0);
		GameRenderGL.position(-self.position.x, -self.position.y, -self.position.z);

	def update_mouse(self):
		if self.focus:
			self.yaw -= (self.main.rel[0]) * self.speed_mouse_sensivity;
			self.pitch += -(self.main.rel[1]) * self.speed_mouse_sensivity;

		if self.pitch >= 90:
			self.pitch = 90;

		if self.pitch <= -90:
			self.pitch = -90;