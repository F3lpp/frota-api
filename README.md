# 🚛 Frota API

API para cadastrar **caminhões** e **implementos** (graneleiro, sider, baú...) e ver qual implemento está engatado em qual caminhão.

Projeto-escola: cada melhoria entra por **branch → commit → Pull Request → review → merge**, igual em um time de verdade.

---

## 🧰 1. Preparar o Windows (só uma vez)

Instale, nesta ordem, aceitando as opções padrão:

| Programa | Link | Atenção |
|---|---|---|
| **Python 3.12+** | https://www.python.org/downloads/ | ✅ Marque **"Add python.exe to PATH"** na primeira tela! |
| **Git** | https://git-scm.com/download/win | Pode dar "Next" em tudo |
| **VS Code** | https://code.visualstudio.com/ | Depois instale a extensão **Python** (da Microsoft) |

Confira se deu certo. Abra o **PowerShell** e rode:

```powershell
python --version
git --version
```

Os dois precisam mostrar um número de versão. Depois, apresente-se ao Git (uma vez só):

```powershell
git config --global user.name "Felipe Prado"
git config --global user.email "SEU_EMAIL_DO_GITHUB"
```

---

## ▶️ 2. Rodar o projeto

```powershell
# baixar o projeto (troque pelo endereço do seu repositório)
git clone https://github.com/SEU_USUARIO/frota-api.git
cd frota-api

# criar o "ambiente virtual" (uma caixinha isolada só com as bibliotecas deste projeto)
python -m venv .venv
.venv\Scripts\Activate.ps1

# instalar as bibliotecas
pip install -r requirements.txt

# ligar a API
fastapi dev app/main.py
```

> Se o PowerShell reclamar de "execução de scripts desabilitada", rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e responda **S**.

Abra no navegador: **http://127.0.0.1:8000/docs**
Essa tela permite testar todos os endereços da API clicando em **"Try it out"**.

---

## 🗺️ 3. Mapa do projeto

```
frota-api/
├── app/
│   ├── main.py       ← a API: os "endereços" (rotas) que o front vai chamar
│   └── database.py   ← conexão com o banco + dados de exemplo
├── schema.sql        ← a planta do banco (as "abas" e "colunas")
├── requirements.txt  ← lista de bibliotecas que o projeto usa
└── .gitignore        ← o que o Git NÃO deve subir pro GitHub
```

### Endereços disponíveis

| Método | Endereço | O que faz |
|---|---|---|
| GET | `/caminhoes` | Lista todos os caminhões |
| GET | `/caminhoes/{id}` | Busca um caminhão |
| POST | `/caminhoes` | Cadastra caminhão |
| DELETE | `/caminhoes/{id}` | Apaga caminhão (e desengata os implementos dele) |
| GET | `/implementos` | Lista implementos |
| POST | `/implementos` | Cadastra implemento |
| GET | `/caminhoes/{id}/conjunto` | Caminhão + implementos engatados (usa **JOIN**) |

### Tradução Excel → Código

| No Excel | Aqui |
|---|---|
| Arquivo .xlsx | Banco de dados (`frota.db`) |
| Aba | Tabela (`caminhoes`, `implementos`) |
| Linha | Registro |
| Validação de dados | Modelo Pydantic (`CaminhaoNovo`) |
| PROCV entre abas | `JOIN` no SQL |
| Alguém pedindo um dado da planilha | Requisição HTTP para a API |

---

## 🔀 4. Fluxo de trabalho (sempre igual)

```powershell
git checkout main
git pull                                   # pega a versão mais nova
git checkout -b feat/nome-da-tarefa        # cria sua branch
# ... edita o código, testa no /docs ...
git add .
git commit -m "feat: descreve o que você fez"
git push -u origin feat/nome-da-tarefa
```

Depois, no GitHub: **Compare & pull request** → descreva o que fez → **Create pull request**.
Eu reviso, você ajusta se precisar e faz o **merge**. 🎉
