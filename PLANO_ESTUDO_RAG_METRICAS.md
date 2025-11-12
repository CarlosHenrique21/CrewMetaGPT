# Plano de Estudo: CrewAI com RAG e Otimização

## 📋 Visão Geral

Este documento descreve um plano completo para implementar e avaliar agentes RAG no sistema CrewAI, com foco em métricas de performance e estudo comparativo entre diferentes abordagens de otimização.

---

## ✅ IDEIA 1: Implementação de Agente RAG

### **Resposta: SIM, é possível e viável**

### Como Aplicar:

#### 1.1 Arquitetura do Agente RAG

```python
# Novo agente: Knowledge Manager (RAG Agent)
- Role: Gerenciador de Base de Conhecimento
- Goal: Fornecer contexto relevante de documentos para outros agentes
- Tools:
  - Document Loader (PDF, MD, TXT, Code)
  - Vector Store (FAISS, ChromaDB, Pinecone)
  - Semantic Search
  - Context Retriever
```

#### 1.2 Componentes Necessários

**A. Document Loader Tool**
```python
@tool("load_documents")
def load_documents_tool(directory: str, file_types: list) -> str:
    """
    Carrega documentos de um diretório e cria embeddings.
    - Suporta: .md, .py, .txt, .pdf, .docx
    - Cria embeddings usando OpenAI/HuggingFace
    - Armazena em vector store
    """
```

**B. Semantic Search Tool**
```python
@tool("semantic_search")
def semantic_search_tool(query: str, top_k: int = 5) -> str:
    """
    Busca semântica na base de conhecimento.
    - Converte query em embedding
    - Busca documentos similares
    - Retorna top_k resultados mais relevantes
    """
```

**C. Context Retriever Tool**
```python
@tool("retrieve_context")
def retrieve_context_tool(task_description: str) -> str:
    """
    Recupera contexto relevante para uma tarefa específica.
    - Analisa a tarefa
    - Busca documentos relacionados
    - Formata contexto para o LLM
    """
```

#### 1.3 Integração com Agentes Existentes

```python
# Modificar agents.py para incluir RAG
def create_rag_knowledge_manager() -> Agent:
    return Agent(
        role="Knowledge Manager",
        goal="Retrieve and provide relevant context from knowledge base",
        backstory="""You are a Knowledge Manager specialized in RAG.
        You have access to a comprehensive knowledge base and can:
        - Search for relevant information
        - Retrieve code examples
        - Find best practices and patterns
        - Provide contextual documentation
        """,
        tools=[
            load_documents_tool,
            semantic_search_tool,
            retrieve_context_tool,
            file_reader_tool,
        ],
        verbose=True,
        allow_delegation=False,
    )

# Adicionar RAG às tarefas
def create_prd_task_with_rag(project_idea: str) -> Task:
    return Task(
        description=f"""
        1. Use the Knowledge Manager to search for similar projects
        2. Retrieve best practices for {project_idea}
        3. Create PRD enriched with retrieved context
        """,
        agent=create_product_manager(),
        context=[retrieve_knowledge_task()]  # Nova task de RAG
    )
```

#### 1.4 Base de Conhecimento Sugerida

Crie um diretório `knowledge_base/`:
```
knowledge_base/
├── best_practices/
│   ├── software_architecture.md
│   ├── coding_standards.md
│   └── testing_strategies.md
├── templates/
│   ├── prd_templates.md
│   ├── architecture_templates.md
│   └── test_plan_templates.md
├── code_examples/
│   ├── python_patterns.py
│   ├── testing_examples.py
│   └── api_examples.py
└── documentation/
    ├── project_guidelines.md
    └── development_process.md
```

#### 1.5 Implementação de Métricas Básicas

```python
# Adicionar ao RAG agent
import time
from dataclasses import dataclass

@dataclass
class RAGMetrics:
    retrieval_latency: float
    num_documents_retrieved: int
    relevance_score: float
    llm_latency: float
    total_latency: float
    tokens_used: int
    estimated_cost: float

def track_rag_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        metrics = RAGMetrics(
            retrieval_latency=end_time - start_time,
            # ... outros campos
        )
        log_metrics(metrics)
        return result
    return wrapper
```

---

## ✅ IDEIA 2: Sistema Completo de Métricas

### **Resposta: SIM, viável e necessário para estudo científico**

### Como Aplicar:

#### 2.1 Métricas a Implementar

