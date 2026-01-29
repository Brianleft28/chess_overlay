import cv2
import numpy as np
import mss
from src.config import CLOCK_OPPONENT, CLOCK_PLAYER, MOTION_THRESHOLD

class TurnManager:
    def __init__(self):
        self.sct = mss.mss()
        self.prev_opp_img = None
        self.prev_player_img = None

    def _grab_region(self, region):
        scr = self.sct.grab(region)
        img = np.array(scr)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        return img

    def update_turn(self):
        """
        Detecta movimiento en los relojes.
        Retorna: 'top_clock_active', 'bottom_clock_active' o None.
        """
        curr_opp = self._grab_region(CLOCK_OPPONENT)
        curr_player = self._grab_region(CLOCK_PLAYER)

        if self.prev_opp_img is None:
            self.prev_opp_img = curr_opp
            self.prev_player_img = curr_player
            return None

        # Diferencia matemática
        diff_opp = cv2.absdiff(curr_opp, self.prev_opp_img)
        diff_player = cv2.absdiff(curr_player, self.prev_player_img)

        score_opp = np.sum(diff_opp)
        score_player = np.sum(diff_player)

        detected = None
        
        # Usamos el umbral definido en config.py (Recomendado: 50)
        if score_opp > MOTION_THRESHOLD:
            detected = "top_clock_active"
        elif score_player > MOTION_THRESHOLD:
            detected = "bottom_clock_active"

        # Actualizamos referencias
        self.prev_opp_img = curr_opp
        self.prev_player_img = curr_player
        
        return detected