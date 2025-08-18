from flask import Flask, request, send_file
import logging
import io
import base64
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Configurar log no arquivo acessos.log
logging.basicConfig(
    filename='acessos.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

CSV_FILE = 'dados_acessos.csv'

@app.route('/')
def home():
    return '🟢 Servidor de rastreamento ativo. Use /pixel.gif?relatorio=SeuRelatorio'

@app.route('/pixel.gif')
def pixel():
    relatorio = request.args.get('relatorio', 'desconhecido')
    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    log_msg = f"Relatório: {relatorio} | IP: {ip} | UA: {user_agent}"
    app.logger.info(log_msg)

    # Salvar também no CSV
    file_exists = os.path.isfile(CSV_FILE)
    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['timestamp', 'relatorio', 'ip', 'user_agent'])
            writer.writerow([datetime.now().isoformat(), relatorio, ip, user_agent])
    except Exception as e:
        app.logger.error(f"Erro ao salvar CSV: {e}")

    # Pixel transparente 1x1 GIF
    gif_base64 = b'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
    gif_bytes = base64.b64decode(gif_base64)
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

@app.route('/logs')
def mostrar_logs():
    try:
        with open('acessos.log', 'r') as f:
            conteudo = f.read()
        return f"<pre>{conteudo}</pre>"
    except Exception as e:
        return f"Erro ao ler log: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
