# app/routes/main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Medicamento
from app.services.analisis_ia import generar_analisis_ia, generar_predicciones_stock, obtener_estadisticas_sistema
from datetime import date, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Fecha actual
    hoy = date.today()
    
    # Estadísticas básicas
    stock_bajo = Medicamento.query.filter(Medicamento.stock <= Medicamento.stock_minimo).count()
    
    treinta_dias = hoy + timedelta(days=30)
    por_vencer = Medicamento.query.filter(
        Medicamento.fecha_vencimiento.between(hoy, treinta_dias)
    ).count()
    
    # Obtener estadísticas completas para el dashboard
    stats = obtener_estadisticas_sistema()
    
    # Generar análisis IA (solo para admin o usuarios avanzados)
    analisis_ia = None
    predicciones_stock = None
    
    if current_user.rol in ['admin', 'vendedor']:
        analisis_ia = generar_analisis_ia()
        predicciones_stock = generar_predicciones_stock()
    
    return render_template('index.html', 
                         stock_bajo=stock_bajo, 
                         por_vencer=por_vencer,
                         hoy=hoy,
                         stats=stats,
                         analisis_ia=analisis_ia,
                         predicciones_stock=predicciones_stock) 