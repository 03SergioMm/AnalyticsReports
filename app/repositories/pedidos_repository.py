import pandas as pd
from sqlalchemy import text
from app.db.database import get_engine
from typing import Optional


class PedidosRepository:

    def get_pedidos(
        self,
        estado: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        metodo_pago: Optional[str] = None,
    ) -> pd.DataFrame:
        query = """
            SELECT
                o.id_order,
                o.order_number,
                o.status              AS estado,
                o.subtotal,
                o.total_amount,
                o.order_date,
                DATE(o.order_date)    AS fecha,
                u.name                AS nombre_cliente,
                u.email               AS email_cliente,
                p.payment_method      AS metodo_pago,
                p.amount              AS monto_pagado,
                p.paid_at
            FROM `order` o
            LEFT JOIN user u    ON u.id_user   = o.id_user
            LEFT JOIN payment p ON p.id_order  = o.id_order
            WHERE o.deleted_at IS NULL
        """
        params: dict = {}

        if estado:
            query += " AND o.status = :estado"
            params["estado"] = estado.upper()
        if fecha_inicio:
            query += " AND DATE(o.order_date) >= :fecha_inicio"
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            query += " AND DATE(o.order_date) <= :fecha_fin"
            params["fecha_fin"] = fecha_fin
        if metodo_pago:
            query += " AND p.payment_method = :metodo_pago"
            params["metodo_pago"] = metodo_pago.upper()

        query += " ORDER BY o.order_date DESC"

        with get_engine().connect() as conn:
            result = conn.execute(text(query), params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
