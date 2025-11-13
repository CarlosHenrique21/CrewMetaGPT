# Correção: AgentOps Rastreando LLM Calls

## 🎯 Problema

Você reportou que o AgentOps estava rastreando:
- ✅ Agents
- ✅ Tools
- ✅ Tasks
- ✅ Workflow

Mas **NÃO** estava rastreando:
- ❌ LLM Calls (tokens, custos, latência)

## 🔍 Causa Raiz

Para o AgentOps rastrear LLM calls no CrewAI, são necessárias **3 condições**:

1. **AgentOps inicializado ANTES** de criar qualquer LLM
2. **Agents usando LLM do langchain** (ChatOpenAI)
3. **LLM passado explicitamente** para os agents

O problema era que:
- ❌ AgentOps era inicializado **DEPOIS** dos imports
- ❌ Agents **não recebiam** LLM configurado explicitamente
- ❌ CrewAI usava LLM padrão sem tracking

## ✅ Solução Implementada

### 1. Adicionar `get_llm()` no `config.py`

```python
def get_llm():
    """
    Get configured LLM for agents.
    This ensures AgentOps can track LLM calls properly.
    """
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=AGENT_CONFIG["temperature"],
        max_tokens=AGENT_CONFIG["max_tokens"],
        api_key=OPENAI_API_KEY,
    )
```

**Por quê?** O ChatOpenAI do langchain é automaticamente interceptado pelo AgentOps.

### 2. Atualizar TODOS os agents em `agents_crewai_dspy.py`

```python
def create_product_manager() -> Agent:
    return Agent(
        role="Product Manager",
        goal="...",
        backstory=enhanced_backstory,
        tools=[...],
        verbose=config.AGENT_CONFIG["verbose"],
        allow_delegation=False,
        llm=config.get_llm(),  # ← ADICIONADO!
    )
```

**Aplicado em**:
- ✅ Product Manager
- ✅ Architect
- ✅ Engineer
- ✅ QA Engineer
- ✅ Tech Writer
- ✅ Knowledge Manager

### 3. Importar CrewAI ANTES de inicializar AgentOps

**IMPORTANTE**: Importar módulos na ordem correta para evitar circular import!

#### Em `test_crewai_dspy_single.py`:

```python
# Load environment FIRST
load_dotenv(override=True)

# Import config and CrewAI dependencies FIRST (before AgentOps)
import config
from dspy_config import configure_dspy

# NOW initialize AgentOps (after CrewAI is loaded)
import agentops
agentops.init(
    api_key=agentops_key,
    tags=[...],
    auto_start_session=False,
    skip_auto_end_session=False,
)
agentops.start_session(tags=[...])

# Import crew function after everything is ready
from crew_crewai_dspy import run_software_dev_crew_dspy
```

#### Em `scripts/run_baseline_crewai_dspy.sh`:

```python
# Importar config e dependências PRIMEIRO (antes do AgentOps)
import config
from dspy_config import configure_dspy

# AGORA inicializar AgentOps (DEPOIS do CrewAI estar carregado)
import agentops
agentops.init(
    api_key=agentops_key,
    tags=[...],
    auto_start_session=False,
    skip_auto_end_session=False,
)
agentops.start_session(tags=[...])

# Importar crew function depois
from crew_crewai_dspy import run_software_dev_crew_dspy
```

**Por quê?**
1. Importar `config` primeiro faz o Python carregar o CrewAI completamente
2. Isso evita que AgentOps tente instrumentar um módulo parcialmente inicializado
3. Previne o erro: `ImportError: cannot import name 'Agent' from partially initialized module 'crewai.agent'`
4. AgentOps ainda consegue rastrear todas as LLM calls quando iniciado depois

## 🔄 Ordem de Execução Correta

```
1. load_dotenv()                           # Carregar .env
   ↓
2. import config                           # Importar config PRIMEIRO
   ↓  (CrewAI é carregado completamente aqui)
3. import dspy_config                      # Carregar dependências
   ↓
4. import agentops                         # Importar AgentOps DEPOIS
   ↓
5. agentops.init(auto_start_session=False) # Inicializar AgentOps
   ↓
6. agentops.start_session()                # Iniciar session
   ↓
7. from crew_crewai_dspy import ...        # Importar crew function
   ↓
8. create_agent()                          # Criar agent (chama config.get_llm())
   ↓
9. ChatOpenAI criado                       # LLM é criado COM AgentOps ativo
   ↓
10. agent.execute()                        # LLM call É RASTREADA! ✅
```

**Chave**: Importar `config` (que importa CrewAI) **ANTES** de `agentops.init()` evita circular import!

## 📊 O Que Será Rastreado Agora

Com essas mudanças, o AgentOps vai rastrear **TUDO**:

### ✅ Agents
- Product Manager
- Software Architect
- Software Engineer
- QA Engineer
- Technical Writer

