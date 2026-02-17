# Multi-Source ETL Pipeline - Header Mapping Guide

## Overview

This advanced ETL pipeline handles **multiple CSV/Excel files with different column names** and consolidates them into a unified output.

## Problem Solved

When you have data from different sources with inconsistent headers:

**Dataset 1 (dataset_1.csv):**
```
emp_id, fname, lname, sex, birth_date, joining_date, annual_salary
```

**Dataset 2 (dataset_2.csv):**
```
employee_id, first_name, last_name, gender, date_of_birth, hire_date, salary
```

**Goal:** Consolidate both into one table with consistent column names:
```
employee_id, first_name, last_name, gender, date_of_birth, hire_date, salary
```

## Features

✅ **Multi-Source Support** - Read from multiple files simultaneously  
✅ **Header Mapping** - Map different column names to unified schema  
✅ **Data Consolidation** - Merge data from all sources  
✅ **Transformations** - Apply same transformations to all consolidated data  
✅ **Source Tracking** - Know which row came from which source  
✅ **Error Handling** - Graceful handling of missing columns  

## Quick Start

### Step 1: Create Pipeline
```python
from multi_source_etl import MultiSourceETLPipeline
from pathlib import Path

pipeline = MultiSourceETLPipeline(
    input_path=Path('data'),
    output_path=Path('output')
)
```

### Step 2: Register Data Sources
```python
# Source 1 with custom column names
pipeline.register_source(
    source_name='dataset_1',
    filename='dataset_1.csv',
    column_mapping={
        'emp_id': 'employee_id',
        'fname': 'first_name',
        'lname': 'last_name',
        'sex': 'gender',
        'birth_date': 'date_of_birth',
        'joining_date': 'hire_date',
        'annual_salary': 'salary',
        'dept': 'department',
        'yrs_old': 'age',
        'active_status': 'status'
    }
)

# Source 2 with standard names (1:1 mapping)
pipeline.register_source(
    source_name='dataset_2',
    filename='dataset_2.csv',
    column_mapping={
        'employee_id': 'employee_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'date_of_birth': 'date_of_birth',
        'hire_date': 'hire_date',
        'salary': 'salary',
        'department': 'department',
        'age': 'age',
        'status': 'status'
    }
)
```

### Step 3: Run Pipeline
```python
config = {
    'date_columns': ['date_of_birth', 'hire_date'],
    'remove_duplicates': True,
    'fill_missing_values': {
        'gender': 'Unknown',
        'status': 'unknown'
    },
    'final_columns': [
        'source',           # Track which dataset each row came from
        'employee_id',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'hire_date',
        'salary'
    ]
}

result = pipeline.run(
    output_filename='consolidated_employees.csv',
    config=config
)
```

## Column Mapping Examples

### Pattern 1: Abbreviations to Full Names
```python
'fname' → 'first_name'
'lname' → 'last_name'
'sex' → 'gender'
'birth_date' → 'date_of_birth'
```

### Pattern 2: Different Naming Conventions
```python
'emp_id' → 'employee_id'
'annual_salary' → 'salary'
'dept' → 'department'
'yrs_old' → 'age'
```

### Pattern 3: Status Values (handled separately)
```python
'active_status' → 'status'  # Maps column name, values are normalized later
```

## Transformation Configuration

```python
config = {
    # Columns to format as dates (YYYY-MM-DD)
    'date_columns': ['date_of_birth', 'hire_date'],
    
    # Remove duplicate rows
    'remove_duplicates': True,
    
    # Fill missing values
    'fill_missing_values': {
        'gender': 'Unknown',
        'status': 'unknown'
    },
    
    # Final output columns (in order)
    'final_columns': [
        'source',
        'employee_id',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'hire_date',
        'salary'
    ]
}
```

## Data Flow

