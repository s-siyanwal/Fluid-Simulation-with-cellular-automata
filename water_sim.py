import pygame
import numpy as np
import sys
import random

pygame.init()
 
# Ancho y alto de la pantalla
width, height = 800 , 800

# Creacion de la pantalla
screen = pygame.display.set_mode((width,height))

# Variable para poner pausa al juego
pauseExect = False


# Color del fondo
bg = 255, 255, 255 # Fondo de color blanco
screen.fill(bg)

# Cantidad de celdas a visualizar
nxC , nyC = 50, 50

# Dimension de las celdas en relacion a su ancho y alto
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas, AIRE = 0 , PISO = 1, AGUA = 2;
AIRE = 0
PISO = 1
AGUA = 2

# Definir colores para aire y piso
aire = (255, 255, 255)
piso = (30, 30, 30)

# Matriz para definir el tipo de bloque contenido en la celda:
bloques = np.zeros((nxC +2 ,nyC + 2))



# Matriz para almacenar la masa de cada celda "mass" y matriz "new_mass" que servira para los calculos en cada iteracion
mass = np.zeros((nxC +2 , nyC + 2))
new_mass = np.zeros((nxC + 2, nyC + 2))

# Propiedades del agua
Max_mass = 1.0 # La masa normal de una celda que no esté bajo presión 
Max_compress = 0.25 # La cantidad adicional de agua que una celda puede contener en comparacion de la celda arriba de esta 
Min_mass = 0.0001 # Masa minima, para ignorar celdas practicamente secas
Maxspeed = 1 # Define la maxima cantidad de agua que puede pasar de una celda a otra por cada iteracion
Minflow = 0.005 # Minima cantidad de agua
flowspeed = 0.5 # Rapidez con la que fluye el agua

# Propiedades para dibujar el agua
MinDraw = 0.01
MaxDraw = 1.1

# Devuelve la cantidad de agua que debe fluir entre celdas
def get_state(total_mass):

	if (total_mass <= Max_mass):
		return Max_mass
	elif (total_mass < 2*Max_mass + Max_compress):
		return (Max_mass*Max_mass + total_mass*Max_compress)/(Max_mass + Max_compress)
	else:
		return (total_mass + Max_compress)/2.0

# Devuelve las coordenadas del poligono entero a dibujar 
def polygon(x, y):
				#Poligono de cada celda para dibujar
				# Las celdas interiores van de 1 a nxC/nyC, se desplazan una posicion
				# para que ocupen toda la ventana (los bordes quedan fuera de pantalla)
				x -= 1
				y -= 1
				poly = [ 	((x    ) * dimCW, y * dimCH),
								((x + 1) * dimCW, y * dimCH),
								((x + 1) * dimCW, ((y + 1) * dimCH)),
								((x    ) * dimCW, (y + 1) * dimCH)]
				return poly


# Restringe un valor dado entre los dos parametros min y max
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# Inicia el mapa con valores aleatorios
def initmap():
	for y in range(1, nyC+1):
			for x in range(1, nxC+1):
				bloques[x, y] = random.randint(0,1)


# Esta funcion servira para "mapear" la masa del agua y convertira en un rgb equivalente
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



# Obtiene una tupla (r,g,b) con tonalidades azules de acuerdo a la cantidad de masa que tenga la celda
def waterColor( mass):
	mass = constrain(mass, MinDraw, MaxDraw)
	r, g = 50, 50

	if (mass < 1):
		b = int(map_range(mass,0.01,1,255,200))
		r = int(map_range(mass,0.01,1,240,50))
		r = constrain(r,50,240)
		g = r
	else:
		b =int(map_range(mass,1,1.1,190,140))
	b = constrain(b, 140, 255)
	return (r,g,b)

# inicia un mapa al azar
# COMENTADO PARA PODER DIBUJAR LIBREMENTE initmap()

# Poner bordes solidos para evitar que el agua se salga de la pantalla
for x in range(0, nxC +2):
	bloques[x, 0] = PISO
	bloques[x, nyC + 1] = PISO

for y in range(0, nyC +2):
	bloques[0, y] = PISO
	bloques[nxC + 1, y] = PISO


# Reloj para limitar los FPS y no consumir 100% del CPU
clock = pygame.time.Clock()
pygame.display.set_caption("Simulacion de agua - Espacio: pausa")

