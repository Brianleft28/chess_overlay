import cv2
import mss
import numpy as np
from config import CLOCK_OPPONENT, CLOCK_PLAYER

def main():
    sct = mss.mss()
    print("--- DEPURADOR DE RELOJES ---")
    print("Presiona 'q' para salir.")
    print(f"Oponente: {CLOCK_OPPONENT}")
    print(f"Jugador:  {CLOCK_PLAYER}")

    while True:
        # Capturamos las zonas definidas en config.py
        scr_opp = sct.grab(CLOCK_OPPONENT)
        scr_player = sct.grab(CLOCK_PLAYER)
        
        # Convertimos a formato imagen
        img_opp = np.array(scr_opp)
        img_player = np.array(scr_player)

        # Mostramos las ventanas
        cv2.imshow("OJO RELOJ OPONENTE", img_opp)
        cv2.imshow("OJO RELOJ JUGADOR", img_player)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()