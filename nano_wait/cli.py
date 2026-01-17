# cli.py
import argparse
import os
import asyncio
from .nano_wait import wait
from .nano_wait_async import wait_async

def main():
    parser = argparse.ArgumentParser(description="Nano-Wait — Adaptive smart wait for Python.")

    parser.add_argument("time", type=float, help="Base time in seconds")
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Run wait asynchronously"
    )
    parser.add_argument("--wifi", type=str, help="Wi-Fi SSID (optional)")
    parser.add_argument("--speed", type=str, default="normal", help="slow | normal | fast | ultra | numeric value")
    parser.add_argument("--smart", action="store_true", help="Enable Smart Context Mode (auto speed)")
    parser.add_argument("--verbose", action="store_true", help="Show debug output")
    parser.add_argument("--log", action="store_true", help="Write log file (nano_wait.log)")
    parser.add_argument("--explain", action="store_true", help="Explain how the wait time was calculated")
    parser.add_argument("--profile", type=str, choices=["ci", "testing", "rpa"], help="Execution profile to adjust wait behavior")

    args = parser.parse_args()

    if args.use_async:
        asyncio.run(wait_async(
            t=args.time,
            wifi=args.wifi,
            speed=args.speed,
            smart=args.smart,
            verbose=args.verbose,
            log=args.log,
            explain=args.explain,
            profile=args.profile
        ))
    else:
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
