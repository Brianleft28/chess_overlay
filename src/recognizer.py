import cv2
import os
import numpy as np

class ChessRecognizer:
    def __init__(self, assets_folder="assets"):
        self.library_list = [] 
        self.load_assets(assets_folder)

    def load_assets(self, folder):
        """Carga imágenes y normaliza nombres (ignora _h)"""
        if not os.path.exists(folder):
            print(f"⚠️ Error: No encuentro la carpeta '{folder}'")
            return

        print(f"--- Cargando Cerebro desde {folder} ---")
        count = 0
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                # Ruta completa
                path = os.path.join(folder, filename)
                img = cv2.imread(path)
                
                # --- NORMALIZACIÓN ---
                # Quitamos extensión y sufijo _h (highlight)
                # Ejemplo: "pb_b_h.png" -> "pb_b"
                raw_name = os.path.splitext(filename)[0]
                piece_id = raw_name.replace("_h", "")
                
                # Guardamos en la lista
                self.library_list.append((piece_id, img))
                count += 1
        
        print(f"✅ Cerebro listo: {count} referencias en memoria.")

    def find_piece(self, square_img):
        """Compara la imagen entrante con TODA la librería"""
        best_match = "unknown"
        min_error = float('inf')

        for name, ref_img in self.library_list:
            # Validación de dimensiones
            if square_img.shape != ref_img.shape:
                continue

            # Diferencia matemática de píxeles
            diff = cv2.absdiff(square_img, ref_img)
            error_score = np.sum(diff)

            if error_score < min_error:
                min_error = error_score
                best_match = name

        return best_match