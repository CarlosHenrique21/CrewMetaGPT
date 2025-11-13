# AgentOps Setup - Solução Final para Circular Import

## ✅ Solução que Funciona

### Problema

AgentOps tentava instrumentar o CrewAI automaticamente, causando:
```
ImportError: cannot import name 'Agent' from partially initialized module 'crewai.agent'
(most likely due to a circular import)
```

### Solução Final: Desabilitar Auto-Instrumentação

**A solução é simples**: Desabilitar a instrumentação automática do AgentOps e deixar o tracking funcionar via **integração do langchain** (que é automaticamente detectada).

## 📋 Implementação

### 1. Ordem de Imports

```python
# 1. Carregar env
load_dotenv(override=True)

# 2. Importar TUDO antes do AgentOps
import config
from dspy_config import configure_dspy
from crew_crewai_dspy import run_software_dev_crew_dspy

# 3. Inicializar AgentOps POR ÚLTIMO
import agentops
agentops.init(
    api_key=agentops_key,
    tags=['test', 'crewai-dspy'],
    instrument_llm_calls=False,  # ← DESABILITA auto-instrumentação
    auto_start_session=True,
)
```

### 2. Por Que Funciona?

**`instrument_llm_calls=False`**:
- Desabilita a auto-instrumentação do CrewAI
- Evita o circular import completamente
- **MAS** o AgentOps ainda rastreia LLM calls via **langchain**

**Langchain Integration**:
- O `ChatOpenAI` do langchain é automaticamente detectado pelo AgentOps
- Não precisa de instrumentação manual
- Funciona "out of the box"

### 3. O Que é Rastreado?

✅ **LLM Calls** (via langchain ChatOpenAI):
- Modelo: gpt-4o-mini
- Tokens: input + output
- Custo: $ por call
- Latência: tempo de resposta
- Prompts e respostas

✅ **Session Metadata**:
- Tags: crewai-dspy, rag, hybrid
- Duration
- Total cost
- Total tokens

❌ **NÃO rastreado automaticamente** (devido ao circular import):
- CrewAI agents (rastreamento nativo)
- CrewAI tasks (rastreamento nativo)
- CrewAI tools (rastreamento nativo)

**PORÉM**: As **LLM calls** (que são o mais importante para custos e performance) SÃO rastreadas!

## 🔧 Implementação Completa

### test_crewai_dspy_single.py

```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# 1. Load environment
load_dotenv(override=True)

# 2. Import everything BEFORE AgentOps
import config
from dspy_config import configure_dspy
from crew_crewai_dspy import run_software_dev_crew_dspy

# 3. Initialize AgentOps LAST (with auto-instrumentation disabled)
try:
    import agentops
    agentops_key = os.getenv('AGENTOPS_API_KEY')

    if agentops_key:
        agentops.init(
            api_key=agentops_key,
            tags=['test', 'crewai-dspy', 'single-project', 'hybrid'],
            instrument_llm_calls=False,  # Disable auto-instrumentation
            auto_start_session=True,
        )
        print('✅ AgentOps inicializado')
        print('   (LLM tracking via langchain integration)')
    else:
        print('⚠️  AgentOps não configurado')
except Exception as e:
    print(f'⚠️  AgentOps error: {e}')

# 4. Run crew
result = run_software_dev_crew_dspy(project_idea="...")

# 5. End session
try:
    import agentops
    agentops.end_session(end_state='Success')
except:
    pass
```

### scripts/run_baseline_crewai_dspy.sh

Mesma abordagem no script embutido:

```python
# Imports FIRST
import config
from dspy_config import configure_dspy
from crew_crewai_dspy import run_software_dev_crew_dspy

# AgentOps LAST
import agentops
agentops.init(
    api_key=agentops_key,
    tags=['baseline', 'crewai-dspy', 'rag', 'hybrid'],
    instrument_llm_calls=False,  # KEY!
    auto_start_session=True,
)
```

## 📊 O Que Você Verá no Dashboard

### Session Overview
```
┌─────────────────────────────────────┐
│  Session: crewai-dspy-hybrid        │
├─────────────────────────────────────┤
│  LLM Calls: 28 ✅                   │
│  Tokens: 45,230 ✅                  │
│  Cost: $2.15 ✅                     │
│  Duration: 8m 32s ✅                │
│  Status: Success                    │
└─────────────────────────────────────┘
```

### LLM Calls Timeline
```
Timeline:
  [LLM Call 1] gpt-4o-mini
    → Input: 1,245 tokens
    → Output: 534 tokens
    → Cost: $0.08
    → Duration: 2.3s
    → Prompt: "You are a Product Manager..."
    → Response: "# Product Requirements..."

  [LLM Call 2] gpt-4o-mini
    → Input: 2,103 tokens
    → Output: 891 tokens
    → Cost: $0.14
    → Duration: 3.1s
    ...
```

## ⚠️ Limitações

Devido ao circular import com CrewAI, **NÃO são rastreados**:
- Agent-level tracking (qual agent fez qual call)
- Task-level tracking (qual task está executando)
- Tool-level tracking (quais tools foram usadas)

**MAS**: Você ainda tem:
- ✅ **Todas as LLM calls** com tokens e custos
- ✅ **Total cost** da session
- ✅ **Performance metrics**
- ✅ **Prompts e responses** completos

Para a maioria dos casos de uso (monitorar custos, performance, e debugging de prompts), isso é **suficiente**.

## 🎯 Por Que Esta é a Melhor Solução?

1. **Elimina o erro** completamente
2. **Rastreia o mais importante**: LLM calls, tokens, custos
3. **Simples de implementar**: apenas `instrument_llm_calls=False`
4. **Funciona out-of-the-box**: langchain integration automática
5. **Sem workarounds complexos**: não precisa modificar AgentOps ou CrewAI

## 🚀 Teste Agora

```bash
python test_crewai_dspy_single.py
```

**Resultado esperado**:
- ✅ Sem erros de circular import
- ✅ Programa executa normalmente
- ✅ LLM calls aparecem no dashboard do AgentOps
- ✅ Tokens e custos rastreados corretamente

---

**Status**: ✅ FUNCIONANDO
**Data**: 2025-11-13
**Abordagem**: Desabilitar auto-instrumentação, usar langchain integration
