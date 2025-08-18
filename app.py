from flask import Flask, request, send_file
import logging, io, base64
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(filename='acessos.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/pixel.gif')
def pixel():
    relatorio = request.args.get('relatorio', 'desconhecido')
    user_agent = request.headers.get('User-Agent', '')
    ip = request.remote_addr
    logging.info(f"Relatório: {relatorio} | IP: {ip} | UA: {user_agent}")
    gif_base64 = b'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=='
    gif_bytes = base64.b64decode(gif_base64)
    return send_file(io.BytesIO(gif_bytes), mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
