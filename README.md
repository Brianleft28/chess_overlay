
# Søren Mirror ♟️👁️
## Chess Overlay

Sistema de Análisis y Visión Artificial en Tiempo Real para Ajedrez

Søren Mirror es una herramienta avanzada de "Realidad Aumentada" para el escritorio. Utiliza visión por computadora para observar una partida de ajedrez en pantalla (ej. Chess.com), interpretar el estado del tablero, gestionar los turnos automáticamente y consultar al motor Stockfish para sugerir jugadas en tiempo real a través de un HUD (Heads-Up Display) flotante.

---

## 🚀 Características Principales

- **Visión Artificial (OpenCV):** Detecta piezas y casillas vacías mediante coincidencia de patrones y análisis de píxeles, sin inyectar código en el navegador (indetectable por métodos tradicionales de scraping).
- **Gestión Automática de Turnos:** Monitorea los relojes de la partida para detectar cambios de turno con precisión de milisegundos.
- **Detección de Color y Perspectiva:** Identifica automáticamente si el usuario juega con Blancas o Negras y ajusta la geometría del tablero (inversión de matriz) para generar el FEN correcto.
- **Integración con Stockfish:** Conecta con el motor de ajedrez más potente del mundo para análisis táctico instantáneo.
- **HUD "Always on Top":** Interfaz gráfica flotante que se superpone al navegador sin bloquear la interacción con el tablero.
- **Modo Stealth/Seguro:** Sistema de pausa (Standby) y validación de integridad del tablero para evitar bloqueos por falsos positivos.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Visión:** OpenCV (cv2), MSS (Captura de pantalla de alta velocidad)
- **Lógica de Ajedrez:** python-chess
- **Motor de IA:** Stockfish 16+ (AVX2)
- **Interfaz:** OpenCV HighGUI

---

## ⚙️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Brianleft28/chess_overlay.git
   cd soren-mirror
   ```
2. **Entorno Virtual (Recomendado)**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```
3. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   > Nota: Asegúrate de que opencv-python, python-chess, mss y numpy estén en tu requirements.txt
4. **Configurar el Motor (Stockfish)**
   - Descarga Stockfish desde [stockfishchess.org](https://stockfishchess.org/).
   - Extrae el archivo .exe.
   - Renómbralo a `stockfish.exe`.
   - Colócalo en la carpeta raíz del proyecto (junto a main.py).

---

## 🔧 Configuración de Coordenadas

Antes de la primera ejecución, el bot necesita saber en qué parte de tu pantalla está el tablero.

1. Abre tu navegador en la página de juego (ej. Chess.com) y ajusta el zoom al 100%.
2. Edita el archivo `src/config.py` con las coordenadas de tu monitor para:
   - `BOARD_REGION`: El área del tablero (x, y, width, height).
   - `CLOCK_OPPONENT`: El área del reloj del rival.
   - `CLOCK_PLAYER`: El área de tu reloj.
3. Asegúrate de que los assets (imágenes de referencia en `assets/`) coincidan con el tema visual de tu tablero.

---

## 🎮 Instrucciones de Uso

Ejecuta el script principal:
```bash
python main.py
```
Aparecerá la ventana "Soren Mirror - HUD".

Acomoda la ventana: Muévela a una esquina donde no tape el tablero.

### Controles de Teclado

> El foco debe estar en la ventana del HUD

| Tecla | Acción           | Descripción                                                        |
|-------|------------------|--------------------------------------------------------------------|
| i     | Iniciar / Pausar | Activa/Desactiva el modo automático. Úsalo al empezar la partida.  |
| v     | Cambiar Vista    | Alterna entre modo "Debug" (video en vivo) y modo "Pro" (fondo negro minimalista). |
| s     | Snapshot         | Guarda una captura del estado actual en `debug_squares/` (útil para re-entrenar la visión). |
| q     | Salir            | Cierra el programa y apaga el motor Stockfish.                     |

---

### Flujo de Trabajo Ideal

1. Abre el programa (Estado: PAUSADO).
2. Empieza la partida en el navegador.
3. Presiona `i` cuando sea tu turno o el del oponente.
4. El bot detectará tu color, esperará al turno rival y, cuando sea tu turno, mostrará la mejor jugada (ej: e2e4) en amarillo neón.

---

## ⚠️ Disclaimer Ético

Este software fue desarrollado con fines educativos y de investigación en el campo de la Visión Artificial y la interacción humano-máquina.

El uso de asistencia por ordenador (engines) en partidas clasificatorias (Ranked) contra humanos está estrictamente prohibido en todas las plataformas de ajedrez online y puede resultar en la suspensión permanente de la cuenta.

El autor no se hace responsable del mal uso de esta herramienta. Se recomienda su uso exclusivamente contra la IA de la plataforma o en modo de análisis post-partida.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

💡 **Tip extra para ti, Brian:**

Como el README menciona requirements.txt, asegúrate de generarlo si no lo tienes. Corre esto en tu terminal:

```bash
pip freeze > requirements.txt
```
