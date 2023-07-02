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


def dibujar_mapa():
    #Dibujamos cada celda del mapa
    for fila in range(1, altoMapa+1):
        for columna in range(1, anchoMapa+1):
            pygame.draw.rect(VENTANA,
                             COLOR_VERDE if mapa[(columna,fila)] == "PARED" else COLOR_BLANCO,
                             ((columna-1)*anchoCelda, (fila-1)*anchoCelda, anchoCelda-1, anchoCelda-1))
    #Dibuja al jugador en su posicion inicial respecto de la ventana
    pygame.draw.circle(VENTANA, COLOR_ROJO, (posX*anchoCelda, posY*anchoCelda),5)
    #Traza un rayo desde la posicion el jugador en la direccion a la que apunta(solo referencial)
    pygame.draw.line(VENTANA, COLOR_AZUL, (posX*anchoCelda, posY*anchoCelda),(posX*anchoCelda + math.cos(anguloJugador)*20, posY*anchoCelda - math.sin(anguloJugador)*20), 3)


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
    print(math.ceil(nuevaPosX),math.ceil(nuevaPosY))
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
        
        dibujar_mapa()
        movimiento_jugador()

        cps = reloj.get_fps()
        mostrar_texto(str(int(cps)),False)

        pygame.display.update()
        
    pygame.quit()
    

if __name__ == "__main__":
    main()