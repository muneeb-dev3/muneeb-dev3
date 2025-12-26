# Power BI Data Validation Framework

## Overview
This framework helps you validate Power BI transformations created with M code against source Excel files. It provides a systematic approach to ensure data integrity throughout your ETL process.

## Why Testing Power BI Transformations?

Just like in software development where we write test cases, Power BI projects need validation to ensure:
- Data accuracy after transformations
- Consistency between source and transformed data
- Detection of data quality issues
- Confidence in M code transformations

## Validation Approaches

### 1. Manual Validation in Power BI Desktop

#### Step-by-Step Process:
1. **Open Power Query Editor**
   - In Power BI Desktop, click "Transform Data"
   - This shows all your M code queries

2. **Check Each Transformation Step**
   - Select a query to see all transformation steps
   - Click each step to verify the data at that point
   - Compare row counts with source Excel

3. **Use Data Profiling**
   - In Power Query Editor, go to View tab
   - Enable: Column Quality, Column Distribution, Column Profile
   - This shows data quality metrics for each column

4. **Validate Against Source**
   - Keep your source Excel file open
   - Compare key metrics:
     - Total row count
     - Column count
     - Data types
     - Sample values
     - Aggregations (sum, count, etc.)

### 2. Automated Validation with Python

Use the provided Python scripts to automate validation:

```bash
# Install required packages
pip install pandas openpyxl

# Run validation
python validate_powerbi_data.py --source source.xlsx --export powerbi_export.csv --config test_config.json
```

### 3. M Code Unit Testing

Create validation queries directly in Power BI:

```m
// Example: Validate row count matches source
let
    SourceCount = Table.RowCount(SourceTable),
    TransformedCount = Table.RowCount(TransformedTable),
    ValidationResult = if SourceCount = TransformedCount 
                       then "PASS: Row counts match" 
                       else "FAIL: Row count mismatch"
in
    ValidationResult
```

## Best Practices

1. **Create Validation Queries**
   - Add separate queries for validation
   - Don't load them to the model (right-click > Enable Load = false)
   - Use them during development

2. **Document Your Transformations**
   - Add comments in M code
   - Create a data dictionary
   - Document business rules

3. **Regular Testing Schedule**
   - Test after major changes
   - Validate before publishing
   - Perform spot checks on production data

4. **Version Control**
   - Export M code to .txt or .pq files
   - Use Git for version control
   - Track changes over time

## Common Validation Checks

### Data Integrity Checks
- ✅ Row count comparison
- ✅ Column count comparison
- ✅ Data type validation
- ✅ Null value counts
- ✅ Duplicate detection
- ✅ Range validation (min/max)
- ✅ Sum/aggregate comparisons

### Transformation Validation
- ✅ Join accuracy (expected row count after merge)
- ✅ Filter logic (rows removed as expected)
- ✅ Calculated columns (spot check formulas)
- ✅ Date transformations (format consistency)
- ✅ Text transformations (case, trim, etc.)

## Tools and Resources

### Export Power BI Data for Testing
1. In Power BI Desktop, go to a visual
2. Click "..." > Export data
3. Save as CSV
4. Use for comparison with source

### Power Query Editor Tips
- Use "Keep/Remove Rows" > "Keep Top Rows" for sampling
- Use "Advanced Editor" to review complete M code
- Use "Query Dependencies" to see data lineage

## Troubleshooting

**Q: How do I export M code?**
A: In Power Query Editor, select query > Advanced Editor > Copy code to text file

**Q: Data doesn't match source?**
A: Check each transformation step, look for filters, joins that might exclude data

**Q: How to handle large files?**
A: Use sampling for validation, compare aggregates instead of row-by-row

## Next Steps

1. Review the sample Python validation script
2. Create your test configuration file
3. Set up regular validation schedule
4. Document your specific test cases

For more information, see the example scripts in this directory.
