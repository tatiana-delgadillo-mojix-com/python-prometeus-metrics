from flask import Flask, Response
from helpers.middleware import setup_metrics
import prometheus_client
import traceback
import logging

LOG_FILENAME = 'aplication.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


app = Flask(__name__)
#Inicializar las metricas
setup_metrics(app)

@app.route('/test/')
def test():
    return 'rest'

@app.route('/test1/')
def test1():
    try:
        1/0
        return 'rest', 200
    except:
        return traceback.format_exc(), 500
    

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
        DEBUG = os.environ.get('DEBUG','True') == "True"
    except ValueError:
        DEBUG = True
        PORT = 5000
    app.logger.info("Starting Service")
    print (HOST,PORT)
    app.run(host=HOST,port=PORT,debug=DEBUG)