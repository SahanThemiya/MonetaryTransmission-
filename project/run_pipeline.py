"""Run the full monetary-transmission forecasting pipeline end to end.

Executes the five model notebooks (VAR/VECM, ARIMA, FFNN, TDNN, LSTM) and
then the comparison notebook, in order, via papermill. Each notebook writes
its metrics_*.csv into results/, and the comparison notebook reads all five
back and writes comparison_summary.csv and best_model_by_window.csv.

Usage:
    python run_pipeline.py
    python run_pipeline.py --data-path /path/to/Monetary_transmission_data_III.xlsx
    python run_pipeline.py --skip 05_lstm.ipynb --skip 04_tdnn.ipynb

By default the data file is expected at data/Monetary_transmission_data_III.xlsx.
Override with --data-path or the MONETARY_DATA_PATH environment variable.
"""
import argparse
import os
from pathlib import Path

import papermill as pm

ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = ROOT / "notebooks"
RESULTS_DIR = ROOT / "results"
EXECUTED_DIR = RESULTS_DIR / "executed_notebooks"

# Order matters only in that the comparison notebook must run last; the five
# model notebooks are independent of one another.
PIPELINE = [
    "01_var_vecm.ipynb",
    "02_arima.ipynb",
    "03_ffnn.ipynb",
    "04_tdnn.ipynb",
    "05_lstm.ipynb",
    "09_model_comparison.ipynb",
]


def run(data_path: str | None, skip: set[str]) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    EXECUTED_DIR.mkdir(exist_ok=True)

    if data_path:
        os.environ["MONETARY_DATA_PATH"] = str(Path(data_path).resolve())

    for name in PIPELINE:
        if name in skip:
            print(f"skip  {name}")
            continue
        src, dst = NOTEBOOKS_DIR / name, EXECUTED_DIR / name
        print(f"run   {name}")
        pm.execute_notebook(str(src), str(dst), cwd=str(NOTEBOOKS_DIR))

    print(f"\ndone — metrics, executed notebooks, and the final comparison are in {RESULTS_DIR}/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--data-path",
        help="Path to Monetary_transmission_data_III.xlsx "
        "(overrides MONETARY_DATA_PATH and the data/ default)",
    )
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        metavar="NOTEBOOK",
        help="Notebook filename to skip (repeatable), e.g. --skip 05_lstm.ipynb",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.data_path, set(args.skip))
