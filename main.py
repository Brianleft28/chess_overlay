import cv2
import os
import time
import numpy as np
from src.config import BOARD_REGION, MOTION_THRESHOLD
from src.vision import ChessObserver
from src.recognizer import ChessRecognizer
from src.fen import generate_fen
from src.turn_manager import TurnManager
from src.utils import auto_detect_player_color
from src.engine import ChessEngine

# --- CONFIGURACIÓN ---
OUTPUT_FOLDER = "debug_squares"
ANIMATION_DELAY = 0.5
THINK_TIME = 0.5 
def scan_and_process(observer, recognizer, engine, current_turn, my_color, auto_update_color=False):
    print(f"\n⚡ Analizando posición... (Turno: {current_turn})")
    
    # 1. VISIÓN
    frame = observer.capture_frame()
    squares = observer.extract_squares(frame)
    board_state = []
    
    for sq_img in squares:
        piece = recognizer.find_piece(sq_img)
        board_state.append(piece)

    # 2. AUTO-COLOR
    new_my_color = my_color
    if auto_update_color:
        detected = auto_detect_player_color(board_state)
        # Importante: Si detecta cambio, actualizamos la variable local
        if detected and detected != my_color:
            print(f"🔄 Color corregido: Ahora eres {detected.upper()}")
            new_my_color = detected

    # --- CORRECCIÓN DE PERSPECTIVA (EL FIX) ---
    # Si somos negras, el tablero visual está rotado 180 grados.
    # El escáner leyó [h1, g1 ... a8], pero el FEN necesita [a8 ... h1].
    # Solución: Invertimos la lista completa.
    processing_board = list(board_state) # Hacemos una copia para no romper nada
    if new_my_color == "b":
        processing_board.reverse()
        print("🔄 Perspectiva invertida (Modo Negras)")
    # ------------------------------------------

    # 3. GENERAR FEN (Usamos la lista corregida 'processing_board')
    fen_code = generate_fen(processing_board, active_color=current_turn)
    print(f"FEN: {fen_code}")
    
    # --- FILTRO DE SEGURIDAD ---
    board_part = fen_code.split(' ')[0] 
    kings_count = board_part.lower().count('k')

    if kings_count > 2 or kings_count == 0:
        print(f"⚠️ ALERTA: Tablero inválido ({kings_count} reyes).")
        return new_my_color, None

    # 4. INTELIGENCIA
    best_move = None
    if engine:
        if engine.engine is None:
             print("♻️ Reviviendo motor...")
             try: engine.__init__("stockfish.exe")
             except: pass

        print("🧠 Consultando a Stockfish...")
        best_move = engine.get_best_move(fen_code, time_limit=THINK_TIME)
        
        if best_move:
            print(f"🚀 JUGADA: {best_move}")
    
    return new_my_color, best_move

def main():
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)

    observer = ChessObserver(BOARD_REGION)
    recognizer = ChessRecognizer("assets")
    turn_manager = TurnManager()
    
    try: engine = ChessEngine("stockfish.exe") 
    except: engine = None

    my_color = "w" 
    current_turn = "w"
    last_turn_state = "w"
    suggestion = ""
    is_active = False
    view_mode = "debug" # 'debug' = video real | 'pro' = fondo negro
    
    # Variables visuales para el "testigo" de los relojes
    clock_indicator = None # Puede ser 'top' o 'bottom'
    clock_timer = 0 # Para que el indicador dure un ratito en pantalla

    window_name = 'Soren Mirror - HUD'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 500, 500)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    print("\n--- SØREN MIRROR: ONLINE ---")
    print("Controles: 'i'=Iniciar/Pausar | 'v'=Cambiar Vista | 'q'=Salir")

    try:
        while True:
            frame = observer.capture_frame()
            
            # --- LÓGICA DE TURNOS ---
            activity = turn_manager.update_turn()
            
            # Gestión del indicador visual (el puntito azul)
            if activity:
                clock_indicator = activity
                clock_timer = 10 # El punto se queda visible 10 frames

            if is_active:
                if activity == "bottom_clock_active": 
                    current_turn = my_color
                elif activity == "top_clock_active": 
                    current_turn = "b" if my_color == "w" else "w"
                    
                if current_turn != last_turn_state:
                    print(f"⏱️ CAMBIO DE TURNO: {current_turn.upper()}")
                    time.sleep(ANIMATION_DELAY)
                    new_color, move = scan_and_process(
                        observer, recognizer, engine, current_turn, my_color, auto_update_color=True
                    )
                    my_color = new_color
                    last_turn_state = current_turn
                    
                    if current_turn == my_color and move: suggestion = move
                    else: suggestion = "" 

            # --- DIBUJADO DE INTERFAZ ---
            if view_mode == "debug":
                display_frame = observer.draw_grid(frame.copy())
            else:
                display_frame = np.zeros_like(frame)

            # Info Estado
            cv2.putText(display_frame, f"Soy: {my_color.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
            color_turno = (0, 255, 0) if current_turn == my_color else (0, 0, 255)
            cv2.putText(display_frame, f"Turno: {current_turn.upper()}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_turno, 2)
            
            if is_active: cv2.putText(display_frame, "AUTO: ON", (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else: cv2.putText(display_frame, "PAUSADO", (150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # --- DIBUJAR INDICADORES DE RELOJ (SENSORES) ---
            # Si clock_timer > 0, dibujamos un círculo azul indicando que el sensor "oyó" algo
            if clock_timer > 0:
                h, w, _ = display_frame.shape
                color_sensor = (255, 255, 0) # Cyan
                if clock_indicator == "top_clock_active":
                    # Círculo arriba a la derecha
                    cv2.circle(display_frame, (w - 30, 30), 10, color_sensor, -1)
                elif clock_indicator == "bottom_clock_active":
                    # Círculo abajo a la derecha
                    cv2.circle(display_frame, (w - 30, h - 30), 10, color_sensor, -1)
                clock_timer -= 1

            # Sugerencia Central
            if suggestion:
                h_img, w_img, _ = display_frame.shape
                # Caja de fondo
                cv2.rectangle(display_frame, (0, h_img//2 - 50), (w_img, h_img//2 + 50), (0,0,0), -1)
                # Texto
                text_size = cv2.getTextSize(suggestion, cv2.FONT_HERSHEY_SIMPLEX, 2, 4)[0]
                text_x = (w_img - text_size[0]) // 2
                cv2.putText(display_frame, suggestion, (text_x, h_img//2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

            cv2.imshow(window_name, display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break
            elif key == ord('v'): 
                view_mode = "pro" if view_mode == "debug" else "debug"
            elif key == ord('i'):
                is_active = not is_active
                if is_active:
                     my_color, _ = scan_and_process(observer, recognizer, engine, "w", "w", auto_update_color=True)
                     last_turn_state = my_color 
            elif key == ord('s'):
                squares = observer.extract_squares(frame)
                ts = int(time.time())
                for i, sq in enumerate(squares): cv2.imwrite(f"{OUTPUT_FOLDER}/{ts}_{i}.png", sq)

    except KeyboardInterrupt: pass
    finally:
        if engine: engine.quit()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()