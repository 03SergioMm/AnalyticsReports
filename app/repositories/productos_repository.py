import pandas as pd
from sqlalchemy import text
from app.db.database import get_engine
from typing import Optional


class ProductosRepository:

    def get_productos_top(
        self,
        categoria: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 10,
    ) -> pd.DataFrame:
        query = """
            SELECT
                oi.item_name,
                oi.item_type,
                pc.product_category_name   AS categoria,
                SUM(oi.quantity)           AS total_vendidos,
                SUM(oi.subtotal)           AS total_ingresos,
                AVG(oi.unit_price)         AS precio_promedio
            FROM order_item oi
            JOIN `order` o   ON o.id_order   = oi.id_order
            LEFT JOIN product pr ON pr.id_product = oi.id_product
            LEFT JOIN product_category pc
                   ON pc.id_product_category = pr.id_product_category
            WHERE o.deleted_at IS NULL
        """
        params: dict = {}

        if categoria:
            query += " AND pc.product_category_name LIKE :categoria"
            params["categoria"] = f"%{categoria}%"
        if fecha_inicio:
            query += " AND DATE(o.order_date) >= :fecha_inicio"
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            query += " AND DATE(o.order_date) <= :fecha_fin"
            params["fecha_fin"] = fecha_fin

        query += f"""
            GROUP BY oi.item_name, oi.item_type, pc.product_category_name
            ORDER BY total_vendidos DESC
            LIMIT {int(limit)}
        """

        with get_engine().connect() as conn:
            result = conn.execute(text(query), params)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
