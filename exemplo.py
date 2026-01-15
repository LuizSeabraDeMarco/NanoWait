import subprocess

result = subprocess.run(
    ["pypistats", "recent", "nano-wait", "--format", "json"],
    capture_output=True,
    text=True
)

print(result.stdout)
