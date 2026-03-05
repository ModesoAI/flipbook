#!/bin/bash

# Navigate to the extension directory
cd "$(dirname "$0")"

# 1. Create a virtual environment if it doesn't exist (redirecting output to stderr)
if [ ! -d ".venv" ]; then
  python3 -m venv .venv >&2
fi

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Install required packages from requirements.txt silently
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt >&2
fi

# 4. Run the actual Python script unbuffered and replace the shell process
exec python -u main.py "$@"