import argparse
from .nano_wait import wait


def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive smart wait for Python."
    )

    # ------------------------
    # Core arguments
    # ------------------------

    parser.add_argument(
        "time",
        type=float,
        help="Base time in seconds"
    )

    parser.add_argument(
        "--wifi",
        type=str,
        help="Wi-Fi SSID (optional)"
    )

    parser.add_argument(
        "--speed",
        type=str,
        default="normal",
        help="slow | normal | fast | ultra"
    )

    parser.add_argument(
        "--smart",
        action="store_true",
        help="Enable Smart Context Mode"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug output"
    )

    parser.add_argument(
        "--log",
        action="store_true",
        help="Write log file"
    )

    # ------------------------
    # Explain mode
    # ------------------------

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Explain how the wait time was calculated"
    )

    args = parser.parse_args()

    # ------------------------
    # Execute NanoWait
    # ------------------------

    result = wait(
        t=args.time,
        wifi=args.wifi,
        speed=args.speed,
        smart=args.smart,
        verbose=args.verbose,
        log=args.log,
        explain=args.explain
    )

    # ------------------------
    # Output explain report
    # ------------------------

    if args.explain and result is not None:
        print("\n--- NanoWait Explain Report ---")
        print(result.explain())


if __name__ == "__main__":
    main()
