CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL 
);

CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    status_contrato BOOLEAN NOT NULL DEFAULT TRUE, -- DEFAULT TRUE assumindo que novos contratos são ativos por padrão
    
    CONSTRAINT fk_contrato_cliente 
        FOREIGN KEY (cliente_id) 
        REFERENCES clientes(id)
        ON DELETE RESTRICT -- RESTRICT para evitar exclusões acidentais
);

CREATE TABLE leituras_energeticas (
    id SERIAL PRIMARY KEY,
    contrato_id INTEGER NOT NULL,
    data_leitura DATE NOT NULL,
    valor_kwh DECIMAL(10,2) NOT NULL CHECK (valor_kwh >= 0), -- DECIMAL para precisão e CHECK pra assegurar valores positivos
    
    CONSTRAINT fk_leitura_contrato 
        FOREIGN KEY (contrato_id) 
        REFERENCES contratos(id)
        ON DELETE RESTRICT,
    
    -- Garante que não haja leituras duplicadas para o mesmo contrato e na mesma data
    CONSTRAINT uniq_leitura_contrato_data 
        UNIQUE (contrato_id, data_leitura)
);

-- Índices para otimização
-- A query principal faz join com contratos pelo cliente_id e filtra por status_contrato
CREATE INDEX idx_contratos_cliente_status ON contratos (cliente_id, status_contrato);
-- Nela também é feio um join pelo contrato_id da tabela leituras_energeticas e um filtro pela coluna data_leitura
CREATE INDEX idx_leituras_contrato_data ON leituras_energeticas(contrato_id, data_leitura);