# Contributing to ClickSUMO

First off, thank you for considering contributing to ClickSUMO! It's people like you that make ClickSUMO such a great tool.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools**

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests (if available)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

Example:
```python
def calculate_signal_timing(cycle_length: int, phases: int) -> List[int]:
    """
    Calculate signal timing based on Webster's method.
    
    Args:
        cycle_length: Total cycle length in seconds
        phases: Number of signal phases
        
    Returns:
        List of phase durations in seconds
    """
    # Implementation here
    pass
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
feat: Add roundabout network template
fix: Resolve edge creation bug in grid networks
docs: Update installation instructions
refactor: Simplify XML generation logic
```

### Testing

Before submitting:
- Test your changes locally
- Ensure existing features still work
- Test on different browsers (if UI changes)
- Check for console errors

### File Structure

When adding new features:
- Network templates go in `src/network/templates.py`
- Core generators go in `src/core/xml_generators.py`
- UI components go in `app.py` (or consider modularizing)
- Documentation goes in `README.md` or separate docs

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Traffic signal optimization algorithms
- [ ] Output file analysis and visualization
- [ ] OpenStreetMap network import
- [ ] Additional network templates
- [ ] Unit tests and test coverage

### Medium Priority
- [ ] Custom network editor UI
- [ ] Advanced demand patterns
- [ ] KPI calculations
- [ ] Export to other formats
- [ ] Internationalization (i18n)

### Low Priority
- [ ] Dark mode theme
- [ ] Mobile responsiveness
- [ ] Additional vehicle types
- [ ] Tutorial videos

## 🐛 Found a Security Vulnerability?

Please **do not** create a public issue. Email directly to:
**6870376421@student.chula.ac.th**

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to ask questions by:
- Opening an issue with the "question" label
- Emailing: 6870376421@student.chula.ac.th

## 🙏 Recognition

Contributors will be:
- Listed in our README
- Mentioned in release notes
- Given credit in documentation

Thank you for contributing! 🎉
