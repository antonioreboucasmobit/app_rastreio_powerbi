from flask import Flask, request, send_file, jsonify
import logging
import io
import base64
import csv
import os
from datetime import datetime
import requests

app = Flask(__name__)

# Configurar log no arquivo acessos.log
logging.basicConfig(
    filename='acessos.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Coloque aqui sua URL do webhook do Apps Script
GOOGLE_SHEETS_WEBHOOK = "https://script.google.com/macros/s/AKfycbz6ZbsG6FMih2ZKm3wc3cUGSoCMXeG7m2ako6h20Y2fNqHx5FgtK7CNmcVaVsgENxd8XA/exec"



CSV_FILE = 'dados_acessos.csv'

@app.route('/')
def home():
    return '🟢 Servidor de rastreamento ativo. Use /pixel.gif?relatorio=SeuRelatorio'

@app.route('/page')
def page():
    relatorio = request.args.get('relatorio', 'IframeRelatorio')
    return f"""
    <html>
    <body>
        <img src="/pixel.gif?relatorio={relatorio}" style="display:none;" />
    </body>
    </html>
    """


@app.route('/log-sheet')
def log_to_google_sheets():
    relatorio = request.args.get('relatorio', 'desconhecido')
    user_agent = request.headers.get('User-Agent', 'desconhecido')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Log local (opcional)
    app.logger.info(f"[GoogleSheets] Relatório: {relatorio} | IP: {ip} | UA: {user_agent}")


    # Geo lookup
    try:
        geo_resp = requests.get(f"http://ip-api.com/json/{ip}")
        geo = geo_resp.json()
        cidade = geo.get("city", "N/A")
        pais = geo.get("country", "N/A")
    except Exception as e:
        cidade = pais = "N/A"
        app.logger.error(f"[Geo] Erro na geolocalização: {e}")

    # Log local (opcional)
    app.logger.info(f"[GoogleSheets] {relatorio} | {ip} | {cidade}, {pais} | UA: {user_agent}")

    # Enviar para Google Sheets
    try:
        
        requests.post(GOOGLE_SHEETS_WEBHOOK, json={
            'relatorio': relatorio,
            'ip': ip,
            'user_agent': user_agent
        })
    except Exception as e:
        app.logger.error(f"[GoogleSheets] Erro ao enviar: {e}")

    # Retorna o pixel invisível
    gif_base64 = b'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
    gif_bytes = base64.b64decode(gif_base64)
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

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

@app.route('/status_server')
def status_server():
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        return jsonify({
            "status": "ok",
            "timestamp": now,
            "message": "Servidor online e funcional"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro interno: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



