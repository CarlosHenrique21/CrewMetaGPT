# CrewAI + DSPy Hybrid Approach

## 🎯 Objetivo

Combinar o melhor de dois mundos:
- **CrewAI**: Framework completo para orquestração de agentes (agents, tasks, tools)
- **DSPy**: Otimização manual de prompts usando few-shot learning

## ❌ Problema Anterior

O `crew_dspy_manual.py` usava **apenas DSPy Modules**, o que causava:
- ❌ Não executava tasks completas
- ❌ Não criava arquivos corretamente
- ❌ AgentOps só rastreava LLM calls (sem tools, agents, tasks)
- ❌ Bypass do framework CrewAI

## ✅ Solução: Hybrid Approach

Integrar DSPy **DENTRO** do CrewAI, não substituir:

```
┌─────────────────────────────────────────────┐
│          CrewAI Framework                    │
│  ┌────────────────────────────────────┐     │
│  │   Agent (role, goal, backstory)    │     │
│  │   + DSPy Few-Shot Examples         │◄────┼── DSPy Manual Optimization
│  │   + RAG Tools                       │     │
│  │   + File Tools                      │     │
│  └────────────────────────────────────┘     │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │   Task (description, agent)        │     │
│  │   + Enhanced Instructions          │     │
│  └────────────────────────────────────┘     │
│                                              │
│  ┌────────────────────────────────────┐     │
│  │   Crew (tasks, process, memory)    │     │
│  └────────────────────────────────────┘     │
└─────────────────────────────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   AgentOps Tracking   │
         ├──────────────────────┤
         │ • Tools              │
         │ • Agents             │
         │ • Tasks              │
         │ • LLM Calls          │
         │ • Costs              │
         └──────────────────────┘
```

## 📁 Arquivos Criados

### 1. `agents_crewai_dspy.py`
- **Agentes CrewAI** com prompts otimizados por DSPy
- Cada agent tem **few-shot examples** no backstory
- Mantém todas as tools (file_writer, file_reader, RAG, etc.)
- Exemplo:
  ```python
  def create_product_manager() -> Agent:
      enhanced_backstory = f"""You are an experienced PM...

      Here is an example of an EXCELLENT PRD:
      {PRD_EXAMPLE}  # ← DSPy few-shot example

      Your PRDs should follow this structure..."""

      return Agent(
          role="Product Manager",
          backstory=enhanced_backstory,
          tools=[file_writer_tool, retrieve_context_tool, ...]  # ← CrewAI tools
      )
  ```

### 2. `crew_crewai_dspy.py`
- **CrewAI Crew** usando os agents otimizados
- Tasks com instruções detalhadas baseadas em DSPy best practices
- Mantém Process.sequential, memory, etc.
- Função principal: `run_software_dev_crew_dspy(project_idea)`

### 3. `scripts/run_baseline_crewai_dspy.sh`
- Script para executar baseline completo (5 projetos)
- Salva métricas em `metrics/data/crewai_dspy/`
- Integra com AgentOps para tracking completo

### 4. `test_crewai_dspy_single.py`
- Teste rápido com 1 projeto
- Verifica se tudo funciona antes do baseline completo

## 🚀 Como Usar

### Teste Rápido (1 projeto)

```bash
python test_crewai_dspy_single.py
```

Isso vai:
1. Executar 1 projeto simples (calculadora CLI)
2. Criar todos os arquivos (prd.md, architecture.md, código, testes, docs)
3. Rastrear tudo no AgentOps
4. Mostrar se files foram criados corretamente

**Duração**: ~5-10 minutos
**Custo**: ~$1-2

### Baseline Completo (5 projetos)

```bash
./scripts/run_baseline_crewai_dspy.sh
```

Isso vai:
1. Executar 5 projetos de teste
2. Cada projeto passa por 5 agents (PM, Architect, Engineer, QA, Tech Writer)
3. Criar estrutura completa de arquivos para cada projeto
4. Rastrear TUDO no AgentOps (tools, agents, tasks, LLM, costs)
5. Salvar métricas em `metrics/data/crewai_dspy/`

**Duração**: ~30-50 minutos
**Custo**: ~$5-10

## 📊 O Que é Rastreado no AgentOps

Com essa abordagem híbrida, AgentOps rastreia:

✅ **Tool Calls**
- `file_writer_tool` (quando cria arquivos)
- `file_reader_tool` (quando lê arquivos)
- `directory_creator_tool` (quando cria diretórios)
- `retrieve_context_tool` (quando busca no knowledge base)
- `semantic_search_tool` (quando faz busca semântica)

✅ **Agent Actions**
- Product Manager
- Software Architect
- Software Engineer
- QA Engineer
- Technical Writer

✅ **Task Execution**
- Create PRD
- Design Architecture
- Implement Code
- Create Tests
- Write Documentation

✅ **LLM Calls**
- Modelo usado (gpt-4o)
- Tokens (input + output)
- Custo de cada call
- Latência

✅ **Costs**
- Custo total por projeto
- Custo por agent
- Custo por task

## 🔍 Diferenças vs Abordagens Anteriores

