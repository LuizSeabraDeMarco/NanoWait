import argparse
from . import wait as nano_wait_func

# Map presets para valores numéricos
SPEED_PRESETS = {
    "slow": 0.5,
    "normal": 1.5,
    "fast": 3.0,
    "ultra": 5.0
}

def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive smart wait for Python."
    )
    parser.add_argument("time", type=float, help="Base time in seconds (e.g. 2.5)")
    parser.add_argument("--wifi", type=str, help="Wi-Fi SSID to use (optional)")
    parser.add_argument(
        "--speed",
        type=str,
        default="normal",
        help="Speed preset (slow, normal, fast, ultra)"
    )
    parser.add_argument("--verbose", action="store_true", help="Show debug output")
    parser.add_argument("--log", action="store_true", help="Write result to log file")

    args = parser.parse_args()

    # Converte preset de speed para float
    speed_value = SPEED_PRESETS.get(args.speed.lower(), 1.5)

    # Chama função wait() do NanoWait
    nano_wait_func(
        t=args.time,
        wifi=args.wifi,
        speed=speed_value,
        verbose=args.verbose,
        log=args.log
    )

if __name__ == "__main__":
    main()
