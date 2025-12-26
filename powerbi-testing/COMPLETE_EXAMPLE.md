# Power BI Testing Framework - Complete Example

This example demonstrates a complete workflow for testing Power BI transformations.

## Scenario

You have a sales data file (`sales_data.xlsx`) and you've created several transformations in Power BI:
1. Filtered out orders with amount < $50
2. Added calculated columns (UnitPrice, Year, Month, Quarter)
3. Removed duplicate customer records
4. Standardized date formats

## Step 1: Set Up Your Testing Environment

### Install Python Dependencies
```bash
cd powerbi-testing
pip install -r requirements.txt
```

## Step 2: Export Your Power BI Data

### In Power BI Desktop:
1. Create a table visual with all columns from your transformed table
2. Click the "..." menu on the visual
3. Select "Export data"
4. Choose "CSV" format
5. Save as `sales_transformed.csv`

## Step 3: Create Your Test Configuration

Create a file `sales_test_config.json`:

```json
{
  "description": "Validation tests for sales data transformation",
  "source_sheet": "Sales Data",
  
  "expected_row_count": 950,
  
  "expected_columns": [
    "CustomerID",
    "CustomerName",
    "OrderDate",
    "TotalAmount",
    "ProductCategory",
    "Quantity",
    "UnitPrice",
    "Year",
    "Month",
    "Quarter"
  ],
  
  "aggregate_tests": [
    {
      "column": "TotalAmount",
      "operation": "sum",
      "tolerance": 0.01,
      "comment": "Total sales should match within 1 cent"
    },
    {
      "column": "Quantity",
      "operation": "sum",
      "tolerance": 0,
      "comment": "Total units sold must match exactly"
    },
    {
      "column": "TotalAmount",
      "operation": "mean",
      "tolerance": 0.01,
      "comment": "Average order value"
    }
  ],
  
  "sample_tests": [
    {
      "column": "CustomerName",
      "row_index": 0,
      "expected_value": "Acme Corporation",
      "comment": "First customer name should be Acme"
    },
    {
      "column": "Year",
      "row_index": 0,
      "expected_value": "2024",
      "comment": "Year column should be extracted correctly"
    }
  ]
}
```

## Step 4: Run Automated Validation

```bash
python validate_powerbi_data.py \
  --source sales_data.xlsx \
  --export sales_transformed.csv \
  --config sales_test_config.json
```

### Expected Output:
```
============================================================
🚀 Power BI Data Validation
============================================================
📂 Loading source file: sales_data.xlsx
✅ Loaded 1000 rows, 6 columns from source
📂 Loading Power BI export: sales_transformed.csv
✅ Loaded 950 rows, 10 columns from export

✅ PASS - Row Count Validation
  Expected: 950, Got: 950

✅ PASS - Column Count Validation
  Source: 6, Export: 10

✅ PASS - Column Existence Validation
  All 10 expected columns found

📊 Data Type Validation for 6 common columns
✅ PASS - Data Types

🔍 Null Count Validation
✅ Null counts match for all common columns

🧮 Aggregate Validation
  ✅ PASS sum(TotalAmount): 145678.90 → 145678.90 (diff: 0.00)
  ✅ PASS sum(Quantity): 5234.00 → 5234.00 (diff: 0.00)
  ✅ PASS mean(TotalAmount): 145.68 → 153.35 (diff: 7.67)

🔬 Sample Value Validation
  ✅ PASS CustomerName[0]: expected 'Acme Corporation', got 'Acme Corporation'
  ✅ PASS Year[0]: expected '2024', got '2024'

============================================================
📊 Validation Summary
============================================================
Tests Passed: 7/7
  ✅ Row Count
  ✅ Column Count
  ✅ Column Existence
  ✅ Data Types
  ✅ Null Counts
  ✅ Aggregates
  ✅ Sample Values

🎉 All validations passed!
============================================================
```

## Step 5: Add M Code Validation Queries in Power BI

### In Power BI Desktop:

1. Open Power Query Editor (Transform Data)
2. Click "New Source" > "Blank Query"
3. Click "Advanced Editor"
4. Paste this validation code:

```m
// Validation Query: Row Count Check
let
    Source = #"Sales Data",
    Transformed = #"Sales Transformed",
    SourceCount = Table.RowCount(Source),
    TransformedCount = Table.RowCount(Transformed),
    ExpectedFiltered = 50,  // We filtered out 50 rows
    
    ValidationResult = if SourceCount - TransformedCount = ExpectedFiltered
                       then "✅ PASS: Filtered 50 rows as expected"
                       else "❌ FAIL: Expected to filter 50 rows, actually filtered " & 
                            Number.ToText(SourceCount - TransformedCount),
    
    ResultTable = #table(
        {"Test", "SourceRows", "TransformedRows", "FilteredRows", "Status"},
        {{"Row Count Validation", SourceCount, TransformedCount, 
          SourceCount - TransformedCount, ValidationResult}}
    )
in
    ResultTable
```