**A. Latency Tracking**
```python
# metrics_tracker.py
import time
from typing import Dict, List
from datetime import datetime

class MetricsTracker:
    def __init__(self):
        self.metrics = {
            'retrieval_times': [],
            'llm_times': [],
            'verification_times': [],
            'tool_usage': {},
            'agent_success_rate': {},
            'throughput': [],
        }

    def track_stage(self, stage_name: str, duration: float):
        """Registra tempo de cada etapa"""
        self.metrics[f'{stage_name}_times'].append({
            'timestamp': datetime.now(),
            'duration': duration
        })

    def track_retrieval(self, duration: float, docs_retrieved: int):
        """Métricas de recuperação RAG"""
        self.metrics['retrieval_times'].append({
            'duration': duration,
            'docs_count': docs_retrieved,
            'timestamp': datetime.now()
        })

    def track_llm_call(self, duration: float, tokens: int, cost: float):
        """Métricas de chamadas LLM"""
        self.metrics['llm_times'].append({
            'duration': duration,
            'tokens': tokens,
            'cost': cost,
            'timestamp': datetime.now()
        })

    def calculate_throughput(self, time_window: int = 60):
        """Queries por minuto"""
        recent_queries = [
            q for q in self.metrics['throughput']
            if (datetime.now() - q['timestamp']).seconds <= time_window
        ]
        return len(recent_queries)
```

**B. Tool Usage Tracking**
```python
class ToolUsageTracker:
    def __init__(self):
        self.tool_calls = {}

    def track_tool_call(self, tool_name: str, success: bool, duration: float):
        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = {
                'total_calls': 0,
                'successful_calls': 0,
                'failed_calls': 0,
                'total_duration': 0,
                'avg_duration': 0
            }

        self.tool_calls[tool_name]['total_calls'] += 1
        if success:
            self.tool_calls[tool_name]['successful_calls'] += 1
        else:
            self.tool_calls[tool_name]['failed_calls'] += 1

        self.tool_calls[tool_name]['total_duration'] += duration
        self.tool_calls[tool_name]['avg_duration'] = (
            self.tool_calls[tool_name]['total_duration'] /
            self.tool_calls[tool_name]['total_calls']
        )
```

**C. Agent Success Rate**
```python
class AgentPerformanceTracker:
    def __init__(self):
        self.agent_metrics = {}

    def track_agent_task(self, agent_name: str, task_id: str,
                         success: bool, duration: float, quality_score: float = None):
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = {
                'tasks_completed': 0,
                'tasks_failed': 0,
                'success_rate': 0.0,
                'avg_duration': 0.0,
                'quality_scores': []
            }

        metrics = self.agent_metrics[agent_name]
        if success:
            metrics['tasks_completed'] += 1
        else:
            metrics['tasks_failed'] += 1

        total_tasks = metrics['tasks_completed'] + metrics['tasks_failed']
        metrics['success_rate'] = metrics['tasks_completed'] / total_tasks

        if quality_score:
            metrics['quality_scores'].append(quality_score)
```

#### 2.2 Integração com AgentOps

```python
# enhanced_tracking.py
import agentops
from metrics_tracker import MetricsTracker, ToolUsageTracker, AgentPerformanceTracker

class EnhancedObservability:
    def __init__(self):
        self.metrics_tracker = MetricsTracker()
        self.tool_tracker = ToolUsageTracker()
        self.agent_tracker = AgentPerformanceTracker()
        self.agentops_session = None

    def init_agentops(self, api_key: str):
        """Inicializa AgentOps com métricas customizadas"""
        self.agentops_session = agentops.init(
            api_key=api_key,
            default_tags=['rag-study', 'performance-metrics'],
            auto_start_session=True,
            instrument_llm_calls=True,
        )

    def log_custom_metrics(self):
        """Envia métricas customizadas para AgentOps"""
        agentops.record({
            'avg_retrieval_latency': self.metrics_tracker.get_avg_retrieval_time(),
            'throughput': self.metrics_tracker.calculate_throughput(),
            'tool_efficiency': self.tool_tracker.get_efficiency_report(),
            'agent_success_rates': self.agent_tracker.get_success_rates()
        })
```

#### 2.3 Dashboard de Métricas

