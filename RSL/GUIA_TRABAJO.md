# Guía de trabajo — RSL v2 (Grupo 4)

## Dónde está cada cosa

| Qué | Dónde | Cómo se trabaja |
|---|---|---|
| **Cribado completo** (búsqueda, Parsif.al, piloto, título/resumen, texto completo, PRISMA, calidad) | `RSL/cribado/README.md` | Scripts de Python, paso a paso |
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

### Reglas para no pisarse
1. Siempre `git pull` antes de empezar y antes de `git push`.
2. **Los Excel no se pueden fusionar.** Cada revisor edita **solo su archivo** (`..._R1.xlsx` o `..._R2.xlsx`). Los `consolidado_*.xlsx` los edita solo el coordinador, en la reunión de consenso.
3. **Cribado independiente:** no abran la hoja del otro revisor, aunque esté en el repositorio.
4. No editen a mano `RSL/manuscrito/generado/` ni las cifras de `datos_busqueda.tex`: los escriben los scripts.
5. Los PDF de los artículos (`RSL/cribado/pdf/` y `RSL/Articulos evaluados por calidad/`) **no se publican**, porque tienen derechos de autor.
6. **OneDrive:** si crea archivos duplicados como `archivo-PC.xlsx` o marca conflictos, no los suban. Si da problemas, muevan el repositorio a `C:\repos\rsl-wilbert`.
7. Si `git pull` dice **CONFLICT**, no sigan: copien el mensaje y pídanme ayuda.

### Comandos útiles

| Quiero… | Comando |
|---|---|
| Ver qué cambié | `git status` |
| Deshacer cambios de un archivo no subido | `git restore RSL\ruta\archivo` |
| Ver el historial | `git log --oneline -10` |
| Ver la versión anterior (v1) | `git checkout main` (para volver: `git checkout claude/loving-volta-papmwq`) |

## Programas necesarios
- **Git** (ya instalado).
- **Python 3** (https://www.python.org, marcar *Add Python to PATH*) y luego `pip install openpyxl`.
- **Overleaf** (en el navegador) para el manuscrito. No hace falta instalar LaTeX.
