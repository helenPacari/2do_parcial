import os
from openai import OpenAI
from app.models import Medicamento, Venta, DetalleVenta, Cliente, Categoria
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url='https://api.groq.com/openai/v1'
)

def obtener_estadisticas_sistema():
    """Obtiene estadísticas del sistema para análisis"""
    hoy = datetime.now().date()
    mes_inicio = datetime.now().replace(day=1).date()
    
    # Ventas del mes
    ventas_mes = Venta.query.filter(
        func.date(Venta.fecha) >= mes_inicio
    ).count()
    
    # Total ventas
    total_ventas = Venta.query.count()
    
    # Productos más vendidos
    productos_mas_vendidos = db.session.query(
        Medicamento.nombre,
        func.sum(DetalleVenta.cantidad).label('total_vendido')
    ).join(DetalleVenta).group_by(Medicamento.id).order_by(desc('total_vendido')).limit(5).all()
    
    # Categorías más populares
    categorias_populares = db.session.query(
        Categoria.nombre,
        func.count(Medicamento.id).label('total_productos')
    ).join(Medicamento).group_by(Categoria.id).order_by(desc('total_productos')).all()
    
    # Stock bajo
    stock_bajo = Medicamento.query.filter(
        Medicamento.stock <= Medicamento.stock_minimo
    ).count()
    
    # Productos por vencer (próximos 30 días)
    treinta_dias = hoy + timedelta(days=30)
    por_vencer = Medicamento.query.filter(
        Medicamento.fecha_vencimiento.between(hoy, treinta_dias)
    ).count()
    
    # Clientes nuevos este mes
    clientes_nuevos = Cliente.query.filter(
        func.date(Cliente.fecha_registro) >= mes_inicio
    ).count()
    
    # Total clientes
    total_clientes = Cliente.query.count()
    
    # Ingresos del mes
    ingresos_mes = db.session.query(
        func.sum(Venta.total)
    ).filter(
        func.date(Venta.fecha) >= mes_inicio
    ).scalar() or 0
    
    # Ingresos totales
    ingresos_totales = db.session.query(
        func.sum(Venta.total)
    ).scalar() or 0
    
    # Producto con mayor stock
    producto_mayor_stock = Medicamento.query.order_by(Medicamento.stock.desc()).first()
    
    # Producto con menor stock (pero > 0)
    producto_menor_stock = Medicamento.query.filter(
        Medicamento.stock > 0
    ).order_by(Medicamento.stock).first()
    
    return {
        'ventas_mes': ventas_mes,
        'total_ventas': total_ventas,
        'productos_mas_vendidos': productos_mas_vendidos,
        'categorias_populares': categorias_populares,
        'stock_bajo': stock_bajo,
        'por_vencer': por_vencer,
        'clientes_nuevos': clientes_nuevos,
        'total_clientes': total_clientes,
        'ingresos_mes': ingresos_mes,
        'ingresos_totales': ingresos_totales,
        'producto_mayor_stock': producto_mayor_stock,
        'producto_menor_stock': producto_menor_stock
    }

