import argparse
from . import wait as nano_wait_func
from .core import NanoWait

# Presets tradicionais
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
        default="auto",
        help="Speed preset (slow, normal, fast, ultra) or 'auto'"
    )
    parser.add_argument("--smart", action="store_true", help="Enable Smart Context Mode")
    parser.add_argument("--verbose", action="store_true", help="Show debug output")
    parser.add_argument("--log", action="store_true", help="Write result to log file")

    args = parser.parse_args()

    nw = NanoWait()

    # Determina o speed
    if args.smart:
        # Smart Context Mode
        pc_score = nw.get_pc_score()
        wifi_score = nw.get_wifi_signal(args.wifi) if args.wifi else 5
        risk_score = (pc_score + wifi_score) / 2
        # Quanto maior o risco (pior PC/Wi-Fi), menor o speed → espera maior
        speed_value = max(0.5, min(5.0, risk_score))
        if args.verbose:
            print(f"[Smart Context] PC={pc_score:.2f}, Wi-Fi={wifi_score:.2f}, risk={risk_score:.2f}, speed={speed_value:.2f}")
    elif args.speed.lower() == "auto":
        # Auto-speed simples (sem Smart Context Mode)
        speed_value = 1.5
    else:
        speed_value = SPEED_PRESETS.get(args.speed.lower(), 1.5)

    nano_wait_func(
        t=args.time,
        wifi=args.wifi,
        speed=speed_value,
        verbose=args.verbose,
        log=args.log
    )

if __name__ == "__main__":
    main()
