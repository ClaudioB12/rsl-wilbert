# Re-cribado ciego (fiabilidad intra-revisor)

Como el cribado lo hizo un solo revisor, la consistencia se mide repitiendo una muestra aleatoria
**sin mirar las decisiones anteriores** y calculando el kappa entre las dos pasadas (se reporta en el artículo).

| Etapa | Archivo | Muestra | Hacerlo desde |
|---|---|---|---|
| Título y resumen | `cribado/revision/recribado_TA.xlsx` | 100 registros | 28/10/2026 (≥ 7 días después del cribado TA) |
| Texto completo | `cribado/revision/recribado_TC.xlsx` | 30 registros | 03/11/2026 (≥ 7 días después del cribado TC) |

## Reglas
1. **No abras** `TA.xlsx`, `REVISION_TEXTO_COMPLETO.xlsx`, Parsif.al ni chats anteriores mientras lo haces.
2. **No uses la IA**: el kappa mide tu consistencia, no la de la IA.
3. Aplica los criterios en el orden fijo (CE-1, CE-5, CI-3, CI-2, CE-2, CE-3, CE-4; en TC también CI-6 y CE-6).
4. TA: llena `DECISIÓN` (Incluir / Duda / Excluir) y `CRITERIO` si excluyes.
   TC: abre el PDF, llena `Texto completo` = Sí, `DECISIÓN` (Incluir / Excluir), `CRITERIO` y `EVIDENCIA` (cita y página).

## Al terminar
```
python cribado/scripts/04b_recribado.py --etapa TA --calcular
python cribado/scripts/04b_recribado.py --etapa TC --calcular
python cribado/scripts/06_resultados_prisma.py
```
El kappa queda en `cribado/salida/fiabilidad.json` y en las macros del manuscrito. Si aparecen discrepancias,
revisa esos registros: si la primera decisión estaba mal, se corrige y se documenta.
