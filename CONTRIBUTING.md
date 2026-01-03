# Contributing to UHIP

We appreciate your interest in contributing to the Unified Hybrid Intelligence Platform (UHIP)! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

All contributors are expected to maintain professional and respectful behavior. Harassment, discrimination, or abusive behavior will not be tolerated and may result in removal from the project.

## Getting Started

### Prerequisites
- Python 3.9+
- Git
- Virtual environment capability
- Basic understanding of distributed systems

### Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/uhip-unified-hybrid-intelligence.git
cd uhip-unified-hybrid-intelligence

# Add upstream remote
git remote add upstream https://github.com/romanchaa997/uhip-unified-hybrid-intelligence.git
```

### Setup Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## Development Workflow

### Creating a Feature Branch
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

#### Code Style
- Follow PEP 8 standards
- Use type hints for function signatures
- Maximum line length: 100 characters
- Write descriptive variable and function names

#### Example Code
```python
def calculate_prediction(
    model_id: str,
    features: Dict[str, float]
) -> Tuple[float, float]:
    """
    Calculate prediction using the specified model.
    
    Args:
        model_id: Identifier of the model to use
        features: Dictionary of feature values
        
    Returns:
        Tuple of (prediction, confidence)
    """
    # Implementation here
    pass
```

#### Code Formatting
```bash
# Format code with black
black src/

# Check code with flake8
flake8 src/

# Sort imports
isort src/

# Type checking
mypy src/
```

### Writing Tests
- Write tests for all new features
- Maintain or improve code coverage
- Use pytest framework
- Follow naming convention: `test_*.py`

```python
import pytest
from uhip.models import Predictor

def test_prediction_creation():
    """Test that predictions are created correctly."""
    predictor = Predictor(model_id="test-model")
    result = predictor.predict({"feature1": 10})
    
    assert result is not None
    assert "prediction" in result
    assert 0 <= result["confidence"] <= 1

@pytest.mark.asyncio
async def test_async_prediction():
    """Test asynchronous prediction."""
    predictor = Predictor(model_id="test-model")
    result = await predictor.predict_async({"feature1": 10})
    
    assert result is not None
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_predictions.py

# Run tests in parallel
pytest -n auto
```

## Committing Changes

### Commit Message Format
Follow conventional commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates

### Example
```
feat(predictions): add support for ensemble models

Implement ensemble prediction strategy combining multiple models.
Added XGBooost ensemble implementation with hyperparameter tuning.

Closes #123
```

### Pushing Changes
```bash
# Commit changes
git add .
git commit -m "feat: your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

## Creating a Pull Request

### PR Title
Be descriptive and follow the same format as commits:
```
[FEATURE] Add support for ensemble models
[FIX] Correct memory leak in prediction cache
[DOCS] Update deployment guide
```

### PR Description Template
```markdown
## Description
Clear description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings generated
```

## Code Review Process

### What to Expect
1. Automated checks will run (linting, tests, coverage)
2. Code review by maintainers
3. Feedback and potential revision requests
4. Approval and merge

### Review Feedback
- Review feedback is constructive and helpful
- Respond to feedback or ask for clarification
- Make requested changes and push updates
- Mark conversations as resolved

## Documentation

### Updating Documentation
- Update README.md for user-facing changes
- Update DEVELOPER_README.md for development changes
- Update docstrings for code changes
- Add comments for complex logic

### Documentation Format
```python
def complex_function(param1: str) -> Dict:
    """
    Brief description of function.
    
    Detailed explanation of what this function does,
    including any important considerations.
    
    Args:
        param1: Description of param1
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        
    Example:
        >>> result = complex_function("input")
        >>> print(result)
    """
    pass
```

## Important Notes

### Base Structure Preservation
**Do NOT change the base structure of the project.** When adding new features or fields:
- Keep existing architecture intact
- Add new features without modifying core components
- Maintain backward compatibility
- Document any structural decisions

### Performance
- Consider performance implications
- Profile code for bottlenecks
- Add benchmarks for critical paths
- Document performance characteristics

### Security
- Never commit secrets or credentials
- Use environment variables for sensitive data
- Follow security best practices
- Report security vulnerabilities privately

## Getting Help

### Resources
- [DEVELOPER_README.md](DEVELOPER_README.md) - Development setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- GitHub Issues - For bugs and feature requests

### Questions?
- Check existing issues and discussions
- Ask in GitHub discussions
- Open an issue with the question tag

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributors section

Thank you for contributing to UHIP!
