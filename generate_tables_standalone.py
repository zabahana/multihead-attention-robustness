#!/usr/bin/env python3
"""
Standalone script to generate tables from notebook results.
This script can be run independently to avoid connection issues.
"""

import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

# Add src to path if needed
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src'))

def load_notebook_results(notebook_path):
    """Load results from executed notebook."""
    print(f"Loading notebook: {notebook_path}")
    
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Extract outputs from cells
    results = {}
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'outputs' in cell:
            # Try to extract printed outputs
            for output in cell['outputs']:
                if 'text' in output:
                    text = ''.join(output['text'])
                    # Look for key indicators
                    if 'R²' in text or 'robustness' in text.lower():
                        print(f"Found output in cell")
    
    return results

def generate_tables_from_data(data_dir=None):
    """
    Generate tables from existing data files.
    This is a workaround - assumes data files exist from notebook execution.
    """
    if data_dir is None:
        data_dir = project_root / 'paper' / 'tables'
    else:
        data_dir = Path(data_dir)
    
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("STANDALONE TABLE GENERATION")
    print("=" * 80)
    print(f"\nLooking for data files in: {data_dir}")
    print("\nThis script generates tables from CSV files created by the notebook.")
    print("If tables don't exist, please run the notebook cells that generate:")
    print("  - model_performance_with_ci.csv")
    print("  - economic_metrics_summary.csv")
    print("\nAlternatively, you can run the notebook in Jupyter/Lab directly.")
    print("=" * 80)
    
    # Check for existing CSV files
    ci_file = data_dir / 'model_performance_with_ci.csv'
    economic_file = data_dir / 'economic_metrics_summary.csv'
    
    if ci_file.exists():
        print(f"\n✓ Found: {ci_file}")
        df = pd.read_csv(ci_file)
        print(f"  Rows: {len(df)}, Columns: {list(df.columns)}")
        
        # Generate LaTeX if not exists
        latex_file = data_dir / 'model_performance_with_ci.tex'
        if not latex_file.exists():
            print(f"\nGenerating LaTeX table...")
            generate_ci_latex_table(df, latex_file)
    else:
        print(f"\n⚠ Not found: {ci_file}")
        print("   Run the notebook cell that creates 'model_performance_with_ci.csv'")
    
    if economic_file.exists():
        print(f"\n✓ Found: {economic_file}")
        df = pd.read_csv(economic_file)
        print(f"  Rows: {len(df)}, Columns: {list(df.columns)}")
        
        # Generate LaTeX if not exists
        latex_file = data_dir / 'economic_metrics_summary.tex'
        if not latex_file.exists():
            print(f"\nGenerating LaTeX table...")
            generate_economic_latex_table(df, latex_file)
    else:
        print(f"\n⚠ Not found: {economic_file}")
        print("   Run the notebook cell that creates 'economic_metrics_summary.csv'")
    
    print("\n" + "=" * 80)
    print("✅ Table generation complete!")
    print("=" * 80)

def generate_ci_latex_table(df, output_path):
    """Generate LaTeX table for CI results."""
    latex = """\\begin{table}[h]
\\centering
\\caption{Model Performance with 95\\% Confidence Intervals}
\\label{tab:model_performance_ci}
\\footnotesize
\\begin{tabular}{lcccccc}
\\toprule
Model & R² & R² SE & R² 95\\% CI & Robustness & Robustness SE & Robustness 95\\% CI \\\\
\\midrule
"""
    
    for _, row in df.iterrows():
        model = row.get('Model', 'N/A')
        r2 = row.get('R²', 'N/A')
        r2_se = row.get('R²_SE', 'N/A')
        r2_ci = row.get('R²_CI_95', 'N/A')
        robustness = row.get('Robustness', 'N/A')
        rob_se = row.get('Robustness_SE', 'N/A')
        rob_ci = row.get('Robustness_CI_95', 'N/A')
        
        latex += f"{model} & {r2} & {r2_se} & {r2_ci} & {robustness} & {rob_se} & {rob_ci} \\\\\n"
    
    latex += """\\bottomrule
\\end{tabular}
\\vspace{0.1cm}
\\footnotesize
\\begin{minipage}{\\columnwidth}
\\textit{Note: R² and Robustness metrics with 95\\% bootstrap confidence intervals (1000 bootstrap samples). 
SE = Standard Error. Robustness is averaged across all attack types (A1-A4) and epsilon values (0.25, 0.5, 1.0).}
\\end{minipage}
\\end{table}
"""
    
    with open(output_path, 'w') as f:
        f.write(latex)
    print(f"✓ Saved: {output_path}")

def generate_economic_latex_table(df, output_path):
    """Generate LaTeX table for economic metrics."""
    latex = """\\begin{table}[h]
\\centering
\\caption{Economically Interpretable Metrics: Clean vs Adversarial Conditions}
\\label{tab:economic_metrics}
\\footnotesize
\\begin{tabular}{lcccccc}
\\toprule
Model & Spearman IC & IC-IR & Portfolio Return & Turnover & Turnover-Adj Return \\\\
\\midrule
"""
    
    for _, row in df.iterrows():
        model = row.get('Model', 'N/A')
        ic = row.get('Spearman_IC', 'N/A')
        ic_ir = row.get('IC_IR', 'N/A')
        portfolio_ret = row.get('Portfolio_Return', 'N/A')
        turnover = row.get('Turnover', 'N/A')
        adj_return = row.get('Turnover_Adjusted_Return', 'N/A')
        
        latex += f"{model} & {ic} & {ic_ir} & {portfolio_ret} & {turnover} & {adj_return} \\\\\n"
    
    latex += """\\bottomrule
\\end{tabular}
\\vspace{0.1cm}
\\footnotesize
\\begin{minipage}{\\columnwidth}
\\textit{Note: Metrics computed under clean and adversarial conditions. 
Spearman IC = Spearman rank Information Coefficient. 
IC-IR = IC Information Ratio (mean IC / std IC). 
Portfolio Return = Long-short portfolio return. 
Turnover-Adj Return = Return adjusted for transaction costs.}
\\end{minipage}
\\end{table}
"""
    
    with open(output_path, 'w') as f:
        f.write(latex)
    print(f"✓ Saved: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate tables from notebook results')
    parser.add_argument('--data_dir', type=str, help='Directory containing CSV files')
    args = parser.parse_args()
    
    generate_tables_from_data(args.data_dir)
