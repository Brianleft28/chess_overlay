import cv2
import numpy as np
import mss
from typing import Dict, List # Importamos List para el tipado

class ChessObserver:
    def __init__(self, region: Dict[str, int]):
        self.region = region
        self.sct = mss.mss()

    def capture_frame(self) -> np.ndarray:
        screenshot = self.sct.grab(self.region)
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def draw_grid(self, frame: np.ndarray) -> np.ndarray:
        # ... (este código ya lo tienes, déjalo igual) ...
        height, width, _ = frame.shape
        step_x = width // 8
        step_y = height // 8
        color = (0, 255, 0)
        for i in range(1, 8):
            cv2.line(frame, (step_x * i, 0), (step_x * i, height), color, 2)
            cv2.line(frame, (0, step_y * i), (width, step_y * i), color, 2)
        return frame

    # --- AGREGA ESTO NUEVO ---
    def extract_squares(self, frame: np.ndarray) -> List[np.ndarray]:
        """
        Corta el tablero en 64 imágenes individuales.
        """
        squares = []
        height, width, _ = frame.shape
        
        # Calculamos el tamaño exacto de cada casilla (aprox 52px)
        sq_h = height // 8
        sq_w = width // 8
        MARGIN = 3 

        for row in range(8):
            for col in range(8):
                # Coordenada base
                y1 = row * sq_h
                y2 = y1 + sq_h
                x1 = col * sq_w
                x2 = x1 + sq_w
                
                # Coordenada con Margen (La Guillotina)
                # Sumamos al inicio y restamos al final para "encoger" la visión
                safe_y1 = y1 + MARGIN
                safe_y2 = y2 - MARGIN
                safe_x1 = x1 + MARGIN
                safe_x2 = x2 - MARGIN
                
                # Validación para no romper nada si el margen es muy grande
                if safe_y2 > safe_y1 and safe_x2 > safe_x1:
                    square_img = frame[safe_y1:safe_y2, safe_x1:safe_x2]
                    squares.append(square_img)
        
        return squares