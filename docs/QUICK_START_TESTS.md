# 🚀 Quick Start - Testes e Scripts

## Scripts Disponíveis

### 1️⃣ Teste Rápido (1 projeto)
```bash
./quick_test.sh
```
- Executa 1 projeto de exemplo
- Duração: ~2-3 minutos
- Usa RAG automaticamente
- Ideal para: Testar instalação

### 2️⃣ Teste Baseline (5 projetos)
```bash
./run_baseline_test.sh
```
- Executa 5 projetos em sequência
- Duração: ~10-15 minutos
- Coleta métricas completas
- Ideal para: Estabelecer baseline

### 3️⃣ Teste RAG Isolado
```bash
python test_rag_setup.py
```
- Testa apenas componentes RAG
- Duração: ~30 segundos
- Não executa crew completo
- Ideal para: Debug do RAG

### 4️⃣ Teste de Integração
```bash
python test_rag_integration.py
```
- Verifica se RAG está integrado nos agentes
- Duração: ~5 segundos
- Não executa LLM calls
- Ideal para: Validar configuração

### 5️⃣ Análise de Resultados
```bash
python analyze_baseline.py
```
- Analisa relatório do baseline
- Mostra estatísticas formatadas
- Projeções de custo/tempo
- Ideal para: Revisar resultados

## Fluxo Recomendado

### Setup Inicial
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar API key
echo "OPENAI_API_KEY=sk-proj-your-key" > .env

# 3. Testar configuração
python test_rag_integration.py
```

### Teste Rápido
```bash
# 4. Executar teste rápido
./quick_test.sh

# 5. Verificar workspace
ls -la workspace/
```

### Baseline Completo
```bash
# 6. Executar baseline (5 projetos)
./run_baseline_test.sh

# 7. Analisar resultados
python analyze_baseline.py

# 8. Ver JSON completo
cat metrics/data/baseline_report.json | python -m json.tool
```

## Outputs Esperados

### quick_test.sh
```
workspace/
├── prd.md
├── architecture.md
├── src/
├── tests.py
└── README.md
```

### run_baseline_test.sh
```
metrics/data/
├── baseline_report.json          # Relatório consolidado
├── baseline_project_01.json      # Métricas projeto 1
├── baseline_project_02.json      # Métricas projeto 2
├── baseline_project_03.json      # Métricas projeto 3
├── baseline_project_04.json      # Métricas projeto 4
└── baseline_project_05.json      # Métricas projeto 5
```

## Estimativas de Custo

| Script | Projetos | Duração | Custo (USD) |
|--------|----------|---------|-------------|
| quick_test.sh | 1 | 2-3 min | ~$0.30-0.50 |
| run_baseline_test.sh | 5 | 10-15 min | ~$1.50-3.00 |
| Estudo completo (50) | 50 | 2-3 horas | ~$15-30 |

## Troubleshooting

### Erro: "API Key não configurada"
```bash
# Configure no .env
echo "OPENAI_API_KEY=sk-proj-your-key" >> .env
```

### Erro: "FAISS não instalado"
```bash
# Instalar FAISS
pip install faiss-cpu

# Ou downgrade numpy se necessário
pip install "numpy<2.0.0"
```

### Erro: "Rate limit"
```bash
# Adicionar delay entre projetos
# Editar run_baseline_test.sh ou test_baseline.py
# Aumentar sleep(5) para sleep(30)
```

### Workspace cheio
```bash
# Limpar antes de executar
rm -rf workspace/*
```

## Próximos Passos

Depois do baseline:

1. **Analisar resultados**
   ```bash
   python analyze_baseline.py
   ```

2. **Executar teste com RAG otimizado**
   - Veja [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md)

3. **Comparar métricas**
   - Baseline vs RAG
   - Identificar melhorias

4. **Executar fase 3 (AutoPDL/DSPy)**
   - Após análise das fases 1 e 2

## Links Úteis

- 📖 [README.md](README.md) - Documentação completa
- 🧪 [BASELINE_TEST_GUIDE.md](BASELINE_TEST_GUIDE.md) - Guia detalhado de testes
- 🔍 [RAG_INTEGRATION.md](RAG_INTEGRATION.md) - Como o RAG funciona
- 📊 [PLANO_ESTUDO_RAG_METRICAS.md](PLANO_ESTUDO_RAG_METRICAS.md) - Estudo completo

---

**Comece agora:**

```bash
./quick_test.sh  # Teste rápido (1 projeto)
```

ou

```bash
./run_baseline_test.sh  # Baseline completo (5 projetos)
```
