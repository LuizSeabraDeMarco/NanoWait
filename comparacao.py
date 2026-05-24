import random
import time
import threading
from statistics import mean

from nano_wait import execute


ITERATIONS = 50
TIMEOUT = 5


# ----------------------------
# Simula carga de CPU
# ----------------------------
def cpu_stress():
    x = 0
    end = time.time() + 15

    while time.time() < end:
        x += random.random() * random.random()


# ----------------------------
# API instável realista
# ----------------------------
def unstable_api():
    # Latência variável
    latency = random.uniform(0.05, 1.2)
    time.sleep(latency)

    # Chance dinâmica de falha
    failure_rate = random.uniform(0.2, 0.7)

    if random.random() < failure_rate:
        raise Exception("Temporary API failure")

    return {
        "latency": latency,
        "status": "OK"
    }


# ----------------------------
# Retry tradicional com sleep
# ----------------------------
def classic_retry():
    attempts = 0
    start = time.perf_counter()

    while True:
        attempts += 1

        try:
            result = unstable_api()

            return {
                "success": True,
                "attempts": attempts,
                "duration": time.perf_counter() - start,
                "result": result
            }

        except Exception:
            if time.perf_counter() - start > TIMEOUT:
                return {
                    "success": False,
                    "attempts": attempts,
                    "duration": time.perf_counter() - start
                }

            # backoff fixo
            time.sleep(0.5)


# ----------------------------
# NanoWait execute()
# ----------------------------
def nanowait_retry():
    result = execute(
        unstable_api,
        timeout=TIMEOUT,
        smart=True,
        profile="testing"
    )

    return {
        "success": result.success,
        "attempts": result.attempts,
        "duration": result.duration
    }


# ----------------------------
# Runner genérico
# ----------------------------
def run_test(fn, label):
    results = []

    for _ in range(ITERATIONS):
        results.append(fn())

    success_rate = sum(r["success"] for r in results)

    avg_time = mean(r["duration"] for r in results)
    avg_attempts = mean(r["attempts"] for r in results)

    print(f"\n{'='*50}")
    print(label)
    print(f"{'='*50}")

    print(f"Success Rate : {success_rate}/{ITERATIONS}")
    print(f"Average Time : {avg_time:.2f}s")
    print(f"Avg Attempts : {avg_attempts:.2f}")


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":

    print("Starting CPU stress thread...")
    threading.Thread(target=cpu_stress, daemon=True).start()

    time.sleep(1)

    run_test(classic_retry, "Classic Retry + sleep")
    run_test(nanowait_retry, "NanoWait execute()")