# Bucle en ejecucion
while True:
	clock.tick(60)
	

	# Registrar una llamada de teclado y raton
	ev = pygame.event.get()

	# Copiar la masa actual
	new_mass = np.copy(mass)

	# Detectar si esta presionado el raton	
	mouseClick = pygame.mouse.get_pressed()

	# Para registrar distintos eventos
	for event in ev:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pauseExect = not pauseExect # Para poner pausa
			elif event.key == pygame.K_c:
				# Limpiar el agua y los pisos interiores
				new_mass[:, :] = 0
				bloques[1:nxC+1, 1:nyC+1] = AIRE
			elif event.key == pygame.K_ESCAPE:
				sys.exit(0)
			
		if event.type == pygame.QUIT:
			sys.exit(0)
	
	# Para colocar agua en un punto dado, eliminar o poner un piso
	if sum(mouseClick) > 0:
		posX, posY = pygame.mouse.get_pos()
		# +1 por el borde; se restringe para no modificar nunca los bordes solidos
		celX = constrain(int(np.floor(posX / dimCW)) + 1, 1, nxC)
		celY = constrain(int(np.floor(posY / dimCH)) + 1, 1, nyC)
		if( mouseClick[0] and bloques[celX,celY] != PISO):
			new_mass[celX,celY] += 5 # Para sumar agua en el punto especificado
		if( mouseClick[1]):
			bloques[celX,celY] = AIRE # Para poner aire con click de la rueda del raton
			new_mass[celX,celY] = 0 
		if( mouseClick[2]):
			bloques[celX,celY] = PISO # Para poner bloques con el click derecho
			new_mass[celX,celY] = 0
	

	if not pauseExect:
		screen.fill(bg)


	

	
				

	flow = 0 # Para almacenar la cantidad de agua que fluye
	remaining_mass = 0 # Agua restante en una celda

#Si no esta en pause ejecutar a hacer los calculos
	if not pauseExect:

		# Este bucle calcula el flow y lo aplica para cada celda
		for y in range(1, nyC+1):
			for x in range(1, nxC+1):

				# Si la celda es un piso, salta la iteracion			
				if (bloques[x, y] == PISO):
					continue
				
				flow = 0
				remaining_mass = mass[x, y]

				# Si la masa restante es 0 salta la iteracion
				if (remaining_mass <=0):
					continue
				
				# PRIMERA REGLA
				# La celda debajo de este  
				if (bloques[x, y+1] != PISO):
					flow = get_state( remaining_mass + mass[x, y + 1]) - mass[x, y + 1]
					if (flow > Minflow):
						flow *= flowspeed 

					flow = constrain(flow, 0, min(Maxspeed, remaining_mass))

					new_mass[x, y] -= flow
					new_mass[x, y+1] += flow
					remaining_mass -= flow

				# Si la masa restante es 0 salta la iteracion
				if (remaining_mass <= 0):
					continue
				
				# SEGUNDA REGLA
				# Para la celda izquierda
				if ( bloques[x-1, y] != PISO):
					# La siguiente expresion iguala el aguna en este bloque y en la de sus dos vecinos
					flow = (mass[x, y] - mass[x-1, y])/ 4
					
					if (flow > Minflow):
						flow *= flowspeed 
					flow = constrain(flow, 0, min(Maxspeed, remaining_mass))

					new_mass[x, y] -= flow
					new_mass[x-1, y] += flow
					remaining_mass -= flow

				# Si la masa restante es 0 salta la iteracion
				if (remaining_mass <= 0):
					continue

				# Para la celda derecha	
				if ( bloques[x+1, y] != PISO):
					# La siguiente expresion iguala el aguna en este bloque y en la de sus dos vecinos
					flow = (mass[x, y] - mass[x+1, y])/ 4
					
					if (flow > Minflow):
						flow *= flowspeed 
					flow = constrain(flow, 0, min(Maxspeed, remaining_mass))

					new_mass[x, y] -= flow
					new_mass[x+1, y] += flow
					remaining_mass -= flow

				# Si la masa restante es 0 salta la iteracion
				if (remaining_mass <= 0):
					continue

				# TERCERA REGLA
				# Para la celda superior, unicamente si el agua esta "comprimida"
				if (bloques[x, y-1] != PISO):
					flow = remaining_mass - get_state( remaining_mass + mass[x, y - 1])
					if( flow > Minflow):
						flow *= flowspeed 

					flow = constrain(flow, 0, min(Maxspeed, remaining_mass))

					new_mass[x, y] -= flow
					new_mass[x, y-1] += flow
					remaining_mass -= flow

		
	# Actualizar el estado de la simulacion
	mass = np.copy(new_mass)
		
	# Actualizar los tags de agua y aire y pintar la respectiva celda
	for x in range(1, nxC+1):
		for y in range(1, nyC+1):
			if (bloques[x, y] == PISO):
				pygame.draw.polygon(screen, piso , polygon(x,y), 0)
				continue
				
			if (mass[x, y] > Min_mass):
				bloques[x, y] = AGUA
				color = waterColor(mass[x,y])
				pygame.draw.polygon(screen, color , polygon(x,y), 0)
			else:
				bloques[x, y] = AIRE
				pygame.draw.polygon(screen, aire,  polygon(x,y), 0)

		

	pygame.display.flip()