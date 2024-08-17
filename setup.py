from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='nano_wait',
    version='1.0.0',
    license='MIT License',
    author='Luiz Filipe Seabra de Marco',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='luizfilipeseabra@icloud.com',
    keywords='automation automação wifi wait',
    description=u'Waiting Time Calculation for Automations Based on WiFi and PC Processing',
    packages=['nano_wait'],
    install_requires=['psutil','pywifi'],)