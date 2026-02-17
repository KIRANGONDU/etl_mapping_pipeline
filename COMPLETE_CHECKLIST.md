# Complete ETL Pipeline Setup Checklist

## ✅ Pre-Setup Checklist

- [ ] You have Python 3.7+ installed
- [ ] You have pip package manager
- [ ] You have a Snowflake account
- [ ] You know your Snowflake account ID
- [ ] You know your Snowflake username
- [ ] You know your Snowflake password
- [ ] You have internet connection

---

## 🔧 Installation Checklist

- [ ] Extract pipeline files to: `c:\Users\srinu\OneDrive\Documents\ppt\etl_pipeline\`
- [ ] Virtual environment is activated: `(venv) PS ...`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Verified pandas installed: `python -c "import pandas; print(pandas.__version__)"`
- [ ] Verified snowflake connector: `python -c "import snowflake.connector; print('OK')"`

---

## ⚙️ Configuration Checklist

- [ ] Opened `snowflake_config.json`
- [ ] Found your Snowflake account ID (format: xy12345.us-east-1)
- [ ] Found your Snowflake username
- [ ] Found your Snowflake password
- [ ] Verified your warehouse name (usually COMPUTE_WH)
- [ ] Edited account: `"account": "YOUR_ACCOUNT_ID.us-east-1"`
- [ ] Edited user: `"user": "YOUR_USERNAME"`
- [ ] Edited password: `"password": "YOUR_PASSWORD"`
- [ ] Edited warehouse: `"warehouse": "COMPUTE_WH"`
- [ ] Saved the file (Ctrl+S)

---

## 📂 Data Checklist

- [ ] Verified input files exist:
  - [ ] `data/dataset_1.csv`
  - [ ] `data/dataset_2.csv`
  - [ ] `data/input_data.csv`
  - [ ] `data/sample_employee_data.csv`
- [ ] Verified `output/` directory exists (created automatically)
- [ ] Checked that input files have data (not empty)

---

## 🚀 Execution Checklist

- [ ] Opened terminal/PowerShell
- [ ] Navigated to: `cd c:\Users\srinu\OneDrive\Documents\ppt\etl_pipeline`
- [ ] Virtual environment activated: `(venv)` visible in prompt
- [ ] Ran command: `python complete_pipeline.py`
- [ ] Saw "EXTRACTION & TRANSFORMATION" section
- [ ] Saw "UPLOADING TO SNOWFLAKE" section
- [ ] Saw "PIPELINE EXECUTION COMPLETE!" message
- [ ] Did NOT see Python errors
- [ ] Pipeline completed with exit code 0

---

## 📊 Output Verification Checklist

- [ ] File exists: `output/consolidated_employees.csv`
- [ ] File size > 0 (not empty)
- [ ] File opened successfully
- [ ] CSV has 6 columns:
  - [ ] employee_id
  - [ ] first_name
  - [ ] last_name
  - [ ] gender
  - [ ] date_of_birth
  - [ ] salary
- [ ] CSV has ~40 rows (data)
- [ ] Gender values are: M, F, or Unknown (no other values)
- [ ] Dates are YYYY-MM-DD format

---

## 📝 Log Verification Checklist

- [ ] File exists: `output/error_log.txt`
- [ ] Reviewed error messages (if any)
- [ ] No CRITICAL errors (warnings are OK)
- [ ] File exists: `output/snowflake_upload_report.txt`
- [ ] Upload report shows: "Status: SUCCESS"
- [ ] Upload report shows: "Rows: 40"
- [ ] Upload report shows: "Columns: 6"

---

## ❄️ Snowflake Verification Checklist

- [ ] Logged into Snowflake Web Console (app.snowflake.com)
- [ ] Selected correct account
- [ ] Database `ETL_DATA` exists (left panel)
- [ ] Schema `EMPLOYEES` exists under `ETL_DATA`
- [ ] Table `CONSOLIDATED_EMPLOYEES` exists under schema
- [ ] Can see table columns in schema browser

---

## 🔍 Data Verification Checklist

Run these queries in Snowflake SQL Editor:

**Query 1: Row Count**
```sql
SELECT COUNT(*) as row_count FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES;
```
- [ ] Returns: 40

**Query 2: Column Names**
```sql
SELECT * FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES LIMIT 1;
```
- [ ] Shows 6 columns (listed above)

**Query 3: Gender Values**
```sql
SELECT DISTINCT GENDER FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES;
```
- [ ] Returns only: M, F, Unknown

**Query 4: Date Format**
```sql
SELECT DATE_OF_BIRTH FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES LIMIT 5;
```
- [ ] All dates in YYYY-MM-DD format

**Query 5: No Nulls in Key Columns**
```sql
SELECT COUNT(*) FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES 
WHERE EMPLOYEE_ID IS NULL OR FIRST_NAME IS NULL OR LAST_NAME IS NULL;
```
- [ ] Returns: 0 (no nulls)

---

## 🎯 Success Confirmation

- [ ] All data successfully processed
- [ ] All 40 rows consolidated
- [ ] All 6 columns present
- [ ] All transformations applied
- [ ] Data uploaded to Snowflake
- [ ] Queries return expected results
- [ ] No critical errors

---

## 🔄 Next Steps (After Success)

- [ ] Schedule pipeline to run daily/weekly (optional)
- [ ] Set up automated alerts (optional)
- [ ] Build analytics queries (optional)
- [ ] Create Snowflake dashboards (optional)
- [ ] Document custom changes (if any)

---

## 🆘 Troubleshooting Checklist

If something failed:

**Pipeline won't start:**
- [ ] Check `snowflake_config.json` syntax (valid JSON)
- [ ] Check file exists: `complete_pipeline.py`
- [ ] Try: `python --version` (verify Python works)

**Connection failed:**
- [ ] Check account ID format: `xy12345.us-east-1`
- [ ] Check username is correct
- [ ] Check password is correct (no special chars issues)
- [ ] Check warehouse exists: `COMPUTE_WH`
- [ ] Test connection in Snowflake UI

**Data not uploaded:**
- [ ] Check `output/error_log.txt` for details
- [ ] Check input files exist and have data
- [ ] Verify column mapping in code
- [ ] Check Snowflake permissions

**Wrong data in output:**
- [ ] Verify input file headers match code expectations
- [ ] Check gender normalization rules
- [ ] Check date format settings
- [ ] Review error log for warnings

---

## 📚 Documentation Reference

If you need help with:

| Topic | Read |
|-------|------|
| Quick setup | QUICKSTART.md |
| What you have | 00_START_HERE.md |
| Complete solution | SOLUTION_SUMMARY.md |
| Architecture | ARCHITECTURE.md |
| Snowflake setup | SNOWFLAKE_GUIDE.md |
| Finding docs | INDEX.md |

---

## 💾 Save This Checklist

- [ ] Printed or bookmarked this file
- [ ] Know where to find it: `COMPLETE_CHECKLIST.md`
- [ ] Have this handy for future runs

---

## ✅ Final Sign-Off

**Date:** ________________  
**Completed By:** ________________  
**Status:** ☐ SUCCESS ☐ PARTIAL ☐ FAILED  

**Notes:**
```
_____________________________________________
_____________________________________________
_____________________________________________
```

---

**Congratulations! Your pipeline is ready! 🎉**

If everything is checked above, you're all set to use the ETL pipeline!

Next time you need to run:
1. Activate venv: `.\venv\Scripts\Activate.ps1`
2. Run pipeline: `python complete_pipeline.py`
3. Check results in Snowflake

**Questions?** See [INDEX.md](INDEX.md) for documentation roadmap.
