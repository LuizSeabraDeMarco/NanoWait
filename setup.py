# ============================================
# setup.py — Nano-Wait (CORE ONLY)
#
# PT: Configuração do pacote para PyPI
# EN: PyPI package configuration file
# ============================================

from setuptools import setup, find_packages

# ----------------------------------------
# Read long description from README
# ----------------------------------------
with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    # ----------------------------------------
    # Basic metadata
    # ----------------------------------------
    name="nano_wait",  # mantém compatibilidade
    version="4.0.7",   # 🚨 BREAKING CHANGE (vision removido)

    license="MIT",
    author="Luiz Filipe Seabra de Marco",
    author_email="luizfilipeseabra@icloud.com",

    description=(
        "Adaptive waiting and execution engine — "
        "replaces time.sleep() with system-aware, deterministic waiting."
    ),

    long_description=readme,
    long_description_content_type="text/markdown",

    # ----------------------------------------
    # PyPI search keywords (ATUALIZADOS)
    # ----------------------------------------
    keywords=[
        "automation",
        "adaptive wait",
        "smart wait",
        "execution engine",
        "system-aware",
        "deterministic automation",
        "rpa core",
        "testing",
        "performance",
        "psutil",
        "wifi awareness",
        "system context",
        "sleep replacement",
    ],

    # ----------------------------------------
    # Packages
    # ----------------------------------------
    packages=find_packages(),
    include_package_data=True,

    # ----------------------------------------
    # Core dependencies (ONLY core)
    # ----------------------------------------
    install_requires=[
        "psutil",   # CPU / memory context
        "pywifi",   # optional Wi-Fi awareness (fails gracefully)
    ],

    # ----------------------------------------
    # Optional dependency groups
    # ----------------------------------------
    extras_require={
        # Development & tests (NOT for end users)
        "dev": [
            "pytest",
            "pytest-mock",
        ],
    },

    # ----------------------------------------
    # CLI entry point
    # ----------------------------------------
    entry_points={
        "console_scripts": [
            "nano-wait = nano_wait.cli:main",
        ],
    },

    # ----------------------------------------
    # Metadata classifiers
    # ----------------------------------------
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.8",
)
