# 🪟 Windows Setup Guide

## Fix for Installation Issues

If you're getting Rust compilation errors (common on Windows with Python 3.13), try these solutions:

### Option 1: Use Simple Requirements (Recommended)

```bash
# Uninstall any partially installed packages
pip uninstall pydantic-core -y

# Install with the simplified requirements
pip install -r requirements-simple.txt
```

### Option 2: Install Pre-compiled Wheels

```bash
# Install packages individually to get pre-compiled wheels
pip install fastapi uvicorn[standard]
pip install langchain langchain-openai langchain-community
pip install chromadb
pip install pypdf2 python-multipart python-dotenv
pip install streamlit openai tiktoken
```

### Option 3: Use Python 3.11 (Most Compatible)

If you continue having issues, consider using Python 3.11:

1. Download Python 3.11 from: https://www.python.org/downloads/release/python-3118/
2. Create a virtual environment:
   ```bash
   python3.11 -m venv policy_chat_env
   policy_chat_env\Scripts\activate
   pip install -r requirements-simple.txt
   ```

### Option 4: Skip Problematic Packages

If some packages still fail, you can run a minimal version:

```bash
# Core packages only
pip install fastapi uvicorn streamlit openai python-dotenv

# Then manually install others as needed
```

## After Installation

1. **Set up the project**:
   ```bash
   python setup.py
   ```

2. **Add your OpenAI API key** to the `.env` file

3. **Run the application**:
   ```bash
   python run.py both
   ```

## Troubleshooting Windows Issues

### "Rust not found" Error
- This is normal for some packages on Windows
- Use Option 1 or 2 above to avoid compilation

### "Microsoft Visual C++ 14.0 is required"
- Install Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use the pre-compiled wheels approach

### Permission Errors
- Run PowerShell as Administrator
- Or use `--user` flag: `pip install --user -r requirements-simple.txt`

### Port Already in Use
- Kill processes using ports 8000/8501:
  ```bash
  netstat -ano | findstr :8000
  taskkill /PID <PID_NUMBER> /F
  ```

## Quick Test

After installation, test if everything works:

```bash
python -c "import fastapi, streamlit, langchain, openai; print('✅ All imports successful!')"
```

If this works, you're ready to run the chatbot!
