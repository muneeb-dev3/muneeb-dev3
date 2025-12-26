# Quick Start Guide: Testing Power BI Transformations

## What is this?
This toolkit helps you validate that your Power BI M code transformations are working correctly - similar to how developers write test cases for their code.

## Why do I need this?
When you create tables in Power BI using M code, you need to ensure:
- ✅ Data is transformed correctly
- ✅ No data is lost unexpectedly  
- ✅ Calculations are accurate
- ✅ Business rules are applied properly

## Quick Start (3 Methods)

### Method 1: Manual Testing (Easiest - Start Here!)

**Step 1: Open Power Query Editor**
1. In Power BI Desktop, click "Transform Data" button
2. You'll see all your queries and transformation steps

**Step 2: Enable Data Profiling**
1. Click the "View" tab
2. Check these boxes:
   - ✅ Column Quality
   - ✅ Column Distribution
   - ✅ Column Profile
3. These show data quality metrics for each column

**Step 3: Check Your Transformations**
1. Click on any query on the left
2. Look at "Applied Steps" on the right
3. Click each step to see what happens to your data
4. Compare the row count at bottom with your source file

**Step 4: Spot Check Values**
1. Open your source Excel file
2. Pick 5-10 random rows
3. Find those same rows in Power BI
4. Verify the values match after transformation

---

### Method 2: M Code Validation (Built into Power BI)

**Step 1: Add a Validation Query**
1. In Power Query Editor, click "New Source" > "Blank Query"
2. Click "Advanced Editor"
3. Copy one of the validation examples from `m_code_validation_examples.m`
4. Replace the table names with your actual table names
5. Click "OK"

**Step 2: Configure the Query**
1. Rename it to "Validation_RowCount" (or similar)
2. Right-click the query
3. UNCHECK "Enable Load" (important - don't load this to your model)

**Step 3: Check Results**
1. Click on the validation query
2. See if it shows "PASS" or "FAIL"
3. Fix issues if needed

**Repeat for other validations:**
- Row count matching
- Column existence
- Null value checks
- Sum comparisons

---

### Method 3: Python Automation (Most Thorough)

**Step 1: Export Your Power BI Data**
1. In Power BI Desktop, create a simple table visual with your data
2. Click the "..." menu on the visual
3. Select "Export data"
4. Save as CSV file (e.g., `powerbi_export.csv`)

**Step 2: Install Python Tools**
```bash
pip install pandas openpyxl
```

**Step 3: Run Validation**
```bash
python validate_powerbi_data.py --source your_source.xlsx --export powerbi_export.csv
```

**Step 4: Review Results**
The script will check:
- ✅ Row counts match
- ✅ Column counts match
- ✅ Data types are correct
- ✅ No unexpected nulls
- ✅ Sums/aggregates match

**Step 5: Use Config for Advanced Testing**
1. Copy `test_config_example.json`
2. Rename to `test_config.json`
3. Edit it with your specific column names and expected values
4. Run: `python validate_powerbi_data.py --source source.xlsx --export export.csv --config test_config.json`

---

## Common Validation Checks

### ✅ Row Count
**Question:** Do I have the right number of rows?
- Check source file row count
- Compare with Power BI row count (bottom of data view)
- If different, trace through your filters/joins

### ✅ Column Count
**Question:** Do I have all expected columns?
- List out what columns you expect
- Verify they all exist in Power BI
- Check for typos in column names

### ✅ Null Values
**Question:** Are there unexpected blank/null values?
- Use Column Quality feature (shows % valid/error/empty)
- Check critical columns shouldn't have nulls
- Investigate why nulls appeared

### ✅ Data Types
**Question:** Are data types correct?
- Numbers should be whole number or decimal
- Dates should be date/datetime
- Text should be text
- Check the column headers for data type icon

### ✅ Sums/Aggregates
**Question:** Do my totals match the source?
- Calculate sum in Excel source file
- Calculate sum in Power BI
- Compare - should match!

### ✅ Sample Values
**Question:** Do specific values look right?
- Pick a few specific cells from source
- Find them in Power BI
- Verify they transformed correctly

---

## Example Workflow

Here's how to validate a typical Power BI project:

**Scenario:** You imported sales data from Excel and created multiple tables

1. **Before starting:** Note your source file has 1,000 rows, 8 columns

2. **After each transformation:**
   - Click the step in Power Query
   - Check row count (bottom of screen)
   - If you filtered data, verify expected rows removed
   - If you added columns, verify new columns appear

3. **Add M code validation queries:**
   - Row count check (should be 1,000 if no filters)
   - Column count check (8+ if you added calculated columns)
   - Null check for CustomerID (should be 0 nulls)
   - Sum check for TotalSales (compare with Excel)

4. **Export and run Python validation:**
   - Export your main table to CSV
   - Run the Python script
   - Review any failures
   - Fix issues in Power Query
   - Re-export and validate again

5. **Document results:**
   - Use the testing checklist
   - Note any expected differences
   - Save validation outputs

---

## Troubleshooting

**Problem: Row counts don't match**
- Solution: Check your filters - did you remove rows intentionally?
- Look for joins that might exclude rows
- Check for duplicates that were removed

**Problem: Column is missing**
- Solution: Check spelling of column name
- Verify you didn't delete it in a step
- Check if it was renamed

**Problem: Sums don't match**
- Solution: Check for nulls (they don't add up)
- Verify data types are numeric
- Check for rounding differences

**Problem: Python script fails**
- Solution: Make sure pandas is installed: `pip install pandas openpyxl`
- Check file paths are correct
- Verify files exist and are readable

---

## Next Steps

1. ✅ Read through the main README.md for detailed information
2. ✅ Use TESTING_CHECKLIST.md when validating your project
3. ✅ Copy M code examples from m_code_validation_examples.m
4. ✅ Try the Python validation script on a small test dataset first
5. ✅ Set up regular validation schedule (e.g., weekly)

---

## Need Help?

Common files in this toolkit:
- `README.md` - Detailed documentation
- `QUICK_START.md` - This file!
- `TESTING_CHECKLIST.md` - Step-by-step checklist
- `validate_powerbi_data.py` - Python validation script
- `test_config_example.json` - Example configuration
- `m_code_validation_examples.m` - M code examples

Start with Method 1 (Manual Testing) if you're new to this!
