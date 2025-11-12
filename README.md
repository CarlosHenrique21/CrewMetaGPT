# CrewAI Software Development Project with RAG

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.86+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Visão Geral

Sistema multi-agente de desenvolvimento de software usando **CrewAI** com:
- ✅ **5 Agentes Especializados** (PM, Architect, Engineer, QA, Tech Writer)
- 🔍 **RAG (Retrieval-Augmented Generation)** com base de conhecimento
- 📊 **Sistema Completo de Métricas** (latência, tokens, custos, throughput)
- 🎯 **Observabilidade com AgentOps**
- 📚 **Base de Conhecimento** com templates e best practices

Este projeto demonstra como criar um sistema de agentes que colaboram para desenvolver software completo, desde a especificação até a documentação, usando RAG para enriquecer as respostas com contexto relevante.

---

## 🎯 Características

### Agentes Especializados
- **Product Manager**: Cria PRDs (Product Requirements Documents)
- **Software Architect**: Projeta arquitetura do sistema
- **Software Engineer**: Implementa código
- **QA Engineer**: Cria planos de teste e test cases
- **Technical Writer**: Documenta o projeto
- **Knowledge Manager** (RAG): Fornece contexto da base de conhecimento

### Sistema RAG
- Vector store com FAISS para busca semântica
- Base de conhecimento pré-populada com:
  - Best practices de arquitetura
  - Padrões de código
  - Templates de documentação
  - Exemplos de código Python
- Tools especializadas para recuperação de contexto

### Métricas e Observabilidade
- Rastreamento de latência por etapa
- Monitoramento de uso de tokens e custos
- Taxa de sucesso por agente
- Throughput (queries/minuto)
- Integração com AgentOps para visualização

---

## 🚀 Quick Start

### Pré-requisitos

```bash
# Python 3.10 ou superior
python --version

# pip atualizado
pip install --upgrade pip
```

### Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd CrewAI-Project
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves:
```bash
# OpenAI API Key (obrigatória)
OPENAI_API_KEY=sk-proj-your-key-here

# AgentOps API Key (opcional, para observabilidade)
AGENTOPS_API_KEY=your-agentops-key
```

### Teste Rápido

Use o script de teste rápido:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

Ou execute diretamente:
```bash
python main.py "crie um jogo de cobra em pygame"
```

---

## 📖 Como Usar

### Uso Básico

```bash
python main.py "sua ideia de projeto aqui"
```

**Exemplos:**
```bash
# Jogo CLI
python main.py "crie um jogo da velha para terminal"

# API REST
python main.py "crie uma API REST para gerenciar tarefas"

# Dashboard
python main.py "crie um dashboard web para visualizar métricas"

# Ferramenta CLI
python main.py "crie uma ferramenta CLI para converter markdown em HTML"
```

### Usando RAG (Base de Conhecimento)

O sistema RAG é automaticamente inicializado quando você executa um projeto. Os agentes terão acesso à base de conhecimento para:
- Buscar best practices
- Recuperar exemplos de código
- Consultar templates de documentação
- Obter padrões de arquitetura

**Exemplo de uso explícito de RAG:**
```python
from rag import setup_knowledge_base, semantic_search_tool

# Inicializar base de conhecimento
vector_store = setup_knowledge_base("knowledge_base/")

# Buscar informações
results = semantic_search_tool("como implementar autenticação JWT")
```

### Visualizando Métricas

As métricas são automaticamente coletadas durante a execução:

```python
from metrics import get_tracker

# Obter tracker global
tracker = get_tracker()

# Ver resumo
tracker.print_summary()

# Salvar métricas em arquivo
tracker.save_metrics("metrics_report.json")
```

Métricas disponíveis:
- ⏱️ Latência por etapa (retrieval, LLM, verificação)
- 💰 Tokens usados e custo estimado
- 📊 Taxa de sucesso por agente
- 🚀 Throughput (queries/minuto)
- 🔧 Eficiência de tools

---

## 📂 Estrutura do Projeto

> 📋 **Veja estrutura completa em**: [STRUCTURE.md](STRUCTURE.md)

