import pandas as pd
from typing import Optional
from app.repositories.productos_repository import ProductosRepository


class ProductosService:
    def __init__(self):
        self.repo = ProductosRepository()

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

        df["total_vendidos"] = pd.to_numeric(df["total_vendidos"], errors="coerce").fillna(0).astype(int)
        df["total_ingresos"] = pd.to_numeric(df["total_ingresos"], errors="coerce").fillna(0).round(2)
        df["precio_promedio"] = pd.to_numeric(df["precio_promedio"], errors="coerce").fillna(0).round(2)

        df_sorted = df.sort_values("total_vendidos", ascending=False).head(limit)

        return {
            "categoria_filtro": categoria,
            "top": df_sorted.to_dict(orient="records"),
        }

    def get_dataframe_productos(
        self,
        categoria: Optional[str] = None,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 10,
    ) -> pd.DataFrame:
        return self.repo.get_productos_top(categoria, fecha_inicio, fecha_fin, limit)