```python
# metrics_dashboard.py
import json
from pathlib import Path

def generate_metrics_report(metrics_tracker, output_file: str = "metrics_report.json"):
    """Gera relatório completo de métricas"""
    report = {
        'summary': {
            'total_queries': len(metrics_tracker.metrics['throughput']),
            'avg_latency': calculate_avg_latency(metrics_tracker),
            'total_cost': calculate_total_cost(metrics_tracker),
            'success_rate': calculate_overall_success_rate(metrics_tracker),
        },
        'detailed_metrics': {
            'latency_breakdown': {
                'retrieval': get_avg(metrics_tracker.metrics['retrieval_times']),
                'llm': get_avg(metrics_tracker.metrics['llm_times']),
                'verification': get_avg(metrics_tracker.metrics['verification_times']),
            },
            'tool_usage': metrics_tracker.tool_calls,
            'agent_performance': metrics_tracker.agent_metrics,
            'throughput_over_time': calculate_throughput_timeline(metrics_tracker),
        }
    }

    Path(output_file).write_text(json.dumps(report, indent=2))
    return report
```

---

## ✅ IDEIA 3: Estudo Comparativo (Atual vs RAG vs Otimizado)

### **Resposta: SIM, excelente abordagem para estudo acadêmico**

### Como Aplicar:

#### 3.1 Estrutura do Estudo

**Fase 1: Baseline (Sistema Atual)**
```
Objetivo: Estabelecer métricas de referência
Duração: 1 semana
Atividades:
- Executar 50 projetos diferentes
- Coletar métricas base
- Documentar limitações
```

**Fase 2: RAG Implementation**
```
Objetivo: Avaliar impacto do RAG
Duração: 2 semanas
Atividades:
- Implementar agente RAG
- Executar mesmos 50 projetos
- Comparar com baseline
- Analisar melhoria de qualidade
```

**Fase 3: Optimization (AutoPDL + DSPy)**
```
Objetivo: Otimizar prompts e fluxo
Duração: 2 semanas
Atividades:
- Aplicar AutoPDL para otimização de prompts
- Usar DSPy para programação declarativa
- Executar mesmos 50 projetos
- Comparar com Fase 1 e 2
```

#### 3.2 Métricas de Comparação

```python
# comparison_study.py
from dataclasses import dataclass
from typing import List

@dataclass
class StudyPhase:
    name: str
    avg_latency: float
    avg_cost: float
    success_rate: float
    quality_score: float  # Avaliação manual ou automatizada
    throughput: float

@dataclass
class ComparativeStudy:
    baseline: StudyPhase
    rag_phase: StudyPhase
    optimized_phase: StudyPhase

    def calculate_improvements(self):
        """Calcula melhorias percentuais"""
        return {
            'rag_vs_baseline': {
                'latency_improvement': self.calculate_improvement(
                    self.baseline.avg_latency,
                    self.rag_phase.avg_latency
                ),
                'cost_reduction': self.calculate_improvement(
                    self.baseline.avg_cost,
                    self.rag_phase.avg_cost
                ),
                'quality_improvement': self.calculate_improvement(
                    self.baseline.quality_score,
                    self.rag_phase.quality_score
                ),
            },
            'optimized_vs_baseline': {
                # Similar calculations
            },
            'optimized_vs_rag': {
                # Similar calculations
            }
        }

    def calculate_improvement(self, baseline: float, new: float) -> float:
        """Calcula % de melhoria"""
        return ((new - baseline) / baseline) * 100
```

#### 3.3 Protocolo de Teste

```markdown
## Protocolo de Teste Científico

### Variáveis Controladas:
- Mesmo conjunto de 50 projetos em todas as fases
- Mesma temperatura LLM (0.7)
- Mesmo modelo (GPT-4)
- Mesma base de conhecimento

### Variáveis Medidas:
1. **Performance**
   - Latência total (ms)
   - Latência por etapa (retrieval, LLM, verification)
   - Throughput (projetos/hora)

2. **Custo**
   - Tokens totais
   - Custo em USD
   - Custo por projeto

3. **Qualidade**
   - Taxa de sucesso (builds que funcionam)
   - Cobertura de requisitos (%)
   - Qualidade do código (score 0-10)
   - Completude da documentação (%)

4. **Eficiência**
   - Número de chamadas LLM
   - Número de tool calls
   - Taxa de reuso de contexto

### Metodologia:
1. Executar 10 projetos de warm-up (não contam)
2. Executar 50 projetos de teste
3. Coletar métricas automaticamente
4. Avaliação manual de qualidade (amostra de 10 projetos)
5. Análise estatística (t-test, ANOVA)
```

#### 3.4 Implementação AutoPDL + DSPy

