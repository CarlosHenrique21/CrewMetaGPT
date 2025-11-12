# 🧪 Guia de Testes Baseline

## O que é o Teste Baseline?

O teste baseline executa **5 projetos em sequência** para estabelecer métricas de referência do sistema. Essas métricas servirão como base de comparação para futuros testes com:
- RAG otimizado
- AutoPDL/DSPy
- Diferentes configurações

## 📋 Projetos de Teste

O baseline inclui 5 projetos variados:

1. **Todo List CLI** - Aplicação CLI simples
2. **URL Shortener API** - API REST básica
3. **Weather CLI** - Integração com API externa
4. **Password Generator** - Utilitário de segurança
5. **Markdown to HTML** - Conversor de formatos

Estes projetos foram escolhidos para representar diferentes tipos de tarefas e complexidades.

## 🚀 Como Executar

### Método 1: Script Bash (Recomendado)

```bash
./run_baseline_test.sh
```

### Método 2: Python Direto

```bash
python test_baseline.py
```

## ⏱️ Tempo de Execução

- **Duração estimada**: 10-15 minutos
- **Duração por projeto**: ~2-3 minutos
- **Pausa entre projetos**: 5 segundos

## 📊 Métricas Coletadas

Para cada projeto, o teste coleta:

### Métricas de Performance
- ⏱️ **Duração total** (segundos)
- 🚀 **Throughput** (queries/minuto)
- ⏳ **Latência por etapa** (retrieval, LLM, verificação)

### Métricas de Custo
- 💰 **Custo total** (USD)
- 🎫 **Tokens usados** (prompt + completion)
- 📊 **Custo por token**

### Métricas de Uso
- 📞 **LLM calls** (número de chamadas)
- 🔧 **Tool calls** (uso de ferramentas)
- 🔍 **RAG retrievals** (se habilitado)

### Métricas de Qualidade
- ✅ **Taxa de sucesso** (% de tasks completadas)
- 📝 **Arquivos gerados** (quantidade e tipos)

## 📁 Outputs Gerados

### 1. Relatório Consolidado
```
metrics/data/baseline_report.json
```

Contém:
- Estatísticas agregadas de todos os projetos
- Comparação entre projetos
- Médias, totais e distribuições

### 2. Métricas Individuais
```
metrics/data/baseline_project_01.json
metrics/data/baseline_project_02.json
metrics/data/baseline_project_03.json
metrics/data/baseline_project_04.json
metrics/data/baseline_project_05.json
```

Cada arquivo contém métricas detalhadas de um projeto específico.

### 3. Arquivos Gerados pelos Agentes
```
workspace/
├── prd.md
├── architecture.md
├── src/
│   └── [código gerado]
├── tests.py
├── README.md
└── user_guide.md
```

## 📈 Exemplo de Relatório

```json
{
  "report_type": "baseline",
  "timestamp": "2025-01-12T14:30:00",
  "batch_duration_seconds": 720.5,
  "total_projects": 5,
  "successful_projects": 5,
  "failed_projects": 0,
  "aggregated_stats": {
    "total_cost": 2.5430,
    "avg_cost_per_project": 0.5086,
    "total_tokens": 85340,
    "avg_tokens_per_project": 17068,
    "total_llm_calls": 75,
    "avg_llm_calls_per_project": 15,
    "total_rag_retrievals": 15,
    "avg_duration_per_project": 144.1
  },
  "projects": [...]
}
```

## 🎯 Como Usar os Resultados

### 1. Análise Individual
Visualize métricas de um projeto específico:
```bash
cat metrics/data/baseline_project_01.json | python -m json.tool
```

### 2. Análise Agregada
Visualize o relatório consolidado:
```bash
cat metrics/data/baseline_report.json | python -m json.tool
```

### 3. Comparação com Python
```python
import json
from pathlib import Path

# Carregar relatório
report = json.loads(Path("metrics/data/baseline_report.json").read_text())

# Estatísticas agregadas
stats = report['aggregated_stats']
print(f"Custo médio: ${stats['avg_cost_per_project']:.4f}")
print(f"Tokens médios: {stats['avg_tokens_per_project']:,}")
print(f"Duração média: {stats['avg_duration_per_project']:.1f}s")
```

