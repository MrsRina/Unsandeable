# Sim api.
from api import GameSetting, GameGui, Camera, Controller, log, TextureManager, OverlayManager;
from util import GameRenderGL, FontRenderer;
from entity import EntityPlayer;
from world import World, Skybox;
from pyglet.window import key;
from pyglet.gl import *

# Esse flag e do propio jogo, ele e so umas coisas retardadas mesmo.
import pyglet.gl as GL11;
import overlay;
import pyglet;
import flag;
import gui;
import sys;

print("Running now, Unsandeable dev version.");

# Resolvi reescrever de madrugada, sao literalmente 02:07 da manha...
# Agora sim... eu vou fazer isso aqui pra ser algo insano, eu to pensando na real.
# e em fazer outro jogo, hihi... nao 3D e nem Minecraft.
class Main(pyglet.window.Window):
	def __init__(self):
		# Nigger.
		self.screen_width = 800;
		self.screen_height = 600;

		# Nao vou especificar a versao porque nao precisa ainda.
		self.window_title = 'Unsandeable v1.0';

		# Inicia as coisas importantes, no init nem tudo tem coisa, mas posso usar futuramente.
		log("Initializing main stuffs.");

		# Esse game settings e perfeito.
		self.game_settings = GameSetting(self);
		self.game_settings.init();

		log("Game settings initialized.");

		self.refresh_display();
		self.set_fullscreen();

		log("Created window.");

		self.texture_manager = TextureManager(self);
		self.texture_manager.init();

		log("Textures initialized.");

		# Meu crush esse game gui.
		self.game_gui = GameGui(self);
		self.game_gui.init();

		log("All GUIs initialized.");

		# Camera.
		self.camera = Camera(self);
		self.camera.focus = True;

		log("OpenGL camera initialized.");

		# Player.
		self.player = EntityPlayer("Bolas");
		self.player.registry(888);
		self.player.init();

		log("Player ID " + str(self.player.id) + " client initialized.");

		# World.
		self.world = World(self);
		self.world.add_entity(self.player);

		log("Dev world initialized.");

		# O skybox e iniciado aqui, porem... eu modifico no meio do jogo.
		self.skybox = Skybox("textures/blocks/dirty/dirty_ISSUE");
		self.skybox.init();

		# The batch for render all and font for draw texts on game.
		self.batch = pyglet.graphics.Batch();
		self.font_renderer = FontRenderer(self, self.batch, "Arial", 19);

		log("Render stuff initialized.");

		# Controller.
		self.controller = Controller(self, self.player, self.camera);

		log("Controller initialized.");

		# As olverlays do jogo, aonde fica a vida etc.
		self.overlay_manager = OverlayManager(self);
		self.overlay_manager.init();

		log("Game overlay initialized.");

		# Agora e mais bonito pra fazer as guis, em termos tecnicos,
		# do MinecraftEmPythonkjkjkjkkk nao era ruim, mas nao era flexivel.
		# Nessa versao ficou supreendentemente mais profissional e flexivel.
		self.game_gui.registry(gui.InitializingPosOpenGameGui(self));
		self.game_gui.registry(gui.GamePaused(self));

		# Tambem registramos as overlays do jogo.
		self.overlay_manager.registry(overlay.Debug(self));

		print("Unsandeable v1.0 started! :)!");

	def refresh_display(self):
		self.window = pyglet.window.Window(width = self.screen_width, height = self.screen_height, caption = self.window_title, resizable = True);

	def set_fullscreen(self):
		if self.game_settings != None and self.game_settings.setting_fullscreen.value("active"):
			self.screen_width  = self.game_settings.setting_fullscreen.value("width");
			self.screen_height = self.game_settings.setting_fullscreen.value("height");

			self.window.set_fullscreen(True);
			self.window.set_width(self.screen_width);
			self.window.set_height(self.screen_height);

	def set_fps(self):
		pass

	def init(self):
		self.running = True;

		self.fov = self.game_settings.setting_fov.value("amount");
		self.fog = 5000.0;

		self.mouse_position_x = 0;
		self.mouse_position_y = 0;

		self.keys = [];
		self.background = [190, 190, 190];

		self.fps = 60;
		self.timer = 0.175;
		self.partial_ticks = 1;

		self.last_delta_time = 0;
		self.delta_time = 0;

		self.no_render_world = False;

		self.keys = key.KeyStateHandler();
		self.window.push_handlers(self.keys);

		self.rel = [0, 0];

		# Abrimos a primeira gui do jogo.
		self.game_gui.open("InitializingPosOpenGame");
		self.world.load_chunk_dirty(12, 0);

	def render(self):
		GameRenderGL.clear(self);
		GameRenderGL.world(self);

		self.camera.update();

		if self.no_render_world is False:
			self.do_world_render();

		GameRenderGL.overlay(self);

		self.do_overlay_render();

	def update_mouse(self, mx, my, dx, dy):
		# MORRA, MORRA MORRA, NAO LIGO, MORRA.
		self.mouse_position_x = mx, my;
		self.mouse_position_y = mx, my;

		self.rel = [dx, dy];
		self.camera.update_mouse();

	def update_partial_ticks(self):
		self.partial_ticks = self.clock.tick(self.fps) / 60;
		self.delta_time = self.partial_ticks - self.last_delta_time;
		self.last_delta_time = self.partial_ticks;

	def do_world_render(self):
		if self.world is not None:
			self.world.render(self.skybox);

	def do_overlay_render(self):
		self.game_gui.process_render(self.mouse_position_x, self.mouse_position_y, self.partial_ticks);

		if self.world is not None and self.game_gui.current_gui is None:
			self.overlay_manager.render();

		GL11.glPushMatrix();
		GL11.glEnable(GL11.GL_TEXTURE_2D);

		GL11.glEnable(GL11.GL_BLEND);
		GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);
		
		self.font_renderer.text.draw();

		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glDisable(GL11.GL_BLEND);
		GL11.glPopMatrix();

	def mouse_event(self, mx, my, key, state):
		# Eu to processando assim agora vou ir dormir, isso e otro diakkkkk sao quase 3 horas da manha.
		# Meu Deus, eu preciso de um namorado.
		self.game_gui.process_mouse_event(self.mouse_position_x, self.mouse_position_y, key, state);

	def keyboard(self, keys):
		if self.world is not None and self.game_gui.current_gui is None:
			self.controller.keyboard(self.keys);

	def keyboard_event(self, k, state):
		# Eu to processando assim agora vou ir dormindo.
		self.game_gui.process_key_event(k, state);

		if self.world is not None:
			if self.game_gui.current_gui is None and k == key.ESCAPE and state == flag.KEYUP:
				self.game_gui.open("GamePaused");

	def update(self, dt):
		self.keyboard(self.keys);

		# Eu nao sei trabalhar com esse sistema de dt do pyglet... eu fiz um timer pra isso.
		self.partial_ticks = dt + self.timer;

		# Update de camera pode ficar aqui, mas vou mudar no futuro.
		self.camera.focus = self.game_gui.current_gui is None;
		self.camera.speed_mouse_sensivity = self.game_settings.setting_in_game.value("mouse-sensivity");

		# Isso tambem vou mudar.
		self.window.set_exclusive_mouse(self.camera.focus);
		self.window.set_mouse_visible(self.camera.focus is not True);

		if self.game_gui.current_gui is not None and self.game_gui.current_gui.active is False:
			self.game_gui.current_gui = None;

		# Nao sei ainda como salvar um world, posso usar json pra isso, ah sei la.
		# Vamos fazer funcionar primeiro pra depois pensar em algo.
		if self.world is not None:
			self.world.update(self.skybox);
			self.controller.update();

