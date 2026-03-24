import pandas as pd
import math
from typing import Optional
from app.repositories.productos_repository import ProductosRepository


class ProductosService:
    def __init__(self):
        self.repo = ProductosRepository()

    def _limpiar_valor(self, valor):
        """Convierte NaN, Infinity y None a 0 para que sea JSON serializable"""
        if valor is None:
            return 0
        try:
            if math.isnan(float(valor)) or math.isinf(float(valor)):
                return 0
        except (TypeError, ValueError):
            pass
        return valor

    def get_productos_top(
        self,
        categoria: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 10,
    ) -> dict:
        df = self.repo.get_productos_top(categoria, fecha_inicio, fecha_fin, limit)

        if df.empty:
            return {"categoria_filtro": categoria, "top": []}

        # Limpiar columnas numéricas — reemplaza NaN/Inf por 0
        df["total_vendidos"] = pd.to_numeric(df["total_vendidos"], errors="coerce").fillna(0).astype(int)
        df["total_ingresos"] = pd.to_numeric(df["total_ingresos"], errors="coerce").fillna(0).round(2)
        df["precio_promedio"] = pd.to_numeric(df["precio_promedio"], errors="coerce").fillna(0).round(2)

        # Limpiar columnas de texto — reemplaza NaN por string vacío
        df["categoria"] = df["categoria"].fillna("Sin categoría")
        df["item_type"] = df["item_type"].fillna("UNKNOWN")
        df["item_name"] = df["item_name"].fillna("Sin nombre")

        df_sorted = df.sort_values("total_vendidos", ascending=False).head(limit)

        # Convertir a dict y limpiar cualquier NaN residual
        registros = df_sorted.to_dict(orient="records")
        registros_limpios = [
            {k: self._limpiar_valor(v) for k, v in row.items()}
            for row in registros
        ]

        return {
            "categoria_filtro": categoria,
            "top": registros_limpios,
        }

    def get_dataframe_productos(
        self,
        categoria: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 10,
    ) -> pd.DataFrame:
        df = self.repo.get_productos_top(categoria, fecha_inicio, fecha_fin, limit)
        if not df.empty:
            df["categoria"] = df["categoria"].fillna("Sin categoría")
            df["total_vendidos"] = pd.to_numeric(df["total_vendidos"], errors="coerce").fillna(0).astype(int)
            df["total_ingresos"] = pd.to_numeric(df["total_ingresos"], errors="coerce").fillna(0).round(2)
            df["precio_promedio"] = pd.to_numeric(df["precio_promedio"], errors="coerce").fillna(0).round(2)
        return df
