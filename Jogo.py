# # **********************************************************************
# # PUCRS/Escola Polit�cnica
# # COMPUTA��O GR�FICA
# #
# # Simulador de Cidade
# #
# # Guilherme Hiago Costa dos Santos
# # guilherme.hiago@pucrs.br
# # **********************************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

#include "Temporizador.h"
from Temporizador import *
T = Temporizador()
AccumDeltaT=0.0

#include "Ponto.h"
#include "ListaDeCoresRGB.h"
from Ponto import*
from ListaDeCoresRGB import *
import Texturas
#GLfloat AspectRatio
AspectRatio = 1
angulo=0

# # Controle do modo de projecao
# # 0: Projecao Paralela Ortografica 1: Projecao Perspectiva
# # A funcao "PosicUser" utiliza esta variavel. O valor dela eh alterado
# # pela tecla 'p'
global ModoDeProjecao
ModoDeProjecao = 1

# Controle do modo de projecao
# 0: Wireframe 1: Faces preenchidas
# A funcao "Init" utiliza esta variavel. O valor dela eh alterado
# pela tecla 'w'
global ModoDeExibicao
ModoDeExibicao = 1

global nFrames, TempoTotal
nFrames=0
TempoTotal=0


# Qtd de ladrilhos do piso. Inicialzada na INIT
QtdX = 30
QtdZ = 30

# Representa o conteudo de uma celula do piso
class Elemento:
    tipo = 1
    cor = 1
    altura = 0.0

# codigos que definem o o tipo do elemento que est� em uma c�lula
VAZIO = 0
PREDIO = 10
RUA = 20
COMBUSTIVEL = 30

# Matriz que armazena informacoes sobre o que existe na cidade
#Elemento Cidade[100][100]
global Cidade, pisoJogador, posJogador, posObserv, alvoCam, alvoJogador, acelera, rotCamera
Cidade = []
pisoJogador = (0,0)
posJogador = Ponto(0, 0, 0)
alvoJogador = Ponto(0, 0, 1)
rotJogador = 0
acelera = False
combJogador = 5

# variaveis camera
thirdPerson = True
POS_THIRDPERSON = Ponto(5,7,8)
posObserv = POS_THIRDPERSON
alvoCam = Ponto()
rotCamera = Ponto()

# variaveis avioes
posAvioes = [Ponto(0,2,1), Ponto(1, -4, 1), Ponto(1, -4, 1)]
alvosAvioes = [Ponto(), Ponto(), Ponto()]
rotAvioes = [90, 45, 45]

curvasAvioes = [[Ponto(0,10,1), Ponto(7,10,10), Ponto(29,10,20)], 
                [Ponto(0,10,29), Ponto(7,10,10), Ponto(15,10,5)], 
                [Ponto(29,10,29), Ponto(8,10,9), Ponto(19,10,19)]]
tempAvioes = [0, 0, 0]
tempTotaisAvioes = [5, 5, 5]

# variaveis disparos
MAX_DISPAROS = 3
disparos = 0
posDisparos = [Ponto(1, -4, 1), Ponto(1, -4, 1), Ponto(1, -4, 1)]

# ***********************************************
#  calcula_ponto(Ponto p, Ponto &out)
#
#  Esta fun��o calcula as coordenadas
#  de um ponto no sistema de refer�ncia do
#  universo (SRU), ou seja, aplica as rota��es,
#  escalas e transla��es a um ponto no sistema
#  de refer�ncia do objeto SRO.
#  Para maiores detalhes, veja a p�gina
#  https://www.inf.pucrs.br/pinho/CG/Aulas/OpenGL/Interseccao/ExerciciosDeInterseccao.html
# ***********************************************
def CalculaPonto(p):
    out = Ponto()
    ponto_novo = [0,0,0,0]
    # matriz_gl = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    i = 0

    matriz_gl = glGetFloatv(GL_MODELVIEW_MATRIX)

    for i in range(4):
        ponto_novo[i] = matriz_gl[0][i] * p.x + matriz_gl[1][i] * p.y + matriz_gl[2][i] * p.z + matriz_gl[3][i]

    out.x = ponto_novo[0]
    out.y = ponto_novo[1]
    out.z = ponto_novo[2]

    return out

