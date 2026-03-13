import os
from openai import OpenAI
from .models import Producto
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url='https://api.groq.com/openai/v1')

def preguntar_chatbot(pregunta):
    productos = Producto.query.limit(5).all()
    lista = ""
    for  p in productos:
        lista += f'{p.nombre} - {p.precio}\n'
        
    contexto = f'Genera una lista de productos de repostería llamada "Dalas" con título, descripción corta y el precio estos son nuestros productos {lista}. REpsonde preguntas de clientes sobre productos y precios.'

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": contexto},
            {"role": "user", "content": pregunta}
        ]
    )
    generated_text = response.choices[0].message.content
    return generated_text