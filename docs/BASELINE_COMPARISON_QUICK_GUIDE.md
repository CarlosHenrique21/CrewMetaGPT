# 🚀 Guia Rápido: Comparação de Baselines

## Execução em 3 Passos

### Passo 1: Executar Baseline COM RAG
```bash
./scripts/run_baseline_test.sh
```
- ⏱️ Duração: 10-15 minutos
- 💰 Custo: ~$1.50-3.00
- 📊 Output: `metrics/data/baseline_report.json`

### Passo 2: Executar Baseline SEM RAG
```bash
./scripts/run_baseline_no_rag.sh
```
- ⏱️ Duração: 10-15 minutos
- 💰 Custo: ~$1.50-3.00
- 📊 Output: `metrics/data/no_rag/baseline_report.json`

### Passo 3: Comparar Resultados
```bash
python scripts/compare_baselines.py
```
- ⏱️ Duração: < 1 segundo
- 💰 Custo: $0
- 📊 Output: `metrics/data/comparison_report.json` + análise no terminal

## O que Esperar

### Output do Passo 3 (Comparação)

```
📊 COMPARAÇÃO ENTRE BASELINES: COM RAG vs SEM RAG
================================================================

💰 COMPARAÇÃO DE CUSTOS
  COM RAG:    $2.5430
  SEM RAG:    $2.3200
  Diferença:  📈 9.61% (RAG mais caro)

🎫 COMPARAÇÃO DE TOKENS
  COM RAG:    85,340
  SEM RAG:    78,920
  Diferença:  📈 8.13% (RAG usa mais)

⏱️  COMPARAÇÃO DE PERFORMANCE
  COM RAG:    144.1s
  SEM RAG:    138.7s
  Diferença:  📈 3.89% (RAG mais lento)

📞 COMPARAÇÃO DE LLM CALLS
  COM RAG:    125
  SEM RAG:    118
  Diferença:  📈 5.93% (RAG faz mais calls)

📈 RESUMO EXECUTIVO
  💰 Custo: RAG aumenta custos em 9.61%
  🎫 Tokens: RAG aumenta uso de tokens em 8.13%
  ⏱️  Performance: RAG aumenta tempo em 3.89%
  📞 LLM Calls: RAG aumenta chamadas em 5.93%
```

## Arquivos Criados

### Código
- `agents_no_rag.py` - Agentes sem RAG
- `tasks_no_rag.py` - Tasks sem RAG
- `crew_no_rag.py` - Crew sem RAG

### Testes
- `tests/test_baseline_no_rag.py` - Teste baseline sem RAG

### Scripts
- `scripts/run_baseline_no_rag.sh` - Executa teste sem RAG
- `scripts/compare_baselines.py` - Compara baselines

### Métricas
```
metrics/data/
├── baseline_report.json          # COM RAG
├── baseline_project_*.json       # Projetos COM RAG
├── comparison_report.json        # Comparação
└── no_rag/
    ├── baseline_report.json      # SEM RAG
    └── baseline_project_*.json   # Projetos SEM RAG
```

### Documentação
- `docs/BASELINE_COMPARISON.md` - Guia completo
- `docs/BASELINE_COMPARISON_QUICK_GUIDE.md` - Este arquivo

## Decisão: Vale a Pena Usar RAG?

### Cenário 1: RAG Vale a Pena ✅
- Qualidade dos outputs é **significativamente** melhor
- Aumento de custo < 20%
- Usuário/cliente valoriza qualidade > custo

### Cenário 2: RAG Não Vale a Pena ❌
- Qualidade dos outputs é **similar**
- Aumento de custo > 20%
- Performance é crítica (tempo sensível)

### Cenário 3: Otimizar RAG 🔧
- Qualidade é melhor, mas custo muito alto
- **Ação**: Otimizar RAG (melhor chunking, filtros, etc)
- Re-executar testes após otimização

## Próximos Passos

1. ✅ Executar ambos os baselines
2. ✅ Comparar métricas quantitativas
3. ⏳ Analisar qualidade dos outputs (manual)
4. ⏳ Decidir se RAG vale a pena
5. ⏳ Se sim: manter; se não: desabilitar; se incerto: otimizar

## Links Úteis

- [Guia Completo](./BASELINE_COMPARISON.md)
- [Baseline COM RAG](./BASELINE_TEST_GUIDE.md)
- [RAG Integration](./RAG_INTEGRATION.md)
- [Plano de Estudo](./PLANO_ESTUDO_RAG_METRICAS.md)

---

**Duração Total**: ~25-30 minutos
**Custo Total**: ~$3-6
**Benefício**: Decisão baseada em dados sobre o uso de RAG