```
CrewAI-Project/
├── 📄 Core Files
│   ├── main.py                  # Ponto de entrada principal
│   ├── agents.py                # Definições dos agentes
│   ├── tasks.py                 # Definições das tasks
│   ├── tools.py                 # Tools customizadas
│   ├── crew.py                  # Configuração do crew
│   ├── config.py                # Configurações gerais
│   ├── requirements.txt         # Dependências Python
│   ├── .env                     # Variáveis de ambiente
│   └── quick_test.sh            # Script de teste rápido
│
├── 📚 docs/                     # Documentação
│   ├── PLANO_ESTUDO_RAG_METRICAS.md    # Plano de estudo completo
│   ├── RAG_INTEGRATION.md              # Como o RAG funciona
│   ├── BASELINE_TEST_GUIDE.md          # Guia de testes baseline
│   ├── QUICK_START_TESTS.md            # Resumo de scripts
│   ├── SETUP_COMPLETO.md               # Setup detalhado
│   ├── TRACKING_STATUS_REPORT.md       # Status do tracking
│   └── ... (outros docs)
│
├── 🧪 tests/                    # Scripts de teste
│   ├── test_baseline.py         # Teste baseline (5 projetos)
│   ├── test_rag_setup.py        # Teste do RAG isolado
│   ├── test_rag_integration.py  # Teste de integração RAG
│   ├── test_crewai_tracking.py  # Teste de tracking
│   └── test_tracking.py         # Testes adicionais
│
├── 🔧 scripts/                  # Scripts auxiliares
│   ├── run_baseline_test.sh     # Executar teste baseline
│   ├── analyze_baseline.py      # Analisar resultados
│   └── quick_test.sh            # Teste rápido (cópia)
│
├── 🔍 rag/                      # Sistema RAG
│   ├── __init__.py
│   ├── vector_store.py          # Vector store com FAISS
│   ├── retriever_tools.py       # Tools de recuperação
│   └── vector_db/               # Banco de dados vetorial (gerado)
│
├── 📊 metrics/                  # Sistema de métricas
│   ├── __init__.py
│   ├── metrics_tracker.py       # Rastreador de métricas
│   └── data/                    # Dados de métricas (gerado)
│       ├── baseline_report.json
│       └── baseline_project_*.json
│
├── 📚 knowledge_base/           # Base de conhecimento RAG
│   ├── best_practices/          # Best practices
│   │   ├── software_architecture.md
│   │   └── coding_standards.md
│   ├── templates/               # Templates de documentos
│   │   └── prd_template.md
│   ├── code_examples/           # Exemplos de código
│   │   └── python_patterns.py
│   └── documentation/           # Guias e documentação
│       └── project_development_guide.md
│
├── 📁 workspace/                # Arquivos gerados pelos agentes
│   ├── prd.md
│   ├── architecture.md
│   ├── src/
│   ├── tests.py
│   └── README.md
│
└── 📂 output/                   # Outputs e logs
```

---

## 🔧 Configuração Avançada

### Personalizar Agentes

Edite `agents.py` para customizar comportamento dos agentes:

```python
def create_product_manager() -> Agent:
    return Agent(
        role="Product Manager",
        goal="Create comprehensive PRDs",
        backstory="You are an experienced PM...",
        tools=[file_writer_tool, retrieve_context_tool],  # Adicione RAG
        verbose=True,
        allow_delegation=False,
    )
```

### Adicionar Documentos à Base de Conhecimento

```bash
# Adicione arquivos .md, .py, .txt em knowledge_base/
knowledge_base/
├── best_practices/
│   └── seu_arquivo.md
├── templates/
│   └── seu_template.md
└── code_examples/
    └── seu_exemplo.py

# Reinicialize o vector store
python -c "from rag import setup_knowledge_base; setup_knowledge_base()"
```

### Configurar Métricas Customizadas

```python
from metrics import MetricsTracker

tracker = MetricsTracker(output_dir="metrics/data")

# Rastrear retrieval customizado
tracker.track_retrieval(
    duration=0.5,
    docs_retrieved=3,
    relevance_score=0.85,
    embedding_latency=0.1
)

# Rastrear LLM call
tracker.track_llm_call(
    duration=2.3,
    tokens_prompt=500,
    tokens_completion=800,
    model="gpt-4o-mini"
)
```

### Integração AgentOps

O AgentOps fornece dashboard visual para:
- Ver timeline de execução
- Monitorar custos em tempo real
- Analisar performance de agentes
- Debug de chamadas LLM

