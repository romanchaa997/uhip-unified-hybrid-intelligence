# Contributing to UHIP

We welcome contributions! Here's how you can help.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/uhip-unified-hybrid-intelligence.git
cd uhip-unified-hybrid-intelligence

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install -e ".[dev]"
```

## Code Style

Follow PEP 8 guidelines:

```bash
black uhip/
isort uhip/
flake8 uhip/
mypy uhip/
```

## Running Tests

```bash
pytest tests/ -v
pytest --cov=uhip --cov-report=html
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Code of Conduct

Be respectful and constructive in all interactions.
