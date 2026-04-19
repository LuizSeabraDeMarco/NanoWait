"""
NanoWait CLI Interface
----------------------
Ponto de entrada para uso da biblioteca via terminal.
Suporta modos de espera, execução de lambdas e agente de automação.
"""

import argparse
import asyncio
import sys
from typing import Any, Callable, Optional

from .nano_wait import wait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool
from .nano_wait_auto import wait_auto
from .execution import execute

# Tenta carregar o módulo Agent se disponível
try:
    from .agent import Agent
except ImportError:
    Agent = None

def safe_eval_lambda(expr: str) -> Callable:
    """
    Avaliação de lambdas com restrições de segurança básicas.
    Apenas expressões começando com 'lambda' são permitidas.
    """
    expr = expr.strip()
    if not expr.startswith("lambda"):
        raise ValueError("A expressão deve começar com 'lambda' (ex: 'lambda: 1+1')")

    # Avaliação com builtins vazios para minimizar riscos
    return eval(expr, {"__builtins__": {}})

def main():
    parser = argparse.ArgumentParser(
        prog="nano-wait",
        description="🚀 NanoWait — Motor de Execução Adaptativo para Python.",
        epilog="Exemplo: nano-wait 2 --smart --profile testing"
    )

    # --- ENTRADA PRINCIPAL ---
    parser.add_argument("time", type=float, nargs="?", help="Tempo base em segundos")

    # --- MODOS DE OPERAÇÃO ---
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--async", dest="use_async", action="store_true", help="Executa em modo assíncrono")
    group.add_argument("--pool", type=float, nargs="+", help="Executa um pool de esperas paralelas")
    group.add_argument("--auto", action="store_true", help="Modo automático baseado em contexto")
    group.add_argument("--exec", type=str, help="Executa uma expressão lambda (ex: --exec 'lambda: 1+1')")
    group.add_argument("--agent", type=str, help="Executa instrução de alto nível (ex: --agent 'click login')")

    # --- CONFIGURAÇÕES DE CONTEXTO ---
    parser.add_argument("--wifi", type=str, help="SSID para monitoramento de rede")
    parser.add_argument("--speed", type=str, default="normal", help="Fator de velocidade (slow, normal, fast, ultra)")
    parser.add_argument("--smart", action="store_true", help="Habilita inteligência adaptativa de hardware")

    # --- DEBUG E CONTROLE ---
    parser.add_argument("--verbose", "-v", action="store_true", help="Ativa logs detalhados")
    parser.add_argument("--log", action="store_true", help="Grava eventos em nano_wait.log")
    parser.add_argument("--explain", action="store_true", help="Mostra relatório detalhado da decisão")
    parser.add_argument("--profile", type=str, choices=["ci", "testing", "rpa"], help="Perfil de agressividade")

    args = parser.parse_args()

    # --- EXECUÇÃO: AGENTE ---
    if args.agent:
        if Agent is None:
            print("❌ Erro: Módulo Agent não disponível. Verifique as dependências.")
            sys.exit(1)
        agent = Agent(verbose=args.verbose)
        print(f"🤖 Agent executando: '{args.agent}'...")
        result = agent.run(args.agent)
        print(f"✅ Resultado: {result}")
        return

    # --- EXECUÇÃO: MOTOR DE EXECUÇÃO ---
    if args.exec:
        try:
            fn = safe_eval_lambda(args.exec)
            print(f"⚙️ Executando lambda: '{args.exec}'...")
            result = execute(
                fn,
                timeout=10,
                interval=0.2,
                profile=args.profile,
                verbose=args.verbose,
                smart=args.smart
            )
            print(result)
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            sys.exit(1)
        return

    # --- EXECUÇÃO: AUTO MODE ---
    if args.auto:
        print("🤖 Iniciando espera automática baseada em contexto...")
        wait_auto(
            wifi=args.wifi,
            profile=args.profile,
            verbose=args.verbose,
            log=args.log
        )
        return

    # --- EXECUÇÃO: POOL MODE ---
    if args.pool:
        print(f"🔁 Executando pool de {len(args.pool)} esperas...")
        results = wait_pool(
            args.pool,
            profile=args.profile,
            wifi=args.wifi,
            speed=args.speed,
            smart=args.smart,
            verbose=args.verbose,
            log=args.log,
            explain=args.explain
        )
        print(f"✅ Resultados do Pool: {results}")
        return

    # --- EXECUÇÃO: ASYNC MODE ---
    if args.use_async:
        if args.time is None:
            print("❌ Erro: Tempo base necessário para o modo assíncrono.")
            sys.exit(1)
        print(f"⚡ Iniciando espera assíncrona de {args.time}s...")
        asyncio.run(
            wait_async(
                t=args.time,
                wifi=args.wifi,
                speed=args.speed,
                smart=args.smart,
                verbose=args.verbose,
                log=args.log,
                explain=args.explain,
                profile=args.profile
            )
        )
        return

    # --- EXECUÇÃO: DEFAULT SYNC WAIT ---
    if args.time is None:
        parser.print_help()
        sys.exit(0)

    print(f"⏱ Esperando {args.time}s (Adaptativo)...")
    result = wait(
        t=args.time,
        wifi=args.wifi,
        speed=args.speed,
        smart=args.smart,
        verbose=args.verbose,
        log=args.log,
        explain=args.explain,
        profile=args.profile
    )

    if args.explain:
        print("\n📊 Relatório de Explicação:")
        print(result.explain() if hasattr(result, 'explain') else result)
    else:
        print(f"✅ Concluído em {result:.4f}s")

if __name__ == "__main__":
    main()
