# cli.py
import argparse
import asyncio

from .nano_wait import wait
from .nano_wait_async import wait_async
from .nano_wait_pool import wait_pool
from .nano_wait_auto import wait_auto


def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive smart wait for Python."
    )

    parser.add_argument(
        "time",
        type=float,
        nargs="?",
        help="Base time in seconds"
    )

    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Run wait asynchronously"
    )

    parser.add_argument(
        "--pool",
        type=float,
        nargs="+",
        help="Run multiple waits in parallel (ex: --pool 2 5 1.5)"
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run minimal adaptive wait (one-line smart wait)"
    )

    parser.add_argument("--wifi", type=str, help="Wi-Fi SSID (optional)")
    parser.add_argument(
        "--speed",
        type=str,
        default="normal",
        help="slow | normal | fast | ultra | numeric value"
    )
    parser.add_argument("--smart", action="store_true", help="Enable Smart Context Mode")
    parser.add_argument("--verbose", action="store_true", help="Show debug output")
    parser.add_argument("--log", action="store_true", help="Write log file (nano_wait.log)")
    parser.add_argument("--explain", action="store_true", help="Explain how the wait time was calculated")
    parser.add_argument(
        "--profile",
        type=str,
        choices=["ci", "testing", "rpa"],
        help="Execution profile"
    )

    args = parser.parse_args()

    # ------------------------
    # AUTO MODE (new)
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
    # DEFAULT (sync wait)
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
