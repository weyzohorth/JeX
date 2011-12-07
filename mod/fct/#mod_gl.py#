from mod.__init__ import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

def rotate_HV(angleH, angleV):
	glRotated(180, 0, 1, 0)
	glRotated(angleH, 0, 0, 1)
	glRotated(-90 + angleV, 0, 1, 0)

def load_texture(filename):
	glEnable(GL_TEXTURE_2D)
	surface = pygame.image.load(filename).convert(32, pygame.SRCALPHA)
	return surface_to_texture(surface)

def surface_to_texture(surface):
	surface = surface.convert(32, pygame.SRCALPHA)
	texture_id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture_id)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	pixels = pygame.image.tostring(surface, 'RGBA_PREMULT', True)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
	return texture_id
	
def draw_axes(coords=(0, 0, 0), echelle=100, largeur=5):
	glLineWidth(largeur)
	glBegin(GL_LINES)
	for i in range(3):
		glColor4f(bool(i==0), bool(i==1), bool(i==2), 1)
		glVertex(coords[0], coords[1], coords[2])
		glVertex(coords[0]+echelle*bool(i==0), coords[1]+echelle*bool(i==1), coords[2]+echelle*bool(i==2))
	glEnd()
	glColor3f(1.0, 1.0, 1.0)

def draw_rect(v1, v2, v3, v4):
	glBegin(GL_TRIANGLE_FAN)
	for v in v1, v2, v3, v4: glVertex3f(v[0], v[1], v[2])
	glEnd()

def draw_rect_col(v1, v2, v3, v4,
				c1=(255, 255, 255, 255), c2=(255, 255, 255, 255), c3=(255, 255, 255, 255), c4=(255, 255, 255, 255)):
	glBegin(GL_TRIANGLE_FAN)
	for v, c in zip((v1, v2, v3, v4), (c1, c2, c3, c4)): glColor4ub(c[0], c[1], c[2], c[3]); glVertex3f(v[0], v[1], v[2])
	glEnd()

def draw_rect_tex(v1, v2, v3, v4, texture, repetition=1):
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, texture)
	glBegin(GL_TRIANGLE_FAN)
	for v, t in zip((v1, v2, v3, v4), ((0, 0), (repetition, 0), (repetition, repetition), (0, repetition))):
		glTexCoord2f(t[0], t[1])
		glVertex3f(v[0], v[1], v[2])
	glEnd()
	glDisable(GL_TEXTURE_2D)

def draw_rect_tex_col(v1, v2, v3, v4, texture, repetition=1,
					c1=(255, 255, 255, 255), c2=(255, 255, 255, 255), c3=(255, 255, 255, 255), c4=(255, 255, 255, 255)):
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, texture)
	glBegin(GL_TRIANGLE_FAN)
	for v, t, c in zip((v1, v2, v3, v4), ((0, 0), (repetition, 0), (repetition, repetition), (0, repetition)), (c1, c2, c3, c4)):
		glColor4ub(c[0], c[1], c[2], c[3])
		glTexCoord2f(t[0], t[1])
		glVertex3f(v[0], v[1], v[2])
	glEnd()
	glDisable(GL_TEXTURE_2D)
	glColor3ub(255,255,255)

def draw_cube(x, y, z, c, aX=0, aY=0, aZ=0):
	v = []
	for X in [-c, c]:
		for Y in [-c, c]:
			for Z in [-c, c]:
				v.append((x+X, y+Y, z+Z))
	glPushMatrix()
	glRotated(aX, 1, 0, 0)
	glRotated(aY, 0, 1, 0)
	glRotated(aZ, 0, 0, 1)

	glColor3ub(255, 0, 0)
	draw_rect(v[0], v[1], v[3], v[2])
	draw_rect(v[4], v[5], v[7], v[6])
	liste = (0, 1, 3, 2)
	for i in range(4):
		glColor3ub(0, 255*bool(not i%2), 255*bool(i%2))
		draw_rect(v[liste[i]], v[liste[(i+1)%4]], v[liste[(i+1)%4]+4], v[liste[i]+4])
	glPopMatrix()
	glColor3ub(255, 255, 255)

