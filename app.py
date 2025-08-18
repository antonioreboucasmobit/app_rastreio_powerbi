from flask import Flask, request, send_file
import logging
import io
import base64
from datetime import datetime

app = Flask(__name__)

# Configurar log para salvar no arquivo acessos.log
logging.basicConfig(
    filename='acessos.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Rota principal para status
@app.route('/')
def home():
    return '🟢 Servidor de rastreamento ativo. Use /pixel.gif?relatorio=SeuRelatorio'

# Rota de rastreamento
@app.route('/pixel.gif')
def pixel():
    # Captura parâmetros e informações
    relatorio = request.args.get('relatorio', 'desconhecido')
    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)  # Render usa proxy

    # Registrar no log
    log_msg = f"Relatório: {relatorio} | IP: {ip} | UA: {user_agent}"
    app.logger.info(log_msg)

    # Pixel transparente 1x1 em base64
    gif_base64 = b'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
    gif_bytes = base64.b64decode(gif_base64)
    
    # Enviar o pixel como resposta
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
