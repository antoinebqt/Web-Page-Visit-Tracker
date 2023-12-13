from flask import Flask, request, jsonify
from psycopg2 import connect
from redis import StrictRedis

import psutil

from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.registry import CollectorRegistry


app = Flask(__name__)
registry = CollectorRegistry(auto_describe=True)

http_requests_total = Counter('http_requests_total', 'Total number of HTTP requests', registry=registry)
request_duration = Histogram('request_duration_seconds', 'Duration of HTTP requests in seconds', registry=registry)
memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes', registry=registry)
cpu_time = Gauge('cpu_time_seconds', 'CPU time consumed in seconds', registry=registry)
@app.before_request
def before_request():
    http_requests_total.inc()

@app.after_request
def after_request(response):
    request_duration.observe(response.elapsed.total_seconds())
    # Record memory usage
    memory_usage.set(psutil.Process().memory_info().rss)

    # Record CPU time
    cpu_time.set(psutil.Process().cpu_percent() / 100.0)
    return response

# Endpoint /metrics pour Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def simulate_work():
    import time
    import random
    import os

    memory_usage.set(os.statvfs('/').f_bsize * os.statvfs('/').f_blocks)
    cpu_time.set(time.process_time())

    # Simuler une charge de travail aléatoire
    time.sleep(random.uniform(0.1, 0.5))

# Endpoint pour simuler le webservice de tracking Polymétrie
@app.route('/track')
def track():
    simulate_work()
    return 'Tracking request processed successfully!'



# Configuration de la base de données client (PostgreSQL)
client_db_conn = connect(
    dbname="postgres",
    user="postgres",
    password="cBxkAqQtZR",
    host="postgresql",
    port=5432
)
client_db_cursor = client_db_conn.cursor()

# Configuration de la base de données du compteur de page (Redis)
page_counter_db = StrictRedis(host='redis-master', port=6379, db=0,password="ov6D2EYYcb")


@app.route('/createTable')
def createTable():
    try:
        # Define the SQL query to create a table
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS clients (
                                       id SERIAL PRIMARY KEY,
                                       url VARCHAR(255) NOT NULL
            );
        '''

        # Execute the query to create the table
        client_db_cursor.execute(create_table_query)

        # Commit the changes to the database
        client_db_conn.commit()

        return jsonify({"message": "Table created successfully!"}), 200

    except Exception as e:
        # Handle any exceptions that might occur during the table creation
        return jsonify({"error": str(e)}), 500


@app.route('/track', methods=['POST'])
def track_page_visit():
    try:
        payload = request.get_json()

        # Récupération du domaine de l'URL
        domain = get_domain_from_url(payload['tracker']['WINDOW_LOCATION_HREF'])

        # Vérification si le site web est autorisé
        if is_client_authorized(domain):
            # Incrémentation du compteur de page dans Redis
            page_counter_db.incr(payload['tracker']['WINDOW_LOCATION_HREF'])
            return jsonify({"status": "success", "message": "Page visit tracked successfully"})
        else:
            return jsonify({"status": "error", "message": "Unauthorized client"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/add_client', methods=['POST'])
def add_client():
    try:
        data = request.get_json()
        client_url = data.get('client_url')

        # Ajout du client à la base de données client
        add_client_to_database(client_url)

        return jsonify({"status": "success", "message": "Client added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/get_clients', methods=['GET'])
def get_clients():
    try:
        # Récupération de la liste de tous les clients depuis la base de données client
        client_db_cursor.execute("SELECT url FROM clients")
        clients = client_db_cursor.fetchall()

        return jsonify({"status": "success", "clients": [client[0] for client in clients]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/metrics_old', methods=['GET'])
def get_redis_data():
    try:
        # Récupération de toutes les clés et valeurs dans la base de données Redis
        keys = page_counter_db.keys('*')
        redis_data = {key.decode(): page_counter_db.get(key).decode() for key in keys}

        return jsonify({"status": "success", "metrics_data": redis_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/delete_client', methods=['POST'])
def delete_client():
    try:
        data = request.get_json()
        client_url = data.get('client_url')

        # Suppression du client de la base de données client
        delete_client_from_database(client_url)

        return jsonify({"status": "success", "message": "Client deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def delete_client_from_database(client_url):
    # Suppression du client de la base de données client
    client_db_cursor.execute("DELETE FROM clients WHERE url = %s", (client_url,))
    client_db_conn.commit()

def is_client_authorized(client_domain):
    # Vérification dans la base de données client si le site web est autorisé
    client_db_cursor.execute("SELECT COUNT(*) FROM clients WHERE url = %s", (client_domain,))
    return client_db_cursor.fetchone()[0] > 0

def add_client_to_database(client_url):
    # Ajout du client à la base de données client
    client_db_cursor.execute("INSERT INTO clients (url) VALUES (%s)", (client_url,))
    client_db_conn.commit()

def get_domain_from_url(url):
    # "https://polytech.univ-cotedazur.fr/ecole/association-alumni" -> "polytech.univ-cotedazur.fr"
    return url.split('/')[2]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
