# Guía de trabajo — RSL v2 (autor único: Wilbert A. Mayta Arotaype)

## Dónde está cada cosa

| Qué | Dónde | Cómo se trabaja |
|---|---|---|
| **Guía completa desde cero** (Python, Parsif.al, búsqueda, cribado asistido, PRISMA, calidad, OSF, Overleaf) | `RSL/cribado/README.md` | Paso a paso, en orden |
| **Textos de Parsif.al** | `RSL/cribado/PARSIFAL_COPIAR_PEGAR.md` | Copiar y pegar |
| **Criterios de inclusión y exclusión** (definiciones, fundamento y ejemplos) | `RSL/cribado/MANUAL_CRIBADO.md` | Leer antes de cribar |
| **Manuscrito** | Overleaf (se crea con `cribado/scripts/08_paquete_overleaf.py`) | Redacción en Overleaf; las cifras las generan los scripts |
| Matriz de extracción y calidad | `RSL/suplementos/` | Scripts (`generar_conteos.py`) |
| Respuesta al ingeniero | `RSL/respuesta_revision.docx` | La actualizamos al final |
| Pendientes | `RSL/PENDIENTES.md` | Lista de control |

## Git: rutina de todos los días

**Al empezar:**
```bat
cd "C:\Users\mayta\OneDrive\Documents\Cursos\2026-2\Investigación IV\rsl-wilbert"
git checkout claude/loving-volta-papmwq
git pull
```
**Al terminar cada avance:**
```bat
git add RSL
git commit -m "Qué hiciste"
git pull
git push
```

### Reglas
1. Sube tu avance a GitHub al final de cada día (`git add RSL`, `git commit`, `git push`).
2. No edites a mano `RSL/manuscrito/generado/` ni las cifras de `datos_busqueda.tex`: los escriben los scripts.
3. Los PDF de los artículos (`RSL/cribado/pdf/` y `RSL/Articulos evaluados por calidad/`) **no se publican**, porque tienen derechos de autor.
4. **OneDrive:** si crea archivos duplicados como `archivo-PC.xlsx`, no los subas. Si da problemas, mueve el repositorio a `C:\repos\rsl-wilbert`.
5. Si Git muestra **CONFLICT** o un error, copia el mensaje y pégamelo en el chat.

### Comandos útiles

| Quiero… | Comando |
|---|---|
| Ver qué cambié | `git status` |
| Deshacer cambios de un archivo no subido | `git restore RSL\ruta\archivo` |
| Ver el historial | `git log --oneline -10` |
| Ver la versión anterior (v1) | `git checkout main` (para volver: `git checkout claude/loving-volta-papmwq`) |

## Programas necesarios
- **Git** (ya instalado).
- **Python 3** (https://www.python.org, marcar *Add Python to PATH*) y luego `pip install openpyxl pypdf`.
- **Overleaf** (en el navegador) para el manuscrito. No hace falta instalar LaTeX.
