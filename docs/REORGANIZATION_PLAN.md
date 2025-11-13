# Plano de Reorganização do Repositório

## 📋 Estrutura Atual vs Proposta

### Problemas Identificados
1. **Muitos arquivos na raiz** (confuso)
2. **Arquivos de teste na raiz** (devem estar em tests/)
3. **Documentação espalhada** (raiz e docs/)
4. **Arquivos DSPy obsoletos** (versões antigas não usadas)
5. **Scripts obsoletos** (versões antigas de baselines)

### Estrutura Proposta

```
CrewAI-Project/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── config.py          # Core configuration
├── main.py            # Entry point principal
├── tools.py           # Shared tools
│
├── agents/            # 🆕 Agents modules
│   ├── __init__.py
│   ├── baseline.py    # agents.py renomeado
│   ├── no_rag.py      # agents_no_rag.py renomeado
│   └── crewai_dspy.py # agents_crewai_dspy.py renomeado
│
├── crews/             # 🆕 Crew definitions
│   ├── __init__.py
│   ├── baseline.py    # crew.py renomeado
│   ├── no_rag.py      # crew_no_rag.py renomeado
│   └── crewai_dspy.py # crew_crewai_dspy.py renomeado
│
├── tasks/             # 🆕 Task definitions
│   ├── __init__.py
│   ├── baseline.py    # tasks.py renomeado
│   └── no_rag.py      # tasks_no_rag.py renomeado
│
├── dspy/              # 🆕 DSPy optimization
│   ├── __init__.py
│   ├── config.py      # dspy_config.py movido
│   └── optimizer.py   # dspy_optimizer.py movido
│
├── rag/               # ✅ RAG system (já existe)
│   ├── __init__.py
│   ├── retriever_tools.py
│   └── vector_store.py
│
├── metrics/           # ✅ Metrics (já existe)
│   ├── __init__.py
│   └── metrics_tracker.py
│
├── scripts/           # ✅ Scripts (limpo)
│   ├── README.md
│   ├── run_baseline_no_rag.sh
│   ├── run_baseline_test.sh
│   ├── run_baseline_crewai_dspy.sh  # 🎯 Baseline final
│   ├── compare_baselines.py
│   ├── compare_all_baselines.py
│   └── analyze_baseline.py
│
├── tests/             # ✅ Tests (limpo e organizado)
│   ├── README.md
│   ├── test_baseline.py
│   ├── test_baseline_no_rag.py
│   ├── test_crewai_dspy.py  # 🆕 test_crewai_dspy_single.py movido
│   ├── test_metrics.py
│   ├── test_rag_integration.py
│   └── test_rag_setup.py
│
├── docs/              # ✅ Documentation (consolidada)
│   ├── README.md
│   ├── SETUP_COMPLETO.md
│   ├── RAG_INTEGRATION.md
│   ├── CREWAI_DSPY_HYBRID.md  # 🆕 Movido da raiz
│   ├── AGENTOPS_TRACKING.md   # 🆕 Consolidado
│   ├── BASELINE_COMPARISON.md
│   └── ...
│
├── workspace/         # ✅ Output workspace
│   └── README.md
│
└── archived/          # 🆕 Arquivos obsoletos
    ├── agents_dspy.py          # Versão auto-otimizada (não usada)
    ├── agents_dspy_manual.py   # Versão antiga (substituída)
    ├── crew_dspy.py            # Versão auto-otimizada (não usada)
    ├── crew_dspy_manual.py     # Versão antiga (substituída)
    ├── run_baseline_dspy.sh    # Script antigo
    ├── run_baseline_dspy_fresh.sh  # Script antigo
    ├── run_baseline_dspy_manual.sh # Script antigo
    ├── train_dspy_optimizer.py # Não usado
    ├── test_dspy_basic.py      # Teste temporário
    ├── test_dspy_llm.py        # Teste temporário
    ├── test_manual_with_logging.py  # Teste temporário
    ├── quick_test.sh           # Script temporário
    ├── run_fresh_test_clean.sh # Script temporário
    └── run_dspy_training_clean.py  # Script temporário
```

