import argparse
from . import wait

def main():
    parser = argparse.ArgumentParser(
        description="Nano-Wait — Adaptive smart wait for Python."
    )
    parser.add_argument("time", type=float, help="Base time in seconds (e.g. 2.5)")
    parser.add_argument("--wifi", type=str, help="Wi-Fi SSID to use (optional)")
    parser.add_argument("--speed", type=str, default="normal", help="Speed preset (slow, normal, fast, ultra)")
    parser.add_argument("--verbose", action="store_true", help="Show debug output")
    parser.add_argument("--log", action="store_true", help="Write result to log file")

    args = parser.parse_args()

    wait(args.time, wifi=args.wifi, speed=args.speed, verbose=args.verbose, log=args.log)

if __name__ == "__main__":
    main()
