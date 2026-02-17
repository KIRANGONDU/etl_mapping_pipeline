# Setup Guide for Another PC

## Step 1: Clone the Repository

Open **PowerShell** or **Command Prompt** and run:

```bash
git clone https://github.com/KIRANGONDU/etl_mapping_pipeline.git
cd etl_mapping_pipeline
```

## Step 2: Create Python Virtual Environment

```bash
python -m venv venv
```

**On Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the ETL Pipeline

### Option A: Basic ETL Pipeline
```bash
python etl_pipeline.py
```

### Option B: Robust Multi-Source Pipeline
```bash
python run_robust_pipeline.py
```

### Option C: Four Sources Pipeline
```bash
python run_four_sources.py
```

### Option D: Multi-Source Pipeline
```bash
python run_multi_source.py
```

## Step 5: Check Output

After running any script, check the generated files in:
- **data/** folder - contains input data
- **output/** folder - contains transformed results

## Troubleshooting

### Git Not Installed?
Download from: https://git-scm.com/download/win

### Python Not Found?
Download from: https://www.python.org/downloads/

### Module Not Found Error?
Make sure your virtual environment is activated:
```bash
# Check if activated (you should see (venv) at the start of your terminal)
# If not, run:
.\venv\Scripts\Activate.ps1
```

Then install packages again:
```bash
pip install -r requirements.txt
```

## File Descriptions

- **etl_pipeline.py** - Main ETL transformation logic
- **robust_etl.py** - Robust error-handling ETL implementation
- **multi_source_etl.py** - Multi-source data pipeline
- **run_robust_pipeline.py** - Execute robust pipeline with sample data
- **run_multi_source.py** - Execute multi-source pipeline
- **run_four_sources.py** - Execute pipeline with 4 data sources
- **example_usage.py** - Example usage demonstrations
- **config.yaml** - Configuration settings
- **requirements.txt** - Python dependencies

## Key Features

✅ Automatic data transformation
✅ Error handling and logging
✅ Multiple data source support
✅ CSV input/output
✅ Data normalization and validation

---

Need help? Check the documentation files:
- README.md - Project overview
- TROUBLESHOOTING.md - Common issues
- ARCHITECTURE.md - System design
