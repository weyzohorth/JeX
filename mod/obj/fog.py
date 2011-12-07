from mod.fct.mod_gl import *

class Fog:
	def __init__(__, index=2, mode=None, couleur=(255, 255, 255), alpha=128, density=0.5, start=50, end=100):
		if not mode in (GL_EXP, GL_EXP2, GL_LINEAR ): __.mode = (GL_EXP, GL_EXP2, GL_LINEAR )[index%3]
		else: __.mode = mode
		__.couleur = couleur
		__.alpha = alpha
		__.density = density
		__.start, __.end = start, end
		glEnable(GL_FOG)

	def draw(__):
		glFogi(GL_FOG_MODE, __.mode)
		glFogfv(GL_FOG_COLOR, (__.couleur[0]/255., __.couleur[1]/255., __.couleur[2]/255., __.alpha/255.))
		glFogf(GL_FOG_DENSITY, __.density)
		glHint(GL_FOG_HINT, GL_DONT_CARE)
		glFogf(GL_FOG_START, __.start)
		glFogf(GL_FOG_END, __.end)
