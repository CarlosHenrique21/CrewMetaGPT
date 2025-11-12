# 📁 Estrutura do Projeto CrewAI

## Visão Geral

Projeto organizado em **6 diretórios principais** + arquivos core:

```
CrewAI-Project/
├── 📄 Core Files (raiz)      # Arquivos principais do sistema
├── 📚 docs/                  # Toda a documentação
├── 🧪 tests/                 # Scripts de teste
├── 🔧 scripts/               # Scripts auxiliares
├── 🔍 rag/                   # Sistema RAG
├── 📊 metrics/               # Sistema de métricas
├── 📚 knowledge_base/        # Base de conhecimento
├── 📁 workspace/             # Outputs gerados
└── 📂 output/                # Logs e temporários
```

---

## 📄 Core Files (Raiz)

Arquivos principais do sistema:

```
├── main.py                  # ⭐ Ponto de entrada principal
├── agents.py                # Definições dos agentes
├── tasks.py                 # Definições das tasks
├── tools.py                 # Tools customizadas
├── crew.py                  # Configuração do crew
├── config.py                # Configurações gerais
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente (gitignored)
├── .env.example             # Template de .env
├── .gitignore               # Arquivos ignorados
├── quick_test.sh            # ⭐ Script de teste rápido
└── README.md                # ⭐ Documentação principal
```

**Arquivos chave:**
- `main.py` - Executa o sistema com RAG + métricas
- `agents.py` - 5 agentes + Knowledge Manager
- `quick_test.sh` - Teste rápido (1 projeto)

---

## 📚 docs/ - Documentação

Toda a documentação do projeto:

```
docs/
├── README.md                           # ⭐ Índice da documentação
├── PLANO_ESTUDO_RAG_METRICAS.md       # ⭐ Plano de estudo completo
├── RAG_INTEGRATION.md                 # ⭐ Como o RAG funciona
├── BASELINE_TEST_GUIDE.md             # ⭐ Guia de testes baseline
├── QUICK_START_TESTS.md               # Resumo de scripts
├── SETUP_COMPLETO.md                  # Setup detalhado
├── TRACKING_STATUS_REPORT.md          # Status do tracking
├── FIX_LLM_TRACKING.md                # Soluções de tracking
├── METAGPT_VS_CREWAI.md               # Comparação frameworks
├── RESUMO_EXECUTIVO.md                # Resumo executivo
└── CORREÇÕES_COMPLETAS.md             # Histórico de correções
```

**Documentos essenciais:**
- `README.md` - Navegação da documentação
- `PLANO_ESTUDO_RAG_METRICAS.md` - Metodologia de pesquisa
- `RAG_INTEGRATION.md` - Entender o sistema RAG
- `BASELINE_TEST_GUIDE.md` - Como testar

---

## 🧪 tests/ - Scripts de Teste

Todos os scripts de teste:

```
tests/
├── README.md                 # ⭐ Guia de testes
├── test_baseline.py          # ⭐ Teste baseline (5 projetos)
├── test_rag_setup.py         # Teste RAG isolado
├── test_rag_integration.py   # Verificação de integração
├── test_crewai_tracking.py   # Teste de tracking
├── test_tracking.py          # Testes adicionais
└── test_prompts.json         # Prompts de exemplo
```

**Testes principais:**
- `test_baseline.py` - Executa 5 projetos, coleta métricas
- `test_rag_integration.py` - Valida configuração RAG
- `test_rag_setup.py` - Testa vector store

---

## 🔧 scripts/ - Scripts Auxiliares

Scripts para executar e analisar:

```
scripts/
├── README.md                 # ⭐ Guia de scripts
├── run_baseline_test.sh      # ⭐ Executa teste baseline
├── analyze_baseline.py       # ⭐ Analisa resultados
└── quick_test.sh             # Teste rápido (cópia)
```

**Scripts principais:**
- `run_baseline_test.sh` - Wrapper do teste baseline
- `analyze_baseline.py` - Análise de métricas

---

## 🔍 rag/ - Sistema RAG

Implementação do RAG:

```
rag/
├── __init__.py               # Exports do módulo
├── vector_store.py           # ⭐ Vector store com FAISS
├── retriever_tools.py        # ⭐ Tools de RAG
└── vector_db/                # Banco de dados vetorial (gerado)
    ├── knowledge_base.index
    └── knowledge_base.pkl
```

**Componentes:**
- `vector_store.py` - FAISS, embeddings, busca semântica
- `retriever_tools.py` - 5 tools para agentes

---

## 📊 metrics/ - Sistema de Métricas

Rastreamento de métricas:

```
metrics/
├── __init__.py               # Exports do módulo
├── metrics_tracker.py        # ⭐ Rastreador completo
└── data/                     # Métricas salvas (gerado)
    ├── baseline_report.json
    └── baseline_project_*.json
```

