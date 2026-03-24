import pandas as pd
from typing import Optional
from app.repositories.metricas_repository import MetricasRepository


class MetricasService:
    def __init__(self):
        self.repo = MetricasRepository()

    def get_metricas(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
    ) -> dict:
        df_resumen = self.repo.get_resumen_general(fecha_inicio, fecha_fin)
        df_estados = self.repo.get_pedidos_por_estado(fecha_inicio, fecha_fin)
        df_pagos   = self.repo.get_ingresos_por_metodo_pago(fecha_inicio, fecha_fin)

        resumen       = df_resumen.iloc[0] if not df_resumen.empty else {}
        total_ventas  = float(resumen.get("total_ventas")  or 0)
        total_pedidos = int(resumen.get("total_pedidos")   or 0)
        ticket_prom   = float(resumen.get("ticket_promedio") or 0)

        pedidos_por_estado = {}
        if not df_estados.empty:
            for _, row in df_estados.iterrows():
                pedidos_por_estado[row["estado"]] = {
                    "cantidad":    int(row["cantidad"]),
                    "total_monto": round(float(row["total_monto"]), 2),
                }

        ingresos_pago = {}
        if not df_pagos.empty:
            for _, row in df_pagos.iterrows():
                ingresos_pago[row["metodo_pago"]] = {
                    "transacciones":    int(row["cantidad_transacciones"]),
                    "total_recaudado":  round(float(row["total_recaudado"]), 2),
                }

        return {
            "total_ventas":             round(total_ventas, 2),
            "total_pedidos":            total_pedidos,
            "ticket_promedio":          round(ticket_prom, 2),
            "pedidos_por_estado":       pedidos_por_estado,
            "ingresos_por_metodo_pago": ingresos_pago,
            "periodo": {
                "fecha_inicio": fecha_inicio or "desde el inicio",
                "fecha_fin":    fecha_fin    or "hasta hoy",
            },
        }
