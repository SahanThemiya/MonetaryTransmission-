# Monetary Transmission Forecasting Pipeline

Forecasts CPI and the exchange rate (EXR) from monthly macroeconomic data
(CPI, EXR, M2b, RSV, BRNT), comparing five models — VAR/VECM, ARIMA, FFNN,
TDNN, and LSTM — across four structural-break sub-periods plus the full
sample.

## Project layout

```
.
├── data/                          # put Monetary_transmission_data_III.xlsx here
├── notebooks/
│   ├── 01_var_vecm.ipynb
│   ├── 02_arima.ipynb
│   ├── 03_ffnn.ipynb
│   ├── 04_tdnn.ipynb
│   ├── 05_lstm.ipynb
│   └── 06_model_comparison.ipynb
├── results/                        # generated: metrics_*.csv, comparison_summary.csv, ...
│   └── executed_notebooks/         # generated: papermill's run copies, with outputs baked in
├── run_pipeline.py
├── requirements.txt
├── environment.yml
└── .gitignore
```

## Setup

**pip**
```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**conda**
```bash
conda env create -f environment.yml
conda activate monetary-transmission
```

Then place the source spreadsheet at `data/Monetary_transmission_data_III.xlsx`.
If it lives somewhere else, either set an environment variable:

```bash
export MONETARY_DATA_PATH=/path/to/Monetary_transmission_data_III.xlsx
```

or pass `--data-path` to the runner (below) — no need to edit the notebooks.

## Running the pipeline

Run everything — all five models, then the comparison — with one command:

```bash
python run_pipeline.py
```

Options:

```bash
# point at a data file that isn't in data/
python run_pipeline.py --data-path /path/to/Monetary_transmission_data_III.xlsx

# skip a slow model (e.g. while iterating on the others)
python run_pipeline.py --skip 05_lstm.ipynb --skip 04_tdnn.ipynb
```

This executes each notebook with [papermill](https://papermill.readthedocs.io/),
saving a fully-run copy (code + outputs + plots) to
`results/executed_notebooks/`, while each model notebook's own export cell
writes `results/metrics_<model>.csv`. The comparison notebook runs last,
reading all five `metrics_*.csv` files and writing:

- `results/comparison_summary.csv` — RMSE/MAE for every model × target × window
- `results/best_model_by_window.csv` — the lowest-RMSE model per window/target

## Running notebooks individually

Each notebook is still a normal notebook — open any one in Jupyter and run it
top to bottom. They pick up `MONETARY_DATA_PATH` if set, otherwise default to
`../data/Monetary_transmission_data_III.xlsx` (relative to `notebooks/`), so
just launch Jupyter from the project root:

```bash
jupyter lab
```

The model notebooks (`01`–`05`) are independent of each other and can run in
any order or in parallel. `06_model_comparison.ipynb` must run after at least
one of them has produced a `metrics_*.csv`, and needs all five to produce the
full comparison table.

## Notes

- FFNN and TDNN use PyTorch; LSTM uses TensorFlow/Keras — both are CPU-friendly
  at this data size, GPU is not required.
- Structural-break windows (`W1`–`W4`) split the sample at 2008-06, 2016-10,
  and 2022-03; `W5` is the full, unsegmented series. All notebooks share this
  partition so results are comparable window-for-window.
- `results/` and `data/` are gitignored (aside from `.gitkeep`) since they
  hold generated output and a private data file respectively.
