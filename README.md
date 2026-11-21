# Linux Auth Log Analyzer

Uma ferramenta desenvolvida em Python para analisar logs de autenticação Linux, identificar tentativas de login malsucedidas, monitorar endereços IP e classificar possíveis atividades suspeitas.

Projeto pessoal desenvolvido com foco em estudos de Cibersegurança e Blue Team.

## Objetivos

- Analisar registros de autenticação SSH.
- Identificar logins bem-sucedidos e malsucedidos.
- Extrair nomes de usuários e endereços IP.
- Contabilizar tentativas de autenticação por IP.
- Classificar padrões de tentativas malsucedidas.
- Gerar relatórios estruturados em JSON.
- Aplicar testes automatizados para validar o funcionamento.

## Tecnologias utilizadas

- Python 3
- Regular Expressions (Regex)
- JSON
- Pytest
- Git e GitHub
- Linux

## Funcionalidades

### Análise de autenticação

Identifica dois tipos de eventos:

- `Failed password`: autenticação malsucedida.
- `Accepted password`: autenticação bem-sucedida.

### Monitoramento de IPs

Agrupa as tentativas malsucedidas por endereço IP e contabiliza suas ocorrências.

### Classificação de risco

O projeto utiliza uma regra simples baseada na quantidade total de falhas por IP:

| Tentativas | Classificação |
|---|---|
| 1 a 2 | NORMAL |
| 3 a 4 | ATENÇÃO |
| 5 ou mais | ALTO RISCO |

Essa classificação é uma heurística didática e não representa uma confirmação de ataque.

### Relatórios JSON

Os resultados são exportados automaticamente para:

`reports/report.json`

O relatório contém:

- Quantidade de logins bem-sucedidos.
- Quantidade de logins malsucedidos.
- Total de IPs analisados.
- Classificação de cada IP.
- Eventos de autenticação identificados.

## Estrutura do projeto

```text
linux-auth-log-analyzer/
│
├── logs/
│   └── sample_auth.log
│
├── reports/
│   └── report.json
│
├── tests/
│   └── test_analyzer.py
│
├── analyzer.py
├── main.py
├── requirements-dev.txt
├── .gitignore
└── README.md
```

## Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/LuscaWorks/linux-auth-log-analyzer.git
```

### 2. Entre no diretório

```bash
cd linux-auth-log-analyzer
```

### 3. Crie um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ative o ambiente virtual

Linux:

```bash
source .venv/bin/activate
```

### 5. Instale as dependências de desenvolvimento

```bash
python -m pip install -r requirements-dev.txt
```

### 6. Execute o analisador

```bash
python main.py
```

O relatório será gerado automaticamente em `reports/report.json`.

## Testes automatizados

O projeto utiliza Pytest para validar suas funcionalidades.

Execute:

```bash
python -m pytest -v
```

Os testes verificam o reconhecimento de eventos, classificação de IPs, análise dos registros e geração dos relatórios JSON.

## Limitações

- O analisador trabalha com registros no formato esperado pelas expressões Regex implementadas.
- A classificação considera a quantidade total de falhas encontrada no arquivo, sem janela temporal.
- Um endereço IP com várias tentativas não representa necessariamente um ataque confirmado.
- O projeto não bloqueia endereços IP nem realiza resposta automática a incidentes.

## Objetivo educacional

Este projeto foi desenvolvido como parte dos meus estudos em Cibersegurança, com direcionamento para Blue Team.

O objetivo é aprofundar conhecimentos em análise de logs, fundamentos de autenticação, automação com Python, identificação de comportamentos suspeitos e geração de relatórios de segurança.

**Desenvolvido por LuscaWorks.**