## 📝 Ações a Realizar

### 1. Criar Novas Pastas
- [x] `agents/`
- [x] `crews/`
- [x] `tasks/`
- [x] `dspy/`
- [x] `archived/`

### 2. Mover Arquivos Ativos

#### Agents
- `agents.py` → `agents/baseline.py`
- `agents_no_rag.py` → `agents/no_rag.py`
- `agents_crewai_dspy.py` → `agents/crewai_dspy.py`

#### Crews
- `crew.py` → `crews/baseline.py`
- `crew_no_rag.py` → `crews/no_rag.py`
- `crew_crewai_dspy.py` → `crews/crewai_dspy.py`

#### Tasks
- `tasks.py` → `tasks/baseline.py`
- `tasks_no_rag.py` → `tasks/no_rag.py`

#### DSPy
- `dspy_config.py` → `dspy/config.py`
- `dspy_optimizer.py` → `dspy/optimizer.py`

#### Tests
- `test_crewai_dspy_single.py` → `tests/test_crewai_dspy.py`

#### Docs
- `CREWAI_DSPY_HYBRID.md` → `docs/`
- `AGENTOPS_TRACKING_COMPLETO.md` + `AGENTOPS_SETUP_FINAL.md` + `LLM_TRACKING_FIX.md` → `docs/AGENTOPS_TRACKING.md` (consolidado)
- `STRUCTURE.md` → `docs/`

### 3. Arquivar Arquivos Obsoletos
- `agents_dspy.py` → `archived/`
- `agents_dspy_manual.py` → `archived/`
- `crew_dspy.py` → `archived/`
- `crew_dspy_manual.py` → `archived/`
- `scripts/run_baseline_dspy.sh` → `archived/`
- `scripts/run_baseline_dspy_fresh.sh` → `archived/`
- `scripts/run_baseline_dspy_manual.sh` → `archived/`
- `scripts/train_dspy_optimizer.py` → `archived/`
- `test_dspy_basic.py` → `archived/`
- `test_dspy_llm.py` → `archived/`
- `test_manual_with_logging.py` → `archived/`
- `quick_test.sh` → `archived/`
- `run_fresh_test_clean.sh` → `archived/`
- `run_dspy_training_clean.py` → `archived/`
- `tests/test_baseline_dspy.py` → `archived/` (versão antiga)
- `tests/test_baseline_dspy_fresh.py` → `archived/` (versão antiga)
- `tests/test_crewai_tracking.py` → `archived/` (teste temporário)
- `tests/test_llm_tracking_fixed.py` → `archived/` (teste temporário)
- `tests/test_tracking.py` → `archived/` (teste temporário)

### 4. Deletar Arquivos Temporários
- `agentops.log`
- `test_prompts.json`
- `scripts/quick_test.sh` (duplicado)

### 5. Limpar Workspace
- Manter apenas `workspace/README.md`
- Deletar outputs antigos (serão regenerados)

### 6. Atualizar Imports

Após mover arquivos, atualizar imports em:
- `main.py`
- `scripts/run_baseline_no_rag.sh`
- `scripts/run_baseline_test.sh`
- `scripts/run_baseline_crewai_dspy.sh`
- `tests/test_baseline.py`
- `tests/test_baseline_no_rag.py`
- `tests/test_crewai_dspy.py`

## ✅ Benefícios

1. **Organização clara** por tipo de componente
2. **Fácil navegação** - tudo em seu lugar
3. **Código limpo** - sem arquivos obsoletos na raiz
4. **Histórico preservado** - arquivos antigos em archived/
5. **Manutenção facilitada** - estrutura modular

## 🎯 Resultado Final

```
Raiz (11 arquivos):
- .env, .gitignore
- README.md, requirements.txt
- config.py, main.py, tools.py
- 4 pastas de módulos: agents/, crews/, tasks/, dspy/
- 3 pastas de suporte: rag/, metrics/, tests/
- 2 pastas auxiliares: scripts/, docs/
- 1 pasta de output: workspace/
- 1 pasta de histórico: archived/
```

**De 30+ arquivos na raiz → 11 arquivos essenciais** ✅
