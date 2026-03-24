import pandas as pd
from typing import Optional
from app.repositories.ventas_repository import VentasRepository


class VentasService:
    def __init__(self):
        self.repo = VentasRepository()

    def get_reporte_ventas(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        metodo_pago: Optional[str] = None,
    ) -> dict:
        df = self.repo.get_ventas(fecha_inicio, fecha_fin, metodo_pago)

        if df.empty:
            return {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_general": 0.0,
                "numero_pedidos": 0,
                "ticket_promedio": 0.0,
                "detalle": [],
            }

        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")

        agrupado = (
            df.groupby("fecha")
            .agg(
                numero_pedidos=("id_order", "count"),
                total_ventas=("total_amount", "sum"),
                ticket_promedio=("total_amount", "mean"),
            )
            .reset_index()
            .sort_values("fecha", ascending=False)
        )

        agrupado["total_ventas"] = agrupado["total_ventas"].round(2)
        agrupado["ticket_promedio"] = agrupado["ticket_promedio"].round(2)

        return {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "total_general": round(float(df["total_amount"].sum()), 2),
            "numero_pedidos": int(len(df)),
            "ticket_promedio": round(float(df["total_amount"].mean()), 2),
            "detalle": agrupado.to_dict(orient="records"),
        }

    def get_dataframe_ventas(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        metodo_pago: Optional[str] = None,
    ) -> pd.DataFrame:
        return self.repo.get_ventas(fecha_inicio, fecha_fin, metodo_pago)
