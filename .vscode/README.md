# VS Code Setup Guide

This project includes VS Code configuration for a seamless Django development experience.

## Quick Setup

1. **Install Recommended Extensions**: VS Code will prompt you to install recommended extensions when you open the project.

2. **Python Interpreter**: Make sure VS Code is using the correct Python interpreter:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose your Python environment

## Available Tasks

Access tasks via `Ctrl+Shift+P` → "Tasks: Run Task":

### Django Tasks
- **Django: Run Server** - Start the development server (background task)
- **Django: Create Sample Data** - Generate sample data for testing
- **Django: Make Migrations** - Create new database migrations
- **Django: Migrate** - Apply database migrations
- **Django: Create Superuser** - Create a Django admin user
- **Django: Run Tests** - Run Django unit tests

### Testing Tasks
- **Test: Run Setup Validation** - Validate environment setup
- **Test: Run API Tests** - Run API endpoint tests

### Other Tasks
- **Install Dependencies** - Install Python packages from requirements.txt

## Debug Configurations

Press `F5` or go to Run and Debug view (`Ctrl+Shift+D`) to access:

- **Django: Debug Server** - Debug the Django development server
- **Django: Create Sample Data** - Debug the sample data creation
- **Django: Run Tests** - Debug Django tests
- **Test: API Tests** - Debug API tests
- **Test: Setup Validation** - Debug setup validation

## Keyboard Shortcuts

- `F5` - Start debugging
- `Ctrl+F5` - Run without debugging
- `Ctrl+Shift+P` - Command palette
- `Ctrl+` ` - Toggle terminal
- `Ctrl+Shift+` ` - Create new terminal

## File Structure

```
.vscode/
├── tasks.json          # Task definitions
├── launch.json         # Debug configurations
├── settings.json       # Workspace settings
├── extensions.json     # Recommended extensions
└── python.json         # Python snippets
```

## Quick Start Commands

1. **First time setup**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Create sample data
   python manage.py create_sample_data
   ```

2. **Run the server**:
   - Use task: "Django: Run Server"
   - Or manually: `python manage.py runserver`

3. **Run tests**:
   - Use task: "Test: Run API Tests"
   - Or manually: `python test_api.py`

## Tips

- Use the integrated terminal (`Ctrl+` `) for Django commands
- The Django server task runs in the background - check the terminal output
- Breakpoints work in debug mode for both Django and test scripts
- Auto-formatting is enabled on save (requires Black formatter)