**AutoPDL (Automatic Prompt Design and Learning)**
```python
# autopldl_optimization.py
from dspy import DSPyModule, Signature, ChainOfThought

class OptimizedProductManager(DSPyModule):
    """Product Manager otimizado com DSPy"""

    def __init__(self):
        super().__init__()
        self.generate_prd = ChainOfThought(PRDSignature)

    def forward(self, project_idea: str, knowledge_base_context: str):
        """Gera PRD com contexto otimizado"""
        return self.generate_prd(
            project_idea=project_idea,
            context=knowledge_base_context
        )

class PRDSignature(Signature):
    """Signature para geração de PRD"""
    project_idea: str = dspy.InputField()
    context: str = dspy.InputField(desc="Relevant knowledge from RAG")
    prd: str = dspy.OutputField(desc="Comprehensive PRD document")

# Treinar com exemplos
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=prd_quality_metric)
optimized_pm = optimizer.compile(
    OptimizedProductManager(),
    trainset=training_examples
)
```

**DSPy Integration**
```python
# dspy_agents.py
import dspy
from dspy import ChainOfThought, Predict

# Configurar LM
lm = dspy.OpenAI(model='gpt-4', max_tokens=4000)
dspy.settings.configure(lm=lm)

class RAGProductManager(dspy.Module):
    def __init__(self):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=5)
        self.generate_prd = ChainOfThought("context, project_idea -> prd")

    def forward(self, project_idea):
        # Retrieve context
        context = self.retrieve(project_idea).passages

        # Generate PRD with context
        prd = self.generate_prd(
            context=context,
            project_idea=project_idea
        )

        return prd
```

#### 3.5 Estrutura de Arquivos do Estudo

```
CrewAI-Project/
├── study/
│   ├── phase1_baseline/
│   │   ├── results/
│   │   ├── metrics/
│   │   └── analysis.ipynb
│   ├── phase2_rag/
│   │   ├── results/
│   │   ├── metrics/
│   │   └── analysis.ipynb
│   ├── phase3_optimized/
│   │   ├── results/
│   │   ├── metrics/
│   │   └── analysis.ipynb
│   ├── comparison/
│   │   ├── comparative_analysis.ipynb
│   │   ├── statistical_tests.py
│   │   └── final_report.md
│   └── test_projects/
│       ├── project_001.txt
│       ├── project_002.txt
│       └── ... (50 projetos)
├── knowledge_base/  # Base de conhecimento RAG
├── metrics/         # Sistema de métricas
│   ├── metrics_tracker.py
│   ├── tool_usage_tracker.py
│   └── agent_performance_tracker.py
├── optimization/    # AutoPDL + DSPy
│   ├── dspy_agents.py
│   ├── autopldl_optimization.py
│   └── prompt_templates/
└── rag/            # Sistema RAG
    ├── rag_agent.py
    ├── vector_store.py
    └── retriever_tools.py
```

---

## 📊 Cronograma de Implementação

### Semana 1-2: Setup e Baseline
- [ ] Criar 50 projetos de teste variados
- [ ] Implementar sistema de métricas básico
- [ ] Executar baseline completo
- [ ] Documentar resultados Fase 1

### Semana 3-4: Implementação RAG
- [ ] Criar estrutura da base de conhecimento
- [ ] Implementar document loader
- [ ] Implementar vector store (FAISS/ChromaDB)
- [ ] Criar agente RAG
- [ ] Integrar RAG com agentes existentes
- [ ] Implementar métricas de retrieval

### Semana 5-6: Testes RAG
- [ ] Executar 50 projetos com RAG
- [ ] Coletar métricas detalhadas
- [ ] Comparar com baseline
- [ ] Análise preliminar

### Semana 7-8: Otimização (AutoPDL + DSPy)
- [ ] Instalar e configurar DSPy
- [ ] Converter agentes para DSPy modules
- [ ] Implementar AutoPDL
- [ ] Treinar prompts otimizados
- [ ] Executar 50 projetos otimizados

### Semana 9-10: Análise e Relatório
- [ ] Análise estatística completa
- [ ] Gerar gráficos comparativos
- [ ] Escrever paper/relatório científico
- [ ] Preparar apresentação

---

## 🔬 Hipóteses do Estudo

**H1:** RAG melhora a qualidade das entregas em 20-30%
- Medida: Quality score, completude, adequação aos requisitos

**H2:** RAG aumenta latência em 10-15% mas reduz custo total em 15-25%
- Medida: Latência total, número de LLM calls, tokens usados