# 	O CODIGO AQUI E BAIXO E HORRIVEL, EU TNEHO QUE QUSFAZER BONITO SE NAO EU PULO DA CAMA.
if (__name__ == "__main__"):
	# bo a noit;l
	game = Main();

	@game.window.event
	def on_close():
		game.running = False;

	@game.window.event
	def on_mouse_press(x, y, button, modifiers):
		game.mouse_event(x, y, button, flag.KEYDOWN);

	@game.window.event
	def on_mouse_release(x, y, button, modifiers):
		game.mouse_event(x, y, button, flag.KEYUP);

	@game.window.event
	def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
		pass

	@game.window.event
	def on_mouse_motion(x, y, dx, dy):
		game.update_mouse(x, y, dx, dy);

	@game.window.event
	def on_key_press(symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			return pyglet.event.EVENT_HANDLED

		game.keyboard_event(symbol, flag.KEYDOWN);

	@game.window.event
	def on_key_release(symbol, modifiers):
		game.keyboard_event(symbol, flag.KEYUP);

	@game.window.event
	def on_resize(width, height):
		game.screen_width = width;
		game.screen_height = height;

	@game.window.event
	def on_draw():
		game.render();

	game.init();

	pyglet.clock.schedule(game.update);

	GameRenderGL.setup(game);
	pyglet.app.run();