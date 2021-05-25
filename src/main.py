# Sim api.
from api import GameSetting, GameGui;

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
		self.window_title = "Usandable v1.0";

		# Inicia as coisas importantes, no init nem tudo tem coisa, mas posso usar futuramente.

		# Esse game settings e perfeito.
		self.game_settings = GameSetting(self);
		self.game_settings.init();

		# Meu crush esse game gui.
		self.game_gui = GameGui(self);
		self.game_gui.init();

		# Agora e mais bonito pra fazer as guis, em termos tecnicos,
		# do MinecraftEmPythonkjkjkjkkk nao era ruim, mas nao era flexivel.
		# Nessa versao ficou supreendentemente mais profissional e flexivel.
		self.game_gui.registry(gui.InitializingPosOpenGameGui());
		self.game_gui.open("InitializingPosOpenGame");

		self.refresh_display();
		self.refresh_title();

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

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_settings.on_save();
					self.running = False;

				if event.type == pygame.KEYDOWN:
					self.keyboard_event(event.key, flag.KEYDOWN);

				if event.type == pygame.KEYUP:
					self.keyboard_event(event.key, flag.KEYUP);

			self.keyboard(pygame.key.get_pressed());

			pygame.display.flip();

		if self.running is False:
			sys.exit();

	def keyboard_event(self, key, state):
		# Eu to processando assim agora vou ir dormindo.
		self.game_gui.process_key_event(key, state);

	def keyboard(self, keys):
		# kkkksim eu fiz isso tambem, vou colocar o mouse e um monte de coisas pra entidades.
		# boa noite.
		self.game_gui.process_key(keys);

if (__name__ == "__main__"):
	# bo a noit;l
	game = Main();
	game.run_tick();