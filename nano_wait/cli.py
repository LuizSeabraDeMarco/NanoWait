import argparse
import asyncio

from .nano_wait import wait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool
from .nano_wait_auto import wait_auto

# 🔥 EXECUTION LAYER
from .execution import execute

# 🔥 NEW (prepare for agent mode)
try:
    from .agent import Agent
except ImportError:
    Agent = None


def safe_eval_lambda(expr: str):
    """
    Safer evaluation for lambda execution.
    Only allows lambda expressions.
    """
    if not expr.strip().startswith("lambda"):
        raise ValueError("Only lambda expressions are allowed in --exec")

    return eval(expr, {"__builtins__": {}})


def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive Execution Engine for Python."
    )

    # ------------------------
    # CORE INPUT
    # ------------------------
    parser.add_argument("time", type=float, nargs="?", help="Base time in seconds")

    # ------------------------
    # MODES
    # ------------------------
    parser.add_argument("--async", dest="use_async", action="store_true")
    parser.add_argument("--pool", type=float, nargs="+")
    parser.add_argument("--auto", action="store_true")

    # 🔥 EXECUTION MODE
    parser.add_argument(
        "--exec",
        type=str,
        help="Execute a Python lambda (ex: --exec 'lambda: 1+1')"
    )

    # 🔥 NEW: AGENT MODE
    parser.add_argument(
        "--agent",
        type=str,
        help="Run high-level instruction (ex: --agent 'click login button')"
    )

    # ------------------------
    # CONTEXT
    # ------------------------
    parser.add_argument("--wifi", type=str)
    parser.add_argument("--speed", type=str, default="normal")
    parser.add_argument("--smart", action="store_true")

    # ------------------------
    # DEBUG / CONTROL
    # ------------------------
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--explain", action="store_true")

    parser.add_argument(
        "--profile",
        type=str,
        choices=["ci", "testing", "rpa"]
    )

    args = parser.parse_args()

    # ==========================================================
    # 🤖 AGENT MODE (NOVO NÍVEL)
    # ==========================================================
    if args.agent:
        if Agent is None:
            print("Agent module not available. Install full version.")
            return

        agent = Agent(verbose=args.verbose)

        result = agent.run(args.agent)

        print("Agent result:", result)
        return

    # ==========================================================
    # ⚙️ EXECUTION MODE
    # ==========================================================
    if args.exec:
        try:
            fn = safe_eval_lambda(args.exec)
        except Exception as e:
            print("Invalid lambda:", e)
            return

        result = execute(
            fn,
            timeout=10,
            interval=0.2,
            profile=args.profile,
            verbose=args.verbose
        )

        print(result)
        return

    # ==========================================================
    # 🤖 AUTO MODE
    # ==========================================================
    if args.auto:
        wait_auto(
            wifi=args.wifi,
            profile=args.profile,
            verbose=args.verbose,
            log=args.log
        )
        return

    # ==========================================================
    # 🔁 POOL MODE
    # ==========================================================
    if args.pool:
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
        print(results)
        return

    # ==========================================================
    # ⚡ ASYNC MODE
    # ==========================================================
    if args.use_async:
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

    # ==========================================================
    # 🧠 DEFAULT MODE
    # ==========================================================
    if args.time is None:
        print("You must provide a time or a mode. Use --help.")
        return

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

    print(result)


if __name__ == "__main__":
    main()