from pydantic import BaseModel
from typing import Optional, List


class VentasResponse(BaseModel):
    fecha_inicio: Optional[str]
    fecha_fin: Optional[str]
    total_general: float
    numero_pedidos: int
    ticket_promedio: float
    detalle: List[dict]


class PedidosResponse(BaseModel):
    total_pedidos: int
    filtros: dict
    distribucion_por_estado: List[dict]
    detalle: List[dict]


class ProductosTopResponse(BaseModel):
    categoria_filtro: Optional[str]
    top: List[dict]


class MetricasResponse(BaseModel):
    total_ventas: float
    total_pedidos: int
    ticket_promedio: float
    pedidos_por_estado: dict
    ingresos_por_metodo_pago: dict
    periodo: dict