def draw_pave(l, L, h, tex=None, couleur=(255, 255, 255, 255), coords=(0, 0, 0), angles=(0, 0, 0)):
	glTranslated(coords[0], coords[1], coords[2])
	glRotated(angles[0], 1, 0, 0)
	glRotated(angles[1], 0, 1, 0)
	glRotated(angles[2], 0, 0, 1)
	if tex and couleur:
		draw_rect_tex_col((0, 0, 0), (0, L, 0), (0, L, h), (0, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur, tex=tex)
		draw_rect_tex_col((0, 0, 0), (l, 0, 0), (l, 0, h), (0, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur, tex=tex)
		draw_rect_tex_col((0, L, 0), (l, L, 0), (l, L, h), (0, L, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur, tex=tex)
		draw_rect_tex_col((0, 0, 0), (0, L, 0), (l, L, 0), (l, 0, 0), c1=couleur, c2=couleur, c3=couleur, c4=couleur, tex=tex)
		draw_rect_tex_col((0, 0, h), (0, L, h), (l, L, h), (l, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur, tex=tex)
	elif tex and not couleur:
		draw_rect_tex((0, 0, 0), (0, L, 0), (0, L, h), (0, 0, h), tex=tex)
		draw_rect_tex((0, 0, 0), (l, 0, 0), (l, 0, h), (0, 0, h), tex=tex)
		draw_rect_tex((0, L, 0), (l, L, 0), (l, L, h), (0, L, h), tex=tex)
		draw_rect_tex((0, 0, 0), (0, L, 0), (l, L, 0), (l, 0, 0), tex=tex)
		draw_rect_tex((0, 0, h), (0, L, h), (l, L, h), (l, 0, h), tex=tex)
	elif couleur:
		draw_rect_col((0, 0, 0), (0, L, 0), (0, L, h), (0, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur)
		draw_rect_col((0, 0, 0), (l, 0, 0), (l, 0, h), (0, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur)
		draw_rect_col((0, L, 0), (l, L, 0), (l, L, h), (0, L, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur)
		draw_rect_col((0, 0, 0), (0, L, 0), (l, L, 0), (l, 0, 0), c1=couleur, c2=couleur, c3=couleur, c4=couleur)
		draw_rect_col((0, 0, h), (0, L, h), (l, L, h), (l, 0, h), c1=couleur, c2=couleur, c3=couleur, c4=couleur)
	else:
		draw_rect((0, 0, 0), (0, L, 0), (0, L, h), (0, 0, h))
		draw_rect((0, 0, 0), (l, 0, 0), (l, 0, h), (0, 0, h))
		draw_rect((0, L, 0), (l, L, 0), (l, L, h), (0, L, h))
		draw_rect((0, 0, 0), (0, L, 0), (l, L, 0), (l, 0, 0))
		draw_rect((0, 0, h), (0, L, h), (l, L, h), (l, 0, h))

def activ_2D(w, h):
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0, w, 0, h)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

def desactiv_2D():
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()

def init(w, h, n=1, f=1000, fovy=70, flags=0):
	pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF | flags, 0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(fovy, float(w)/h, n, f)

def aff_text(x, y, w, h, text, fontcolor=pygame.Color(0, 0, 0), fontname="data/fonts/lords3.ttf", fontsize=24):
	font = pygame.font.Font(fontname, fontsize)
	surface = font.render(text, True, fontcolor).convert(32, pygame.HWSURFACE | pygame.SRCALPHA)
	surface.set_colorkey(pygame.Color(0, 0, 0))
	tex = surface_to_texture(surface)
	temp = glGenLists(1)
	glNewList(temp, GL_COMPILE)
	glColor3ub(255, 255, 255)
	draw_rect_tex((x, y, 0), (x+w, y, 0), (x+w, y+h, 0), (x, y+h, 0), tex)
	glEndList()
	return (temp, tex)
