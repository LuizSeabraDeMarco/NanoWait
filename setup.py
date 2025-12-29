# ============================================
# setup.py — Nano-Wait
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
    name="nano_wait",  # mantém compatibilidade com versões anteriores
    version="3.3.0",

    license="MIT",
    author="Luiz Filipe Seabra de Marco",
    author_email="luizfilipeseabra@icloud.com",

    description=(
        "Adaptive waiting and computer vision execution engine — "
        "replaces time.sleep() with system-aware, vision-driven automation."
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
        "gui automation",
        "computer vision",
        "vision mode",
        "ocr",
        "screen automation",
        "rpa",
        "ai automation",
        "pyautogui",
        "selenium alternative",
        "testing",
        "wifi awareness",
        "system context",
    ],

    # ----------------------------------------
    # Packages
    # ----------------------------------------
    packages=find_packages(),
    include_package_data=True,

    # ----------------------------------------
    # Core dependencies (always installed)
    # ----------------------------------------
    install_requires=[
        "psutil",     # CPU / memory context
        "pywifi",     # optional Wi-Fi awareness (fails gracefully)
    ],

    # ----------------------------------------
    # Optional dependency groups
    # ----------------------------------------
    extras_require={
        # Vision Mode (OCR + screen interaction)
        "vision": [
            "pyautogui",
            "pytesseract",
            "pynput",
            "opencv-python",
            "numpy",
            "Pillow",
        ],

        # Development & tests (NOT required for users)
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
