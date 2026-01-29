def auto_detect_player_color(board_state):
    """
    Escanea las filas inferiores (6 y 7) del tablero para encontrar al Rey.
    Retorna 'w' si encuentra Rey Blanco, 'b' si encuentra Rey Negro.
    Retorna None si no encuentra ninguno (ej: tablero vacío o error).
    """
    # El tablero es una lista de 64 elementos.
    # Las filas 6 y 7 (donde empieza el jugador) son los índices del 48 al 63.
    player_zone = board_state[48:]
    
    for piece in player_zone:
        # piece es un string tipo "rn_b" (Rey Negro en Blanco) o "rb_n", etc.
        
        if piece.startswith("rb"): 
            return "w" # Rey Blanco detectado en zona de jugador
            
        if piece.startswith("rn"): 
            return "b" # Rey Negro detectado en zona de jugador
            
    return None