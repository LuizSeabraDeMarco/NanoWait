# dashboard.py
import threading
import queue
import tkinter as tk
from tkinter import ttk
from time import sleep


class TelemetryDashboard(threading.Thread):
    def __init__(self, telemetry_queue: queue.Queue):
        super().__init__(daemon=True)
        self.q = telemetry_queue
        self.running = True

    def run(self):
        self.root = tk.Tk()
        self.root.title("NanoWait — Telemetry Dashboard")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self.factor_var = tk.StringVar(value="—")
        self.interval_var = tk.StringVar(value="—")
        self.count_var = tk.StringVar(value="0")

        ttk.Label(self.root, text="NanoWait Telemetry", font=("Arial", 14, "bold")).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Adaptive Factor:").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.factor_var).grid(row=0, column=1, sticky="e")

        ttk.Label(frame, text="Interval (s):").grid(row=1, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.interval_var).grid(row=1, column=1, sticky="e")

        ttk.Label(frame, text="Adjustments:").grid(row=2, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.count_var).grid(row=2, column=1, sticky="e")

        ttk.Separator(self.root).pack(fill="x", pady=10)

        self.status = ttk.Label(self.root, text="Running…", foreground="green")
        self.status.pack()

        self.root.after(100, self.poll_queue)
        self.root.mainloop()

    def poll_queue(self):
        try:
            while not self.q.empty():
                data = self.q.get_nowait()

                if data == "__STOP__":
                    self.status.config(text="Finished", foreground="gray")
                    self.running = False
                    self.root.after(800, self.root.destroy)
                    return

                self.factor_var.set(str(data["factor"]))
                self.interval_var.set(str(data["interval"]))
                self.count_var.set(str(data["count"]))

        except Exception:
            pass

        if self.running:
            self.root.after(100, self.poll_queue)
# dashboard.py
import threading
import queue
import tkinter as tk
from tkinter import ttk
from time import sleep


class TelemetryDashboard(threading.Thread):
    def __init__(self, telemetry_queue: queue.Queue):
        super().__init__(daemon=True)
        self.q = telemetry_queue
        self.running = True

    def run(self):
        self.root = tk.Tk()
        self.root.title("NanoWait — Telemetry Dashboard")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self.factor_var = tk.StringVar(value="—")
        self.interval_var = tk.StringVar(value="—")
        self.count_var = tk.StringVar(value="0")

        ttk.Label(self.root, text="NanoWait Telemetry", font=("Arial", 14, "bold")).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Adaptive Factor:").grid(row=0, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.factor_var).grid(row=0, column=1, sticky="e")

        ttk.Label(frame, text="Interval (s):").grid(row=1, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.interval_var).grid(row=1, column=1, sticky="e")

        ttk.Label(frame, text="Adjustments:").grid(row=2, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.count_var).grid(row=2, column=1, sticky="e")

        ttk.Separator(self.root).pack(fill="x", pady=10)

        self.status = ttk.Label(self.root, text="Running…", foreground="green")
        self.status.pack()

        self.root.after(100, self.poll_queue)
        self.root.mainloop()

    def poll_queue(self):
        try:
            while not self.q.empty():
                data = self.q.get_nowait()

                if data == "__STOP__":
                    self.status.config(text="Finished", foreground="gray")
                    self.running = False
                    self.root.after(800, self.root.destroy)
                    return

                self.factor_var.set(str(data["factor"]))
                self.interval_var.set(str(data["interval"]))
                self.count_var.set(str(data["count"]))

        except Exception:
            pass

        if self.running:
            self.root.after(100, self.poll_queue)