5. Rename the query to "Validation_RowCount"
6. Right-click and UNCHECK "Enable Load"
7. Repeat for other validation types

### Additional M Code Validations:

#### Sum Validation
```m
let
    Source = #"Sales Data",
    Transformed = #"Sales Transformed",
    
    SourceSum = List.Sum(Table.Column(Source, "TotalAmount")),
    TransformedSum = List.Sum(Table.Column(Transformed, "TotalAmount")),
    
    // Allow for small rounding differences
    Difference = Number.Abs(SourceSum - TransformedSum),
    Tolerance = 0.01,
    
    ValidationResult = if Difference <= Tolerance
                       then "✅ PASS: Sums match within tolerance"
                       else "❌ FAIL: Sum difference of " & Number.ToText(Difference),
    
    Result = #table(
        {"Test", "SourceSum", "TransformedSum", "Difference", "Status"},
        {{"Sum Validation", SourceSum, TransformedSum, Difference, ValidationResult}}
    )
in
    Result
```

#### Calculated Column Validation
```m
let
    Transformed = #"Sales Transformed",
    
    // Check a few sample calculations
    Samples = Table.FirstN(Transformed, 10),
    
    // Verify UnitPrice = TotalAmount / Quantity
    ValidationResults = Table.AddColumn(
        Samples,
        "UnitPriceValid",
        each Number.Abs([UnitPrice] - ([TotalAmount] / [Quantity])) < 0.01
    ),
    
    FailedCalculations = Table.SelectRows(
        ValidationResults,
        each [UnitPriceValid] = false
    ),
    
    FailCount = Table.RowCount(FailedCalculations),
    
    ValidationStatus = if FailCount = 0
                       then "✅ PASS: All UnitPrice calculations correct"
                       else "❌ FAIL: " & Number.ToText(FailCount) & " incorrect calculations",
    
    Result = #table(
        {"Test", "SamplesTested", "FailedCalculations", "Status"},
        {{"Calculated Column Validation", 10, FailCount, ValidationStatus}}
    )
in
    Result
```

## Step 6: Manual Verification Checklist

Use `TESTING_CHECKLIST.md` and verify:

- [ ] Source file has 1000 rows
- [ ] Transformed table has 950 rows (50 filtered out)
- [ ] All 10 expected columns exist
- [ ] No unexpected null values in critical columns
- [ ] UnitPrice = TotalAmount / Quantity (spot check)
- [ ] Year/Month/Quarter extracted correctly from OrderDate
- [ ] No duplicate CustomerIDs
- [ ] Total sales amount matches (within rounding)

## Step 7: Document Your Results

Create a test results document:

```markdown
# Sales Data Transformation - Test Results
Date: 2024-01-15
Tester: Muneeb

## Test Summary
- ✅ All automated tests passed
- ✅ Manual validation completed
- ✅ M code validation queries added

## Key Findings
- Source: 1,000 rows → Transformed: 950 rows
- 50 rows filtered (TotalAmount < $50) as expected
- 4 calculated columns added successfully
- All aggregates match source data
- No data quality issues found

## Transformations Validated
1. ✅ Filter: Remove orders < $50 (50 rows removed)
2. ✅ Calculated: UnitPrice = TotalAmount / Quantity
3. ✅ Calculated: Year from OrderDate
4. ✅ Calculated: Month from OrderDate  
5. ✅ Calculated: Quarter from OrderDate

## Next Steps
- Deploy to production
- Schedule weekly validation runs
- Monitor data quality metrics
```

## Tips for Success

1. **Run validation after each major change**
   - Don't wait until the end of development
   - Catch issues early

2. **Keep test config in version control**
   - Track changes to expected values
   - Document why thresholds changed

3. **Automate regular testing**
   - Set up a weekly validation schedule
   - Export fresh data from Power BI
   - Run validation script
   - Review results

4. **Combine multiple validation methods**
   - Automated Python validation (comprehensive)
   - M code queries (during development)
   - Manual spot checks (final verification)

5. **Document exceptions**
   - Not all "failures" are real issues
   - Some differences may be expected
   - Document the business reason

## Troubleshooting

### Problem: Aggregate sums don't match
**Possible causes:**
- Filter removed some rows (expected)
- Calculation error in Power BI
- Data type conversion issue
- Null values not handled correctly

**Solution:**
- Review filter steps in Power Query
- Check transformation logic
- Verify null handling

### Problem: Row count is different
**Possible causes:**
- Intentional filtering
- Duplicate removal
- Join operation
- Data refresh timing

**Solution:**
- Review all filter steps
- Check join types (Inner vs Left)
- Document expected row count in config

### Problem: Data types don't match
**Possible causes:**
- CSV export converts dates to strings
- Number precision changes
- Implicit type conversions

**Solution:**
- This is often expected with CSV exports
- Use Excel export instead of CSV for testing
- Adjust tolerance in validation