**H3:** Otimização com AutoPDL/DSPy reduz latência em 25-35% vs baseline
- Medida: Latência, throughput

**H4:** Sistema otimizado tem taxa de sucesso 40-50% maior que baseline
- Medida: Success rate, builds funcionais

---

## 📈 Métricas de Sucesso do Estudo

### Quantitativas:
- **Performance**: Redução de 20%+ em latência média
- **Custo**: Redução de 15%+ em custo por projeto
- **Qualidade**: Aumento de 25%+ em quality score
- **Throughput**: Aumento de 30%+ em projetos/hora

### Qualitativas:
- Código mais robusto e bem estruturado
- Documentação mais completa
- Menor taxa de erros/bugs
- Melhor aderência aos requisitos

---

## 🛠️ Ferramentas e Dependências

```bash
# requirements_study.txt
crewai>=0.28.0
agentops>=0.2.0
langchain>=0.1.0
langchain-openai>=0.0.5
openai>=1.10.0

# RAG
faiss-cpu>=1.7.4  # ou faiss-gpu
chromadb>=0.4.22
sentence-transformers>=2.3.1
pypdf>=4.0.0
python-docx>=1.1.0

# Optimization
dspy-ai>=2.0.0

# Metrics & Analysis
pandas>=2.1.0
numpy>=1.24.0
matplotlib>=3.8.0
seaborn>=0.13.0
scipy>=1.11.0
jupyter>=1.0.0
```

---

## 📝 Template de Relatório Final

```markdown
# Estudo Comparativo: CrewAI com RAG e Otimização

## Abstract
[Resumo dos resultados]

## 1. Introdução
### 1.1 Motivação
### 1.2 Objetivos
### 1.3 Contribuições

## 2. Background
### 2.1 Multi-Agent Systems
### 2.2 RAG (Retrieval-Augmented Generation)
### 2.3 Prompt Optimization (AutoPDL, DSPy)

## 3. Metodologia
### 3.1 Configuração Experimental
### 3.2 Métricas
### 3.3 Protocolo de Teste

## 4. Resultados
### 4.1 Fase 1: Baseline
### 4.2 Fase 2: RAG
### 4.3 Fase 3: Otimizado
### 4.4 Análise Comparativa

## 5. Discussão
### 5.1 Validação de Hipóteses
### 5.2 Trade-offs
### 5.3 Limitações

## 6. Conclusão
### 6.1 Principais Achados
### 6.2 Trabalhos Futuros

## Referências
```

---

## 🎯 Resumo Executivo

### ✅ IDEIA 1 - RAG Agent: **VIÁVEL**
- Implementação estimada: 2 semanas
- Complexidade: Média
- Impacto esperado: Alto (qualidade +25%)

### ✅ IDEIA 2 - Sistema de Métricas: **NECESSÁRIO**
- Implementação estimada: 1 semana
- Complexidade: Baixa-Média
- Impacto esperado: Essencial para estudo científico

### ✅ IDEIA 3 - Estudo Comparativo: **EXCELENTE**
- Duração total: 10 semanas
- Complexidade: Alta
- Impacto esperado: Publicação científica, contribuição acadêmica

---

## 🚀 Próximos Passos Imediatos

1. **Criar base de conhecimento inicial** (1 dia)
   ```bash
   mkdir -p knowledge_base/{best_practices,templates,examples}
   ```

2. **Implementar metrics_tracker.py** (2 dias)
   - MetricsTracker class
   - ToolUsageTracker class
   - AgentPerformanceTracker class

3. **Definir 50 projetos de teste** (1 dia)
   - Variados em complexidade
   - Diferentes domínios
   - Documentados em test_projects/

4. **Executar baseline** (2-3 dias)
   - Rodar todos os 50 projetos
   - Coletar métricas
   - Analisar resultados

5. **Implementar RAG basic** (1 semana)
   - Document loader
   - Vector store
   - Basic retrieval

---

## 📚 Referências Úteis

- **DSPy**: https://github.com/stanfordnlp/dspy
- **LangChain RAG**: https://python.langchain.com/docs/use_cases/question_answering/
- **FAISS**: https://github.com/facebookresearch/faiss
- **AgentOps**: https://docs.agentops.ai/
- **AutoPDL Paper**: [Link quando disponível]

---

**Última atualização:** 2025-11-12
**Versão:** 1.0
**Status:** Plano Aprovado - Pronto para Execução
