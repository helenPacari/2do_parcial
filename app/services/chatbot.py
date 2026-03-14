import os
from openai import OpenAI
from app.models import Medicamento, Categoria
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url='https://api.groq.com/openai/v1'
)

def obtener_contexto_medicamentos():
    """Obtiene todos los medicamentos para contexto"""
    medicamentos = Medicamento.query.filter_by(activo=True).all()
    
    contexto = "CATÁLOGO DE MEDICAMENTOS DISPONIBLES:\n\n"
    
    for med in medicamentos:
        contexto += f"""
ID: {med.id}
Nombre: {med.nombre}
Nombre Genérico: {med.nombre_generico or 'N/A'}
Categoría: {med.categoria.nombre if med.categoria else 'General'}
Laboratorio: {med.laboratorio.nombre if med.laboratorio else 'N/A'}
Presentación: {med.presentacion or 'N/A'}
Concentración: {med.concentracion or 'N/A'}
Precio: ${med.precio_venta:,.0f}
Stock: {med.stock} unidades
Requiere Receta: {'Sí' if med.requiere_receta else 'No'}
Descripción: {med.descripcion or 'Sin descripción'}
------------------------"""
    
    return contexto

def consultar_chatbot(sintomas, edad=None, alergias=None):
    """
    Consulta al chatbot sobre posibles medicamentos para síntomas
    """
    contexto = obtener_contexto_medicamentos()
    
    system_prompt = f"""
Eres un asistente farmacéutico experto que ayuda a vendedores a recomendar medicamentos.
Basado en los síntomas del cliente, debes sugerir medicamentos apropiados de nuestro catálogo.

{contexto}

INSTRUCCIONES IMPORTANTES:
1. SOLO recomienda medicamentos que existen en nuestro catálogo
2. Indica si el medicamento requiere receta médica
3. Muestra el precio y stock disponible
4. Si los síntomas son graves, recomienda consultar a un médico
5. Pregunta por edad y alergias si es relevante
6. Sé claro y conciso en tus respuestas
7. Si no hay medicamento apropiado, sugiere consultar a un médico

FORMATO DE RESPUESTA RECOMENDADO:
- Medicamento sugerido: [nombre]
- Para qué sirve: [breve explicación]
- Precio: $[precio]
- Requiere receta: [Sí/No]
- Stock: [cantidad]
- Advertencias: [si aplica]
"""
    
    user_prompt = f"Síntomas del cliente: {sintomas}"
    if edad:
        user_prompt += f"\nEdad: {edad} años"
    if alergias:
        user_prompt += f"\nAlergias conocidas: {alergias}"
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error al consultar el chatbot: {str(e)}"

def buscar_por_sintomas(sintomas):
    """Búsqueda local de medicamentos por síntomas (fallback)"""
    sintomas = sintomas.lower()
    resultados = []
    
    # Palabras clave y medicamentos relacionados
    keywords = {
        'dolor': ['Analgésicos', 'Antiinflamatorios'],
        'fiebre': ['Antipiréticos', 'Analgésicos'],
        'tos': ['Antitusivos', 'Expectorantes'],
        'gripe': ['Antigripales', 'Analgésicos'],
        'alergia': ['Antihistamínicos'],
        'inflamación': ['Antiinflamatorios'],
        'migraña': ['Analgésicos', 'Antimigrañosos'],
        'estómago': ['Antiácidos', 'Antiespasmódicos'],
        'diarrea': ['Antidiarreicos'],
        'estreñimiento': ['Laxantes']
    }
    
    categorias_relacionadas = []
    for key, cats in keywords.items():
        if key in sintomas:
            categorias_relacionadas.extend(cats)
    
    if categorias_relacionadas:
        from sqlalchemy import or_
        resultados = Medicamento.query.join(Categoria).filter(
            or_(
                Medicamento.descripcion.ilike(f'%{sintomas}%'),
                Categoria.nombre.in_(categorias_relacionadas)
            )
        ).filter(Medicamento.activo == True).limit(5).all()
    
    return resultados