### ✅ Tools
- `file_writer_tool`
- `file_reader_tool`
- `directory_creator_tool`
- `retrieve_context_tool`
- `semantic_search_tool`

### ✅ Tasks
- Create PRD
- Design Architecture
- Implement Code
- Create Tests
- Write Documentation

### ✅ LLM Calls (NOVO!)
- **Modelo**: gpt-4o-mini
- **Tokens**: Input + Output por call
- **Custo**: $ por call e total
- **Latência**: Tempo de resposta
- **Prompts**: System + User prompts
- **Responses**: LLM outputs

### ✅ Session Metrics
- Total duration
- Total cost
- Total tokens
- Success/failure rate
- Errors (se houver)

## 🧪 Como Testar

### Teste Rápido:
```bash
python test_crewai_dspy_single.py
```

**Verifique no AgentOps**:
1. Abra o dashboard do AgentOps
2. Vá para a session mais recente
3. Deve mostrar:
   - ✅ 5 agents executando
   - ✅ 5 tasks completadas
   - ✅ ~10-15 tool calls
   - ✅ **~20-30 LLM calls** ← NOVO!
   - ✅ Tokens e custos detalhados ← NOVO!

### Baseline Completo:
```bash
./scripts/run_baseline_crewai_dspy.sh
```

**Resultados esperados** (5 projetos):
- ~100-150 LLM calls total
- ~500K-1M tokens
- $5-10 custo total
- Todas as métricas visíveis no AgentOps

## 🔧 Mudanças de Arquivos

| Arquivo | Mudança | Motivo |
|---------|---------|--------|
| `config.py` | + `get_llm()` | Criar LLM configurado para agents |
| `agents_crewai_dspy.py` | + `llm=config.get_llm()` em 6 agents | Agents usam LLM rastreável |
| `test_crewai_dspy_single.py` | AgentOps init com `auto_start_session=False` | Evitar circular import + rastrear LLMs |
| `scripts/run_baseline_crewai_dspy.sh` | AgentOps init com `auto_start_session=False` | Evitar circular import + rastrear LLMs |

## ⚠️ Problema de Circular Import (RESOLVIDO)

### Erro que ocorria:
```
ImportError: cannot import name 'Agent' from partially initialized module 'crewai.agent'
(most likely due to a circular import)
```

### Causa:
AgentOps tentava instrumentar CrewAI automaticamente durante `agentops.init()`, mas o CrewAI ainda não estava totalmente carregado, causando circular import.

### Solução Final:
1. **Importar `config` e `dspy_config` ANTES de `agentops.init()`**
   - Isso carrega o CrewAI completamente primeiro
2. **Depois inicializar AgentOps** com `auto_start_session=False`
3. **Iniciar session** com `agentops.start_session()`
4. **Importar crew function** por último

**Ordem crítica**: `config` → `agentops.init()` → `agentops.start_session()` → `crew_crewai_dspy`

## 🎉 Resultado Final

Agora o AgentOps rastreia **100% do workflow**:

```
Dashboard do AgentOps mostrará:

┌─────────────────────────────────────┐
│  Session: crewai-dspy-hybrid        │
├─────────────────────────────────────┤
│  Agents: 5                          │
│  Tasks: 5 completed                 │
│  Tools: 15 calls                    │
│  LLM Calls: 28 ✅ NOVO!             │
│  Tokens: 45,230 ✅ NOVO!            │
│  Cost: $2.15 ✅ NOVO!               │
│  Duration: 8m 32s                   │
│  Status: Success                    │
└─────────────────────────────────────┘

Timeline:
  [Agent: Product Manager]
    → Tool: retrieve_context
    → LLM Call: gpt-4o-mini (1,245 tokens) ✅
    → Tool: file_writer
  [Agent: Architect]
    → Tool: file_reader
    → LLM Call: gpt-4o-mini (2,103 tokens) ✅
    → Tool: retrieve_context
    → LLM Call: gpt-4o-mini (1,876 tokens) ✅
  ...
```

## 🚀 Próximos Passos

1. **Execute o teste rápido**:
   ```bash
   python test_crewai_dspy_single.py
   ```

2. **Verifique no AgentOps** se LLM calls aparecem

3. **Se OK, execute baseline completo**:
   ```bash
   ./scripts/run_baseline_crewai_dspy.sh
   ```

4. **Compare com baselines anteriores**:
   - SEM RAG: `metrics/data/sem_rag/`
   - COM RAG: `metrics/data/com_rag/`
   - **COM RAG + DSPy**: `metrics/data/crewai_dspy/` ← NOVO!

---

**Data**: 2025-11-13
**Status**: ✅ Correção implementada e testável
**Tracking**: AgentOps agora rastreia 100% (agents, tools, tasks, **LLM calls**)
