from flask import Flask, request, send_file
from datetime import datetime
import logging
import io
import base64

app = Flask(__name__)

# Configura log
logging.basicConfig(filename='acessos.log', level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/pixel.gif')
def pixel():
    relatorio = request.args.get('relatorio', 'desconhecido')
    user_agent = request.headers.get('User-Agent', 'N/A')
    ip = request.remote_addr

    log_message = f"Acesso - Relatório: {relatorio} | IP: {ip} | User-Agent: {user_agent}"
    app.logger.info(log_message)

    # Pixel GIF 1x1 (base64)
    gif_base64 = b'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
    gif_bytes = base64.b64decode(gif_base64)
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
