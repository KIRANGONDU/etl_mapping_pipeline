# Robust ETL Pipeline - Error Handling & Auto-Rectification Guide

## Overview

This is an enterprise-grade ETL pipeline with comprehensive error handling, detailed logging, and automatic data rectification.

## Key Features

### ✅ Error Detection & Reporting
- **File validation** - Check if files exist before processing
- **Data validation** - Verify dataframe integrity
- **Type checking** - Detect data type mismatches
- **Column mapping** - Identify missing or misnamed columns
- **Detailed logging** - Track every operation with timestamps

### ✅ Automatic Rectification
- **Missing columns** - Add null columns if mapping fails
- **Data type conversion** - Auto-convert dates and numeric fields
- **Duplicate removal** - Detect and remove duplicate rows
- **Missing value imputation** - Fill nulls with default values
- **Gender normalization** - Handle multiple gender formats

### ✅ Graceful Failure Handling
- **Partial processing** - Continue even if some sources fail
- **Error recovery** - Attempt automatic correction at each step
- **Source tracking** - Know which data came from where
- **Detailed logs** - Save error reports as JSON

### ✅ Comprehensive Logging
- **Stage tracking** - Know exactly where errors occur
- **Error details** - Full traceback for debugging
- **Correction tracking** - Know what was fixed
- **Performance metrics** - Track processing time and row counts

## Architecture

```
Robust ETL Pipeline
│
├── Error Handler
│   ├── Log Errors
│   ├── Log Warnings
│   ├── Track Corrections
│   └── Generate Reports
│
├── Data Validator
│   ├── Validate Files
│   ├── Validate DataFrames
│   ├── Rectify Missing Columns
│   ├── Rectify Data Types
│   ├── Rectify Duplicates
│   └── Rectify Missing Values
│
└── ETL Pipeline
    ├── Extract & Map (with error handling)
    ├── Consolidate (with validation)
    ├── Transform (with rectification)
    └── Load (with verification)
```

## Quick Start

### Step 1: Run the Pipeline

```bash
python run_robust_pipeline.py
```

### Step 2: Check Results

```bash
# View output CSV
cat output/consolidated_all_sources_robust.csv

# View error log (if any issues occurred)
cat output/error_log.json
```

## Error Handling Features

### 1. Missing File Detection
```
❌ File not found: data/dataset_1.csv
✓ Pipeline continues with other sources
```

### 2. Missing Column Handling
```
⚠ Missing columns detected: ['joining_date']
✓ Column added with None values
✓ Mapping continues with available columns
```

### 3. Data Type Conversion
```
✓ Converting 'salary' to numeric
✓ Converting 'date_of_birth' to datetime
✓ Auto-rectified 5 columns
```

### 4. Duplicate Detection
```
✓ Removed 3 duplicate rows from source_2
```

### 5. Missing Value Imputation
```
✓ Filled 12 missing gender values with 'Unknown'
✓ Filled 8 missing status values with 'unknown'
```

## Error Log Structure

`output/error_log.json` contains:

```json
{
  "total_errors": 2,
  "total_warnings": 5,
  "total_corrections": 12,
  "errors": [
    {
      "timestamp": "2026-02-18T10:30:45.123456",
      "stage": "extraction_source_1",
      "error": "Failed to read file: data/dataset_1.csv",
      "details": "File contains encoding issues",
      "traceback": "..."
    }
  ],
  "warnings": [
    {
      "timestamp": "2026-02-18T10:30:46.234567",
      "stage": "mapping_source_1",
      "warning": "Missing columns in mapping: ['joining_date']"
    }
  ],
  "corrections": [
    {
      "timestamp": "2026-02-18T10:30:47.345678",
      "stage": "source_1_mixed",
      "action": "Removed duplicate rows",
      "affected_rows": 3
    }
  ]
}
```

## Pipeline Phases

### Phase 1: Extract & Map
**What happens:**
- Read each CSV file
- Validate file exists and is readable
- Validate dataframe structure
- Map columns to unified schema
- Auto-rectify data types
- Remove duplicates
- Add source tracking column

**Error handling:**
- Missing files → Skip and log
- Missing columns → Log warning, use available columns
- Type errors → Auto-convert or log warning
- Empty dataframes → Skip source

### Phase 2: Consolidation
**What happens:**
- Merge all successfully processed sources
- Concatenate rows while preserving source information
- Validate consolidated data

**Error handling:**
- No sources processed → Fatal error with detailed message
- Partial consolidation → Continue with available data

### Phase 3: Transformation
**What happens:**
- Normalize gender values
- Format dates to YYYY-MM-DD
- Fill missing values based on rules
- Remove duplicates from consolidated data
- Select final output columns

**Error handling:**
- Missing gender column → Log warning, skip
- Invalid dates → Convert to None, log warning
- Missing output columns → Log and use available

### Phase 4: Load
**What happens:**
- Save to CSV file
- Verify output file created
- Log file path and statistics

**Error handling:**
- Write permission denied → Log error
- Invalid filename → Use default name
- Disk full → Attempt cleanup and retry

