from util import Vec, GameRenderGL, Math;

import pygame;

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
			del self.data[value_name];

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
			del self.data[value_name];

class GameSetting:
	def __init__(self, main):
		self.main = main;
		self.settings = [];

		# All settings.
		self.setting_fullscreen = Setting("fullscreen");
		self.setting_fov = Setting("fov");
		self.setting_in_game = Setting("ingame");

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
		self.setting_in_game.value("move-forward", pygame.K_w);
		self.setting_in_game.value("move-backward", pygame.K_s);
		self.setting_in_game.value("move-left", pygame.K_a);
		self.setting_in_game.value("move-right", pygame.K_d);
		self.setting_in_game.value("move-jump", pygame.K_SPACE);

		# Registry all settings.
		self.registry(self.setting_fullscreen);
		self.registry(self.setting_fov);
		self.registry(self.setting_in_game);

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

	def process_key(self, keys):
		if self.current_gui is not None:
			self.current_gui.on_key(keys);

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
		self.speed = 50000;
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

	def process_yaw(self, amount):
		self.yaw -= amount;

	def process_pitch(self, amount):
		self.pitch += amount;

	def update(self):
		GameRenderGL.identity();

		keys = pygame.key.get_pressed();
		rel  = pygame.mouse.get_rel();

		if self.focus:
			self.process_yaw((rel[0]) * self.speed_mouse_sensivity);
			self.process_pitch((rel[1]) * self.speed_mouse_sensivity);

		pygame.event.set_grab(self.focus)
		pygame.mouse.set_visible(self.focus is not True);

		if self.pitch >= 90:
			self.pitch = 90;

		if self.pitch <= -90:
			self.pitch = -90;

		GameRenderGL.rotate(self.pitch, 1, 0, 0)
		GameRenderGL.rotate(360 - self.yaw, 0, 1, 0);
		GameRenderGL.position(-self.position.x, -self.position.y, -self.position.z);