from flask import request
from prometheus_client import Counter, Histogram
import time
import sys
# Tipo de datos incremental Contador creciente
REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
# Tipo de dato histograma 
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint', 'http_status']
)

def start_timer():
    request.start_time = time.time()
#Registro de latencia desd el tiempo de inicio de request hasta el tiempo de fin
def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('webapp', request.path, response.status_code).observe(resp_time)
    return response
#Contador de ingresos mediante http a la aplicacion
def record_request_data(response):
    REQUEST_COUNT.labels('webapp', request.method, request.path,
            response.status_code).inc()
    return response
#Configurar metricas
def setup_metrics(app):
    #antes del request iniciar el tiempo
    app.before_request(start_timer)
    #Despues del request incrementar el Count
    app.after_request(record_request_data)
    #Despues del request verificar el tiempo tardado en la respuesta
    app.after_request(stop_timer)