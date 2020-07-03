import pygame
from random import randint
import backtracking_ubongo


class CFigura:
    x = 0
    y = 0
    _id = 0
    col = (0, 0, 0)
    image = 0
    mat = []
    ma_pos = []

    def __init__(self, x, y, n, filename):
        self.x = x
        self.y = y
        self._id = n
        self.imagen(filename, True)
        if self._id == 4 or self._id == 6 or self._id == 10:
            self.col = self.image.get_at((51, 25))
        else:
            self.col = self.image.get_at((0, 0))
        self.formaMatriz()

    def formaMatriz(self):
        ancho, alto = self.image.get_rect().size
        self.mat = [[-1 for i in range(ancho // 50)] for j in range(alto // 50)]
        for i in range(0, alto // 50):
            for j in range(0, ancho // 50):
                pixelcol = self.image.get_at((j * 50, i * 50))
                if pixelcol == self.col:
                    self.mat[i][j] = self._id

    def imagen(self, filename, transparent=False):
        self.image = pygame.image.load(filename)
        self.image = self.image.convert()
        if transparent:
            color = self.image.get_at((0, 0))
            self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)

    def cargarImg(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def rotarImg(self, angulo):
        if angulo == 0:
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.image = pygame.transform.rotate(self.image, -90)

    def voltearImg(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def reescalarImg(self):
        if self._id == 1:
            self.image = pygame.transform.scale(self.image, (150, 50))

    def acomodarImg(self):
        self.x -= (self.x % 50)
        self.y -= (self.y % 50)

    def getId(self):
        return self._id

    def getCol(self):
        return self.col

    def getPos(self):
        return self.x, self.y

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def getImage(self):
        return self.image

    def getWidth(self):
        self.width = self.image.get_width()
        return self.width

    def getHeight(self):
        self.height = self.image.get_height()
        return self.height

    def getMat(self):
        return self.mat

    def getMatPos(self):
        return self.ma_pos

    def setMatPos(self, pos):
        self.ma_pos = pos


class Plantilla:
    # ESCENARIOS

    Figuras = []
    ma_vali = []
    color = (0, 0, 0)
    pos = (0, 0)
    tabla_pc = []
    piezas = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Figuras = [
            CFigura(150, (50), 1, "Fichas/Ficha1.png"),
            CFigura(150, (150), 2, "Fichas/Ficha2.png"),
            CFigura(150, (200), 3, "Fichas/Ficha3.png"),
            CFigura(150, (250), 4, "Fichas/Ficha4.png"),
            CFigura(150, (300), 5, "Fichas/Ficha5.png"),
            CFigura(150, (350), 6, "Fichas/Ficha6.png"),
            CFigura(150, (50), 7, "Fichas/Ficha7.png"),
            CFigura(150, (150), 8, "Fichas/Ficha8.png"),
            CFigura(150, (200), 9, "Fichas/Ficha9.png"),
            CFigura(150, (250), 10, "Fichas/Ficha10.png"),
            CFigura(150, (300), 11, "Fichas/Ficha11.png"),
            CFigura(150, (350), 12, "Fichas/Ficha12.png")]

        self.tabla_pc = backtracking_ubongo.gen_matrix("""
                                               00001
                                               10001
                                               10000
                                               11001
                                               """)

        self.piezas = [backtracking_ubongo.gen_matrix("""
                                                                220
                                                                020
                                                                022
                                                                """
                                                      ), backtracking_ubongo.gen_matrix("""
                                                           33
                                                           33
                                                           03
                                                           """),
                       backtracking_ubongo.gen_matrix("""
                                                        4
                                                        4
                                                        4
                                                        """)]

    def colocar(self, piez_x, piez_y, aux):
        n_col = len(self.ma_vali[0])
        n_fil = len(self.ma_vali)
        pos = []
        aux.formaMatriz()
        aux_mat = aux.getMat()
        if (piez_x >= self.x and piez_x + len(
                aux_mat[0]) * 50 <= self.x + n_col * 50 and piez_y >= self.y and piez_y + len(
                aux_mat) * 50 <= self.y + n_fil * 50):
            x = (piez_x - self.x) // 50
            y = (piez_y - self.y) // 50
            for f in range(len(aux_mat)):
                for c in range(len(aux_mat[f])):
                    if aux_mat[f][c] != -1:
                        if (self.ma_vali[f + y][c + x] == 0):
                            pos.append([f + y, c + x])
                        else:
                            print(self.ma_vali)
                            return
            for i in range(len(pos)):
                self.ma_vali[pos[i][0]][pos[i][1]] = aux.getId()
            aux.setMatPos(pos)
        else:
            actual_pos = aux.getMatPos()
            for i in range(len(actual_pos)):
                self.ma_vali[actual_pos[i][0]][actual_pos[i][1]] = 0

        print(self.ma_vali)

    def IsComplete(self):
        for i in range(len(self.ma_vali)):
            if 0 in self.ma_vali[i]:
                return False
        return True

    def getMat(self):
        return self.ma_vali

    def getTabla_pc(self):
        return self.tabla_pc

    def getPiezas(self):
        return self.piezas

    # 3 Fichas
    def DibujarPlantilla1(self, surface, x, y):
        self.color = (255, 255, 255)
        self.x = x

        # Fila 1
        self.y = 250
        pygame.draw.rect(surface, self.color, [(self.x, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 200, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[0, 0, 0, 0, -1],
                            [-1, 0, 0, 0, -1],
                            [-1, 0, 0, 0, 0],
                            [-1, -1, 0, 0, -1]]

    # 3 FICHAS
    def DibujarPlantilla2(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x

        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        # Fila 5
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 200), (50, 50)])
        # Fila 6
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 250), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[0, 0, -1],
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0],
                            [-1, -1, 0],
                            [-1, -1, 0]]

    # 4 FICHAS
    def DibujarPlantilla3(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x

        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        # Fila 5
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 200), (50, 50)])
        # Fila 6
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 250), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 250), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[-1, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [-1, 0, 0, 0],
                            [-1, 0, 0, -1],
                            [-1, 0, 0, -1]]

    # 4 FICHAS
    def DibujarPlantilla4(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 200, self.y + 150), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[-1, 0, 0, -1, -1],
                            [0, 0, 0, -1, -1],
                            [0, 0, 0, 0, -1],
                            [-1, 0, 0, 0, 0, ]]

    # 4 FICHAS
    def DibujarPlantilla5(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        # Fila 5
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 200), (50, 50)])
        # Fila 6
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 250), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[-1, -1, 0, 0],
                            [-1, -1, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [-1, 0, -1, -1]]

    # 4 FICHAS
    def DibujarPlantilla6(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        # Fila 5
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 200), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[-1, -1, 0, 0],
                            [-1, -1, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [-1, 0, 0, 0]]

    # 4 FICHAS
    def DibujarPlantilla7(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        # Fila 5
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 200), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 200), (50, 50)])
        # Fila 6
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 250), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 250), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[-1, 0, 0, -1],
                            [-1, 0, 0, 0],
                            [-1, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, -1, -1],
                            [0, 0, -1, -1]]

    # 4 FICHAS
    def DibujarPlantilla8(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [-1, 0, 0, 0],
                            [-1, 0, 0, 0]]

    # 4 FICHAS
    def DibujarPlantilla9(self, surface, x, y):
        self.color = (33, 33, 33)
        self.x = x
        # y = 0
        # DIBUJAR TABLERO DE JUGADOR PERSONA
        # Fila 1
        # pygame.draw.rect(surface, color, [(x, y), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 50, y), (50, 50)])
        # Fila 2
        # pygame.draw.rect(surface, color, [(x, y + 50), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 50, y + 50), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 100, y + 50), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 150, y + 50), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 200, y + 50), (50, 50)])
        # Fila 3
        # pygame.draw.rect(surface, color, [(x, y + 100), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 50, y + 100), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 100, y + 100), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 150, y + 100), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 200, y + 100), (50, 50)])
        # Fila 4
        # pygame.draw.rect(surface, color, [(x, y + 150), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 50, y + 150), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 100, y + 150), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 150, y + 150), (50, 50)])
        # pygame.draw.rect(surface, color, [(x + 200, y + 150), (50, 50)])

        # DIBUJAR TABLERO DE JUGADOR COMPUTADORA
        self.y = 250
        # Fila 1
        pygame.draw.rect(surface, self.color, [(self.x, self.y), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y), (50, 50)])
        # Fila 2
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 50), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 200, self.y + 50), (50, 50)])
        # Fila 3
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 100), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 200, self.y + 100), (50, 50)])
        # Fila 4
        pygame.draw.rect(surface, self.color, [(self.x, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 50, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 100, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 150, self.y + 150), (50, 50)])
        pygame.draw.rect(surface, self.color, [(self.x + 200, self.y + 150), (50, 50)])

        if len(self.ma_vali) == 0:
            self.ma_vali = [[0, 0, -1, -1, -1],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0]]

    def getFiguras(self):
        return self.Figuras

    def cargarFiguras(self, surface, cara, nplantilla):
        if nplantilla == 1:
            if cara == 0:
                self.Figuras[3].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
            elif cara == 1:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
            elif cara == 2:
                self.Figuras[0].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
            elif cara == 3:
                self.Figuras[1].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 4:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 5:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[3].cargarImg(surface)

        if nplantilla == 2:
            if cara == 0:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 1:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
            elif cara == 2:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 3:
                self.Figuras[7].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
            elif cara == 4:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 5:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)

        if nplantilla == 3:
            if cara == 0:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 1:
                self.Figuras[3].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
            elif cara == 2:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 3:
                self.Figuras[7].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 4:
                self.Figuras[4].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
            elif cara == 5:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)

        if nplantilla == 4:
            if cara == 0:
                self.Figuras[4].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 1:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 2:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
            elif cara == 3:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
            elif cara == 4:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 5:
                self.Figuras[11].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)

        if nplantilla == 5:
            if cara == 0:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
            elif cara == 1:
                self.Figuras[11].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 2:
                self.Figuras[4].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[3].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
            elif cara == 3:
                self.Figuras[11].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
            elif cara == 4:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
                self.Figuras[3].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
            elif cara == 5:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)

        if nplantilla == 6:
            if cara == 0:
                self.Figuras[0].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
            elif cara == 1:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
            elif cara == 2:
                self.Figuras[4].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
            elif cara == 3:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
            elif cara == 4:
                self.Figuras[8].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 5:
                self.Figuras[9].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)

        if nplantilla == 7:
            if cara == 0:
                self.Figuras[1].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
            elif cara == 1:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 2:
                self.Figuras[0].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[3].cargarImg(surface)
            elif cara == 3:
                self.Figuras[7].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
            elif cara == 4:
                self.Figuras[5].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
            elif cara == 5:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)

        if nplantilla == 8:
            if cara == 0:
                self.Figuras[8].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
            elif cara == 1:
                self.Figuras[5].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
            elif cara == 2:
                self.Figuras[2].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
            elif cara == 3:
                self.Figuras[7].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
                self.Figuras[8].cargarImg(surface)
            elif cara == 4:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
            elif cara == 5:
                self.Figuras[8].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[0].cargarImg(surface)

        if nplantilla == 9:
            if cara == 0:
                self.Figuras[10].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
                self.Figuras[3].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
            elif cara == 1:
                self.Figuras[6].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
            elif cara == 2:
                self.Figuras[4].cargarImg(surface)
                self.Figuras[7].cargarImg(surface)
                self.Figuras[9].cargarImg(surface)
                self.Figuras[11].cargarImg(surface)
            elif cara == 3:
                self.Figuras[1].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
            elif cara == 4:
                self.Figuras[7].cargarImg(surface)
                self.Figuras[1].cargarImg(surface)
                self.Figuras[2].cargarImg(surface)
                self.Figuras[4].cargarImg(surface)
            elif cara == 5:
                self.Figuras[11].cargarImg(surface)
                self.Figuras[6].cargarImg(surface)
                self.Figuras[5].cargarImg(surface)
                self.Figuras[10].cargarImg(surface)
