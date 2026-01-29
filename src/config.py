# Definimos la región del tablero (X, Y, Ancho, Alto).
# Tienes que ajustar estos números probando hasta que encaje perfecto en tu pantalla.
# Basado en tu screenshot, el tablero está centrado y es grande.
BOARD_REGION = {
    "top": 281,
    "left": 440,
    "width": 624,
    "height": 624
}

CLOCK_OPPONENT = {
    "top": 204,
    "left": 884,
    "width": 178,                                                                                                                                  
    "height": 58                                                                                                                                     
}             

CLOCK_PLAYER = {
    "top": 987,
    "left": 883,
    "width": 182,
    "height": 58
}

# Umbral de sensibilidad (cuánto tiene que cambiar la imagen para contar como movimiento)
MOTION_THRESHOLD = 50

# Configuración de visualización
SHOW_DEBUG = True