"""
Setup script for UHIP - Unified Hybrid Intelligence Platform
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="uhip",
    version="1.0.0",
    author="UHIP Development Team",
    author_email="dev@uhip.io",
    description="Unified Hybrid Intelligence Platform - Production-Ready System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/romanchaa997/uhip-unified-hybrid-intelligence",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
            "pylint>=2.17.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.1.0",
            "mkdocstrings[python]>=0.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "uhip=uhip.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="artificial-intelligence machine-learning quantum blockchain edge-computing hybrid-intelligence parallel-processing",
    project_urls={
        "Bug Reports": "https://github.com/romanchaa997/uhip-unified-hybrid-intelligence/issues",
        "Source": "https://github.com/romanchaa997/uhip-unified-hybrid-intelligence",
        "Documentation": "https://romanchaa997.github.io/uhip-unified-hybrid-intelligence/",
    },
)
