import pygame
import math

pygame.init()

#Ancho de la ventana
ANCHO = 600
#Alto de la ventana
ALTO = 600
#Ventana de juego
VENTANA = pygame.display.set_mode((ANCHO,ALTO))
#Colores utilizados para graficar
COLOR_BLANCO = (255,255,255) 
COLOR_NEGRO = (0,0,0)
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_VERDE = (0,255,0)
CPS = 60
#Variables necesarias para ray casting y movimiento del jugador
FOV = math.pi/3
MITAD_FOV = FOV/2
NUMERO_RAYOS = ANCHO//2
DELTA_ANGULO_RAYO = FOV/NUMERO_RAYOS
DISTANCIA_A_PANTALLA = (ANCHO//2)/math.tan(MITAD_FOV)
ESCALA = (ANCHO//NUMERO_RAYOS)
DIRECCION_ARCHIVO = "laberinto.txt"
FUENTE_TEXTO = pygame.font.SysFont('Arial',30,bold=True)
anchoCelda = int
anchoMapa = int
altoMapa = int
anguloJugador = 0
mapa = dict()
posX = int
posY = int


with open(DIRECCION_ARCHIVO) as archivo:
    lineas = archivo.readlines()
    x = 1 #Columna del mapa
    y = 1 #Fila del mapa
    for linea in lineas:
        x = 1
        for caracter in linea:
            if(caracter == "#"):
                mapa.update({(x,y):"PARED"})
            elif(caracter == " "):
                mapa.update({(x,y):"VACIO"})
            elif(caracter == "S"):
                mapa.update({(x,y):"INICIO"})
                posX = x
                posY = y
            elif(caracter == "E"):
                mapa.update({(x,y):"SALIDA"})
            x += 1
        y += 1

    altoMapa = y - 1
    anchoMapa = len(lineas[0]) - 1

    mayorMedida = anchoMapa if anchoMapa >= altoMapa else altoMapa
    anchoCelda = int(ANCHO/mayorMedida)

#Deteccion de entradas de teclado
def movimiento_jugador():
    global anguloJugador, posX, posY
    distX = math.cos(anguloJugador)*0.01
    distY = math.sin(anguloJugador)*0.01

    teclas = pygame.key.get_pressed()

    if(teclas[pygame.K_w]):
        actualizar_posicion(posX + distX, posY - distY)
    if(teclas[pygame.K_s]):
        actualizar_posicion(posX - distX, posY + distY)
    if(teclas[pygame.K_a]):
        anguloJugador += 0.1
    if(teclas[pygame.K_d]):
        anguloJugador -= 0.1 
    
#Actualizar posicion
def actualizar_posicion(nuevaPosX, nuevaPosY):
    global posX, posY
    if(not detectar_pared(nuevaPosX, nuevaPosY)):
        posX = nuevaPosX
        posY = nuevaPosY
    if mapa[(math.ceil(posX),math.ceil(posY))] == "SALIDA":
        mostrar_texto("HAS SALIDO DEL LABERINTO :)",True)

#Deteccion de colisiones con paredes
def detectar_pared(nuevaPosX, nuevaPosY):
    if mapa[(math.ceil(nuevaPosX),math.ceil(nuevaPosY))] == "PARED":
        return True
    return False

#Mensaje que aparece al terminar el laberinto
def mostrar_texto(texto, centrado=False, x=0, y=0):
    mensaje = FUENTE_TEXTO.render(texto,False,COLOR_AZUL)
    if centrado:
        VENTANA.blit(mensaje,(ANCHO/2 - mensaje.get_width()/2,ALTO/2))
    else:
        VENTANA.blit(mensaje,(x,y))

#Algoritmo de raycasting metodo 2
def emitir_rayos():
    global posX, posY,anguloJugador
    grillaPosX = posX #Posicion del jugador respecto del mapa en X
    grillaPosY = posY #Posicion del jugador respecto del mapa en Y
    grillaX = int(posX) #Punto inicial de la celda actual
    grillaY = int(posY) #Punto inicla de la celda actual

    anguloRayo = anguloJugador - MITAD_FOV
    
    for rayo in range(NUMERO_RAYOS):
        dirRayoX = math.cos(anguloRayo)
        dirRayoY = math.sin(anguloRayo)

        #Intersecciones con las lineas Horizontales
        if(dirRayoY > 0):
            pasoY = -1 #Paso en Y respecto a la grilla
            y_H =  grillaY - 1e-6 #Coordenada Y del punto de interseccion con la linea horizontal
        else:
            pasoY = 1
            y_H = grillaY + 1

        distHorz = abs((y_H - grillaPosY)/dirRayoY) #Distancia del rayo desde el jugador a la linea horizontal
        x_H = grillaPosX + distHorz*dirRayoX 

        deltaDist = abs(pasoY/dirRayoY)
        pasoX = deltaDist*dirRayoX
        # x_H: Columna donde se encuentra la cuadricula
        # y_H: Fila donde se encuentra la cuadricula

        for i in range(100):
            if dirRayoY > 0:
                cuadricula = (math.ceil(x_H),math.ceil(y_H))
            else:
                cuadricula = (math.ceil(x_H),math.ceil(y_H+1))
            if cuadricula in mapa.keys() and mapa[cuadricula] == "PARED":
                break
            x_H += pasoX
            y_H += pasoY
            distHorz += deltaDist

        #Intersecciones con las lineas Verticales
        if(dirRayoX > 0):
            pasoX = 1 #Paso en X respecto a la grilla
            x_V =  grillaX + 1 #Coordenada X del punto de interseccion con la linea vertical
        else:
            pasoX = -1
            x_V = grillaX - 1e-6

        distVert = (x_V - grillaPosX)/dirRayoX #Distancia del rayo desde el jugador a la linea vertical
        if dirRayoY < 0:
            y_V = grillaPosY + abs(distVert*dirRayoY) #Coordenada Y del punto de interseccion con la linea vertical
        else:
            y_V = grillaPosY - abs(distVert*dirRayoY)

        deltaDist = pasoX/dirRayoX 
        pasoY = deltaDist*dirRayoY

        # x_V: Columna donde se encuentra la cuadricula
        # y_V: Fila donde se encuentra la cuadricula

        for i in range(100):
            if dirRayoX > 0:
                cuadricula = (math.ceil(x_V+1),math.ceil(y_V))
            else:
                cuadricula = (math.ceil(x_V),math.ceil(y_V))

            if cuadricula in mapa.keys() and mapa[cuadricula] == "PARED":
                break
            x_V += pasoX
            y_V -= pasoY
            distVert += deltaDist

        #Distancia total
        if(distHorz<distVert):
            distAPared = distHorz
        else:
            distAPared = distVert

        #Proyectamos las paredes 
        
        altoPared = DISTANCIA_A_PANTALLA/(distAPared+0.0001)

        proyectar_paredes(rayo,altoPared)


        anguloRayo += DELTA_ANGULO_RAYO

    

def proyectar_paredes(rayo,alto):
    pygame.draw.rect(VENTANA,COLOR_BLANCO,(rayo*ESCALA, (ALTO/2) - alto//2, ESCALA, alto))


#Funcion principal
def main():
    jugando = True
    reloj = pygame.time.Clock()

    #Bucle de juego
    while jugando:
        
        #Limitamos el numero de cuadros por segundo a 60
        reloj.tick(CPS)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        VENTANA.fill(COLOR_NEGRO)
        
        movimiento_jugador()
        emitir_rayos()
        cps = reloj.get_fps()
        mostrar_texto(str(int(cps)),False)

        pygame.display.update()
        
    pygame.quit()
    

if __name__ == "__main__":
    main()