```
Input Files:
├── dataset_1.csv (emp_id, fname, lname, sex, ...)
└── dataset_2.csv (employee_id, first_name, last_name, gender, ...)
        ↓
    EXTRACT & MAP
    ├── Apply source1 mapping
    └── Apply source2 mapping
        ↓
    CONSOLIDATE
    ├── Concatenate all mapped data
    └── Add 'source' column for tracking
        ↓
    TRANSFORM
    ├── Normalize gender values
    ├── Format dates to YYYY-MM-DD
    ├── Fill missing values
    └── Select final columns
        ↓
Output:
└── consolidated_employees.csv (unified schema)
```

## File Structure

```
etl_pipeline/
├── data/
│   ├── dataset_1.csv         ← Source 1 (different headers)
│   ├── dataset_2.csv         ← Source 2 (different headers)
│   └── sample_employee_data.csv
├── output/
│   └── consolidated_employees.csv  ← Consolidated output
├── multi_source_etl.py       ← Main multi-source module
├── run_multi_source.py       ← Example usage script
└── MULTI_SOURCE_GUIDE.md     ← This file
```

## Running the Example

```bash
cd etl_pipeline
python run_multi_source.py
```

Output will show:
- Data extracted from each source
- Columns mapped successfully
- Final consolidated data
- Data distribution by source, gender, department

## Adding More Sources

```python
# Register a 3rd source
pipeline.register_source(
    source_name='dataset_3',
    filename='dataset_3.csv',
    column_mapping={
        'worker_id': 'employee_id',
        'given_name': 'first_name',
        'family_name': 'last_name',
        # ... etc
    }
)
```

## Advanced: Custom Transformations

```python
# After consolidation, apply custom logic
pipeline.extract_and_map()
pipeline.consolidate()

# Custom transformation before final transform
consolidated = pipeline.consolidated_data
consolidated['salary_band'] = pd.cut(consolidated['salary'], bins=5)

# Then apply standard transformations
pipeline.transformed_data = consolidated
pipeline.load('custom_output.csv')
```

## Troubleshooting

### Missing Column Warning
```
WARNING - Column 'xyz' not found in dataset_1
```
**Solution**: Check source file has this column or remove from mapping

### All Rows from One Source
**Solution**: Ensure all sources are registered before calling `run()`

### Date Formatting Issues
**Solution**: Ensure date columns are in recognizable format (YYYY-MM-DD, MM/DD/YYYY, etc.)

## Key Methods

| Method | Purpose |
|--------|---------|
| `register_source()` | Register a new data source with header mapping |
| `extract_and_map()` | Read files and apply header mappings |
| `consolidate()` | Merge all sources into one dataframe |
| `transform()` | Apply transformations (gender norm, date format, etc.) |
| `load()` | Save output to CSV |
| `run()` | Execute full pipeline in one call |

## Output Example

**Input (2 files):**
```
File 1 (5 rows): emp_id, fname, lname, sex, birth_date, joining_date, annual_salary, dept, yrs_old, active_status
File 2 (5 rows): employee_id, first_name, last_name, gender, date_of_birth, hire_date, salary, department, age, status

Total: 10 rows from 2 sources
```

**Output (1 unified file):**
```
source    | employee_id | first_name | last_name | gender | date_of_birth | hire_date  | salary | department | age
----------|-------------|-----------|-----------|--------|----------------|-----------|--------|-----------|-----
dataset_1 | 101         | John      | Doe       | M      | 1990-01-15    | 2015-06-01| 50000  | IT        | 34
dataset_1 | 102         | Jane      | Smith     | F      | 1992-03-22    | 2016-08-15| 65000  | HR        | 32
dataset_2 | 201         | Diana     | Jones     | F      | 1993-07-30    | 2015-11-18| 68000  | HR        | 31
...
```

## Best Practices

1. **Use consistent target names** - Define clear unified schema
2. **Document mappings** - Keep record of which source uses which names
3. **Test incrementally** - Add sources one at a time
4. **Track source** - Always include 'source' column for audit trail
5. **Validate output** - Check row counts match input totals
6. **Handle errors** - Missing columns won't crash pipeline

---

**Ready to run?**
```bash
python run_multi_source.py
```
