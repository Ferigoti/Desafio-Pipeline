# Solução - Desafio Pipeline de Dados EX-001

## 1. O que o Projeto Faz:
Este projeto captura dados de uma máquina pela internet, salva essas informações em um banco de dados e, por fim, exibe os resultados em um painel de controle (dashboard) interativo.

## 2. Como Foi Feito:
A solução foi construída em três partes principais:

### Parte 1: O Banco de Dados
- Arquivo criado (db/init.sql) para preparar o banco de dados.

- Este arquivo cria a tabela dados_maquina, que é onde todas as informações da máquina são guardadas. A coluna de data e hora foi configurada para evitar problemas com fuso horário e para permitir buscas rápidas.

### Parte 2: Script Python
- Criei um script Python que se conecta à internet para receber os dados da máquina.

- O código foi dividido em arquivos menores (config.py, database.py, mqtt_client.py) para ficar mais limpo e organizado.

- O script fica "ouvindo" um canal específico (o tópico MQTT).

- Sempre que um novo dado da máquina chega, o script o pega e salva imediatamente no nosso banco de dados.

### Parte 3: O Painel de Controle (Dashboard)
- Criei um dashboard do zero no Grafana para visualizar os 6 indicadores pedidos.

- Conectei o Grafana ao nosso banco de dados.

- Para cada indicador, escrevi um comando SQL que faz o cálculo necessário (soma de peças, cálculo de porcentagens, etc.).

#### Total de Peças Produzidas:
```
SELECT SUM(pecas_boas) AS "Total de Peças Produzidas"
FROM dados_maquina WHERE $__timeFilter(datahora)
```

#### Total de Peças Defeituosas:

```
SELECT SUM(pecas_ruins) AS "Total de Peças Defeituosas"
FROM dados_maquina WHERE $__timeFilter(datahora)
```

#### Qualidade:

```
SELECT (SUM(pecas_boas) * 100.0) / NULLIF(SUM(pecas_boas) + SUM(pecas_ruins), 0) AS "Qualidade"
FROM dados_maquina WHERE $__timeFilter(datahora)
```

#### Disponibilidade:

```
SELECT (COUNT(CASE WHEN ligada THEN 1 END) * 100.0) / COUNT(*) AS "Disponibilidade"
FROM dados_maquina WHERE $__timeFilter(datahora)
```

#### Performance:

```
SELECT (SUM(pecas_boas) / NULLIF((COUNT(CASE WHEN operacao THEN 1 END) * 100.0 / 12.0), 0)) * 100 AS "Performance"
FROM dados_maquina WHERE $__timeFilter(datahora)
```

#### OEE:

```
WITH kpis AS (
  SELECT
    (COUNT(CASE WHEN ligada THEN 1 END) * 100.0) / COUNT(*) AS disponibilidade,
    (SUM(pecas_boas) / NULLIF((COUNT(CASE WHEN operacao THEN 1 END) * 100.0 / 12.0), 0)) AS performance,
    (SUM(pecas_boas) * 1.0) / NULLIF(SUM(pecas_boas) + SUM(pecas_ruins), 0) AS qualidade
  FROM dados_maquina WHERE $__timeFilter(datahora)
)
SELECT disponibilidade * performance * qualidade AS "OEE"
FROM kpis
```

- Ajustei o visual de cada indicador para mostrar os números e os símbolos de porcentagem (%) de forma clara.

## 3. Comandos Utilizados
Estes foram os comandos usados no terminal para configurar e rodar o projeto.

### 1. Preparar o Ambiente:

Primeiro, copie o arquivo de exemplo para criar sua própria configuração:
```
cp .env.example .env
```

Depois, abra o arquivo .env e preencha com as senhas e configurações necessárias.
```
- MQTT_HOST = mqtt.ecoplus-apps.com
- MQTT_PORT = 1883
- MQTT_USER = ecoplus_temp:user_temp
- MQTT_PASS = u9JJ8d8DOp
```

## 2. Executar o Projeto:
Para ligar todos os programas (banco de dados, script Python e Grafana), use este comando:
```
docker-compose up --build
```

## 3. Acessar o Dashboard:
Após rodar o comando acima, o painel de controle estará disponível no seu navegador no seguinte endereço:
```http://localhost:3000``` (usuário: admin, senha: admin)

## 4. O Resultado Final
### 4.1. Dashboard
O resultado é um painel de controle que mostra os dados da máquina em tempo real.

![Dashboard OEE](docs/dashboard.png)

#### O arquivo que contém o design completo deste dashboard está salvo em:
```grafana/provisioning/dashboards/dashboard_oee.json```
