# ============================================
# setup.py — Nano-Wait
#
# PT: Configuração do pacote para PyPI
# EN: PyPI package configuration file
# ============================================

from setuptools import setup, find_packages

# PT: Lê o README.md para descrição longa
# EN: Read README.md for long description
with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    # ----------------------------------------
    # Basic metadata
    # ----------------------------------------
    name="nano_wait",  # mantém compatibilidade
    version="3.1.3",

    license="MIT",
    author="Luiz Filipe Seabra de Marco",
    author_email="luizfilipeseabra@icloud.com",

    description=(
        "Adaptive waiting and smart automation library — "
        "includes Wi-Fi, system context, and Vision Mode for screen-based decisions."
    ),

    long_description=readme,
    long_description_content_type="text/markdown",

    # ----------------------------------------
    # SEARCH TAGS (PyPI keywords)
    # PT: Essas são as 'tags' reais do PyPI
    # EN: These are real PyPI search tags
    # ----------------------------------------
    keywords=[
        "automation",
        "gui automation",
        "adaptive wait",
        "smart wait",
        "computer vision",
        "vision mode",
        "ocr",
        "screen automation",
        "rpa",
        "ai automation",
        "pyautogui",
        "selenium",
        "testing",
        "wifi",
        "system context",
    ],

    # ----------------------------------------
    # Packages
    # ----------------------------------------
    packages=find_packages(),
    include_package_data=True,

    # ----------------------------------------
    # Dependencies
    # ----------------------------------------
    install_requires=[
        "psutil",
        "pywifi",
    ],

    extras_require={
        # PT: Dependências opcionais para Vision Mode
        # EN: Optional dependencies for Vision Mode
        "vision": [
            "pyautogui",
            "pytesseract",
            "pynput",
            "opencv-python",
            "numpy",
        ]
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
    # Classifiers (credibilidade + filtros)
    # ----------------------------------------
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
        "Topic :: Desktop Environment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
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
