#!/usr/bin/env python3
"""
Setup script para o pacote cora_boletos.
"""

from setuptools import setup, find_packages
import os

# Ler o README para usar como long_description
def read_readme():
    """Lê o arquivo README.md"""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Ler requirements.txt
def read_requirements():
    """Lê o arquivo requirements.txt"""
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cora_boletos",
    version="2.0.0",
    author="Afonso Carvalho",
    author_email="afonso@email.com",
    description="Sistema de geração automatizada de boletos utilizando a API da Cora",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/afonsorcarvalho/cora_boletos",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cora-boletos=libs.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cora_boletos": [
            "config/*.yaml",
            "examples/*.py",
            "docs/*.md",
        ],
    },
    keywords="boleto, cora, api, pagamento, financeiro, cobrança",
    project_urls={
        "Bug Reports": "https://github.com/afonsorcarvalho/cora_boletos/issues",
        "Source": "https://github.com/afonsorcarvalho/cora_boletos",
        "Documentation": "https://github.com/afonsorcarvalho/cora_boletos/tree/main/docs",
    },
)