# Classificação de E-mails com IA

Aplicação full-stack para classificar e analisar e-mails utilizando um provedor de IA. O projeto é dividido em dois módulos:
- Backend em Python (lógica de classificação e integração com provedor de IA)
- Frontend em TypeScript/Next.js (interface web)

## Sumário
- [Arquitetura](#arquitetura)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Pré-requisitos](#pré-requisitos)
- [Configuração](#configuração)
- [Executando Localmente](#executando-localmente)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Qualidade de Código](#qualidade-de-código)
- [Deploy](#deploy)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [English version](#english-version)

---

## Arquitetura

- Backend (Python)
    - Implementa a lógica de classificação e a integração com o provedor de IA.
    - Código principal em [backend/main.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/main.py).
    - Integração com IA em [backend/ai_provider.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/ai_provider.py).
# Classificação de Email com IA

Este projeto utiliza técnicas de Processamento de Linguagem Natural (NLP) para classificar emails automaticamente usando inteligência artificial.

Para acessar o vídeo de apresentação, visite: [Classificação de Email via IA - FullStack - Next.Js | Typescript | Python](https://www.youtube.com/watch?v=z4vGtRVMOk0)

Para acessar a aplicação, visite: [Classificação de Email com IA](https://classificacao-email-ia.vercel.app/)

## Práticas de NLP

As principais práticas de NLP estão implementadas em [backend/nlp.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/nlp.py).

## Como instalar

1. Clone o repositório:
   ```bash
   git clone https://github.com/VitorManuel01/classificacao_email_ia.git
   cd classificacao_email_ia
   ```
2. Instale as dependências (requer Python 3.8+):
   ```bash
   pip install -r requirements.txt
   ```

## Como usar

Execute o script principal para classificar emails:
.py)
    - Dependências em [backend/requirements.txt](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/requirements.txt).

- Frontend (Next.js + TypeScript)
    - Interface web construída com Next.js.
    - Configurações principais:
        - [frontend/next.config.ts](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/next.config.ts)
        - [frontend/package.json](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/package.json)
        - [frontend/tsconfig.json](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/tsconfig.json)
        - [frontend/eslint.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/eslint.config.mjs)
        - [frontend/postcss.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/postcss.config.mjs)

- Infra
    - Arquivo de configuração para Render: [render.yaml](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/render.yaml)

## Estrutura do Repositório

```
.
├─ backend/
│  ├─ ai_provider.py
│  ├─ main.py
│  ├─ nlp.py  
│  ├─ requirements.txt
│  └─ .gitignore
├─ frontend/
│  ├─ public/
│  ├─ src/
│  ├─ package.json
│  ├─ package-lock.json
│  ├─ next.config.ts
│  ├─ tsconfig.json
│  ├─ eslint.config.mjs
│  ├─ postcss.config.mjs
│  └─ .gitignore
├─ render.yaml
└─ README.md
```

## Pré-requisitos

- Backend
    - Python 3.10+ recomendado
    - pip

- Frontend
    - Node.js 18+ (ou versão LTS mais recente)
    - npm ou yarn

## Configuração

1) Clone o repositório
```bash
git clone https://github.com/VitorManuel01/classificacao_email_ia.git
cd classificacao_email_ia
```

2) Backend – dependências
```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

3) Frontend – dependências
```bash
cd ../frontend
npm install
# ou
yarn install
```

## Executando Localmente

- Backend (opções comuns; ajuste conforme sua stack)
    - Se o servidor for iniciado via script Python:
      ```bash
      cd backend
      python main.py
      ```
    - Se for uma aplicação ASGI (por exemplo, FastAPI) com um objeto `app` em `main.py`, você pode usar:
      ```bash
      cd backend
      uvicorn main:app --reload --host 0.0.0.0 --port 8000
      ```
    - A URL local típica será algo como: http://localhost:8000

- Frontend (Next.js)
  ```bash
  cd frontend
  npm run dev
  # ou
  yarn dev
  ```
    - A URL local típica: http://localhost:3000

Certifique-se de configurar a URL do backend consumida pelo frontend (ver seção de variáveis de ambiente).

## Variáveis de Ambiente

Dependendo do provedor de IA utilizado no [ai_provider.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/ai_provider.py), você provavelmente precisará definir uma ou mais chaves de API. Variáveis comuns:

- No backend (arquivo `.env` ou variáveis do ambiente do sistema):
    - `AI_API_KEY` (por exemplo, chave do provedor de IA)
    - `AI_API_BASE_URL` (se aplicável)
    - Outras variáveis específicas do provedor (modelo, versão, etc.)

- No frontend:
    - `NEXT_PUBLIC_API_BASE_URL` com a URL do backend (ex.: `http://localhost:8000` ou a URL do serviço em produção)

Exemplos:

```bash
# backend/.env
AI_API_KEY=coloque_sua_chave_aqui

# frontend/.env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Observação: Ajuste os nomes conforme a implementação real do projeto.

## Qualidade de Código

- Frontend:
    - ESLint configurado em [eslint.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/eslint.config.mjs).
    - TypeScript configurado em [tsconfig.json](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/tsconfig.json).
    - PostCSS configurado em [postcss.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/postcss.config.mjs).

- Backend:
    - Dependências e versões gerenciadas via [requirements.txt](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/requirements.txt).

## Deploy

- Render
    - O repositório inclui [render.yaml](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/render.yaml) para definição de serviços.
    - Passos gerais:
        1. Crie um novo projeto no Render e conecte este repositório.
        2. Render irá detectar o `render.yaml` e sugerir a criação dos serviços.
        3. Configure as variáveis de ambiente dos serviços (backend e frontend) conforme necessário.
        4. Faça o deploy e verifique as URLs geradas para o frontend e backend.

## Contribuição

Contribuições são bem-vindas!
1. Abra uma issue descrevendo sua proposta ou problema.
2. Crie um fork e uma branch com sua feature/bugfix.
3. Envie um Pull Request com uma descrição clara do que foi alterado e como testar.

## Licença

Nenhuma licença declarada até o momento.

---

## English version

# Email Classification with AI

Full-stack app to classify and analyze emails using an AI provider. It consists of:
- Python backend (classification logic and AI provider integration)
- TypeScript/Next.js frontend (web UI)

- Languages:
    - Python (~93.6%)
    - TypeScript (~6.4%)

See:
- Backend entry points: [backend/main.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/main.py), [backend/ai_provider.py](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/ai_provider.py), and [backend/requirements.txt](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/backend/requirements.txt).
- Frontend configs: [frontend/next.config.ts](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/next.config.ts), [frontend/package.json](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/package.json), [frontend/tsconfig.json](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/tsconfig.json), [frontend/eslint.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/eslint.config.mjs), [frontend/postcss.config.mjs](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/frontend/postcss.config.mjs).
- Render infra: [render.yaml](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/render.yaml).

Quickstart
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python main.py             # or: uvicorn main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

Environment variables (adjust to your implementation):
- Backend: `AI_API_KEY`, `AI_API_BASE_URL`, etc.
- Frontend: `NEXT_PUBLIC_API_BASE_URL` pointing to the backend.

Deploy with Render:
- Connect the repo on Render; it will pick up [render.yaml](https://github.com/VitorManuel01/classificacao_email_ia/blob/master/render.yaml).
- Set environment variables for services, then deploy.

License: Not declared.
