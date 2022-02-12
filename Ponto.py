from math import sin
from math import cos

class Ponto:
    def __init__(self, x=0, y=0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z
        pass

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def imprime(self):
        print("(",self.x,", ",self.y,", ",self.z,")")
    

    def multiplica(self, x, y, z):
        self.x *= x
        self.y *= y
        self.z *= z
    

    def soma(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
    

    def ObtemMaximo(P1, P2):
        Max = Ponto()

        Max.x = P2.x if (P2.x > P1.x) else P1.x
        Max.y = P2.y if (P2.y > P1.y) else P1.y
        Max.z = P2.z if (P2.z > P1.x) else P1.z
        return Max
    
    def ObtemMinimo (P1, P2):
        Min = Ponto()
        
        Min.x = P2.x if (P2.x < P1.x) else P1.x
        Min.y = P2.y if (P2.y < P1.y) else P1.y
        Min.z = P2.z if (P2.z < P1.x) else P1.z
        return Min
    
    def __add__(self, P2):
        temp = Ponto()
        temp = self
        temp.x += P2.x
        temp.y += P2.y
        temp.z += P2.z
        return temp

    def __sub__(self, P2):
        temp = Ponto()
        temp = self
        temp.x -= P2.x
        temp.y -= P2.y
        temp.z -= P2.z
        return temp

    def __mul__(self, k):
        temp = Ponto()
        temp.x = self.x * k
        temp.y = self.y * k
        temp.z = self.z * k
        return temp

    def rotacionaZ(self, angulo):
        xr, yr = 0, 0
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*cos(anguloRad) - self.y*sin(anguloRad)
        yr = self.x*sin(anguloRad) + self.y*cos(anguloRad)
        self.x = xr
        self.y = yr


    def rotacionaY(self, angulo):
        xr, zr = 0, 0
        anguloRad = angulo* 3.14159265359/180.0
        xr =  self.x*cos(anguloRad) + self.z*sin(anguloRad)
        zr = -self.x*sin(anguloRad) + self.z*cos(anguloRad)
        self.x = xr
        self.z = zr

    def rotacionaX(self, angulo):
        yr, zr = 0, 0
        anguloRad = angulo* 3.14159265359/180.0
        yr =  self.y*cos(anguloRad) - self.z*sin(anguloRad)
        zr =  self.y*sin(anguloRad) + self.z*cos(anguloRad)
        self.y = yr
        self.z = zr

    # Ponto operator-(Ponto P1)
    # :
    #     return P1 * -1