# 🔧 Scripts CrewAI Project

## Scripts Disponíveis

### 1. run_baseline_test.sh ⭐
**Executa teste baseline completo**

```bash
./scripts/run_baseline_test.sh
```

**O que faz:**
- Verifica API key configurada
- Executa `tests/test_baseline.py`
- Mostra progresso e resultados
- Salva métricas em `metrics/data/`

**Duração:** 10-15 minutos
**Custo:** ~$1.50-3.00

**Output esperado:**
```
🧪 CrewAI Baseline Test
======================================

Verificando configuração...
✅ API Key configurada

Iniciando teste baseline...
[Executa 5 projetos]

✅ Teste baseline concluído com sucesso!

📊 Resultados:
   - Relatório: metrics/data/baseline_report.json
   - Métricas individuais: metrics/data/baseline_project_*.json
```

### 2. analyze_baseline.py
**Analisa resultados do baseline**

```bash
python scripts/analyze_baseline.py
```

**O que faz:**
- Lê `metrics/data/baseline_report.json`
- Calcula estatísticas agregadas
- Mostra análises formatadas
- Faz projeções de custo/tempo

**Output esperado:**
```
================================================================================
📊 ANÁLISE DO BASELINE
================================================================================

--- CUSTOS ---
💰 Custo total: $2.5430
💰 Custo médio/projeto: $0.5086

--- TOKENS ---
🎫 Total de tokens: 85,340
🎫 Média/projeto: 17,068

--- PERFORMANCE ---
⏱️  Duração média/projeto: 144.1s
🚀 Throughput: 25.0 projetos/hora
```

### 3. quick_test.sh
**Teste rápido de 1 projeto**

```bash
./scripts/quick_test.sh
# ou na raiz
./quick_test.sh
```

**O que faz:**
- Verifica API key
- Executa 1 projeto de teste
- Valida outputs em workspace/

**Duração:** 2-3 minutos
**Custo:** ~$0.30-0.50

## Como Usar

### Primeiro Uso

1. **Configure API key**
   ```bash
   cd ..
   echo "OPENAI_API_KEY=sk-proj-your-key" >> .env
   ```

2. **Teste rápido**
   ```bash
   ./quick_test.sh
   ```

3. **Baseline completo**
   ```bash
   ./scripts/run_baseline_test.sh
   ```

4. **Analisar resultados**
   ```bash
   python scripts/analyze_baseline.py
   ```

### Uso Regular

```bash
# Executar baseline
./scripts/run_baseline_test.sh

# Ver análise
python scripts/analyze_baseline.py

# Ver JSON bruto
cat metrics/data/baseline_report.json | python -m json.tool
```

## Estrutura de Scripts

```
scripts/
├── README.md                 # Este arquivo
├── run_baseline_test.sh      # ⭐ Executa baseline completo
├── analyze_baseline.py       # Analisa resultados
└── quick_test.sh             # Teste rápido (cópia)
```

## Customização

### Modificar Projetos do Baseline

Edite `tests/test_baseline.py`:

```python
TEST_PROJECTS = [
    {
        "id": "project_01",
        "name": "Seu Projeto",
        "description": "descrição...",
    },
    # Adicione mais...
]
```

### Ajustar Delay Entre Projetos

Edite `tests/test_baseline.py`:

```python
# Linha ~150
time.sleep(5)  # Mudar para 30 se rate limit
```

### Customizar Análise

Edite `scripts/analyze_baseline.py`:

```python
def analyze_report(report_path: Path):
    # Adicione suas análises customizadas
    pass
```

## Troubleshooting

### Script não encontra arquivos

```bash
# Certifique-se de estar no diretório raiz
cd /path/to/CrewAI-Project

# Execute com caminho relativo
./scripts/run_baseline_test.sh
```

### Permission denied

```bash
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### API Key não configurada

```bash
# Verificar se existe
cat .env | grep OPENAI_API_KEY

# Configurar
echo "OPENAI_API_KEY=sk-proj-your-key" >> .env
```

### Erro ao importar módulos

```bash
# Certifique-se de estar no diretório raiz
cd /path/to/CrewAI-Project
python scripts/analyze_baseline.py
```

## Outputs Gerados

### run_baseline_test.sh
```
metrics/data/
├── baseline_report.json          # Relatório consolidado
├── baseline_project_01.json      # Projeto 1
├── baseline_project_02.json      # Projeto 2
├── baseline_project_03.json      # Projeto 3
├── baseline_project_04.json      # Projeto 4
└── baseline_project_05.json      # Projeto 5
```

### analyze_baseline.py
- Output no terminal (formatado)
- Não cria arquivos (apenas lê)

### quick_test.sh
```
workspace/
├── prd.md
├── architecture.md
├── src/
├── tests.py
└── README.md
```

## Integração com Outros Componentes

### Com Sistema RAG
```bash
# RAG é automaticamente inicializado
./scripts/run_baseline_test.sh
```

### Com Sistema de Métricas
```bash
# Métricas são coletadas automaticamente
# Ver em: metrics/data/
```

### Com AgentOps
```bash
# Se AGENTOPS_API_KEY configurada
# Dashboard: https://app.agentops.ai
```

## Próximos Passos

1. **Executar baseline**
   ```bash
   ./scripts/run_baseline_test.sh
   ```

2. **Analisar**
   ```bash
   python scripts/analyze_baseline.py
   ```

3. **Estudar plano completo**
   - [docs/PLANO_ESTUDO_RAG_METRICAS.md](../docs/PLANO_ESTUDO_RAG_METRICAS.md)

## Links Úteis

- 📖 [README Principal](../README.md)
- 📚 [Documentação](../docs/)
- 🧪 [Testes](../tests/)
- 📊 [Baseline Test Guide](../docs/BASELINE_TEST_GUIDE.md)

---

**Voltar para**: [README Principal](../README.md) | [Documentação](../docs/README.md) | [Testes](../tests/README.md)
