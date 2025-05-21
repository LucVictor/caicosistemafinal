from ..main import *
import os
log_file = os.path.join(static_folder, 'logs.txt')
static_folder = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/download-log')
def download_log():
    log_path = os.path.join(os.path.dirname(__file__), 'static', 'logs.txt')
    if os.path.exists(log_path):
        return send_file(
            log_path,
            as_attachment=True,
            download_name='logs.txt',
            mimetype='text/plain'
        )
    else:
        return "Arquivo de log não encontrado.", 404
