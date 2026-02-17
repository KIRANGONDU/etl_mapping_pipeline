# Quick Start: Complete ETL + Snowflake Pipeline

## 📋 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Snowflake Credentials

Get from your Snowflake account:
- Account ID (e.g., `xy12345.us-east-1`)
- Username
- Password
- Warehouse name (usually `COMPUTE_WH`)

### 3. Edit Configuration

Edit `snowflake_config.json`:

```json
{
  "account": "YOUR_ACCOUNT_ID",
  "user": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "warehouse": "COMPUTE_WH",
  "role": "SYSADMIN"
}
```

### 4. Run Pipeline

```bash
python complete_pipeline.py
```

That's it! ✅

## 📊 What Happens

```
Your 4 Input Files
    ↓
Automatic Header Mapping
    ↓
Data Transformation & Validation
    ↓
Error Detection & Auto-Rectification
    ↓
Snowflake Upload
    • Creates ETL_DATA database
    • Creates EMPLOYEES schema
    • Creates CONSOLIDATED_EMPLOYEES table
    • Uploads 6-column consolidated data
    ↓
Professional Data Warehouse Ready!
```

## 📁 Output Files

After running:
```
output/
├── consolidated_employees.csv          (6 columns, 20 rows)
├── snowflake_upload_report.txt        (Upload details)
└── error_log.txt                      (If errors occurred)
```

## 🔍 Access Your Data

### In Snowflake Web Console

1. Log in to Snowflake
2. Navigate to `ETL_DATA` database
3. Select `EMPLOYEES` schema
4. View `CONSOLIDATED_EMPLOYEES` table

### Via SQL Query

```sql
SELECT * FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES;
```

## 🎯 Sample Results

| Employee_ID | First_Name | Last_Name | Gender | Date_of_Birth | Salary |
|-------------|-----------|-----------|--------|---------------|--------|
| 101 | John | Doe | M | 1990-01-15 | 50000 |
| 102 | Jane | Smith | F | 1992-03-22 | 65000 |
| ... | ... | ... | ... | ... | ... |

## ⚙️ Features

✅ Handles 4 input files with different column names
✅ Automatic header mapping
✅ Data validation and error handling
✅ Automatic rectification of common errors
✅ Gender normalization (M/F/Unknown)
✅ Date formatting (YYYY-MM-DD)
✅ Automatic Snowflake setup
✅ Professional database structure
✅ Upload verification
✅ Detailed error logging

## 🚀 Advanced Usage

### Modify Output Columns

Edit `complete_pipeline.py`, change `final_columns`:

```python
'final_columns': [
    'employee_id',
    'first_name',
    'last_name',
    'gender',
    'date_of_birth',
    'salary',
    'department',      # Add more columns
    'age'
]
```

### Change Database/Schema Name

Edit `complete_pipeline.py`:

```python
database_name = 'YOUR_DATABASE_NAME'
schema_name = 'YOUR_SCHEMA_NAME'
```

### Add More Input Files

In `complete_pipeline.py`, add to `sources` dict:

```python
'your_file.csv': {
    'old_column_name': 'new_column_name',
    # ... mapping
}
```

## ❓ Troubleshooting

**Q: "Module snowflake.connector not found"**
```bash
pip install snowflake-connector-python
```

**Q: "Authentication failed"**
- Check account ID format: `xy12345.us-east-1`
- Verify username/password
- Ensure account exists

**Q: Where's my data in Snowflake?**
```sql
SELECT * FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES;
```

**Q: How do I view transformation errors?**
```bash
type output\error_log.txt
```

## 📞 Need Help?

1. Check `SNOWFLAKE_GUIDE.md` for detailed documentation
2. Review `output/error_log.txt` for specific errors
3. Check `output/snowflake_upload_report.txt` for upload details

---

**Congratulations! Your ETL + Snowflake pipeline is ready! 🎉**
