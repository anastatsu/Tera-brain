import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/tera', methods=['POST'])
def procesar_orden():
    datos = request.json
    orden_usuario = datos.get("mensaje", "")
    
    
    instruccion_tera = (
        "Eres TERA, una IA sofisticada y leal. Responde siempre llamando al usuario 'Señor'. "
        "Analiza su orden y responde ESTRICTAMENTE en formato JSON con esta estructura exacta: "
        '{"accion": "ejecutar", "comando": "chrome", "respuesta": "Abriendo el navegador web, señor."} '
        'o si solo te saluda: {"accion": "hablar", "comando": "ninguno", "respuesta": "A su servicio, señor."}'
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruccion_tera},
                {"role": "user", "content": orden_usuario}
            ],
            model="llama3-8b-8192", 
            response_format={"type": "json_object"}
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return jsonify({"accion": "hablar", "comando": "ninguno", "respuesta": "Error en el procesamiento de la orden."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))