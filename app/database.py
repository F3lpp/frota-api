"""
database.py — tudo que conversa com o banco de dados mora aqui.

Usamos SQLite: o banco é UM ARQUIVO (frota.db) na pasta do projeto.
Não precisa instalar nada. Mais pra frente trocamos para PostgreSQL.
"""
import sqlite3
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
ARQUIVO_BANCO = PASTA_PROJETO / "frota.db"
ARQUIVO_SCHEMA = PASTA_PROJETO / "schema.sql"


def conectar() -> sqlite3.Connection:
    """Abre a 'planilha' do banco. row_factory faz cada linha virar um dicionário."""
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")  # liga a checagem do caminhao_id
    return conexao


def criar_tabelas() -> None:
    """Roda o schema.sql e, se o banco estiver vazio, coloca dados de exemplo."""
    with conectar() as conexao:
        conexao.executescript(ARQUIVO_SCHEMA.read_text(encoding="utf-8"))

        total = conexao.execute("SELECT COUNT(*) FROM caminhoes").fetchone()[0]
        if total == 0:
            conexao.executemany(
                "INSERT INTO caminhoes (placa, marca, modelo, ano, eixos) VALUES (?, ?, ?, ?, ?)",
                [
                    ("ABC1D23", "Scania", "R 450", 2022, 3),
                    ("XYZ9K87", "Volvo", "FH 540", 2023, 3),
                ],
            )
            conexao.executemany(
                "INSERT INTO implementos (placa, tipo, fabricante, ano, caminhao_id) VALUES (?, ?, ?, ?, ?)",
                [
                    ("RND2E34", "Graneleiro", "Randon", 2021, 1),
                    ("LBR5F67", "Sider", "Librelato", 2022, None),
                ],
            )
