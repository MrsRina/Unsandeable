from api import Data;
from util import Math, Vec;

class Entity:
	def __init__(self):
		self.flag = Data("Entity");
		self.rendering = True;
		self.position = Vec(0, 0, 0);
		self.position_linear = Vec(0, 0, 0);
		self.velocity = Vec(0, 0, 0);
		self.id = 0;

	def init(self):
		pass;

	def registry(self, id):
		self.id = id;

class EntityPlayer(Entity):
	def __init__(self, name):
		super().__init__();

		self.name = name;
		self.request_respawn = True;

		self.forward = 0;
		self.strafe = 0;

		self.yaw = 0;
		self.pitch = 0;

		self.width = 0;
		self.height = 0;

	def init(self):
		self.flag.registry("living", self.boolean(True));
		self.flag.registry("spriting", self.boolean(False));
		self.flag.registry("health", self.health(200));
		self.flag.registry("flying", self.boolean(True));
		self.flag.registry("godmode", self.boolean(True));

	def do_jump(self):
		flying = self.flag.get("flying");

		if flying:
			self.position_linear.y += 0.2;

	def do_crouch(self):
		flying = self.flag.get("flying");

		if flying:
			self.position_linear.y -= 0.2;

	def boolean(self, value):
		return value;

	def health(self, value):
		return Math.clamp(value, 0, 200);

	def set(self, flag, value):
		self.flag.set(flag, value);

	def update(self, delta_time):
		health = self.flag.get("health");
		living = self.flag.get("living");
		godmode = self.flag.get("godmode");

		# Here we update position from linear interpolation.
		self.position.x = Math.interpolation_linear(self.position.x, self.position_linear.x, delta_time);
		self.position.y = Math.interpolation_linear(self.position.y, self.position_linear.y, delta_time);
		self.position.z = Math.interpolation_linear(self.position.z, self.position_linear.z, delta_time);

		if living is False and self.request_respawn:
			self.flag.set("health", self.health(100));
			self.flag.set("living", self.boolean(True));

			self.request_respawn = False;

		if godmode is not True:
			if health <= 0.0 and living:
				self.flag.set("living", self.boolean(False));

	def render(self):
		pass