def generate_fen(board_matrix, active_color="w"): # <--- AQUI ESTABA EL ERROR (Faltaba este argumento)
    """
    Traduce tu matriz de nombres a notación FEN estándar.
    Recibe el estado del tablero y de quién es el turno ('w' o 'b').
    """
    fen_rows = []

    # Diccionario de traducción: Tu Nombre -> Letra FEN
    piece_map = {
        "tn": "r", "cn": "n", "an": "b", "qn": "q", "rn": "k", "pn": "p",
        "tb": "R", "cb": "N", "ab": "B", "qb": "Q", "rb": "K", "pb": "P"
    }

    for row in range(8):
        start = row * 8
        end = start + 8
        row_data = board_matrix[start:end]
        
        fen_row = ""
        empty_count = 0

        for item in row_data:
            # item es algo como "tn_b" o "fondo_vacio_blanco"
            
            # Detectamos si es vacío
            if "vacio" in item:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                
                # Traducimos la pieza
                # "tn_b" -> parts[0] es "tn"
                parts = item.split("_")
                identity = parts[0] 
                
                if identity in piece_map:
                    fen_row += piece_map[identity]
                else:
                    fen_row += "?"

        if empty_count > 0:
            fen_row += str(empty_count)
            
        fen_rows.append(fen_row)

    position = "/".join(fen_rows)
    
    # Usamos la variable active_color para definir el turno en el string final
    return f"{position} {active_color} KQkq - 0 1"