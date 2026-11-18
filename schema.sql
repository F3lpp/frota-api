-- =====================================================================
-- schema.sql — a "planta" do nosso banco de dados
-- Pense em cada TABLE como uma ABA do Excel, e cada coluna como... coluna.
-- =====================================================================

-- Aba 1: caminhões (o cavalo mecânico / veículo trator)
CREATE TABLE IF NOT EXISTS caminhoes (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- número da linha, gerado sozinho
    placa   TEXT    NOT NULL UNIQUE,            -- obrigatório e não pode repetir
    marca   TEXT    NOT NULL,                   -- ex: Scania, Volvo, Mercedes-Benz
    modelo  TEXT    NOT NULL,                   -- ex: R 450, FH 540
    ano     INTEGER NOT NULL,
    eixos   INTEGER NOT NULL DEFAULT 3
);

-- Aba 2: implementos (semirreboque, reboque, carreta...)
CREATE TABLE IF NOT EXISTS implementos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    placa       TEXT    NOT NULL UNIQUE,
    tipo        TEXT    NOT NULL,               -- ex: Graneleiro, Baú, Sider, Tanque
    fabricante  TEXT    NOT NULL,               -- ex: Randon, Librelato, Facchini
    ano         INTEGER NOT NULL,
    -- Liga o implemento a um caminhão (como um PROCV para outra aba).
    -- Pode ficar vazio (NULL) = implemento desengatado no pátio.
    caminhao_id INTEGER REFERENCES caminhoes(id)
);
