import pandas as pd
import math
from typing import Optional
from app.repositories.pedidos_repository import PedidosRepository


class PedidosService:
    def __init__(self):
        self.repo = PedidosRepository()

    def _limpiar_valor(self, valor):
        """Convierte NaN, Infinity y None a valores JSON seguros"""
        if valor is None:
            return None
        try:
            if isinstance(valor, float) and (math.isnan(valor) or math.isinf(valor)):
                return None
        except (TypeError, ValueError):
            pass
        return valor

    def _limpiar_registro(self, registro: dict) -> dict:
        return {k: self._limpiar_valor(v) for k, v in registro.items()}

    def get_reporte_pedidos(
        self,
        estado: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        metodo_pago: Optional[str] = None,
    ) -> dict:
        df = self.repo.get_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)

        if df.empty:
            return {
                "total_pedidos": 0,
                "filtros": {
                    "estado": estado,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "metodo_pago": metodo_pago,
                },
                "distribucion_por_estado": [],
                "detalle": [],
            }

        # Limpiar numéricos
        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
        df["monto_pagado"] = pd.to_numeric(df["monto_pagado"], errors="coerce").fillna(0)

        # Limpiar fechas
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

        # Limpiar texto — NaN por None explícito
        df["metodo_pago"]     = df["metodo_pago"].where(df["metodo_pago"].notna(), None)
        df["nombre_cliente"]  = df["nombre_cliente"].where(df["nombre_cliente"].notna(), "Sin nombre")
        df["email_cliente"]   = df["email_cliente"].where(df["email_cliente"].notna(), "Sin email")
        df["paid_at"]         = df["paid_at"].where(df["paid_at"].notna(), None)

        # Distribución por estado
        por_estado = (
            df.groupby("estado")
            .agg(
                cantidad=("id_order", "count"),
                monto_total=("total_amount", "sum"),
            )
            .reset_index()
        )
        por_estado["monto_total"] = por_estado["monto_total"].round(2)

        # Detalle
        columnas = [
            "id_order", "order_number", "estado", "nombre_cliente",
            "email_cliente", "total_amount", "metodo_pago", "order_date",
        ]
        detalle_raw = df[columnas].to_dict(orient="records")
        detalle = [self._limpiar_registro(r) for r in detalle_raw]

        return {
            "total_pedidos": int(len(df)),
            "filtros": {
                "estado": estado,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "metodo_pago": metodo_pago,
            },
            "distribucion_por_estado": por_estado.to_dict(orient="records"),
            "detalle": detalle,
        }

    def get_dataframe_pedidos(
        self,
        estado: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        metodo_pago: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.repo.get_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)
        if not df.empty:
            df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
            df["monto_pagado"] = pd.to_numeric(df["monto_pagado"], errors="coerce").fillna(0)
            df["metodo_pago"]  = df["metodo_pago"].fillna("Sin pago")
            df["nombre_cliente"] = df["nombre_cliente"].fillna("Sin nombre")
            df["email_cliente"]  = df["email_cliente"].fillna("Sin email")
        return df