## Configuration

### Transformation Config Options

```python
config = {
    # Columns to format as dates (YYYY-MM-DD)
    'date_columns': ['date_of_birth', 'hire_date'],
    
    # Remove duplicate rows
    'remove_duplicates': True,
    
    # Fill missing values
    'fill_missing_values': {
        'gender': 'Unknown',
        'status': 'unknown',
        'department': 'Unassigned'
    },
    
    # Final output columns (in order)
    'final_columns': [
        'employee_id',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'salary'
    ]
}
```

## Gender Normalization Examples

| Input | Output | Notes |
|-------|--------|-------|
| 'm' | M | Lowercase m |
| 'M' | M | Uppercase M |
| 'mm' | M | Double m |
| 'male' | M | Full word |
| 'MALE' | M | Case insensitive |
| 'f' | F | Lowercase f |
| 'F' | F | Uppercase F |
| 'ff' | F | Double f |
| 'female' | F | Full word |
| '0' | Unknown | Zero value |
| None | Unknown | Null/empty |
| 'other' | Unknown | Invalid values |

## Date Formatting Examples

| Input | Output | Status |
|-------|--------|--------|
| '2023-01-15' | 2023-01-15 | ✓ Already correct |
| '01/15/2023' | 2023-01-15 | ✓ Converted |
| '15-01-2023' | 2023-01-15 | ✓ Converted |
| '2023/01/15' | 2023-01-15 | ✓ Converted |
| 'invalid' | None | ⚠ Logged |
| None | None | ✓ Remains null |

## Running Examples

### Example 1: Standard Run
```bash
python run_robust_pipeline.py
```

Output:
```
===============================================================================
                    ROBUST FOUR-SOURCE ETL PIPELINE
            With Error Handling & Auto-Rectification
===============================================================================

📁 Registering Source 1: dataset_1.csv
📁 Registering Source 2: dataset_2.csv
...

===============================================================================
PIPELINE CONFIGURATION
===============================================================================
✓ Sources: 4 files
✓ Output Columns: 6
✓ Date Formatting: YYYY-MM-DD
✓ Gender Normalization: M/F/Unknown
✓ Error Handling: Enabled with auto-rectification
✓ Error Logging: Enabled (error_log.json)
===============================================================================

[Processing...]

================================================================================
✓✓✓ PIPELINE EXECUTION SUCCESSFUL ✓✓✓
================================================================================
```

### Example 2: With Missing File

If `dataset_1.csv` doesn't exist:
```
[Extract & Map Phase]
✓ source_1_abbreviated: File not found - Skipping
✓ source_2_standard: Extracted successfully
✓ source_3_mixed: Extracted successfully
✓ source_4_sample: Extracted successfully

✓ Successfully processed: 3 sources
⚠ Failed sources: ['source_1_abbreviated']

[Consolidation Phase]
✓ Consolidated 3 sources into 40 rows
```

### Example 3: Check Error Log

```bash
# View full error report
cat output/error_log.json | python -m json.tool

# View only errors
cat output/error_log.json | python -c "import json, sys; d=json.load(sys.stdin); [print(f\"[{e['stage']}] {e['error']}\") for e in d['errors']]"
```

## Troubleshooting

### Issue: File not found
**Solution:**
- Check file exists in `data/` folder
- Verify filename matches exactly (case-sensitive on Linux)
- Check file permissions

### Issue: Missing columns error
**Solution:**
- Pipeline automatically handles this
- Check `error_log.json` for details
- Verify column mapping is correct

### Issue: Data type conversion failed
**Solution:**
- Check input data format
- Dates should be recognizable format
- Salary fields should be numeric (or convertible)

### Issue: All sources failed
**Solution:**
- Check all input files exist
- Verify files are valid CSV/Excel
- Check file encoding (should be UTF-8)
- Review error_log.json for details

## Performance Notes

- **Small datasets (< 10K rows)**: < 1 second
- **Medium datasets (10K-100K rows)**: 1-5 seconds
- **Large datasets (> 100K rows)**: 5-30 seconds

Performance depends on:
- File I/O speed
- Number of transformations
- Data validation checks
- System resources

## Best Practices

1. **Always check error_log.json** after running
2. **Validate input files** before running pipeline
3. **Document column mappings** for each source
4. **Use consistent naming** in configuration
5. **Monitor error counts** for data quality issues
6. **Keep backup** of original input files
7. **Review correction logs** to understand auto-fixes
8. **Test incrementally** with small datasets first

## Files Generated

After successful pipeline execution:

```
output/
├── consolidated_all_sources_robust.csv    ← Main output (6 columns)
├── error_log.json                         ← Error/warning/correction log
└── [other outputs]
```

## Next Steps

1. Review the CSV output: `consolidated_all_sources_robust.csv`
2. Check error log: `error_log.json`
3. Validate data quality
4. Load into database or BI tool
5. Monitor for any data quality issues

---

**Ready to run?**
```bash
python run_robust_pipeline.py
```
