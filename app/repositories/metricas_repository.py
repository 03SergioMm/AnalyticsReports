import pandas as pd
from sqlalchemy import text
from app.db.database import get_engine
from typing import Optional

# Estados que representan una venta confirmada
ESTADOS_CONFIRMADOS = "('ACCEPTED', 'IN_PROGRESS', 'READY')"


class MetricasRepository:

    def get_resumen_general(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
    ) -> pd.DataFrame:
        query = f"""
            SELECT
                COUNT(o.id_order)     AS total_pedidos,
                SUM(o.total_amount)   AS total_ventas,
                AVG(o.total_amount)   AS ticket_promedio,
                MIN(o.total_amount)   AS pedido_minimo,
                MAX(o.total_amount)   AS pedido_maximo
            FROM `order` o
            WHERE o.deleted_at IS NULL
              AND o.status IN {ESTADOS_CONFIRMADOS}
        """
        params: dict = {}
        if fecha_inicio:
            query += " AND DATE(o.order_date) >= :fecha_inicio"
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            query += " AND DATE(o.order_date) <= :fecha_fin"
            params["fecha_fin"] = fecha_fin

        with get_engine().connect() as conn:
            result = conn.execute(text(query), params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_pedidos_por_estado(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
    ) -> pd.DataFrame:
        # Este sí muestra TODOS los estados para ver distribución completa
        query = """
            SELECT
                o.status              AS estado,
                COUNT(o.id_order)     AS cantidad,
                SUM(o.total_amount)   AS total_monto
            FROM `order` o
            WHERE o.deleted_at IS NULL
        """
        params: dict = {}
        if fecha_inicio:
            query += " AND DATE(o.order_date) >= :fecha_inicio"
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            query += " AND DATE(o.order_date) <= :fecha_fin"
            params["fecha_fin"] = fecha_fin
        query += " GROUP BY o.status"

        with get_engine().connect() as conn:
            result = conn.execute(text(query), params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_ingresos_por_metodo_pago(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
    ) -> pd.DataFrame:
        query = f"""
            SELECT
                p.payment_method      AS metodo_pago,
                COUNT(p.id_payment)   AS cantidad_transacciones,
                SUM(p.amount)         AS total_recaudado
            FROM payment p
            JOIN `order` o ON o.id_order = p.id_order
            WHERE o.deleted_at IS NULL
              AND o.status IN {ESTADOS_CONFIRMADOS}
        """
        params: dict = {}
        if fecha_inicio:
            query += " AND DATE(o.order_date) >= :fecha_inicio"
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            query += " AND DATE(o.order_date) <= :fecha_fin"
            params["fecha_fin"] = fecha_fin
        query += " GROUP BY p.payment_method"

        with get_engine().connect() as conn:
            result = conn.execute(text(query), params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())