# cli.py
import argparse
import os

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
        help="slow | normal | fast | ultra | numeric value"
    )

    parser.add_argument(
        "--smart",
        action="store_true",
        help="Enable Smart Context Mode (auto speed)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug output"
    )

    parser.add_argument(
        "--log",
        action="store_true",
        help="Write log file (nano_wait.log)"
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
    # Headless mode (macOS safe)
    # ------------------------
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Disable any UI / Tk / dashboard (recommended on macOS & CI)"
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
    # Force headless behavior
    # ------------------------
    if args.headless:
        # Environment flag that NanoWait (and submodules) can read
        os.environ["NANOWAIT_HEADLESS"] = "1"

        # Safety: disable telemetry UI automatically
        if args.telemetry:
            print("[NanoWait] Headless mode enabled → telemetry UI disabled")
            args.telemetry = False

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
    # Output explain
    # ------------------------
    if args.explain:
        print("\n--- NanoWait Explain Report ---")

        if isinstance(result, tuple):
            report, telemetry = result
            print(report.explain())

            if telemetry is not None:
                print("\n--- Telemetry Summary ---")
                print(telemetry)
        else:
            print(result.explain())


if __name__ == "__main__":
    main()
