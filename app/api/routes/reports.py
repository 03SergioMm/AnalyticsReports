from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, Literal
from app.utils.auth import require_role
from app.utils.export import dataframe_to_csv_response, dataframe_to_excel_response
from app.services.ventas_service import VentasService
from app.services.pedidos_service import PedidosService
from app.services.productos_service import ProductosService
from app.services.metricas_service import MetricasService

router = APIRouter()

ventas_svc   = VentasService()
pedidos_svc  = PedidosService()
productos_svc = ProductosService()
metricas_svc = MetricasService()


@router.get("/ventas", summary="Reporte de ventas agrupadas por día")
def reporte_ventas(
    fecha_inicio: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_fin:    Optional[str] = Query(None, description="YYYY-MM-DD"),
    metodo_pago:  Optional[str] = Query(None, description="CASH | CARD | TRANSFER"),
    format: Optional[Literal["json", "csv", "xlsx"]] = Query("json"),
    _user=Depends(require_role),
):
    try:
        if format == "json":
            return ventas_svc.get_reporte_ventas(fecha_inicio, fecha_fin, metodo_pago)
        df = ventas_svc.get_dataframe_ventas(fecha_inicio, fecha_fin, metodo_pago)
        if format == "csv":
            return dataframe_to_csv_response(df, "ventas")
        return dataframe_to_excel_response(df, "ventas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pedidos", summary="Reporte de pedidos con filtros")
def reporte_pedidos(
    estado:       Optional[str] = Query(None, description="PENDING | ACCEPTED | IN_PROGRESS | READY | CANCELLED_BY_EMPLOYEE"),
    fecha_inicio: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_fin:    Optional[str] = Query(None, description="YYYY-MM-DD"),
    metodo_pago:  Optional[str] = Query(None, description="CASH | CARD | TRANSFER"),
    format: Optional[Literal["json", "csv", "xlsx"]] = Query("json"),
    _user=Depends(require_role),
):
    try:
        if format == "json":
            return pedidos_svc.get_reporte_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)
        df = pedidos_svc.get_dataframe_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)
        if format == "csv":
            return dataframe_to_csv_response(df, "pedidos")
        return dataframe_to_excel_response(df, "pedidos")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/productos-top", summary="Top productos más vendidos")
def productos_top(
    categoria:    Optional[str] = Query(None, description="Nombre categoría"),
    fecha_inicio: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_fin:    Optional[str] = Query(None, description="YYYY-MM-DD"),
    limit: int = Query(10, ge=1, le=50),
    format: Optional[Literal["json", "csv", "xlsx"]] = Query("json"),
    _user=Depends(require_role),
):
    try:
        if format == "json":
            return productos_svc.get_productos_top(categoria, fecha_inicio, fecha_fin, limit)
        df = productos_svc.get_dataframe_productos(categoria, fecha_inicio, fecha_fin, limit)
        if format == "csv":
            return dataframe_to_csv_response(df, "productos_top")
        return dataframe_to_excel_response(df, "productos_top")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metricas", summary="Métricas resumen del negocio")
def metricas(
    fecha_inicio: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_fin:    Optional[str] = Query(None, description="YYYY-MM-DD"),
    _user=Depends(require_role),
):
    try:
        return metricas_svc.get_metricas(fecha_inicio, fecha_fin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export", summary="Exportación consolidada de reportes")
def export_reporte(
    reporte: Literal["ventas", "pedidos", "productos"] = Query("ventas"),
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin:    Optional[str] = Query(None),
    estado:       Optional[str] = Query(None),
    categoria:    Optional[str] = Query(None),
    metodo_pago:  Optional[str] = Query(None),
    format: Literal["json", "csv", "xlsx"] = Query("csv"),
    _user=Depends(require_role),
):
    try:
        if reporte == "ventas":
            df = ventas_svc.get_dataframe_ventas(fecha_inicio, fecha_fin, metodo_pago)
            nombre = "ventas"
        elif reporte == "pedidos":
            df = pedidos_svc.get_dataframe_pedidos(estado, fecha_inicio, fecha_fin, metodo_pago)
            nombre = "pedidos"
        else:
            df = productos_svc.get_dataframe_productos(categoria, fecha_inicio, fecha_fin)
            nombre = "productos_top"

        if format == "json":
            return df.to_dict(orient="records")
        if format == "csv":
            return dataframe_to_csv_response(df, nombre)
        return dataframe_to_excel_response(df, nombre)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/debug/tablas", summary="Diagnóstico - contar registros por tabla")
def debug_tablas(_user=Depends(require_role)):
    from sqlalchemy import text
    from app.db.database import get_engine

    tablas = ["`order`", "order_item", "payment", "user", "product", "burger"]
    resultado = {}

    with get_engine().connect() as conn:
        for tabla in tablas:
            try:
                r = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
                resultado[tabla.replace("`", "")] = r.fetchone()[0]
            except Exception as e:
                resultado[tabla.replace("`", "")] = f"ERROR: {str(e)}"

    return resultado
