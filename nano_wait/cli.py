import argparse
import asyncio

from .nano_wait import wait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool
from .nano_wait_auto import wait_auto

# 🔥 NEW
from .execution import execute


def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive smart wait for Python."
    )

    parser.add_argument("time", type=float, nargs="?", help="Base time in seconds")

    parser.add_argument("--async", dest="use_async", action="store_true")
    parser.add_argument("--pool", type=float, nargs="+")
    parser.add_argument("--auto", action="store_true")

    # 🔥 NEW
    parser.add_argument(
        "--exec",
        type=str,
        help="Execute a Python lambda (ex: --exec 'lambda: 1+1')"
    )

    parser.add_argument("--wifi", type=str)
    parser.add_argument("--speed", type=str, default="normal")
    parser.add_argument("--smart", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--explain", action="store_true")
    parser.add_argument(
        "--profile",
        type=str,
        choices=["ci", "testing", "rpa"]
    )

    args = parser.parse_args()

    # ------------------------
    # EXECUTION MODE 🔥
    # ------------------------
    if args.exec:
        fn = eval(args.exec)

        result = execute(
            fn,
            timeout=10,
            interval=0.2,
            profile=args.profile,
            verbose=args.verbose
        )

        print(result)
        return

    # ------------------------
    # AUTO MODE
    # ------------------------
    if args.auto:
        wait_auto(
            wifi=args.wifi,
            profile=args.profile,
            verbose=args.verbose,
            log=args.log
        )
        return

    # ------------------------
    # POOL
    # ------------------------
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

    # ------------------------
    # ASYNC
    # ------------------------
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

    # ------------------------
    # DEFAULT
    # ------------------------
    wait(
        t=args.time,
        wifi=args.wifi,
        speed=args.speed,
        smart=args.smart,
        verbose=args.verbose,
        log=args.log,
        explain=args.explain,
        profile=args.profile
    )


if __name__ == "__main__":
    main()