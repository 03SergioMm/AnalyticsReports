import pandas as pd
from typing import Optional
from app.repositories.pedidos_repository import PedidosRepository


class PedidosService:
    def __init__(self):
        self.repo = PedidosRepository()

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
                },
                "distribucion_por_estado": [],
                "detalle": [],
            }

        df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)
        df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        por_estado = (
            df.groupby("estado")
            .agg(
                cantidad=("id_order", "count"),
                monto_total=("total_amount", "sum"),
            )
            .reset_index()
        )

        detalle = df[[
            "id_order", "order_number", "estado", "nombre_cliente",
            "email_cliente", "total_amount", "metodo_pago", "order_date",
        ]].to_dict(orient="records")

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
        return self.repo.get_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)
