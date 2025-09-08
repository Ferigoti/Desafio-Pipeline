import logging
from sqlalchemy import create_engine, text
from config import DATABASE_URL


# Gerenciar conexão com o banco.
engine = create_engine(DATABASE_URL)

# Modelo enviado ao banco de dados.
def insert_data(data: dict):
    sql = text("""
        INSERT INTO dados_maquina (
            maquina_id, datahora, ligada, operacao, manutencao_corretiva,
            manutencao_preventiva, pecas_boas, pecas_ruins
        ) VALUES (
            :maquina_id, :datahora, :ligada, :operacao, :manutencao_corretiva,
            :manutencao_preventiva, :pecas_boas, :pecas_ruins
        )
    """)

    # Abre a conexão, envia o comando com os dados e salva.
    try:
        with engine.connect() as connection:
            params = {
                "maquina_id": data['maquina_id'],
                "datahora": data['datahora'],
                "ligada": data['ligada'],
                "operacao": data['operacao'],
                "manutencao_corretiva": data['manutencao_corretiva'],
                "manutencao_preventiva": data['manutencao_preventiva'],
                "pecas_boas": data['pecas_boas'],
                "pecas_ruins": data['pecas_ruins']
            }
            connection.execute(sql, params)
            connection.commit()
        logging.info("Dados inseridos no banco com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao inserir dados no banco: {e}")
