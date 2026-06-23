# Project Config — kyc_googlesheet

## Code Architecture
- **Feature-Based Folder Architecture** with **Clean Architecture** per feature

```
project/
├── app.py                    # Entry point — thin, only wires dependencies
├── core/                     # Shared domain: constants, utils (pure, no framework imports)
├── data_layer/               # Data access: load, transform, cache (no UI code)
├── features/                 # Feature modules
│   ├── charts/               # Reusable chart builders (pure functions return Plotly figs)
│   ├── <feature_a>/          # Each feature is a vertical slice
│   │   ├── logic.py          # Business rules, calculations (pure, no Streamlit)
│   │   └── presentation.py   # UI rendering (Streamlit only)
│   └── <feature_b>/
│       ├── logic.py
│       └── presentation.py
├── sidebar/                  # Navigation + filters (same pattern: logic + presentation)
└── storage/                  # Static data files (Excel, CSV, JSON)
```

- **Layer rules**:
  - `core/` → zero dependencies (no pandas, no streamlit)
  - `data_layer/` → only pandas + file I/O (no streamlit)
  - `features/*/logic.py` → only pandas, numpy (no streamlit)
  - `features/*/presentation.py` → streamlit + plotly (can import logic, charts, core)
  - `features/charts/` → only plotly + pandas (return fig objects, no st.*)
  - `sidebar/presentation.py` → streamlit only
  - `app.py` → streamlit only (imports from all layers, wires them together)
- **Chart rules** (Plotly):
  - All pie charts: < 2% slices → no label; legend always includes count (e.g. `948 B2C-EGENIUS`)
  - All bar charts: `orientation="h"`, labels on Y axis, never rotated
  - Reusable chart functions go in `features/charts/`
- When refactoring: keep `app_backup.py` before restructuring
