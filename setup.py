# ============================================
# setup.py — nano-wait
#
# PT: Configuração do pacote para PyPI
# EN: PyPI package configuration file
# ============================================

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    # ----------------------------------------
    # Basic metadata
    # ----------------------------------------
    name="nano-wait",      # padronizado com hífen (pip install nano-wait)
    version="7.1.0",

    license="MIT",
    author="Luiz Filipe Seabra de Marco",
    author_email="luizfilipeseabra@icloud.com",

    description=(
        "Adaptive waiting and execution engine — "
        "replaces time.sleep() with system-aware, predictable waiting."
    ),

    long_description=readme,
    long_description_content_type="text/markdown",

    # ----------------------------------------
    # PyPI search keywords
    # ----------------------------------------
    keywords=[
        "automation",
        "adaptive wait",
        "smart wait",
        "execution engine",
        "system-aware",
        "deterministic automation",
        "rpa",
        "testing",
        "selenium",
        "playwright",
        "performance",
        "psutil",
        "sleep replacement",
        "polling",
        "retry",
    ],

    # ----------------------------------------
    # Packages
    # ----------------------------------------
    packages=find_packages(),
    include_package_data=True,

    # ----------------------------------------
    # Core dependencies — mínimo absoluto
    # ----------------------------------------
    install_requires=[
        "psutil",
    ],

    # ----------------------------------------
    # Grupos opcionais
    # ----------------------------------------
    extras_require={
        # Suporte a medição de sinal Wi-Fi (Windows)
        "wifi": [
            "pywifi",
        ],
        # Desenvolvimento e testes
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
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.8",
)