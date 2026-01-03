# Contributing to UHIP

Thank you for your interest in contributing to UHIP!

## How to Contribute

1. **Fork the Repository**
   - Fork the project on GitHub
   - Clone your fork locally

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add tests for new features

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

5. **Format Code**
   ```bash
   black uhip/
   isort uhip/
   flake8 uhip/
   ```

6. **Commit Changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit Pull Request**
   - Open a PR on GitHub
   - Describe your changes
   - Link any related issues

## Development Setup

```bash
# Clone the repository
git clone https://github.com/romanchaa997/uhip-unified-hybrid-intelligence.git
cd uhip-unified-hybrid-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for all public functions
- Keep line length to 100 characters

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation

## Questions?

Open an issue or start a discussion on GitHub.

Thank you for contributing! 🙏
