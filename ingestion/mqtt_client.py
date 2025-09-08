import paho.mqtt.client as mqtt
import logging
import json
from config import MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS, MQTT_TOPIC
from database import insert_data

# Funções do MQTT

# Verifica se conectou com o broker, se sim, começa a receber dados
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado ao Broker MQTT com sucesso!")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"Inscrito no tópico: {MQTT_TOPIC}")
    else:
        logging.error(f"Falha ao conectar ao broker, código de retorno: {rc}")


# Pega cada mensagem que chega, trata os dados e manda para o banco.
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        logging.info(f"Mensagem recebida: {payload}")
        
        data = json.loads(payload)
        
        insert_data(data)
        
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar JSON: {msg.payload.decode()}")
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")


# Prepara e inicia o cliente, mantendo o programa rodando para receber mensagens.
def start_mqtt_client():
    client = mqtt.Client(client_id="ingestion-service-ex001")
    client.username_pw_set(MQTT_USER, MQTT_PASS)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        logging.info(f"Conectando ao broker em {MQTT_HOST}:{MQTT_PORT}...")
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        
        client.loop_forever()
    except Exception as e:
        logging.error(f"Não foi possível iniciar o cliente MQTT: {e}")
