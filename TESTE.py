"""
verify_nanowait_usage.py

Verifica APENAS chamadas reais para funções importadas da NanoWait,
ignorando funções com o mesmo nome de outras bibliotecas.

Uso:
    python verify_nanowait_usage.py .
"""

import ast
import os
import sys
from collections import defaultdict

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
    "site-packages",
}


class NanoWaitVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nanowait_aliases = set()
        self.nanowait_modules = set()
        self.calls = []

    def visit_Import(self, node):
        """
        import nano_wait
        import nano_wait as nw
        import nano_wait.core as core
        """

        for alias in node.names:

            if alias.name.startswith("nano_wait"):

                self.nanowait_modules.add(
                    alias.asname or alias.name.split(".")[0]
                )

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """
        from nano_wait import wait
        from nano_wait import wait as w
        from nano_wait.core import execute
        """

        if node.module and node.module.startswith("nano_wait"):

            for alias in node.names:

                self.nanowait_aliases.add(
                    alias.asname or alias.name
                )

        self.generic_visit(node)

    def visit_Call(self, node):

        function_name = None

        # wait()
        if isinstance(node.func, ast.Name):

            if node.func.id in self.nanowait_aliases:

                function_name = node.func.id

        # nano_wait.wait()
        # nw.wait()
        elif isinstance(node.func, ast.Attribute):

            if isinstance(node.func.value, ast.Name):

                module_name = node.func.value.id

                if module_name in self.nanowait_modules:

                    function_name = (
                        f"{module_name}.{node.func.attr}"
                    )

        if function_name:

            self.calls.append(
                {
                    "function": function_name,
                    "line": node.lineno,
                }
            )

        self.generic_visit(node)


def should_skip(path_parts):

    for part in path_parts:

        if part in SKIP_DIRS:
            return True

    return False


def scan_file(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            source = f.read()

        tree = ast.parse(source)

        visitor = NanoWaitVisitor()
        visitor.visit(tree)

        return visitor.calls

    except Exception as e:

        print(
            f"[ERRO] {file_path}: {e}"
        )

        return []


def scan_project(root_path):

    results = []

    for root, dirs, files in os.walk(root_path):

        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIRS
        ]

        normalized = root.replace("\\", "/")

        if "/nano_wait/" in normalized:
            continue

        if normalized.endswith("/nano_wait"):
            continue

        for filename in files:

            if not filename.endswith(".py"):
                continue

            full_path = os.path.join(
                root,
                filename
            )

            path_parts = set(
                full_path.replace("\\", "/").split("/")
            )

            if should_skip(path_parts):
                continue

            calls = scan_file(full_path)

            if calls:

                results.append(
                    {
                        "file": full_path,
                        "calls": calls,
                    }
                )

    return results


def print_report(results):

    total_calls = 0

    print("\n" + "=" * 80)
    print("USO REAL DA NANOWAIT")
    print("=" * 80)

    usage_count = defaultdict(int)

    for item in results:

        print(f"\n📄 {item['file']}")

        for call in item["calls"]:

            total_calls += 1

            usage_count[
                call["function"]
            ] += 1

            print(
                f"   Linha {call['line']:>4} "
                f"-> {call['function']}"
            )

    print("\n" + "=" * 80)
    print("RESUMO")
    print("=" * 80)

    for func, count in sorted(
        usage_count.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(
            f"{func:<35} {count}"
        )

    print("\n" + "=" * 80)
    print(
        f"TOTAL DE CHAMADAS: {total_calls}"
    )
    print("=" * 80)


def main():

    project_root = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "."
    )

    print(
        f"\nEscaneando: "
        f"{os.path.abspath(project_root)}"
    )

    results = scan_project(
        project_root
    )

    if not results:

        print(
            "\nNenhuma chamada real da "
            "NanoWait foi encontrada."
        )

        return

    print_report(results)


if __name__ == "__main__":
    main()