def generar_analisis_ia():
    """Genera análisis automático de los datos usando IA"""
    stats = obtener_estadisticas_sistema()
    
    # Formatear datos para la IA
    contexto = f"""
ANÁLISIS DE DATOS DE FARMACIA - {datetime.now().strftime('%B %Y')}

DATOS ACTUALES:
- Ventas este mes: {stats['ventas_mes']}
- Total ventas históricas: {stats['total_ventas']}
- Ingresos este mes: ${stats['ingresos_mes']:,.0f}
- Ingresos totales: ${stats['ingresos_totales']:,.0f}
- Clientes nuevos este mes: {stats['clientes_nuevos']}
- Total clientes: {stats['total_clientes']}
- Productos con stock bajo: {stats['stock_bajo']}
- Productos por vencer (30 días): {stats['por_vencer']}

PRODUCTOS MÁS VENDIDOS:
{chr(10).join([f"- {p[0]}: {p[1]} unidades" for p in stats['productos_mas_vendidos']])}

CATEGORÍAS POPULARES:
{chr(10).join([f"- {c[0]}: {c[1]} productos" for c in stats['categorias_populares']])}

PRODUCTO CON MÁS STOCK:
- {stats['producto_mayor_stock'].nombre if stats['producto_mayor_stock'] else 'N/A'}: {stats['producto_mayor_stock'].stock if stats['producto_mayor_stock'] else 0} unidades

PRODUCTO CON MENOS STOCK:
- {stats['producto_menor_stock'].nombre if stats['producto_menor_stock'] else 'N/A'}: {stats['producto_menor_stock'].stock if stats['producto_menor_stock'] else 0} unidades
"""

    prompt = f"""
Basado en los siguientes datos de una farmacia, genera un análisis inteligente con:

1. ANÁLISIS GENERAL: Resumen ejecutivo de máximo 3 líneas sobre el estado del negocio.
2. INSIGHTS CLAVE: 3 observaciones importantes sobre ventas, clientes o inventario.
3. PREDICCIONES: 2 predicciones simples basadas en los datos actuales (ej: "Basado en la tendencia, X producto podría agotarse en Y días").
4. RECOMENDACIONES: 2 recomendaciones accionables para mejorar el negocio.
5. DESTACADO DEL MES: Destacar un logro o dato positivo.

DATOS:
{contexto}

Formato de respuesta deseado (en HTML simple con clases de Bootstrap):
<div class="analisis-ia">
    <div class="alert alert-info">
        <strong>📊 ANÁLISIS GENERAL</strong><br>
        [texto]
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-header bg-primary text-white">
                    <strong>💡 INSIGHTS CLAVE</strong>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li>🔹 [insight 1]</li>
                        <li>🔹 [insight 2]</li>
                        <li>🔹 [insight 3]</li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-header bg-warning">
                    <strong>🔮 PREDICCIONES</strong>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li>📌 [predicción 1]</li>
                        <li>📌 [predicción 2]</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-header bg-success text-white">
                    <strong>✅ RECOMENDACIONES</strong>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled">
                        <li>✔️ [recomendación 1]</li>
                        <li>✔️ [recomendación 2]</li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-header bg-info text-white">
                    <strong>🏆 DESTACADO DEL MES</strong>
                </div>
                <div class="card-body">
                    [texto destacado]
                </div>
            </div>
        </div>
    </div>
</div>
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un analista de negocios experto en farmacias. Genera análisis inteligentes basados en datos reales."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f'<div class="alert alert-danger">Error al generar análisis: {str(e)}</div>'

def generar_predicciones_stock():
    """Genera predicciones simples sobre stock"""
    medicamentos = Medicamento.query.filter(
        Medicamento.activo == True,
        Medicamento.stock > 0
    ).all()
    
    predicciones = []
    
    for med in medicamentos:
        # Calcular velocidad de venta (promedio últimos 30 días)
        fecha_limite = datetime.now() - timedelta(days=30)
        ventas_30d = db.session.query(
            func.sum(DetalleVenta.cantidad)
        ).join(Venta).filter(
            DetalleVenta.medicamento_id == med.id,
            Venta.fecha >= fecha_limite
        ).scalar() or 0
        
        if ventas_30d > 0:
            venta_diaria = ventas_30d / 30
            if venta_diaria > 0:
                dias_restantes = med.stock / venta_diaria
                
                if dias_restantes < 7:
                    nivel = "CRÍTICO"
                    color = "danger"
                elif dias_restantes < 15:
                    nivel = "ADVERTENCIA"
                    color = "warning"
                else:
                    nivel = "NORMAL"
                    color = "success"
                
                predicciones.append({
                    'medicamento': med.nombre,
                    'stock': med.stock,
                    'venta_diaria': round(venta_diaria, 1),
                    'dias_restantes': round(dias_restantes),
                    'nivel': nivel,
                    'color': color
                })
    
    return sorted(predicciones, key=lambda x: x['dias_restantes'])[:5]