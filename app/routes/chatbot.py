from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.chatbot import consultar_chatbot, buscar_por_sintomas

bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

@bp.route('/')
@login_required
def index():
    """Página principal del chatbot"""
    return render_template('chatbot/index.html')

@bp.route('/consultar', methods=['POST'])
@login_required
def consultar():
    """Endpoint para consultar al chatbot"""
    data = request.get_json()
    sintomas = data.get('sintomas', '')
    edad = data.get('edad')
    alergias = data.get('alergias')
    
    if not sintomas:
        return jsonify({'error': 'Debes ingresar los síntomas'}), 400
    
    respuesta = consultar_chatbot(sintomas, edad, alergias)
    
    # Búsqueda local como respaldo
    resultados_locales = buscar_por_sintomas(sintomas)
    
    return jsonify({
        'respuesta': respuesta,
        'resultados_locales': [
            {
                'id': m.id,
                'nombre': m.nombre,
                'precio': m.precio_venta,
                'stock': m.stock,
                'requiere_receta': m.requiere_receta
            } for m in resultados_locales
        ]
    })

@bp.route('/buscar', methods=['GET'])
@login_required
def buscar():
    """Búsqueda rápida de medicamentos"""
    query = request.args.get('q', '')
    if len(query) < 3:
        return jsonify([])
    
    resultados = Medicamento.query.filter(
        Medicamento.nombre.ilike(f'%{query}%')
    ).filter(Medicamento.activo == True).limit(5).all()
    
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'precio': m.precio_venta,
        'stock': m.stock,
        'url': url_for('medicamentos.detalle', id=m.id)
    } for m in resultados])