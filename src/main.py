# Sim api.
from api import GameSetting, GameGui, Camera, Controller;
from util import GameRenderGL, FontRenderer;
from entity import EntityPlayer;
from world import World, Skybox;

# Esse flag e do propio jogo, ele e so umas coisas retardadas mesmo.
import pygame;
import flag;
import gui;
import sys;

# Balls?
pygame.init();

# Resolvi reescrever de madrugada, sao literalmente 02:07 da manha...
# Agora sim... eu vou fazer isso aqui pra ser algo insano, eu to pensando na real.
# e em fazer outro jogo, hihi... nao 3D e nem Minecraft.
class Main:
	def __init__(self):
		# Nigger.
		self.screen_width = 800;
		self.screen_height = 600;

		# Nao vou especificar a versao porque nao precisa ainda.
		self.window_title = "Unsandeable v1.0";

		# Inicia as coisas importantes, no init nem tudo tem coisa, mas posso usar futuramente.
		print("Initializing main stuffs.");

		# Esse game settings e perfeito.
		self.game_settings = GameSetting(self);
		self.game_settings.init();

		print("Game settings initialized.");

		self.refresh_display();
		self.refresh_title();

		print("Created window.");

		# Meu crush esse game gui.
		self.game_gui = GameGui(self);
		self.game_gui.init();

		print("All GUIs initialized.");

		# Camera.
		self.camera = Camera(self);
		self.camera.focus = True;

		print("OpenGL camera initialized.");

		# Player.
		self.player = EntityPlayer(888);
		self.player.init();

		print("Player ID " + str(self.player.id) + " client initialized.");

		# World.
		self.world = World(self);
		self.world.add(self.player);

		print("Dev world initialized.");

		# O skybox e iniciado aqui, porem... eu modifico no meio do jogo.
		self.skybox = Skybox("textures/skybox/");
		self.skybox.init();

		print("Render stuff initialized.");

		# Controller.
		self.controller = Controller(self, self.player, self.camera);

		print("Controller initialized.");

		# Agora e mais bonito pra fazer as guis, em termos tecnicos,
		# do MinecraftEmPythonkjkjkjkkk nao era ruim, mas nao era flexivel.
		# Nessa versao ficou supreendentemente mais profissional e flexivel.
		self.game_gui.registry(gui.InitializingPosOpenGameGui(self));
		self.game_gui.registry(gui.GamePaused(self));

		print("Unsandeable v1.0 started! :)!");

	def refresh_display(self):
		flags = pygame.OPENGL | pygame.DOUBLEBUF; 

		# Deveria usar uma lista? Talvez nao, ficaria com menos performance.
		# E nos estamos falando de Python e tambem de flexibilidade,
		# sempre vai ser mais facil especificar uma variavel do que algo em uma lista.
		# bjs vou ir dormir, ja sao 02:17.
		if self.game_settings != None and self.game_settings.setting_fullscreen.value("active"):
			flags |= pygame.FULLSCREEN;

			self.screen_width  = self.game_settings.setting_fullscreen.value("width");
			self.screen_height = self.game_settings.setting_fullscreen.value("height");

		# Tchau thau, se quer ler coisas, le isso por ultimo, dessa funcao tudo.
		self.display = pygame.display.set_mode((self.screen_width, self.screen_height), flags);

	def refresh_title(self):
		pygame.display.set_caption(self.window_title);

	def run_tick(self):
		self.running = True;

		self.fov = self.game_settings.setting_fov.value("amount");
		self.fog = 5000.0;

		self.mouse_position_x = 0;
		self.mouse_position_y = 0;

		self.keys = [];
		self.background = [190, 190, 190];

		self.fps = 60;
		self.partial_ticks = 1;

		self.clock = pygame.time.Clock();
		self.last_delta_time = 0;
		self.delta_time = 0;

		self.no_render_world = False;
		self.font_renderer = FontRenderer("Verdana", 19);

		# Abrimos a primeira gui do jogo.
		self.game_gui.open("InitializingPosOpenGame");

		GameRenderGL.setup(self);

		while self.running:
			self.update_partial_ticks();

			# Render part.

			GameRenderGL.clear(self);

			if self.no_render_world is False:
				self.do_world_render();

			GameRenderGL.push_matrix();
			GameRenderGL.overlay(self);

			self.do_overlay_render();

			GameRenderGL.world(self);
			GameRenderGL.pop_matrix();

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_settings.on_save();
					self.running = False;

				if event.type == pygame.MOUSEBUTTONDOWN:
					self.mouse_event(event.button, flag.KEYDOWN);

				if event.type == pygame.MOUSEBUTTONUP:
					self.mouse_event(event.button, flag.KEYUP);

				if event.type == pygame.KEYDOWN:
					self.keyboard_event(event.key, flag.KEYDOWN);

				if event.type == pygame.KEYUP:
					self.keyboard_event(event.key, flag.KEYUP);

			# Update part.
			# Quem literalmente e voce.
			self.keys = pygame.key.get_pressed();

			# MORRA, MORRA MORRA, NAO LIGO, MORRA.
			self.mouse_position_x = pygame.mouse.get_pos()[0];
			self.mouse_position_y = pygame.mouse.get_pos()[1];

			self.keyboard();
			self.update();

			pygame.display.flip();

		if self.running is False:
			print("Bye!");

			sys.exit();

	def update_partial_ticks(self):
		self.partial_ticks = self.clock.tick(self.fps) / 60;
		self.delta_time = self.partial_ticks - self.last_delta_time;
		self.last_delta_time = self.partial_ticks;

	def do_world_render(self):
		if self.world is not None:
			self.world.render(self.skybox);

	def do_overlay_render(self):
		self.game_gui.process_render(self.mouse_position_x, self.mouse_position_y, self.partial_ticks);

	def mouse_event(self, key, state):
		# Eu to processando assim agora vou ir dormir, isso e otro diakkkkk sao quase 3 horas da manha.
		# Meu Deus, eu preciso de um namorado.
		self.game_gui.process_mouse_event(self.mouse_position_x, self.mouse_position_y, key, state);

	def keyboard_event(self, key, state):
		# Eu to processando assim agora vou ir dormindo.
		self.game_gui.process_key_event(key, state);

		if self.world is not None:
			if self.game_gui.current_gui is None and key == pygame.K_ESCAPE:
				self.game_gui.open("GamePaused");

	def update(self):
		self.camera.update();

		self.camera.focus = self.game_gui.current_gui is None;
		self.camera.speed_mouse_sensivity = self.game_settings.setting_in_game.value("mouse-sensivity");

		if self.game_gui.current_gui is not None and self.game_gui.current_gui.active is False:
			self.game_gui.current_gui = None;

		if self.world is not None:
			self.world.update(self.skybox);
			self.controller.update();

	def keyboard(self):
		# kkkksim eu fiz isso tambem, vou colocar o mouse e um monte de coisas pra entidades.
		# boa noite.
		self.game_gui.process_key(self.keys);

		if self.world is not None and self.game_gui.current_gui is None:
			self.controller.keyboard(self.keys);

if (__name__ == "__main__"):
	# bo a noit;l
	game = Main();
	game.run_tick();