# **********************************************************************
#
# **********************************************************************
def InicializaCidade( QtdX,  QtdZ):
    for i in range(QtdZ):
        Cidade.append([])
        for j in range(QtdX):
            Cidade[i].append(Elemento())

    # print(Cidade)

    arq = open("mapa.txt")

    tempZ = 0
    for l in arq:
        valores = l.split(" ")
        tempX = 0
        # rua(-2), uma quadra(-1), um prédio com sua altura(>0), ou posição inicial do jogador(0)

        for e in valores:
            if int(e) == 0:
                global pisoJogador, posJogador, alvoCam, alvoJogador
                pisoJogador = (tempZ, tempX)
                posJogador = Ponto(tempX, 0.5, tempZ)
                alvoJogador = Ponto(0, 0, 1)
                alvoCam = Ponto(tempX, 0, tempZ)
                # pos do jogador deve ser piso
                Cidade[tempZ][tempX].tipo = RUA
                Cidade[tempZ][tempX].cor = Gray
            elif int(e) == -2:
                Cidade[tempZ][tempX].tipo = RUA
                Cidade[tempZ][tempX].cor = Gray
            elif int(e) == -3:
                Cidade[tempZ][tempX].tipo = COMBUSTIVEL
                Cidade[tempZ][tempX].cor = OrangeRed
            elif int(e) > 0:
                Cidade[tempZ][tempX].tipo = PREDIO
                Cidade[tempZ][tempX].altura = int(e)
                
                a = [DarkOliveGreen,DarkOrchid,DarkSlateBlue,DarkSlateGray,DarkSlateGrey,DarkTurquoise]
                Cidade[tempZ][tempX].cor = a[random.randrange(0, len(a))]
            else:
                Cidade[tempZ][tempX].tipo = VAZIO
                Cidade[tempZ][tempX].cor = Red
            tempX += 1
        tempZ += 1
    
    arq.close()


# **********************************************************************
#  void init(void)
#    Inicializa os parametros globais de OpenGL
# **********************************************************************
def init():
    glClearColor(0.0, 0.0, 1.0, 1.0) # Fundo de tela preto
   
    glShadeModel(GL_SMOOTH)
    #glShadeModel(GL_FLAT)
    glColorMaterial ( GL_FRONT, GL_AMBIENT_AND_DIFFUSE )
    if (ModoDeExibicao): # Faces Preenchidas??
        glEnable(GL_DEPTH_TEST)
        glEnable (GL_CULL_FACE )
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glEnable(GL_DEPTH_TEST)
        glEnable (GL_CULL_FACE )
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glEnable(GL_NORMALIZE)
    
    # srand((unsigned int)time(NULL))
    
    # QtdX = 10#0
    # QtdZ = 10#0
    global QtdX, QtdZ
    
    Texturas.CarregaTexturas()
    glBindTexture(GL_TEXTURE_2D, 0)
    InicializaCidade(QtdX, QtdZ)


# **********************************************************************
#
# **********************************************************************
def animate():
    global AccumDeltaT, TempoTotal, nFrames, angulo

    dt = T.getDeltaT()
    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if (AccumDeltaT > 1.0/60): # fixa a atualiza��o da tela em 30
        AccumDeltaT = 0
        angulo += 1
        glutPostRedisplay()
    
    if (TempoTotal > 5.0):
        print("Tempo Acumulado: ", TempoTotal, " segundos. ")
        print("Nros de Frames sem desenho: ", nFrames)
        print("FPS(sem desenho): ", nFrames/TempoTotal)
        TempoTotal = 0
        nFrames = 0
    
    moveJogador(dt)
    moveAvioes(dt)
    moveDisparos(dt)
    atualizaCamera()