Acesse: [https://app.agentops.ai](https://app.agentops.ai)

---

## 🧪 Testes

### Executar Teste Rápido
```bash
./quick_test.sh
```

### Executar com Projeto Específico
```bash
python main.py "criar calculadora científica CLI"
```

### Verificar Outputs
```bash
ls -la workspace/
cat workspace/prd.md
cat workspace/architecture.md
```

### Testar RAG Isoladamente
```python
from rag import semantic_search_tool, initialize_knowledge_base_tool

# Inicializar
initialize_knowledge_base_tool()

# Buscar
result = semantic_search_tool("padrão singleton em python", top_k=3)
print(result)
```

---

## 📊 Análise de Métricas

### Visualizar Métricas em Tempo Real

```python
from metrics import get_tracker

tracker = get_tracker()
tracker.print_summary()
```

Saída esperada:
```
================================================================================
📊 MÉTRICAS DO SISTEMA - RESUMO
================================================================================

Session ID: 20240115_143000
Duração: 180s

--- ESTATÍSTICAS GERAIS ---
Total de Queries: 15
Total de Retrievals: 12
Total de LLM Calls: 25
Total de Tool Calls: 45
Total de Agent Tasks: 5

--- PERFORMANCE ---
Latência Média Retrieval: 0.450s
Latência Média LLM: 2.350s
Throughput: 5.0 queries/min

--- CUSTOS ---
Total de Tokens: 45,230
Custo Estimado: $1.3560

--- EFICIÊNCIA DE TOOLS ---
retrieve_context:
  Chamadas: 12
  Taxa de Sucesso: 100.0%
  Duração Média: 0.450s

--- PERFORMANCE DE AGENTES ---
Product Manager:
  Tasks Completadas: 1
  Taxa de Sucesso: 100.0%

================================================================================
```

### Exportar Métricas para JSON

```python
tracker = get_tracker()
filepath = tracker.save_metrics("metrics_20240115.json")
print(f"Métricas salvas em: {filepath}")
```

---

## 📚 Documentação Adicional

### Arquivos de Documentação

Toda a documentação está organizada em **`docs/`**:

- **[PLANO_ESTUDO_RAG_METRICAS.md](docs/PLANO_ESTUDO_RAG_METRICAS.md)** - Plano completo de implementação RAG e estudo comparativo
- **[RAG_INTEGRATION.md](docs/RAG_INTEGRATION.md)** - Como o RAG funciona e está integrado
- **[BASELINE_TEST_GUIDE.md](docs/BASELINE_TEST_GUIDE.md)** - Guia completo de testes baseline
- **[QUICK_START_TESTS.md](docs/QUICK_START_TESTS.md)** - Resumo rápido de todos os scripts
- **[SETUP_COMPLETO.md](docs/SETUP_COMPLETO.md)** - Guia detalhado de configuração
- **[TRACKING_STATUS_REPORT.md](docs/TRACKING_STATUS_REPORT.md)** - Status do tracking com AgentOps

### Scripts de Teste

Todos os testes estão em **`tests/`** e scripts auxiliares em **`scripts/`**:

```bash
# Teste rápido (1 projeto)
./quick_test.sh

# Teste baseline (5 projetos)
./scripts/run_baseline_test.sh

# Análise de resultados
python scripts/analyze_baseline.py

# Testes unitários
python tests/test_rag_setup.py
python tests/test_rag_integration.py
```

### Base de Conhecimento

A base de conhecimento está em **`knowledge_base/`**:
- **best_practices/** - Arquitetura de software, padrões de código
- **templates/** - PRD, arquitetura, documentação
- **code_examples/** - Padrões de design em Python
- **documentation/** - Processo completo de desenvolvimento

---

## 🔬 Estudo Comparativo (Experimental)

Este projeto suporta estudos comparativos entre:
1. **Baseline**: Sistema atual com RAG
2. **Otimizado**: Sistema com AutoPDL + DSPy
3. **Customizado**: Outras configurações

Veja o plano completo em: **[docs/PLANO_ESTUDO_RAG_METRICAS.md](docs/PLANO_ESTUDO_RAG_METRICAS.md)**

---

## ❓ Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"
```bash
# Verifique se a variável está configurada
echo $OPENAI_API_KEY

# Configure manualmente
export OPENAI_API_KEY="sk-proj-your-key"
```

### Erro: "FAISS não instalado"
```bash
pip install faiss-cpu
# ou para GPU
pip install faiss-gpu
```

### Erro: "Vector store vazio"
```bash
# Inicialize a base de conhecimento
python -c "from rag import setup_knowledge_base; setup_knowledge_base()"
```

### Workspace vazio após execução
```bash
# Verifique logs
tail -f agentops.log

# Execute em modo verbose
AGENT_VERBOSE=true python main.py "seu projeto"
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

### Guidelines
- Siga o PEP 8 para código Python
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Use commits semânticos

---

## 📝 Changelog

### v2.1.0 (2025-01-12)
- 🗂️ **Reorganização completa do repositório**
  - Toda documentação movida para `docs/`
  - Todos os testes movidos para `tests/`
  - Scripts auxiliares em `scripts/`
  - READMEs contextuais em cada diretório
  - Estrutura profissional e organizada
- 📚 Adicionado [STRUCTURE.md](STRUCTURE.md) com mapa completo
- 📝 Links e referências atualizados

### v2.0.0 (2025-01-12)
- ✨ Adicionado sistema RAG completo
- ✨ Implementado Knowledge Manager agent
- ✨ Sistema de métricas detalhadas
- ✨ Base de conhecimento pré-populada
- 📚 Documentação expandida
- 🧪 Teste baseline (5 projetos)

### v1.0.0 (2024-11-11)
- 🎉 Release inicial
- ✨ 5 agentes especializados
- ✨ Integração com AgentOps
- ✨ Tools customizadas
- 📝 Documentação básica

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🙏 Agradecimentos

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Framework multi-agente
- [AgentOps](https://www.agentops.ai/) - Observabilidade
- [OpenAI](https://openai.com/) - Modelos LLM
- [FAISS](https://github.com/facebookresearch/faiss) - Vector store

---

## 📧 Contato

Para questões e suporte:
- Abra uma issue no GitHub
- Consulte a documentação em `docs/`

---

## 🚦 Status do Projeto

**Status**: ✅ Ativo e em desenvolvimento

**Próximas Features**:
- [ ] Integração com DSPy para otimização de prompts
- [ ] Suporte a múltiplos modelos LLM
- [ ] Interface web para visualização
- [ ] Exportação de métricas para Grafana
- [ ] Suporte a bases de conhecimento externas

---

**Última Atualização**: Janeiro 2025
**Versão**: 2.0.0
