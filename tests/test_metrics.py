from metrics import get_tracker
# tracker = get_tracker()
# filepath = tracker.save_metrics("metrics_20240115.json")
# print(f"Métricas salvas em: {filepath}")



tracker = get_tracker()
tracker.print_summary()