# **********************************************************************
def CalculaBezier3(PC, t):
    # pc = array[3] (ponto)
    # Ponto P
    UmMenosT = 1-t
    
    P =  PC[0] * UmMenosT * UmMenosT + PC[1] * 2 * UmMenosT * t + PC[2] * t*t
    #P.z = 5
    return P

# **********************************************************************
def TracaBezier3Pontos():
    for i in range(len(curvasAvioes)):
        t=0.0
        DeltaT = 1.0/10
        P = Ponto()
        #cout << "DeltaT: " << DeltaT << endl
        glBegin(GL_LINE_STRIP)
        
        while(t<1.0):
            P = CalculaBezier3(curvasAvioes[i], t)
            glVertex3f(P.x, P.y, P.z)
            t += DeltaT
        # P.imprime() cout << endl

        P = CalculaBezier3(curvasAvioes[i], 1.0) # faz o fechamento da curva
        glVertex3f(P.x, P.y, P.z)
        glEnd()

# **********************************************************************
#  void DesenhaCubo()
#
#
# **********************************************************************
def DesenhaCubo():
    glBegin ( GL_QUADS )
    # Front Face
    glNormal3f(0,0,1)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    # Back Face
    glNormal3f(0,0,-1)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    # Top Face
    glNormal3f(0,1,0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    # Bottom Face
    glNormal3f(0,-1,0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    # Right face
    glNormal3f(1,0,0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    # Left Face
    glNormal3f(-1,0,0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glEnd()


# **********************************************************************
#  Desenha um pr�dio no meio de uam c�lula
# **********************************************************************
def DesenhaPredio(altura):
    glPushMatrix()

    glScalef(0.2, altura, 0.2)
    glTranslatef(0, 1, 0)
    DesenhaCubo()

    glPopMatrix()

# **********************************************************************
#  Desenha um veiculo
# **********************************************************************
def DesenhaVeiculo():
    global posJogador
    glPushMatrix()
    defineCor(DarkOrchid)
    # pos.rotacionaY(rotJogador)
    # alvoJogador.rotacionaY(rotJogador)
    glTranslate(posJogador.x, posJogador.y, posJogador.z)

    #rotJogador * 3.1415 / 180
    glRotate(rotJogador, 0, 1, 0)

    # if acelera:
    #     # glTranslate(0, 0, 0.2)
    #     posJogador += alvoJogador

    glScalef(0.1, 0.25, 0.2)
    # glTranslatef(0, 1, 0)
    DesenhaCubo()

    glPopMatrix()

    glPushMatrix()
    
    frente = Ponto(0, 0, 0.2)
    frente.rotacionaY(rotJogador)
    glTranslate(posJogador.x+frente.x, posJogador.y-0.05, posJogador.z+frente.z)
    # glTranslate(alvoJogador.x*0.1, alvoJogador.y, alvoJogador.z*0.1)
    glRotate(rotJogador, 0, 1, 0)

    glScalef(0.05, 0.15, 0.2)
    defineCor(GreenCopper)
    DesenhaCubo()

    glPopMatrix()


# **********************************************************************
#  Desenha um Aviao
# **********************************************************************
def DesenhaAviao():
    global posAvioes, rotAvioes
    
    for i in range(len(posAvioes)):
        
        glPushMatrix()
        defineCor(DarkOrchid)
        
        glTranslate(posAvioes[i].x, posAvioes[i].y, posAvioes[i].z)

        #rotJogador * 3.1415 / 180
        glRotate(rotAvioes[i], 0, 1, 0)

        glScalef(0.1, 0.15, 0.4)

        DesenhaCubo()

        glPopMatrix()

        glPushMatrix()
        
        frente = Ponto(0, 0, 0.2)
        frente.rotacionaY(rotAvioes[i])
        glTranslate(posAvioes[i].x+frente.x, posAvioes[i].y, posAvioes[i].z+frente.z)
        # glTranslate(alvoJogador.x*0.1, alvoJogador.y, alvoJogador.z*0.1)
        glRotate(rotAvioes[i], 0, 1, 0)

        glScalef(0.6, 0.05, 0.1)
        defineCor(GreenCopper)
        DesenhaCubo()

        glPopMatrix()

        glPushMatrix()
        
        frente = Ponto(0, 0, -0.3)
        frente.rotacionaY(rotAvioes[i])
        glTranslate(posAvioes[i].x+frente.x, posAvioes[i].y, posAvioes[i].z+frente.z)
        # glTranslate(alvoJogador.x*0.1, alvoJogador.y, alvoJogador.z*0.1)
        glRotate(rotAvioes[i], 0, 1, 0)

        glScalef(0.25, 0.02, 0.05)
        defineCor(GreenCopper)
        DesenhaCubo()

        glPopMatrix()

        glPushMatrix()
        
        frente = Ponto(0, 0, -0.3)
        frente.rotacionaY(rotAvioes[i])
        glTranslate(posAvioes[i].x+frente.x, posAvioes[i].y+0.2, posAvioes[i].z+frente.z)
        # glTranslate(alvoJogador.x*0.1, alvoJogador.y, alvoJogador.z*0.1)
        glRotate(rotAvioes[i], 0, 1, 0)

        glScalef(0.05, 0.1, 0.05)
        defineCor(GreenCopper)
        DesenhaCubo()

        glPopMatrix()


# **********************************************************************
#  Desenha um veiculo
# **********************************************************************
def DesenhaDisparos():
    global posDisparos

    for i in range(len(posDisparos)):
        if posDisparos[i].y < 0:
            continue

        glPushMatrix()
        defineCor(Black)
        
        glTranslate(posDisparos[i].x, posDisparos[i].y, posDisparos[i].z)
        # glScalef(0.1, 0.25, 0.2)

        sphere = gluNewQuadric() #Create new sphere
        defineCor(Black)
        gluSphere(sphere, 0.2, 16, 8)

        glPopMatrix()

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma c�lula do piso.
# Eh possivel definir a cor da borda e do interior do piso
# O ladrilho tem largula 1, centro no (0,0,0) e est� sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho(corBorda, corDentro):
    defineCor(corBorda) # desenha QUAD preenchido
    glBegin ( GL_QUADS )

    glNormal3f(0,1,0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-0.5,  0.0, -0.5)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-0.5,  0.0,  0.5)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 0.5,  0.0,  0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( 0.5,  0.0, -0.5)
    glTexCoord2f(0.0, 0.0)

    glEnd()
    
    defineCor(corDentro)
    glBegin ( GL_LINE_STRIP ) # desenha borda do ladrilho

    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)

    glEnd()


# **********************************************************************
# DesenhaCidade(int nLinhas, int nColunas)
# QtdX: nro de c�lulas em X
# QtdZ: nro de c�lulas em Z
# Desenha elementos que compiem a cidade
# **********************************************************************
def DesenhaCidade( QtdX,  QtdZ):
    
    # glPushMatrix()

    # glTranslatef(0, 0, 0)
    # DesenhaLadrilho(Red, Black)
    # defineCor(Yellow)
    # DesenhaPredio(2)

    # glPopMatrix()
    # glPushMatrix()

    # glTranslatef(-1, 0, 0)
    # DesenhaLadrilho(Gray, Black)
    # defineCor(Green)
    # DesenhaPredio(1.2)

    # glPopMatrix()

    for i in range(QtdZ):
        for j in range(QtdX):
            glPushMatrix()

            glTranslatef(j, 0, i)
            # defineCor(Cidade[i][j].cor)

            if Cidade[i][j].tipo == PREDIO:
                DesenhaLadrilho(Red, Black)
                defineCor(Cidade[i][j].cor)
                DesenhaPredio(Cidade[i][j].altura)
            elif Cidade[i][j].tipo == RUA or Cidade[i][j].tipo == COMBUSTIVEL:
                acima, abaixo, esq, dir = False,False,False,False
                val = Texturas.PISOS["None"]+1

                acima = True if (i-1 >= 0 and (Cidade[i-1][j].tipo == RUA or Cidade[i-1][j].tipo == COMBUSTIVEL)) else False
                abaixo = True if (i+1 < len(Cidade) and (Cidade[i+1][j].tipo == RUA or Cidade[i+1][j].tipo == COMBUSTIVEL)) else False
                esq = True if (j-1 >= 0 and (Cidade[i][j-1].tipo == RUA or Cidade[i][j-1].tipo == COMBUSTIVEL)) else False
                dir = True if (j+1 < len(Cidade[0]) and (Cidade[i][j+1].tipo == RUA or Cidade[i][j+1].tipo == COMBUSTIVEL)) else False


                if acima and abaixo and esq and dir:
                    val = Texturas.PISOS["CROSS"]+1
                elif acima and abaixo and esq:
                    val = Texturas.PISOS["ULR"]+1
                elif acima and abaixo and dir:
                    val = Texturas.PISOS["DLR"]+1
                elif abaixo and dir and not (esq and abaixo):
                    val = Texturas.PISOS["DR"]+1
                elif acima and dir and not (abaixo or esq):
                    val = Texturas.PISOS["DL"]+1
                elif abaixo and esq and not (dir and abaixo):
                    val = Texturas.PISOS["UR"]+1
                elif acima and esq and not (abaixo or dir):
                    val = Texturas.PISOS["UL"]+1
                elif (esq or dir):
                    val = Texturas.PISOS["UD"]+1
                elif (acima or abaixo):
                    val = Texturas.PISOS["LR"]+1
                
                glBindTexture(GL_TEXTURE_2D, val)
                DesenhaLadrilho(White, Black)
                glBindTexture(GL_TEXTURE_2D, 0)

                if Cidade[i][j].tipo == COMBUSTIVEL:#and j/2 == len(Cidade[0])//2:
                    glTranslatef(0, 0.2, 0)
                    sphere = gluNewQuadric() #Create new sphere
                    defineCor(Cidade[i][j].cor)
                    gluSphere(sphere, 0.2, 16, 8)
            else:
                glBindTexture(GL_TEXTURE_2D, 0)
                DesenhaLadrilho(Cidade[i][j].cor, Black)

            glPopMatrix()


def DesenhaEm2D():
    ativarLuz = False
    if (glIsEnabled(GL_LIGHTING)):
        glDisable(GL_LIGHTING)
        ativarLuz = True
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Salva o tamanho da janela
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    # Define a area a ser ocupada pela area OpenGL dentro da Janela
    glViewport(0, 0, w, int(h*0.1)) # a janela de mensagens fica na parte de baixo da janela

    # Define os limites logicos da area OpenGL dentro da Janela
    glOrtho(0,10, 0,10, 0,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Desenha linha que Divide as �reas 2D e 3D
    defineCor(Yellow)
    glLineWidth(5)
    glBegin(GL_LINES)
    glVertex2f(0,10)
    glVertex2f(10,10)
    glEnd()
    
    s = "Combustivel: " + str(combJogador)
    printString(s, 0, 1, Yellow)
    # printString("Vermelho", 4, 2, Red)
    # printString("Verde", 8, 4, Green)


    # // Resataura os par�metro que foram alterados
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, int(h*0.1), w, h-(int(h*0.1)))

    if (ativarLuz):
        glEnable(GL_LIGHTING)
    glRasterPos2i(100, 75)
    # glRasterPos3i(0, 3, 0)
    glColor4f(0.0, 0.0, 0.0, 1.0)
    
    # glutBitmapCharacter(globals()['GLUT_BITMAP_TIMES_ROMAN_24'], c_int(65))

# **********************************************************************
#  void DefineLuz(void)
# **********************************************************************
def DefineLuz(void=0):
    # Define cores para um objeto dourado
    # tudi array GLfloat
    LuzAmbiente = [0.4, 0.4, 0.4] 
    LuzDifusa = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9 ]
    # era pos veiculo
    PosicaoLuz0 = [posObserv.x, posObserv.y, posObserv.z]# [0.0, 3.0, 5.0 ]  # Posi��o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    # Habilita o uso de ilumina��o
    glEnable(GL_LIGHTING)

    # Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz n�mero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentra��oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado ser� o brilho. (Valores v�lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)


# **********************************************************************
#  void PosicUser()
#
#
# **********************************************************************

def PosicUser():

    # Define os par�metros da proje��o Perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Define o volume de visualiza��o sempre a partir da posicao do
    # observador
    if (ModoDeProjecao == 0):
        glOrtho(-10, 10, -10, 10, 0, 20) # Projecao paralela Orthografica
    else:
        gluPerspective(90,AspectRatio,0.01,1500) # Projecao perspectiva

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(posObserv.x, posObserv.y, posObserv.z,   # Posi��o do Observador 0, 5, 8
              alvoCam.x,alvoCam.y,alvoCam.z,     # Posi��o do Alvo 2,0,0
              0.0,1.0,0.0) # UP

# **********************************************************************
#  void atualizaCamera()
#
#
# **********************************************************************

def atualizaCamera():
    # atualiza a camera
    global posObserv, alvoCam
    # Se for 3 pessoa
    if thirdPerson:
        # if posObserv.x == 5 and posObserv.y == 5 and posObserv.z == 8
        #posObserv = POS_THIRDPERSON
        alvoCam = Ponto(posJogador.x, posJogador.y, posJogador.z)
    # Se for primeira pessoa
    else:
        frente = Ponto(0, 0, 0.1)
        frente.rotacionaY(rotJogador)

        posObserv = Ponto(posJogador.x+frente.x, posJogador.y+0.4, posJogador.z+frente.z)

        alv = alvoJogador * 1

        alv.rotacionaY(rotCamera.y)
        # alv.rotacionaX(rotCamera.x)
        # alv.rotacionaZ(rotCamera.x*-1)
        alv.y += rotCamera.x

        alvoCam = Ponto(posJogador.x+alv.x, posJogador.y+alv.y, posJogador.z+alv.z)

# **********************************************************************
#  void moveJogador()
#
#
# **********************************************************************
def moveJogador(deltaTime):
    global acelera, alvoJogador, posJogador, Cidade, combJogador
    
    if acelera and combJogador > 0:
        proxPos = posJogador + (alvoJogador * 3 * deltaTime)

        cellAtualX = int(proxPos.x)
        cellAtualZ = int(proxPos.z)

        if proxPos.x - cellAtualX >= 0.55:
            cellAtualX += 1
        if proxPos.z - cellAtualZ >= 0.55:
            cellAtualZ += 1

        if proxPos.x - cellAtualX <= -0.55:
            cellAtualX -= 1
        if proxPos.z - cellAtualZ <= -0.55:
            cellAtualZ -= 1

        # print(proxPos.x, proxPos.z)
        # print(cellAtualX, cellAtualZ)

        limiteSuperiro = cellAtualZ >= len(Cidade) or cellAtualX >= len(Cidade[0])
        limiteInferior = cellAtualZ < 0 or cellAtualX < 0

        # se posição for invalida volta
        if limiteSuperiro or limiteInferior:
            acelera = False
        else:
            if Cidade[cellAtualZ][cellAtualX].tipo not in [RUA, COMBUSTIVEL]:
                acelera = False
            else:
                posJogador = proxPos

                if combJogador > 0: 
                    combJogador -= 1 * deltaTime
                
                    if combJogador < 0: 
                        combJogador = 0

                # colisao das meleculas de combustivel
                if Cidade[cellAtualZ][cellAtualX].tipo == COMBUSTIVEL:
                    combJogador += COMBUSTIVEL
                    Cidade[cellAtualZ][cellAtualX].tipo = RUA

# **********************************************************************
#  void moveAvioes()
#
#
# **********************************************************************
def moveAvioes(deltaTime):
    for i in range(len(posAvioes)):

        t = 0
        t = tempAvioes[i]/tempTotaisAvioes[i]
        if (t>1.0):
            # inverte a curva do aviao (caminho inverso)
            temp = curvasAvioes[i][2] * 1
            curvasAvioes[i][2] = curvasAvioes[i][0] * 1
            curvasAvioes[i][0] = temp
            
            tempAvioes[i] = 0
            rotAvioes[i] *= -1
            # tempTotaisAvioes[i] = 0
        else:
            #Ponto[3]{caminhos[i][0], caminhos[i][1], caminhos[i][2]}
            posAvioes[i] = CalculaBezier3(curvasAvioes[i], t)
            tempAvioes[i] += deltaTime

        a = random.randrange(1, 100)
        global posDisparos, disparos
        if a == 3 and disparos < MAX_DISPAROS and i == 0:
            for j in range(len(posDisparos)):
                if posDisparos[j].y < 0 and disparos < MAX_DISPAROS:
                    # print("Dispara", i)
                    # print(i, "qtd disparos:", disparos)
                    posDisparos[j] = posAvioes[j] * 1
                    disparos += 1

# **********************************************************************
#  void moveDisparos()
#
#
# **********************************************************************
def moveDisparos(deltaTime):
    global posDisparos, Cidade, disparos
    
    for i in range(len(posDisparos)):
        if posDisparos[i].y < -2:
            continue

        alvoDisparo = Ponto(0, -1, 0)
        proxPos = posDisparos[i] + (alvoDisparo * 1 * deltaTime)

        cellAtualX = int(proxPos.x)
        cellAtualZ = int(proxPos.z)

        limiteSuperiro = cellAtualZ >= len(Cidade) or cellAtualX >= len(Cidade[0])
        limiteInferior = cellAtualZ < 0 or cellAtualX < 0

        posDisparos[i] = proxPos * 1

        # se posição for invalida volta
        if limiteSuperiro or limiteInferior:
            acelera = False
        else:
            # if Cidade[cellAtualZ][cellAtualX].tipo == PREDIO:
            #     print("disparo em predio")

            if Cidade[cellAtualZ][cellAtualX].tipo in [RUA, COMBUSTIVEL] and posDisparos[i].y <= 0 and posDisparos[i].y > -1:
                Cidade[cellAtualZ][cellAtualX].tipo = VAZIO
                Cidade[cellAtualZ][cellAtualX].cor = Red
                posDisparos[i] = Ponto(1, -4, 1)
                disparos -= 1
            elif Cidade[cellAtualZ][cellAtualX].tipo == PREDIO and posDisparos[i].y <= Cidade[cellAtualZ][cellAtualX].altura*2 and posDisparos[i].y > -1:
                Cidade[cellAtualZ][cellAtualX].tipo = VAZIO
                Cidade[cellAtualZ][cellAtualX].cor = Red
                posDisparos[i] = Ponto(1, -4, 1)
                disparos -= 1
                print("destroi predio")
            elif posDisparos[i].y <= -2:
                posDisparos[i] = Ponto(1, -4, 1)
                disparos -= 1

# **********************************************************************
#  void reshape( int w, int h )
#		trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w, h):

    # Evita divis�o por zero, no caso de uam janela com largura 0.
    if(h == 0): h = 1
    # Ajusta a rela��o entre largura e altura para evitar distor��o na imagem.
    # Veja fun��o "PosicUser".
    global AspectRatio
    AspectRatio = 1.0 * w / h
    # Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    #glViewport(0, 0, w, h)
    glViewport(0, int(h*0.1), w, h-(int(h*0.1)))
    #cout << "Largura" << w << endl

    PosicUser()


def printString(s, posX, posY, cor):
    defineCor(cor)
    
    glRasterPos3i(posX, posY, 0)
    for i in range(len(s)):
        #GLUT_BITMAP_HELVETICA_18,
        glutBitmapCharacter(globals()['GLUT_BITMAP_TIMES_ROMAN_24'], c_int(ord(s[i])))

# **********************************************************************
#  void display( void )
#
#
# **********************************************************************
def display( ):
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    PosicUser()
    glLineWidth(2)

    glMatrixMode(GL_MODELVIEW)

    glColor3f(1,1,1)
    TracaBezier3Pontos()

    DefineLuz()

    DesenhaCidade(QtdX,QtdZ)

    DesenhaVeiculo()
    DesenhaAviao()
    DesenhaDisparos()

    DesenhaEm2D()

    glutSwapBuffers()

# **********************************************************************
#  void keyboard ( unsigned char key, int x, int y )
#
#
# **********************************************************************
def keyboard (  key,  x,  y ):
    global rotCamera, acelera

    if key == '27':
        exit(0)
    elif key == bytes('p', "utf-8"):
        global ModoDeProjecao
        ModoDeProjecao = not ModoDeProjecao
        glutPostRedisplay()
    elif key == bytes('e', "utf-8"):
        # global ModoDeProjecao
        ModoDeProjecao = not ModoDeProjecao
        init()
        glutPostRedisplay()
    elif key == bytes('f', "utf-8"):
        glutFullScreen() # Go Into Full Screen Mode
    elif key == bytes('q', "utf-8"):
        global posObserv, alvoCam, thirdPerson

        if thirdPerson:
            posObserv = Ponto(posJogador.x, posJogador.y+0.2, posJogador.z)
            alvoCam = Ponto(posJogador.x, posJogador.y, posJogador.z+1)
            thirdPerson = False
        else:
            posObserv = POS_THIRDPERSON
            alvoCam = posJogador
            thirdPerson = True
    elif key == bytes('a', "utf-8"):
        rotCamera.y += 2
    elif key == bytes('d', "utf-8"):
        rotCamera.y -= 2
    elif key == bytes('w', "utf-8"):
        rotCamera.x += 0.1
    elif key == bytes('s', "utf-8"):
        rotCamera.x -= 0.1
    elif key == bytes(' ', "utf-8"):
        acelera = not acelera
    else:
        print(key)


# **********************************************************************
#  void arrow_keys ( int a_keys, int x, int y )  
#
#
# **********************************************************************
def arrow_keys ( a_keys,  x,  y ) :
    global rotJogador, acelera, alvoJogador

    if a_keys == GLUT_KEY_DOWN:
        glutInitWindowSize  ( 700, 500 )
    elif a_keys == GLUT_KEY_LEFT:
        rotJogador += 4
        # print("rot:", rotJogador)
        alvoJogador = Ponto(0, 0, 1)
        alvoJogador.rotacionaY(rotJogador)
        atualizaCamera()
    elif a_keys == GLUT_KEY_RIGHT:
        rotJogador -= 4
        # print("rot:", rotJogador)
        alvoJogador = Ponto(0, 0, 1)
        alvoJogador.rotacionaY(rotJogador)
        atualizaCamera()
    else:
        return

# **********************************************************************
#  void main ( int argc, char** argv )
#
#
# **********************************************************************
# def main ( argc, argv ):

glutInit            (sys.argv ) 
glutInitDisplayMode (GLUT_DOUBLE | GLUT_DEPTH | GLUT_RGB )
glutInitWindowPosition (0,0)
glutInitWindowSize  ( 700, 700 )
glutCreateWindow    ( "Computacao Grafica - Exemplo Basico 3D" ) 
    
init ()
#system("pwd")

glutDisplayFunc ( display )  
glutReshapeFunc ( reshape )
glutKeyboardFunc ( keyboard )
glutSpecialFunc ( arrow_keys )
glutIdleFunc ( animate )

glutMainLoop ( )          
# return 0 