import logging
import time
from database import engine
from mqtt_client import start_mqtt_client


# configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Tenta conectar ao banco, se falhar, espera 5s e tenta de novo.
def wait_for_db():
    logging.info("Aguardando o banco de dados ficar disponível...")
    while True:
        try:
            with engine.connect():
                break 
        except Exception:
            logging.warning("Banco de dados indisponível, tentando novamente em 5 segundos...")
            time.sleep(5)
    logging.info("Conexão com o banco de dados estabelecida com sucesso!")


# Executa os passos na ordem para iniciar
if __name__ == "__main__":
    wait_for_db()
    logging.info("Iniciando o serviço de ingestão de dados...")
    start_mqtt_client()

