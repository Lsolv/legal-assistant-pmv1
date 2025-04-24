from flask import Flask, request, jsonify, render_template
import json
import random

app = Flask(__name__)

# Cargar base de conocimiento legal
with open('app/legal_db.json', 'r', encoding='utf-8') as f:
    legal_db = json.load(f)

# Preguntas frecuentes por tipo de discapacidad
FAQ = {
    "motriz": [
        "¿Cómo solicito una pensión por discapacidad?",
        "¿Qué documentos necesito para una demanda por accesibilidad?",
        "¿Dónde puedo obtener un certificado de discapacidad?"
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form['question']
    
    # Búsqueda simple (mejorar con NLP en futuras versiones)
    answer = "Lo siento, no tengo información sobre eso."
    for topic in legal_db:
        if topic.lower() in user_question.lower():
            answer = random.choice(legal_db[topic])
            break
    
    return jsonify({
        "question": user_question,
        "answer": answer,
        "suggestions": FAQ.get("motriz", [])
    })

if __name__ == '__main__':
    app.run(debug=True)