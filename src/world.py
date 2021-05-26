from util import GameRenderGL;
from api import Face;

from OpenGL import GL as GL11;

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
			file_path = os.path.join(os.path.abspath(path + sides));

			try:
				self.textures[sides] = GameRenderGL.convert_to_texture(pygame.image.load(file_path + ".png"));
			except:
				self.no_render = True;

		if self.no_render:
			return

		self.list = GL11.glGenLists(1);

		self.x = self.x - self.w / 2;
		self.y = self.y - self.h / 2;
		self.z = self.z - self.l / 2;

	def init(self):
		if self.no_render:
			return;

		GL11.glNewList(self.list, GL11.GL_COMPILE);
		GL11.glColor(1, 1, 1);

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["front"]);

		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["back"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0)
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["left"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["right"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["up"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["down"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glEndList();

	def update(self):
		if self.no_render:
			return;

	def render(self):
		if self.no_render:
			return;

		GL11.glPushMatrix();
		GL11.glColor(1, 1, 1);
		GL11.glCallList(self.list);
		GL11.glColor(1, 1, 1);
		GL11.glPopMatrix();

class World:
	def __init__(self, main):
		self.main = main;

		self.entity_list = [];
		self.loaded_chunk = [];
		self.seed = 0;
		self.time = 0;

	def add(self, entity):
		self.entity_list.append(entity);

	def remove_entity(self, id):
		entity = None;
		index = 0;

		for i in range(0, len(self.entity_list)):
			entities = self.entity_list[index];

			if entities.id == id:
				entity = entities;
				index = i;

				break;

		if entity is not None:
			del self.entity_list[index];

	def get(self, id):
		for entities in self.entity:
			if entities.id == id:
				return entities;

		return None;

	def render(self, skybox):
		skybox.render();

	def update(self, skybox):
		delta_time = self.main.delta_time;

		for entities in self.entity_list:
			entities.update(delta_time);

		skybox.update();