#!/usr/bin/env bash
# Execute the paper notebook locally (generates tables/figures from model outputs).
# Run from project root: ./run_notebook_local.sh
# Or: bash run_notebook_local.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NOTEBOOK="notebooks/Final_Models_Demo_6heads_executed.ipynb"
DATA_FILE="data/cross_sectional/master_table.csv"

echo "=========================================="
echo "Running notebook locally: $NOTEBOOK"
echo "=========================================="

# Optional: ensure master_table.csv exists (build from ticker CSVs if needed)
if [ ! -f "$DATA_FILE" ]; then
  echo "Warning: $DATA_FILE not found."
  if [ -f "scripts/build_master_table.py" ]; then
    echo "Building master_table.csv from ticker data..."
    python scripts/build_master_table.py
  else
    echo "Please ensure $DATA_FILE exists (e.g. from Colab/Drive or build from data/cross_sectional/*_prices.csv)."
    echo "Exiting."
    exit 1
  fi
fi

# Execute with nbconvert. Run from project root so notebook sees repo_root = . (or notebooks/ parent)
if command -v jupyter &>/dev/null; then
  jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=3600 \
    --ExecutePreprocessor.kernel_name=python3 \
    "$NOTEBOOK"
  echo ""
  echo "Done. Tables and figures written to paper/tables/ and paper/figures/."
elif command -v python &>/dev/null; then
  python -c "
import sys
from pathlib import Path
root = Path('.').resolve()
nb_path = root / '$NOTEBOOK'
try:
  import nbformat
  from nbconvert.preprocessors import ExecutePreprocessor
  with open(nb_path) as f:
    nb = nbformat.read(f, as_version=4)
  ep = ExecutePreprocessor(timeout=3600)
  # Run notebook with cwd = project root so repo_root in notebook = root
  ep.preprocess(nb, {'metadata': {'path': str(root)}})
  with open(nb_path, 'w') as f:
    nbformat.write(nb, f)
  print('Done. Tables and figures written to paper/tables/ and paper/figures/.')
except Exception as e:
  print('Execute failed:', e)
  sys.exit(1)
"
else
  echo "Need jupyter or python with nbformat/nbconvert. Install with: pip install jupyter nbformat nbconvert"
  exit 1
fi
