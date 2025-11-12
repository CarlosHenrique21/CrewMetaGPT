# metrics/metrics_tracker.py
"""
Sistema completo de métricas para o projeto CrewAI com RAG.
Rastreia latência, throughput, uso de tools e performance de agentes.
"""
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from statistics import mean, median, stdev


@dataclass
class RAGMetrics:
    """Métricas específicas para operações RAG."""
    retrieval_latency: float
    num_documents_retrieved: int
    relevance_score: float
    embedding_latency: float
    total_latency: float
    timestamp: str


@dataclass
class LLMMetrics:
    """Métricas de chamadas LLM."""
    duration: float
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    estimated_cost: float
    model: str
    timestamp: str


@dataclass
class ToolMetrics:
    """Métricas de uso de tools."""
    tool_name: str
    duration: float
    success: bool
    timestamp: str


@dataclass
class AgentMetrics:
    """Métricas de performance de agentes."""
    agent_name: str
    task_id: str
    success: bool
    duration: float
    quality_score: Optional[float]
    timestamp: str


class MetricsTracker:
    """
    Rastreador central de métricas do sistema.
    """

    def __init__(self, output_dir: str = "metrics/data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.metrics = {
            'retrieval_times': [],
            'llm_calls': [],
            'tool_usage': [],
            'agent_performance': [],
            'throughput': [],
        }

        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")

    def track_retrieval(self, duration: float, docs_retrieved: int,
                       relevance_score: float, embedding_latency: float):
        """Rastreia operação de retrieval RAG."""
        metrics = RAGMetrics(
            retrieval_latency=duration - embedding_latency,
            num_documents_retrieved=docs_retrieved,
            relevance_score=relevance_score,
            embedding_latency=embedding_latency,
            total_latency=duration,
            timestamp=datetime.now().isoformat()
        )
        self.metrics['retrieval_times'].append(asdict(metrics))
        return metrics

    def track_llm_call(self, duration: float, tokens_prompt: int,
                      tokens_completion: int, model: str = "gpt-4"):
        """Rastreia chamada LLM."""
        # Custos aproximados (ajustar conforme modelo)
        cost_per_1k_prompt = 0.03 if "gpt-4" in model else 0.0015
        cost_per_1k_completion = 0.06 if "gpt-4" in model else 0.002

        estimated_cost = (
            (tokens_prompt / 1000) * cost_per_1k_prompt +
            (tokens_completion / 1000) * cost_per_1k_completion
        )

        metrics = LLMMetrics(
            duration=duration,
            tokens_prompt=tokens_prompt,
            tokens_completion=tokens_completion,
            tokens_total=tokens_prompt + tokens_completion,
            estimated_cost=estimated_cost,
            model=model,
            timestamp=datetime.now().isoformat()
        )
        self.metrics['llm_calls'].append(asdict(metrics))
        return metrics

    def track_tool_call(self, tool_name: str, duration: float, success: bool):
        """Rastreia uso de tool."""
        metrics = ToolMetrics(
            tool_name=tool_name,
            duration=duration,
            success=success,
            timestamp=datetime.now().isoformat()
        )
        self.metrics['tool_usage'].append(asdict(metrics))
        return metrics

    def track_agent_task(self, agent_name: str, task_id: str,
                        success: bool, duration: float,
                        quality_score: Optional[float] = None):
        """Rastreia execução de task por agente."""
        metrics = AgentMetrics(
            agent_name=agent_name,
            task_id=task_id,
            success=success,
            duration=duration,
            quality_score=quality_score,
            timestamp=datetime.now().isoformat()
        )
        self.metrics['agent_performance'].append(asdict(metrics))
        return metrics

    def track_query(self):
        """Registra uma query para cálculo de throughput."""
        self.metrics['throughput'].append({
            'timestamp': datetime.now().isoformat()
        })

    def calculate_throughput(self, time_window: int = 60) -> float:
        """
        Calcula throughput (queries por minuto).

        Args:
            time_window: Janela de tempo em segundos (default: 60s)
        """
        now = datetime.now()
        recent_queries = [
            q for q in self.metrics['throughput']
            if (now - datetime.fromisoformat(q['timestamp'])).seconds <= time_window
        ]
        return len(recent_queries)

    def get_avg_retrieval_time(self) -> float:
        """Calcula latência média de retrieval."""
        if not self.metrics['retrieval_times']:
            return 0.0
        times = [r['total_latency'] for r in self.metrics['retrieval_times']]
        return mean(times)

    def get_avg_llm_time(self) -> float:
        """Calcula latência média de LLM calls."""
        if not self.metrics['llm_calls']:
            return 0.0
        times = [l['duration'] for l in self.metrics['llm_calls']]
        return mean(times)

    def get_total_cost(self) -> float:
        """Calcula custo total estimado."""
        if not self.metrics['llm_calls']:
            return 0.0
        return sum(l['estimated_cost'] for l in self.metrics['llm_calls'])

    def get_total_tokens(self) -> int:
        """Calcula total de tokens usados."""
        if not self.metrics['llm_calls']:
            return 0
        return sum(l['tokens_total'] for l in self.metrics['llm_calls'])

    def get_tool_efficiency(self) -> Dict[str, Any]:
        """Calcula eficiência por tool."""
        if not self.metrics['tool_usage']:
            return {}

        tool_stats = {}
        for tool_call in self.metrics['tool_usage']:
            tool_name = tool_call['tool_name']
            if tool_name not in tool_stats:
                tool_stats[tool_name] = {
                    'total_calls': 0,
                    'successful_calls': 0,
                    'failed_calls': 0,
                    'total_duration': 0.0,
                    'avg_duration': 0.0,
                    'success_rate': 0.0
                }

            tool_stats[tool_name]['total_calls'] += 1
            if tool_call['success']:
                tool_stats[tool_name]['successful_calls'] += 1
            else:
                tool_stats[tool_name]['failed_calls'] += 1
            tool_stats[tool_name]['total_duration'] += tool_call['duration']

        # Calcular médias e taxas
        for tool_name, stats in tool_stats.items():
            stats['avg_duration'] = stats['total_duration'] / stats['total_calls']
            stats['success_rate'] = stats['successful_calls'] / stats['total_calls']

        return tool_stats

    def get_agent_success_rates(self) -> Dict[str, Any]:
        """Calcula taxa de sucesso por agente."""
        if not self.metrics['agent_performance']:
            return {}

        agent_stats = {}
        for task in self.metrics['agent_performance']:
            agent_name = task['agent_name']
            if agent_name not in agent_stats:
                agent_stats[agent_name] = {
                    'tasks_completed': 0,
                    'tasks_failed': 0,
                    'success_rate': 0.0,
                    'avg_duration': 0.0,
                    'quality_scores': []
                }

            if task['success']:
                agent_stats[agent_name]['tasks_completed'] += 1
            else:
                agent_stats[agent_name]['tasks_failed'] += 1

            if task['quality_score'] is not None:
                agent_stats[agent_name]['quality_scores'].append(task['quality_score'])

        # Calcular taxas e médias
        for agent_name, stats in agent_stats.items():
            total = stats['tasks_completed'] + stats['tasks_failed']
            stats['success_rate'] = stats['tasks_completed'] / total if total > 0 else 0

            if stats['quality_scores']:
                stats['avg_quality_score'] = mean(stats['quality_scores'])
                stats['median_quality_score'] = median(stats['quality_scores'])

        return agent_stats

    def get_summary(self) -> Dict[str, Any]:
        """Gera resumo completo das métricas."""
        return {
            'session_id': self.session_id,
            'session_duration': (datetime.now() - self.session_start).seconds,
            'summary': {
                'total_queries': len(self.metrics['throughput']),
                'total_retrievals': len(self.metrics['retrieval_times']),
                'total_llm_calls': len(self.metrics['llm_calls']),
                'total_tool_calls': len(self.metrics['tool_usage']),
                'total_agent_tasks': len(self.metrics['agent_performance']),
                'avg_retrieval_latency': self.get_avg_retrieval_time(),
                'avg_llm_latency': self.get_avg_llm_time(),
                'total_cost': self.get_total_cost(),
                'total_tokens': self.get_total_tokens(),
                'throughput': self.calculate_throughput(),
            },
            'detailed_metrics': {
                'tool_efficiency': self.get_tool_efficiency(),
                'agent_success_rates': self.get_agent_success_rates(),
            }
        }

    def save_metrics(self, filename: Optional[str] = None):
        """Salva métricas em arquivo JSON."""
        if filename is None:
            filename = f"metrics_{self.session_id}.json"

        filepath = self.output_dir / filename
        summary = self.get_summary()
        summary['raw_metrics'] = self.metrics

        filepath.write_text(json.dumps(summary, indent=2))
        return filepath

    def print_summary(self):
        """Imprime resumo das métricas."""
        summary = self.get_summary()

        print("\n" + "=" * 80)
        print("📊 MÉTRICAS DO SISTEMA - RESUMO")
        print("=" * 80)
        print(f"\nSession ID: {summary['session_id']}")
        print(f"Duração: {summary['session_duration']}s")
        print("\n--- ESTATÍSTICAS GERAIS ---")
        print(f"Total de Queries: {summary['summary']['total_queries']}")
        print(f"Total de Retrievals: {summary['summary']['total_retrievals']}")
        print(f"Total de LLM Calls: {summary['summary']['total_llm_calls']}")
        print(f"Total de Tool Calls: {summary['summary']['total_tool_calls']}")
        print(f"Total de Agent Tasks: {summary['summary']['total_agent_tasks']}")

        print("\n--- PERFORMANCE ---")
        print(f"Latência Média Retrieval: {summary['summary']['avg_retrieval_latency']:.3f}s")
        print(f"Latência Média LLM: {summary['summary']['avg_llm_latency']:.3f}s")
        print(f"Throughput: {summary['summary']['throughput']:.1f} queries/min")

        print("\n--- CUSTOS ---")
        print(f"Total de Tokens: {summary['summary']['total_tokens']:,}")
        print(f"Custo Estimado: ${summary['summary']['total_cost']:.4f}")

        print("\n--- EFICIÊNCIA DE TOOLS ---")
        for tool_name, stats in summary['detailed_metrics']['tool_efficiency'].items():
            print(f"\n{tool_name}:")
            print(f"  Chamadas: {stats['total_calls']}")
            print(f"  Taxa de Sucesso: {stats['success_rate']*100:.1f}%")
            print(f"  Duração Média: {stats['avg_duration']:.3f}s")

        print("\n--- PERFORMANCE DE AGENTES ---")
        for agent_name, stats in summary['detailed_metrics']['agent_success_rates'].items():
            print(f"\n{agent_name}:")
            print(f"  Tasks Completadas: {stats['tasks_completed']}")
            print(f"  Taxa de Sucesso: {stats['success_rate']*100:.1f}%")
            if 'avg_quality_score' in stats:
                print(f"  Quality Score Médio: {stats['avg_quality_score']:.2f}")

        print("\n" + "=" * 80)


def track_timing(stage_name: str):
    """
    Decorator para rastrear tempo de execução de funções.

    Usage:
        @track_timing("retrieval")
        def my_function():
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                print(f"⏱️  [{stage_name}] {func.__name__}: {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                print(f"❌ [{stage_name}] {func.__name__}: {duration:.3f}s (FAILED: {e})")
                raise
        return wrapper
    return decorator


# Instância global do tracker (opcional)
global_tracker = None

def get_tracker() -> MetricsTracker:
    """Retorna instância global do tracker."""
    global global_tracker
    if global_tracker is None:
        global_tracker = MetricsTracker()
    return global_tracker


def reset_tracker():
    """Reseta tracker global."""
    global global_tracker
    global_tracker = MetricsTracker()
    return global_tracker
