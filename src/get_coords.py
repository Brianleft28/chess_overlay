import mss
import cv2
import numpy as np
import time

# Variables globales para guardar los clics
coords = []

def mouse_callback(event, x, y, flags, param):
    """Manejador de eventos del mouse"""
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        print(f"Click registrado en: x={x}, y={y}")
        
        # Dibujar un círculo donde hiciste clic para referencia visual
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibrador Manual - Haz clic en la esquina sup-izq y luego inf-der", param)

def main():
    print("--- MODO CALIBRACIÓN MANUAL ---")
    print("1. Se abrirá una captura estática de tu pantalla.")
    print("2. Haz CLIC en la esquina SUPERIOR IZQUIERDA del tablero (Torre a8).")
    print("3. Haz CLIC en la esquina INFERIOR DERECHA del tablero (Torre h1).")
    print("4. Presiona 'q' para calcular y salir.\n")

    print("--- MODO CALIBRACIÓN ---")
    print("TIENES 3 SEGUNDOS PARA MINIMIZAR ESTA TERMINAL...")
    time.sleep(3) 
    
    with mss.mss() as sct:
        # Capturamos TODA la pantalla (monitor 1)
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        
        # Convertimos a formato compatible con OpenCV
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Creamos la ventana y asignamos el 'escucha' del mouse
        window_name = "Calibrador Manual - Haz clic en la esquina sup-izq y luego inf-der"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, mouse_callback, img_bgr)

        # Mostramos la imagen y esperamos
        cv2.imshow(window_name, img_bgr)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
            # Si ya tenemos 2 puntos, podemos dibujar el rectángulo previo
            if len(coords) >= 2:
                # Calcular datos
                x1, y1 = coords[0]
                x2, y2 = coords[1]
                top = min(y1, y2)
                left = min(x1, x2)
                width = abs(x1 - x2)
                height = abs(y1 - y2)
                
                print("\n" + "="*40)
                print("¡CALIBRACIÓN COMPLETADA!")
                print("Copia y pega esto en tu src/config.py:")
                print("="*40)
                print(f"BOARD_REGION = {{")
                print(f'    "top": {top},')
                print(f'    "left": {left},')
                print(f'    "width": {width},')
                print(f'    "height": {height}')
                print(f"}}")
                print("="*40)
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()