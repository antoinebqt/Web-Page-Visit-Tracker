from threading import Thread

from flask import Flask, request, jsonify
from psycopg2 import connect
from redis import StrictRedis
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge
import os
import time

metrics_initialised = False

website_metric = Gauge('website_visits', 'Number of visits to the website', ['subscriber', 'url_page'])


app = Flask(__name__)
PrometheusMetrics(app)

BASE_URI = ""

# Connexion à la base de données des clients (PostgreSQL)
client_db_conn = connect(
    dbname="postgres",
    user="postgres",
    password="postgrespass",
    host="postgresql",
    port=5432
)
client_db_cursor = client_db_conn.cursor()

# Connexion à la base de données du tracker (Redis)
page_counter_db = StrictRedis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    db=os.environ.get("REDIS_DB"),
    password=os.environ.get("REDIS_PASSWORD"))

app.config['table_created'] = False

def createTable():
    if app.config['table_created']:
        return
    else:
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

            app.config['table_created'] = True

        except Exception as e:
            # Handle any exceptions that might occur during the table creation
            return jsonify({"error": str(e)}), 500

@app.route(BASE_URI + '/track', methods=['POST'])
def track_page_visit():
    try:
        global metrics_initialised
        if not metrics_initialised:
            initialise_metrics(1)
        if not app.config['table_created']:
            createTable()

        payload = request.get_json()


        # Récupération du domaine de l'URL
        domain = get_domain_from_url(payload['tracker']['WINDOW_LOCATION_HREF'])
        # Vérification si le site web est autorisé
        if is_client_authorized(domain):
            # Incrémentation du compteur de page dans Redis
            page_counter_db.incr(payload['tracker']['WINDOW_LOCATION_HREF'])
            website_metric.labels(subscriber=get_domain_from_url(payload['tracker']['WINDOW_LOCATION_HREF']), url_page=payload['tracker']['WINDOW_LOCATION_HREF']).set(page_counter_db.get(payload['tracker']['WINDOW_LOCATION_HREF']).decode())
            return jsonify({"status": "success", "message": "Page visit tracked successfully"})
        else:
            return jsonify({"status": "error", "message": "Unauthorized client"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})

@app.route(BASE_URI + '/add_client', methods=['POST'])
def add_client():
    try:
        if not app.config['table_created']:
            createTable()

        data = request.get_json()
        client_url = data.get('client_url')

        # Vérification si le client existe déjà
        if is_client_exists(client_url):
            return jsonify({"status": "error", "message": "Client already exists"})

        # Ajout du client à la base de données client
        add_client_to_database(client_url)

        return jsonify({"status": "success", "message": "Client added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route(BASE_URI + '/get_clients', methods=['GET'])
def get_clients():
    try:
        if not app.config['table_created']:
            createTable()

        # Récupération de la liste de tous les clients depuis la base de données client
        client_db_cursor.execute("SELECT url FROM clients")
        clients = client_db_cursor.fetchall()

        return jsonify({"status": "success", "clients": [client[0] for client in clients]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route(BASE_URI + '/data', methods=['GET'])
def get_redis_data():
    try:
        # Récupération de toutes les clés et valeurs dans la base de données Redis
        keys = page_counter_db.keys('*')
        redis_data = {key.decode(): page_counter_db.get(key).decode() for key in keys}

        return jsonify({"status": "success", "metrics_data": redis_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route(BASE_URI + '/delete_client', methods=['POST'])
def delete_client():
    try:
        if not app.config['table_created']:
            createTable()

        data = request.get_json()
        client_url = data.get('client_url')

        # Vérification si le client existe avant de le supprimer
        if not is_client_exists(client_url):
            return jsonify({"status": "error", "message": "Client does not exist"})

        # Suppression du client de la base de données client
        delete_client_from_database(client_url)

        return jsonify({"status": "success", "message": "Client deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def list_routes():
    result = []
    for rule in app.url_map.iter_rules():
        result.append({
            'endpoint': rule.endpoint,
            'methods': ', '.join(rule.methods),
            'path': str(rule),
        })
    return result

@app.route(BASE_URI + '/', methods=['GET'])
def show_routes():
    routes = list_routes()
    return jsonify({'routes': routes})

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

def is_client_exists(client_url):
    # Vérification dans la base de données client si le client existe déjà
    client_db_cursor.execute("SELECT COUNT(*) FROM clients WHERE url = %s", (client_url,))
    return client_db_cursor.fetchone()[0] > 0

def initialise_metrics(timeToSleep=120):
    global metrics_initialised
    metrics_initialised=True
    time.sleep(timeToSleep)
    keys = page_counter_db.keys('*')
    for key in keys:
        print("url_page " + key.decode())
        print("subscriber " + get_domain_from_url(key.decode()))
        print("counter" + page_counter_db.get(key).decode())

        website_metric.labels(subscriber=get_domain_from_url(key.decode()),
                              url_page=key.decode()).set(
            page_counter_db.get(key).decode())


if __name__ == '__main__':


    flask_thread = Thread(target=initialise_metrics)
    flask_thread.start()

    app.run(host='0.0.0.0', port=5000)




