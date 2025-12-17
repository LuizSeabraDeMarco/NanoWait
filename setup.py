from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name='nano_wait',
    version='3.1.3',
    license='MIT License',
    author='Luiz Filipe Seabra de Marco',
    author_email='luizfilipeseabra@icloud.com',
    description=(
        u'Adaptive waiting and smart automation library — '
        u'includes Wi-Fi, system context, and Vision Mode for screen-based decisions.'
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='automation automação wifi wait vision ocr screen adaptive ai',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'pywifi'
    ],
    extras_require={
    "vision": [
        "pyautogui",
        "pytesseract",
        "pynput",
        "opencv-python",
        "numpy"
    ]
}
,
    entry_points={
        'console_scripts': [
            'nano-wait = nano_wait.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.8',
)
