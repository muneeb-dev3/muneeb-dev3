# Power BI Testing Checklist

Use this checklist when validating your Power BI project:

## Pre-Testing Setup
- [ ] Export M code from all queries to text files for version control
- [ ] Document expected row counts for each transformation
- [ ] Identify key columns that should not have nulls
- [ ] Document business rules and transformation logic
- [ ] Create test configuration file with expected values

## Manual Testing in Power BI Desktop

### Data Profiling
- [ ] Open Power Query Editor (Transform Data)
- [ ] Enable View > Column Quality
- [ ] Enable View > Column Distribution  
- [ ] Enable View > Column Profile
- [ ] Check for unexpected nulls, errors, or data quality issues

### Step-by-Step Validation
- [ ] Review each query in Power Query Editor
- [ ] Click through each transformation step
- [ ] Verify row counts at each step match expectations
- [ ] Check sample values look correct
- [ ] Verify data types are correct

### Source Comparison
- [ ] Compare total row count: Source vs Final
- [ ] Compare column count: Source vs Final
- [ ] Spot check 5-10 random rows
- [ ] Compare key aggregates (sums, counts, averages)
- [ ] Verify date ranges are within expected bounds

## Automated Testing

### Python Validation Script
- [ ] Export Power BI table to CSV (Data > Export data from visual)
- [ ] Install Python dependencies: `pip install pandas openpyxl`
- [ ] Run validation script with source and export files
- [ ] Review validation results
- [ ] Fix any issues identified
- [ ] Re-run validation until all tests pass

### M Code Validation Queries
- [ ] Add row count validation query
- [ ] Add column validation query
- [ ] Add null value check query
- [ ] Add sum validation query
- [ ] Add duplicate check query
- [ ] Add data type validation query
- [ ] Set all validation queries to "Enable Load = false"
- [ ] Review validation query results in Power Query Editor

## Transformation-Specific Checks

### For Filters
- [ ] Verify expected number of rows removed
- [ ] Check that filter criteria are correct
- [ ] Ensure no unintended data loss

### For Joins/Merges
- [ ] Verify join type is correct (Inner, Left, Right, Full)
- [ ] Check row count after merge matches expectations
- [ ] Verify no unexpected nulls from failed joins
- [ ] Check for duplicate rows if using wrong join

### For Calculated Columns
- [ ] Spot check calculated values manually
- [ ] Verify formulas are correct
- [ ] Check for null handling in calculations
- [ ] Compare aggregates with source data

### For Date Transformations
- [ ] Verify date format is consistent
- [ ] Check time zones are handled correctly
- [ ] Validate date parsing (no errors)
- [ ] Verify date range is reasonable

### For Text Transformations
- [ ] Check case changes (Upper/Lower/Proper)
- [ ] Verify trim operations removed whitespace
- [ ] Check text replacements worked correctly
- [ ] Validate text splitting/merging

## Performance Checks
- [ ] Check query folding is happening where possible
- [ ] Review Applied Steps - look for performance issues
- [ ] Consider query dependencies and load order
- [ ] Test with representative data volumes

## Documentation
- [ ] Document all validation results
- [ ] Note any deviations from expected results
- [ ] Record reasons for any data discrepancies
- [ ] Update data dictionary if schema changed
- [ ] Version control all M code exports

## Before Publishing
- [ ] Run full validation suite
- [ ] Review all validation queries
- [ ] Check data refresh works correctly
- [ ] Test with latest source data
- [ ] Verify all visuals display correct data
- [ ] Check row-level security if applicable

## Post-Deployment
- [ ] Schedule regular validation checks
- [ ] Monitor data refresh success/failure
- [ ] Set up alerts for data quality issues
- [ ] Review validation results weekly
- [ ] Update tests when business rules change

## Common Issues to Check
- [ ] Circular dependencies in queries
- [ ] Privacy level errors preventing query folding
- [ ] Data type mismatches causing errors
- [ ] Column name changes breaking downstream queries
- [ ] Filter order causing incorrect results
- [ ] Duplicates from incorrect joins
- [ ] Missing data from overly restrictive filters
- [ ] Calculation errors from null values
- [ ] Date format inconsistencies
- [ ] Text encoding issues

## Notes Section
Use this space to document specific findings:

```
Date: _______________
Tester: _______________
Issue Found: _______________
Resolution: _______________
```
