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
		self.setting_fullscreen = Setting("fullscreen");
		self.settings = [];

	def init(self):
		self.setting_fullscreen.value("active", False);
		self.setting_fullscreen.value("width", 1280);
		self.setting_fullscreen.value("height", 720);

		# Registry first setting balls!
		self.registry(self.setting_fullscreen);

	def registry(self, setting):
		self.settings.append(setting);

	def on_save(self):
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

	def on_mouse_down(self, mx, my, button):
		pass

	def on_mouse_up(self, mx, my, button):
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

	def process_mouse_down(self, mx, my, button):
		if self.current_gui is not None:
			self.current_gui.on_mouse_down(mx, my, keys);

	def process_mouse_up(self, mx, my, button):
		if self.current_gui is not None:
			self.current_gui.on_mouse_down(mx, my, keys);

	def proces_render(self, mx, my, partial_ticks):
		if self.current_gui is not None:
			self.current_gui.on_render(mx, my, partial_ticks);
