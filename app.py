import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from Agentes.agent_inventory import inventory_agent

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("agente_jp.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")

# Memoria conversacional en servidor: {session_id: {last_sql, last_context, last_results}}
# Simple dict en memoria (se limpia al reiniciar el servidor)
_session_memory = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').strip()
    history = data.get('history', [])
    session_id = data.get('session_id', 'default')

    if not message:
        return jsonify({"error": "Mensaje vacío"}), 400

    # Recuperar memoria de sesión previa
    memory = _session_memory.get(session_id, {})

    logging.info(f"[INVENTARIO] [{session_id[:8]}] Consulta: '{message}'")
    response_data = inventory_agent.get_response(message, history, memory)

    # Guardar nueva memoria (SQL y contexto de esta consulta)
    if response_data.get('success'):
        _session_memory[session_id] = response_data.pop('memory', {})
    else:
        response_data.pop('memory', None)

    response_data['agent'] = 'Inventario 📦'
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)