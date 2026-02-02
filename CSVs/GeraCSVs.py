import csv
import random
from datetime import datetime, timedelta

random.seed(42)
num_clientes = 100
num_contratos_por_cliente_min = 1
num_contratos_por_cliente_max = 3
leituras_por_contrato_por_mes = 1
meses_leituras = 12

# Gerar clientes
clientes = []
for i in range(1, num_clientes + 1):
    clientes.append({
        'id': i,
        'nome': f'Cliente {i:03d}'
    })

# Gerar contratos
contratos = []
contrato_id = 1
for cliente in clientes:
    num_contratos = random.randint(num_contratos_por_cliente_min, num_contratos_por_cliente_max)
    for _ in range(num_contratos):
        data_inicio = datetime.now() - timedelta(days=random.randint(0, 730))
        # 80% dos contratos ativos
        status = random.random() < 0.8
        contratos.append({
            'id': contrato_id,
            'cliente_id': cliente['id'],
            'data_inicio': data_inicio.strftime('%Y-%m-%d'),
            'status_contrato': status
        })
        contrato_id += 1

# Gerar leituras
leituras = []
leitura_id = 1
for contrato in contratos:
    # Se o contrato está ativo, gerar leituras
    if contrato['status_contrato']:
        # Data de início para leituras (máximo entre data_inicio do contrato e 12 meses atrás)
        data_inicio_contrato = datetime.strptime(contrato['data_inicio'], '%Y-%m-%d')
        data_inicio_leituras = max(data_inicio_contrato, datetime.now() - timedelta(days=30*meses_leituras))
        
        current_date = data_inicio_leituras
        while current_date <= datetime.now():
            # Base de consumo: média de 150 kWh, com variação por cliente
            base_consumo = 150
            # Adicionar variação baseada no ID do cliente (para tornar alguns clientes consistentemente altos/baixos)
            variacao_cliente = (contrato['cliente_id'] % 10) * 10  # Varia de 0 a 90
            consumo = random.normalvariate(base_consumo + variacao_cliente, 30)
            # Garantir que não seja negativo
            consumo = max(10, consumo)
            
            # Criar alguns outliers
            if contrato['cliente_id'] < 10 and contrato['cliente_id'] % 2 == 0:  # Alguns outliers alto
                consumo *= random.uniform(3, 5)
            elif contrato['cliente_id'] > 90 and contrato['cliente_id'] % 2 == 1:  # Alguns outliers baixos
                consumo *= random.uniform(0.1, 0.3)
            
            leituras.append({
                'id': leitura_id,
                'contrato_id': contrato['id'],
                'data_leitura': current_date.strftime('%Y-%m-%d'),
                'valor_kwh': round(consumo, 2)
            })
            leitura_id += 1
            current_date += timedelta(days=30)

with open('clientes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'nome'])
    writer.writeheader()
    writer.writerows(clientes)

with open('contratos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'cliente_id', 'data_inicio', 'status_contrato'])
    writer.writeheader()
    writer.writerows(contratos)

with open('leituras.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'contrato_id', 'data_leitura', 'valor_kwh'])
    writer.writeheader()
    writer.writerows(leituras)

print(f"Gerados: {len(clientes)} clientes, {len(contratos)} contratos, {len(leituras)} leituras")