# Running the Notebook Locally

You can execute the paper notebook on your machine so that all tables and figures are generated from actual model outputs.

## Requirements

- **Python 3.8+** with: `numpy`, `pandas`, `torch`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`
- **Jupyter** (recommended): `pip install jupyter nbformat nbconvert`
- **Data**: `data/cross_sectional/master_table.csv` must exist (same format as used on Colab: date, symbol, features, target). If you have this file from a Colab/Drive run, copy it into `data/cross_sectional/`.

## Execute the notebook

From the **project root** (`multihead-attention-robustness`):

```bash
chmod +x run_notebook_local.sh
./run_notebook_local.sh
```

Or:

```bash
bash run_notebook_local.sh
```

If you have `jupyter` installed, the script uses `jupyter nbconvert --execute`. Otherwise it falls back to Python with `nbformat` and `nbconvert`. The notebook runs with the project root as the working directory so paths like `repo_root / 'data' / 'cross_sectional' / 'master_table.csv'` resolve correctly.

## After a successful run

- **Tables**: `paper/tables/` (e.g. `validation_results_summary.tex`, `robustness_summary_stress.tex`, `adversarial_effectiveness_summary.tex`, `robustness_training_epsilons.tex`)
- **Figures**: `paper/figures/` (e.g. `performance_comparison_by_model.png`, `robustness_vs_epsilon_all_models_attacks.pdf`, `standard_vs_adversarial_robustness.pdf`, `clean_vs_adversarial_ts.png`)

Recompile the LaTeX paper so it uses these outputs.

## If you don't have `master_table.csv`

The notebook expects a single cross-sectional CSV at `data/cross_sectional/master_table.csv` (date index, symbol, features such as mom_1m, vol_3m, and target). If you only have the per-ticker price CSVs in `data/cross_sectional/`, you need to build the master table with your own pipeline (feature computation, alignment, and stacking) or obtain it from the same source used on Colab/Drive.
