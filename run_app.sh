#!/bin/bash

# Pre-flight sanity check
if [ ! -d ".venv" ]; then
  echo "❌ .venv not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

source .venv/bin/activate

# Check that streamlit is installed
if ! python -c "import streamlit" &> /dev/null; then
  echo "❌ Streamlit is not installed. Run: pip install -r requirements.txt"
  exit 1
fi

# Check PYTHONPATH and set if needed
if [[ "$PYTHONPATH" != "." ]]; then
  export PYTHONPATH=.
  echo "🔧 Set PYTHONPATH=."
fi

# Launch Streamlit app
echo "🚀 Launching Streamlit app..."
streamlit run app/api/streamlit_app.py
