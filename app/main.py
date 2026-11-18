"""
main.py — a API. Cada função com @app.get / @app.post é um "endereço"
que o front (ou você, pelo navegador) pode chamar.

  GET    = buscar dados        (ler a planilha)
  POST   = criar dado novo     (inserir linha)
  DELETE = apagar dado         (excluir linha)
"""
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import conectar, criar_tabelas


@asynccontextmanager
async def ao_iniciar(app: FastAPI):
    criar_tabelas()  # garante que as tabelas existem quando a API liga
    yield


app = FastAPI(title="Frota API", version="0.1.0", lifespan=ao_iniciar)


# ---------------------------------------------------------------------
# Modelos: o "formato" que um dado precisa ter para entrar na API.
# É como uma validação de dados do Excel: se vier errado, a API recusa.
# ---------------------------------------------------------------------
class CaminhaoNovo(BaseModel):
    placa: str = Field(min_length=7, max_length=7, examples=["DEF4G56"])
    marca: str = Field(examples=["Mercedes-Benz"])
    modelo: str = Field(examples=["Actros 2651"])
    ano: int = Field(ge=1980, le=2030, examples=[2024])
    eixos: int = Field(default=3, ge=2, le=4)


class ImplementoNovo(BaseModel):
    placa: str = Field(min_length=7, max_length=7, examples=["FCH1H23"])
    tipo: str = Field(examples=["Baú"])
    fabricante: str = Field(examples=["Facchini"])
    ano: int = Field(ge=1980, le=2030, examples=[2023])
    caminhao_id: int | None = None


# ---------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------
@app.get("/")
def inicio():
    return {"mensagem": "Frota API no ar! Acesse /docs para testar."}


@app.get("/caminhoes")
def listar_caminhoes():
    with conectar() as conexao:
        linhas = conexao.execute("SELECT * FROM caminhoes ORDER BY id").fetchall()
    return [dict(linha) for linha in linhas]


@app.get("/caminhoes/{caminhao_id}")
def buscar_caminhao(caminhao_id: int):
    with conectar() as conexao:
        linha = conexao.execute(
            "SELECT * FROM caminhoes WHERE id = ?", (caminhao_id,)
        ).fetchone()
    if linha is None:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")
    return dict(linha)


@app.post("/caminhoes", status_code=201)
def criar_caminhao(caminhao: CaminhaoNovo):
    try:
        with conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO caminhoes (placa, marca, modelo, ano, eixos) VALUES (?, ?, ?, ?, ?)",
                (caminhao.placa.upper(), caminhao.marca, caminhao.modelo, caminhao.ano, caminhao.eixos),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe caminhão com essa placa")
    return {"id": cursor.lastrowid, **caminhao.model_dump(), "placa": caminhao.placa.upper()}


@app.delete("/caminhoes/{caminhao_id}", status_code=204)
def apagar_caminhao(caminhao_id: int):
    with conectar() as conexao:
        # antes de apagar o caminhão, desengata os implementos dele
        conexao.execute("UPDATE implementos SET caminhao_id = NULL WHERE caminhao_id = ?", (caminhao_id,))
        cursor = conexao.execute("DELETE FROM caminhoes WHERE id = ?", (caminhao_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Caminhão não encontrado")


@app.get("/implementos")
def listar_implementos():
    with conectar() as conexao:
        linhas = conexao.execute("SELECT * FROM implementos ORDER BY id").fetchall()
    return [dict(linha) for linha in linhas]


@app.post("/implementos", status_code=201)
def criar_implemento(implemento: ImplementoNovo):
    try:
        with conectar() as conexao:
            cursor = conexao.execute(
                "INSERT INTO implementos (placa, tipo, fabricante, ano, caminhao_id) VALUES (?, ?, ?, ?, ?)",
                (implemento.placa.upper(), implemento.tipo, implemento.fabricante, implemento.ano, implemento.caminhao_id),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Placa repetida ou caminhão inexistente")
    return {"id": cursor.lastrowid, **implemento.model_dump(), "placa": implemento.placa.upper()}


@app.get("/caminhoes/{caminhao_id}/conjunto")
def ver_conjunto(caminhao_id: int):
    """Mostra o caminhão + os implementos engatados nele (um JOIN = PROCV entre abas)."""
    caminhao = buscar_caminhao(caminhao_id)
    with conectar() as conexao:
        linhas = conexao.execute(
            """
            SELECT i.placa, i.tipo, i.fabricante, i.ano
            FROM implementos AS i
            JOIN caminhoes   AS c ON c.id = i.caminhao_id
            WHERE c.id = ?
            """,
            (caminhao_id,),
        ).fetchall()
    return {"caminhao": caminhao, "implementos": [dict(linha) for linha in linhas]}