### 4. Comparação com Futuros Testes
```python
import json

# Carregar baseline e novo teste
baseline = json.loads(Path("metrics/data/baseline_report.json").read_text())
rag_test = json.loads(Path("metrics/data/rag_report.json").read_text())

# Comparar custos
baseline_cost = baseline['aggregated_stats']['avg_cost_per_project']
rag_cost = rag_test['aggregated_stats']['avg_cost_per_project']

improvement = ((baseline_cost - rag_cost) / baseline_cost) * 100
print(f"Redução de custo: {improvement:.1f}%")
```

## 🔬 Estudos Comparativos

Este baseline é a **Fase 1** do estudo comparativo:

### Fase 1: Baseline (Este teste)
- Sistema atual sem otimizações
- Estabelece métricas de referência

### Fase 2: RAG (Próximo)
- Sistema com Retrieval-Augmented Generation
- Compare com baseline

### Fase 3: Otimizado (Futuro)
- Sistema com AutoPDL + DSPy
- Compare com baseline e RAG

Veja [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md) para detalhes.

## 🛠️ Personalização

### Modificar Projetos de Teste

Edite `test_baseline.py`:

```python
TEST_PROJECTS = [
    {
        "id": "project_01",
        "name": "Seu Projeto",
        "description": "descrição do projeto...",
    },
    # Adicione mais projetos...
]
```

### Ajustar Métricas

Edite as funções em `test_baseline.py`:
- `run_single_project()` - Coleta de métricas por projeto
- `generate_baseline_report()` - Agregação e relatório

### Desabilitar RAG Temporariamente

Para testar baseline puro sem RAG:
```bash
# Renomear knowledge_base
mv knowledge_base knowledge_base.disabled

# Executar teste
./run_baseline_test.sh

# Restaurar
mv knowledge_base.disabled knowledge_base
```

## 📊 Visualização de Métricas

### Terminal
O script imprime resumo automático:
```
================================================================================
📊 RELATÓRIO BASELINE - RESUMO CONSOLIDADO
================================================================================

Total de projetos: 5
✅ Sucesso: 5
❌ Falhas: 0
⏱️  Duração total: 720.50s (12.0 min)

--- ESTATÍSTICAS AGREGADAS ---
💰 Custo total: $2.5430
💰 Custo médio por projeto: $0.5086
🎫 Tokens totais: 85,340
...
```

### Python Script
Crie script customizado:
```python
# analyze_baseline.py
import json
from pathlib import Path

report = json.loads(Path("metrics/data/baseline_report.json").read_text())

# Suas análises customizadas...
```

### Jupyter Notebook
```python
import json
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
report = json.loads(Path("metrics/data/baseline_report.json").read_text())
df = pd.DataFrame(report['projects'])

# Visualizar
df[['project_name', 'duration_seconds', 'metrics.summary.total_cost']].plot()
plt.show()
```

## ⚠️ Considerações

### Custos
- Cada projeto usa ~$0.50 em média
- Batch completo: ~$2.50
- Verifique saldo da API antes de executar

### Tempo
- Reserve 15-20 minutos
- Não interrompa durante execução
- Use `Ctrl+C` se necessário (gera relatório parcial)

### Reprodutibilidade
Para resultados consistentes:
- Use mesma temperatura LLM (0.7)
- Execute em horários similares
- Use mesmo modelo (GPT-4)
- Mantenha mesma base de conhecimento

## 🐛 Troubleshooting

### Erro: "API Key não configurada"
```bash
# Configure no .env
echo "OPENAI_API_KEY=sk-proj-your-key" >> .env
```

### Erro: "Rate limit exceeded"
```bash
# Adicione delay maior entre projetos
# Edite test_baseline.py, linha com sleep(5)
time.sleep(30)  # Aumentar para 30s
```

### Workspace cheio
```bash
# Limpar antes de executar
rm -rf workspace/*
./run_baseline_test.sh
```

### Erro em um projeto específico
- O teste continua para próximos projetos
- Erro é registrado no relatório
- Revise logs para debug

## 📚 Referências

- [README.md](README.md) - Documentação principal
- [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md) - Plano de estudo completo
- [RAG_INTEGRATION.md](RAG_INTEGRATION.md) - Como o RAG funciona

---

**Pronto para começar?**

```bash
./run_baseline_test.sh
```

Boa sorte com seus testes! 🚀