### `crew_dspy_manual.py` (Anterior - Problema)
```python
# Usava APENAS DSPy Modules
pipeline = SoftwareDevPipelineManual()  # ← Puro DSPy
result = pipeline(project_idea)         # ← Sem CrewAI

# Resultado:
# ❌ Sem tasks tracking
# ❌ Sem tools tracking
# ❌ Sem agents tracking
# ❌ Arquivos não criados corretamente
```

### `crew_crewai_dspy.py` (Nova - Solução)
```python
# Usa CrewAI COM prompts otimizados por DSPy
crew = create_software_dev_crew_dspy(project_idea)  # ← CrewAI Crew
result = crew.kickoff()                             # ← CrewAI execution

# Resultado:
# ✅ Tasks completas
# ✅ Tools executadas
# ✅ Agents rastreados
# ✅ Arquivos criados corretamente
# ✅ AgentOps tracking completo
```

## 🎨 Como DSPy Melhora os Prompts

### Sem DSPy (baseline original)
```python
backstory = """You are a Product Manager.
Create a PRD for the project."""
```

### Com DSPy Manual (hybrid)
```python
backstory = f"""You are a Product Manager.

Here is an example of an EXCELLENT PRD:
{PRD_EXAMPLE}  # ← Exemplo completo de PRD de qualidade

Your PRDs should follow this structure and include:
- Project goals with clear objectives
- Functional requirements with FR-IDs
- Non-functional requirements with metrics
- Success criteria with KPIs
- Constraints and assumptions"""
```

O DSPy fornece **exemplos concretos** que guiam o LLM a gerar outputs de maior qualidade.

## 📈 Comparação de Baselines

Agora você terá 3 baselines para comparar:

| Baseline | RAG | DSPy | Tracking | Files Created |
|----------|-----|------|----------|---------------|
| **SEM RAG** | ❌ | ❌ | Full | ✅ |
| **COM RAG** | ✅ | ❌ | Full | ✅ |
| **COM RAG + DSPy** | ✅ | ✅ | Full | ✅ |

## 🔧 Arquitetura Técnica

```python
# 1. Agent com DSPy few-shot
agent = Agent(
    role="Product Manager",
    backstory=enhanced_backstory,  # ← Inclui DSPy examples
    tools=[file_writer_tool, retrieve_context_tool]
)

# 2. Task usando o agent
task = Task(
    description="Create PRD...",
    agent=agent  # ← Agent otimizado
)

# 3. Crew orquestrando tudo
crew = Crew(
    tasks=[task1, task2, ...],
    process=Process.sequential
)

# 4. Execução
result = crew.kickoff()  # ← CrewAI executa, AgentOps rastreia tudo
```

## 📝 Métricas Salvas

Após executar o baseline, você terá:

```
metrics/data/crewai_dspy/
├── baseline_project_01.json
├── baseline_project_02.json
├── baseline_project_03.json
├── baseline_project_04.json
├── baseline_project_05.json
└── baseline_report.json
```

Cada arquivo contém:
- `project_id`, `project_name`
- `status` (success/error)
- `duration_seconds`
- `timestamp`
- `approach`: "crewai_dspy_hybrid"

O `baseline_report.json` contém resumo agregado de todos os projetos.

## 🎯 Próximos Passos

1. **Execute o teste rápido**:
   ```bash
   python test_crewai_dspy_single.py
   ```

2. **Verifique no AgentOps** se está rastreando:
   - Tools ✅
   - Agents ✅
   - Tasks ✅
   - LLM calls ✅

3. **Se tudo OK, execute baseline completo**:
   ```bash
   ./scripts/run_baseline_crewai_dspy.sh
   ```

4. **Compare os 3 baselines** usando os dados de `metrics/data/`:
   - `sem_rag/` - Baseline sem RAG
   - `com_rag/` - Baseline com RAG
   - `crewai_dspy/` - Baseline com RAG + DSPy

## ✨ Vantagens da Abordagem Híbrida

1. **Full Observability**: AgentOps vê tudo (tools, agents, tasks, LLM)
2. **Better Prompts**: DSPy few-shot examples melhoram qualidade dos outputs
3. **RAG Context**: Knowledge base fornece exemplos e best practices
4. **Proper Execution**: CrewAI garante que tasks sejam completadas e files criados
5. **Easy Comparison**: Métricas consistentes com outros baselines

## 🐛 Troubleshooting

### Se AgentOps não rastrear tools:
- Verifique se `AGENTOPS_API_KEY` está configurada no `.env`
- Verifique se agents estão usando os tools do `tools.py`

### Se files não forem criados:
- Verifique se `WORKSPACE_DIR` está configurado no `config.py`
- Verifique logs do CrewAI para ver se tools foram chamadas

### Se LLM calls falharem:
- Verifique se `OPENAI_API_KEY` está configurada e válida
- Verifique se tem créditos na conta OpenAI

## 📚 Referências

- **CrewAI**: https://github.com/joaomdmoura/crewAI
- **DSPy**: https://github.com/stanfordnlp/dspy
- **AgentOps**: https://www.agentops.ai/

---

**Criado em**: 2025-11-13
**Abordagem**: Hybrid CrewAI + DSPy + RAG + AgentOps
**Status**: ✅ Pronto para teste
