import chess
import chess.engine
import os

class ChessEngine:
    def __init__(self, engine_path="stockfish.exe"):
        if not os.path.exists(engine_path):
            raise FileNotFoundError(f"⚠️ NO ENCUENTRO A STOCKFISH. Asegúrate de que '{engine_path}' esté junto a main.py")
        
        try:
            # Hash 32MB es ligero y rápido
            self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            self.engine.configure({"Hash": 32}) 
            print(f"🤖 Motor conectado: Stockfish está listo.")
        except Exception as e:
            print(f"❌ Error fatal al iniciar Stockfish: {e}")
            self.engine = None

    def get_best_move(self, fen, time_limit=0.1):
        if not self.engine: return None

        try:
            board = chess.Board(fen)
            # Limitamos el tiempo para que responda al toque
            result = self.engine.play(board, chess.engine.Limit(time=time_limit))
            return str(result.move)
        except chess.engine.EngineTerminatedError:
            print("💀 El motor murió inesperadamente.")
            self.engine = None 
            return None
        except Exception as e:
            print(f"⚠️ Error analizando: {e}")
            return None

    def quit(self):
        # Esta es la corrección: Preguntamos antes de disparar
        if self.engine:
            try:
                self.engine.quit()
            except:
                pass 