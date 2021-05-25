from OpenGL import GL as GL11, GLU;
class GameRenderGL:
	def prepare_world(main):
		GL11.glClearDepth(1)

		GL11.glViewport(0, 0, main.screen_width, main.screen_height);
		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();
	
		GLU.gluPerspective(main.fov, (main.screen_width / main.screen_height), 0.1, main.fog);
	
		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glLoadIdentity();

		GL11.glDisable(GL11.GL_CULL_FACE);
		GL11.glEnable(GL11.GL_DEPTH_TEST);
