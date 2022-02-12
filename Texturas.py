from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL.Image import *
import numpy as np
# Estruturas para armazenar as texturas de uma cidade

# Constantes para indexar as texturas 
PISOS = {
    "CROSS":0,
    "DL":1,
    "DLR":2,
    "DR":3,
    "LR":4,
    "None":5,
    "UD":6,
    "UDL":7,
    "UDR":8,
    "UL":9,
    "ULR":10,
    "UR":11,
}

# Lista de nomes das texturas
nomeTexturas = [
    "CROSS.png",
    "DL.png",
    "DLR.png",
    "DR.png",
    "LR.png",
    "None.png",
    "UD.png",
    "UDL.png",
    "UDR.png",
    "UL.png",
    "ULR.png",
    "UR.png"]

# int idTexturaRua[LAST_IMG]  vetor com os identificadores das texturas


# **********************************************************************
# void CarregaTexturas()
# **********************************************************************
def CarregaTexturas():
    glEnable(GL_TEXTURE_2D)

    for k in PISOS.keys():
        image = open("TexturaAsfalto/" + nomeTexturas[PISOS[k]])

        ix = image.size[0]
        iy = image.size[1]
        image = image.convert("RGBX")
        image = np.array(image)
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, id)

        formato = GL_RGBA

        glTexImage2D(GL_TEXTURE_2D, 0, formato, ix, iy, 0, formato, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
