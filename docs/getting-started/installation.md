# Installation

This guide will help you install UHIP on your system.

## Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
pip install uhip
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/romanchaa997/uhip-unified-hybrid-intelligence.git
cd uhip-unified-hybrid-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and package
pip install -r requirements.txt
pip install -e .
```

### Method 3: Docker Installation

```bash
# Pull the Docker image
docker pull uhip/uhip:latest

# Run UHIP in a container
docker run -it uhip/uhip:latest uhip --demo
```

## Verification

Verify your installation:

```bash
# Check UHIP version
uhip --help

# Run demo to ensure everything works
uhip --demo
```

Expected output:
```
============================================================
UHIP Demonstration Mode
============================================================
...
```

## Development Installation

For development work, install additional dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- pytest (testing)
- black (code formatting)
- flake8 (linting)
- mypy (type checking)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'uhip'`

**Solution**: Make sure you've activated your virtual environment and installed the package:
```bash
source venv/bin/activate
pip install -e .
```

**Issue**: Permission denied errors

**Solution**: Use `--user` flag or run in a virtual environment:
```bash
pip install --user uhip
```

**Issue**: Dependency conflicts

**Solution**: Create a fresh virtual environment:
```bash
python -m venv fresh_env
source fresh_env/bin/activate
pip install uhip
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration](configuration.md)
- [Basic Usage](../user-guide/basic-usage.md)
