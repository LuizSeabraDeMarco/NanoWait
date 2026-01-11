# cli.py
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

    # ------------------------
    # Local Telemetry (opt-in)
    # ------------------------
    parser.add_argument(
        "--telemetry",
        action="store_true",
        help="Enable local experimental telemetry (no remote collection)"
    )

    # ------------------------
    # Execution Profile
    # ------------------------
    parser.add_argument(
        "--profile",
        type=str,
        choices=["ci", "testing", "rpa"],
        help="Execution profile to adjust wait behavior"
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
        explain=args.explain,
        telemetry=args.telemetry,
        profile=args.profile
    )

    # ------------------------
    # Output explain / telemetry
    # ------------------------
    if args.explain:
        print("\n--- NanoWait Explain Report ---")

        if isinstance(result, tuple):
            report, telemetry = result
            print(report.explain())

            if args.telemetry:
                print("\n--- Telemetry Summary ---")
                print(telemetry)
        else:
            print(result.explain())


if __name__ == "__main__":
    main()
