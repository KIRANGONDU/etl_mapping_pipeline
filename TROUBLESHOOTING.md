# 🔧 Troubleshooting Guide

## Common Issues & Solutions

### ❌ Issue 1: Import Errors in VS Code

**Error Message:**
```
Import "snowflake.connector" could not be resolved
Import "snowflake.connector.pandas_tools" could not be resolved
```

**Status:** ✅ **FIXED** - These are harmless Pylance warnings

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Why it happens:**
- Snowflake connector not yet installed
- VS Code's intellisense can't find the package
- **Code handles this gracefully** with try-except

**After installing:**
- Warnings disappear ✅
- Snowflake connector available ✅
- Pipeline fully functional ✅

---

### ❌ Issue 2: "ModuleNotFoundError: No module named 'pandas'"

**Error Message:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
```bash
pip install pandas numpy openpyxl pyyaml snowflake-connector-python
```

Or:
```bash
pip install -r requirements.txt
```

---

### ❌ Issue 3: "ModuleNotFoundError: No module named 'snowflake'"

**Error Message:**
```
ModuleNotFoundError: No module named 'snowflake'
```

**Solution:**
```bash
pip install snowflake-connector-python
```

**Note:** The pipeline can still work without this - it will:
- Process data into CSV ✅
- Skip Snowflake upload
- Show helpful message

---

### ❌ Issue 4: Virtual Environment Not Activated

**Error Message:**
```
Python not found or module import errors vary
```

**Solution:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Then run
python complete_pipeline.py
```

**Verify:** Look for `(venv)` in your terminal prompt

---

### ❌ Issue 5: Snowflake Connection Failed

**Error Message:**
```
Failed to connect to Snowflake: Invalid credentials or account not found
```

**Solutions:**

1. **Check credentials in snowflake_config.json:**
```json
{
  "account": "YOUR_ACCOUNT_ID.us-east-1",
  "user": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "warehouse": "COMPUTE_WH",
  "role": "SYSADMIN"
}
```

2. **Verify account ID format:**
   - Should be: `xy12345.us-east-1`
   - NOT: `xy12345` (missing region)

3. **Test Snowflake access:**
   - Log into https://app.snowflake.com
   - Verify username/password works
   - Confirm account exists

4. **Check network:**
   - Verify internet connection
   - Check firewall settings
   - Try from different network if needed

---

### ❌ Issue 6: "TypeError: 'NoneType' object is not callable"

**Error Message:**
```
TypeError: 'NoneType' object is not callable
```

**Cause:** Snowflake not installed but code tried to use it

**Solution:**
```bash
pip install snowflake-connector-python
```

---

### ❌ Issue 7: No Output Files Generated

**Symptom:** `output/` folder is empty

**Possible Causes:**
1. Input data files missing or empty
2. Transformation errors (check error_log.txt)
3. Permissions issue with output folder

**Solutions:**

1. **Verify input files exist:**
```bash
ls data/
# Should show: dataset_1.csv, dataset_2.csv, input_data.csv, sample_employee_data.csv
```

2. **Check error log:**
```bash
type output\error_log.txt
```

3. **Check permissions:**
```bash
# Ensure you can write to output/
# Try creating a test file
echo test > output\test.txt
```

---

### ❌ Issue 8: Data Not Uploaded to Snowflake

**Symptom:** CSV created but Snowflake table empty

**Check:**
1. `output/snowflake_upload_report.txt` - Check status
2. `output/error_log.txt` - Check for errors
3. Snowflake console - Verify database/schema/table exists

**Solutions:**

1. **Check upload report:**
```bash
type output\snowflake_upload_report.txt
```

2. **Check error log:**
```bash
type output\error_log.txt
```

3. **Verify in Snowflake:**
```sql
SELECT COUNT(*) FROM ETL_DATA.EMPLOYEES.CONSOLIDATED_EMPLOYEES;
```

4. **Check Snowflake permissions:**
```sql
-- As ACCOUNTADMIN:
GRANT ALL PRIVILEGES ON DATABASE ETL_DATA TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON SCHEMA ETL_DATA.EMPLOYEES TO ROLE SYSADMIN;
```

---

### ❌ Issue 9: "ExecutionPolicy" Error (Windows Only)

**Error Message:**
```
File cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

Then activate venv:
```powershell
.\venv\Scripts\Activate.ps1
```

---

### ❌ Issue 10: "Cannot find Python"

**Error Message:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

1. **Verify Python installed:**
```bash
python --version
```

2. **Check PATH environment variable:**
   - Windows: Settings → Environment Variables
   - Add Python installation directory

3. **Use full path:**
```bash
C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe complete_pipeline.py
```

4. **Reinstall Python:**
   - Download from python.org
   - Check "Add Python to PATH" during installation

---

## 🔍 Diagnostics

### Run Diagnostic Check

```bash
# Check Python version
python --version

# Check pip
pip --version

# Check installed packages
pip list

# Check if pandas installed
python -c "import pandas; print(pandas.__version__)"

# Check if snowflake available
python -c "import snowflake.connector; print('Snowflake OK')"
```

---

## 📝 Getting Help

### When Creating Issue Report, Include:

1. **Python version:** `python --version`
2. **Error message:** Full error output
3. **Command used:** What you ran
4. **Error log:** `output/error_log.txt`
5. **Upload report:** `output/snowflake_upload_report.txt`
6. **Snowflake status:** Can you connect to Snowflake UI?

---

## ✅ Verification Checklist

Before running pipeline:

- [ ] Python 3.7+ installed
- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Input files exist: `data/*.csv`
- [ ] Credentials configured: `snowflake_config.json`
- [ ] Output directory writable: `output/`

---

## 🚀 If All Else Fails

1. **Clean install:**
```bash
# Delete virtual environment
rmdir /s venv

# Create new one
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

2. **Run with verbose output:**
```bash
python -u complete_pipeline.py 2>&1 | tee output\debug.log
```

3. **Check logs:**
```bash
type output\error_log.txt
type output\debug.log
```

---

## 📞 Support

- **Documentation:** See README_FIRST.txt
- **Quick Start:** See QUICKSTART.md
- **Error Details:** Check output/error_log.txt
- **Upload Status:** Check output/snowflake_upload_report.txt

---

**Most issues are resolved by running:**
```bash
pip install -r requirements.txt
```

**Good luck!** 🚀
