# case39A

### 1. Setup Inicial
```bash
docker-compose up -d
```
Ao executar o docker-compose um banco de dados PostgreSQL será criado com o nome `energia_db` e o script DDL.sql será executado automaticamente dentro dele.

------------
### 2. Dados

Dentro da pasta CSVs existe um arquivo `dados.zip` que poderá ser consumido pelo workflow de popular o banco de dados. Dentro dessa pasta também estão os 3 arquivos CSV contidos no zip e o script em python usado para gerar os dados de clientes, contratos e leituras, que garante a presença de pelo menos alguns outliers.

------------
### 3. PopulaDb.json - Popular Database

#### Endpoint `POST http://localhost:5678/webhook/popula-db`
O workflow recebe um arquivo ZIP contendo os 3 CSVs e popula o banco de dados.

```bash
curl -X POST -F "data=@CSVs/dados.zip" http://localhost:5678/webhook/popula-db
```

------------
### 4. AnaliseConsumo.json - Análise de consumo com LLM

#### Endpoint `GET http://localhost:5678/webhook/analise-consumo`
Analisa as leituras dos últimos 3 meses de contratos ativos e identifica outliers. Para a detecção dos outliers foi utilizado o método do intervalo interquartil (IQR) com fator 1.5, pois dados de consumo de energia não costumam seguir distribuição normal, podendo ter distribuição assimétrica com outliers naturais (familias grandes, imóveis vazios, etc).

Também pode gerar um relatório através de um LLM junto com a análise. Para isso é necessário passar o query param `llm=true`. Sem esse parâmetro o webhook trará somente os dados da análise (nomes dos clientes, média de consumo e status entre normal e outlier).
```bash
curl -X GET http://localhost:5678/webhook/analise-consumo?llm=true
```