**Métricas coletadas:**
- Latência (retrieval, LLM, total)
- Tokens e custos
- Taxa de sucesso
- Throughput

---

## 📚 knowledge_base/ - Base de Conhecimento

Documentos para RAG:

```
knowledge_base/
├── best_practices/
│   ├── software_architecture.md    # Padrões de arquitetura
│   └── coding_standards.md         # Standards de código
├── templates/
│   └── prd_template.md             # Template de PRD
├── code_examples/
│   └── python_patterns.py          # Design patterns
└── documentation/
    └── project_development_guide.md # Processo completo
```

**5 documentos** carregados automaticamente no RAG.

---

## 📁 workspace/ - Outputs Gerados

Arquivos gerados pelos agentes:

```
workspace/
├── prd.md                    # Product Requirements
├── architecture.md           # Arquitetura do sistema
├── src/                      # Código implementado
├── tests.py                  # Testes gerados
├── README.md                 # Documentação
└── user_guide.md             # Guia do usuário
```

**Limpar workspace:**
```bash
rm -rf workspace/*
```

---

## 📂 output/ - Logs e Temporários

Logs e arquivos temporários:

```
output/
└── (arquivos temporários)
```

**Gitignored** - não commitado.

---

## 🎯 Navegação Rápida

### Para Iniciantes
1. Ler: [README.md](README.md)
2. Ler: [docs/SETUP_COMPLETO.md](docs/SETUP_COMPLETO.md)
3. Executar: `./quick_test.sh`

### Para Desenvolvedores
1. Explorar: `agents.py`, `rag/`, `metrics/`
2. Ler: [docs/RAG_INTEGRATION.md](docs/RAG_INTEGRATION.md)
3. Testar: `python tests/test_rag_integration.py`

### Para Pesquisadores
1. Ler: [docs/PLANO_ESTUDO_RAG_METRICAS.md](docs/PLANO_ESTUDO_RAG_METRICAS.md)
2. Executar: `./scripts/run_baseline_test.sh`
3. Analisar: `python scripts/analyze_baseline.py`

---

## 📝 Comandos Úteis

### Visualizar Estrutura
```bash
# Listar arquivos principais
ls -la *.py *.sh

# Ver documentação
ls -la docs/

# Ver testes
ls -la tests/

# Ver scripts
ls -la scripts/
```

### Executar Testes
```bash
# Teste rápido
./quick_test.sh

# Teste completo
./scripts/run_baseline_test.sh

# Verificar RAG
python tests/test_rag_integration.py
```

### Ver Métricas
```bash
# Analisar baseline
python scripts/analyze_baseline.py

# Ver JSON
cat metrics/data/baseline_report.json | python -m json.tool
```

---

## 🔄 Mudanças na Reorganização

### O que foi movido:

**Documentação** (`*.md` → `docs/`)
- ✅ PLANO_ESTUDO_RAG_METRICAS.md
- ✅ RAG_INTEGRATION.md
- ✅ BASELINE_TEST_GUIDE.md
- ✅ QUICK_START_TESTS.md
- ✅ E mais 7 documentos...

**Testes** (`test_*.py` → `tests/`)
- ✅ test_baseline.py
- ✅ test_rag_setup.py
- ✅ test_rag_integration.py
- ✅ E mais 3 testes...

**Scripts** → `scripts/`
- ✅ run_baseline_test.sh
- ✅ analyze_baseline.py

### O que permaneceu na raiz:
- ✅ README.md (principal)
- ✅ quick_test.sh (acesso rápido)
- ✅ Arquivos .py core
- ✅ requirements.txt, .env, .gitignore

---

## 📚 READMEs por Diretório

Cada diretório tem seu próprio README:

- **[README.md](README.md)** - Principal (raiz)
- **[docs/README.md](docs/README.md)** - Índice da documentação
- **[tests/README.md](tests/README.md)** - Guia de testes
- **[scripts/README.md](scripts/README.md)** - Guia de scripts

---

## ✅ Benefícios da Organização

### Antes (❌)
```
CrewAI-Project/
├── [15+ arquivos .md na raiz]
├── [8+ test_*.py na raiz]
├── [scripts misturados]
└── [difícil de navegar]
```

### Depois (✅)
```
CrewAI-Project/
├── 📄 Core Files (limpo)
├── 📚 docs/ (toda documentação)
├── 🧪 tests/ (todos os testes)
├── 🔧 scripts/ (scripts organizados)
└── [fácil navegação]
```

**Melhorias:**
- ✅ Estrutura clara e profissional
- ✅ Fácil encontrar documentação
- ✅ Separação lógica de componentes
- ✅ READMEs contextuais
- ✅ Links atualizados
- ✅ Pronto para produção

---

**Última atualização:** 2025-01-12
**Versão da estrutura:** 2.0
