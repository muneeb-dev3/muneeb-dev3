# Power BI Testing Framework - File Guide

Welcome to the Power BI Data Validation Framework! This guide helps you navigate all the files in this directory.

## 📚 Where to Start?

**New to testing Power BI projects?**
→ Start with [QUICK_START.md](QUICK_START.md)

**Want detailed documentation?**
→ Read [README.md](README.md)

**Ready to implement?**
→ Follow [COMPLETE_EXAMPLE.md](COMPLETE_EXAMPLE.md)

---

## 📋 Documentation Files

### [QUICK_START.md](QUICK_START.md)
**Perfect for beginners!** Shows 3 easy methods to validate your Power BI transformations:
- Method 1: Manual testing (easiest)
- Method 2: M code validation (built into Power BI)
- Method 3: Python automation (most thorough)

### [README.md](README.md)
**Complete reference guide** covering:
- Why you need testing for Power BI
- Manual validation in Power BI Desktop
- Automated validation with Python
- M code unit testing
- Best practices and common validation checks

### [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)
**Step-by-step checklist** for validating your Power BI project:
- Pre-testing setup
- Manual testing steps
- Automated testing steps
- Transformation-specific checks
- Before publishing checklist

### [COMPLETE_EXAMPLE.md](COMPLETE_EXAMPLE.md)
**End-to-end example** showing:
- Complete workflow from start to finish
- Sample configuration files
- M code examples
- Expected outputs
- Troubleshooting tips

---

## 🐍 Python Scripts

### [validate_powerbi_data.py](validate_powerbi_data.py)
**Main validation script** - compares your Power BI export with source Excel file.

**Usage:**
```bash
python validate_powerbi_data.py --source source.xlsx --export powerbi_export.csv
python validate_powerbi_data.py --source source.xlsx --export export.csv --config test_config.json
```

**Features:**
- ✅ Row count validation
- ✅ Column validation
- ✅ Data type checking
- ✅ Null value comparison
- ✅ Aggregate validation (sum, mean, min, max, count)
- ✅ Sample value testing
- ✅ Configurable via JSON

### [generate_sample_data.py](generate_sample_data.py)
**Helper script** to generate sample data for testing the framework.

**Usage:**
```bash
python generate_sample_data.py
```

This creates:
- `sample_source.xlsx` - Sample source data (100 rows)
- `sample_powerbi_export.csv` - Sample transformed data

---

## ⚙️ Configuration Files

### [test_config_example.json](test_config_example.json)
**Example configuration** showing all available validation options.

Copy and customize for your project:
```bash
cp test_config_example.json my_project_config.json
# Edit my_project_config.json with your values
```

Configuration options:
- `source_sheet`: Which Excel sheet to read
- `expected_row_count`: Expected number of rows after transformation
- `expected_columns`: List of columns that must exist
- `aggregate_tests`: Sum/mean/min/max validations
- `sample_tests`: Specific value checks

### [requirements.txt](requirements.txt)
**Python dependencies** needed to run the validation scripts.

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 📝 M Code Examples

### [m_code_validation_examples.m](m_code_validation_examples.m)
**Ready-to-use M code queries** for Power BI validation:

**Available validations:**
1. Row Count Validation
2. Column Validation
3. Null Value Check
4. Sum Validation
5. Duplicate Check
6. Data Type Validation
7. Date Range Validation
8. Comprehensive Validation Dashboard

**How to use:**
1. Copy a validation query
2. In Power BI Desktop → Transform Data
3. New Source → Blank Query → Advanced Editor
4. Paste the code
5. Replace table names with yours
6. Set "Enable Load" = false

---

## 🎯 Quick Reference

### Common Tasks

**Test my Power BI transformations for the first time:**
1. Read [QUICK_START.md](QUICK_START.md)
2. Start with Method 1 (manual testing)
3. Graduate to Method 3 (Python automation)

**Set up automated validation:**
1. Export Power BI table to CSV
2. Install dependencies: `pip install -r requirements.txt`
3. Copy and edit `test_config_example.json`
4. Run: `python validate_powerbi_data.py --source source.xlsx --export export.csv --config config.json`

**Add validation to Power BI project:**
1. Open [m_code_validation_examples.m](m_code_validation_examples.m)
2. Copy the validation queries you need
3. Add them to your Power BI project
4. Set "Enable Load" = false for validation queries

**Generate test data:**
```bash
python generate_sample_data.py
```

**Validate with test data:**
```bash
python validate_powerbi_data.py --source sample_source.xlsx --export sample_powerbi_export.csv
```

---

## 🔍 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| QUICK_START.md | Beginner's guide | First time using this framework |
| README.md | Complete documentation | Need detailed reference |
| TESTING_CHECKLIST.md | Step-by-step checklist | During actual testing |
| COMPLETE_EXAMPLE.md | Full workflow example | Implementing for real project |
| validate_powerbi_data.py | Python validation script | Automated testing |
| generate_sample_data.py | Create test data | Testing the framework |
| test_config_example.json | Config template | Setting up your tests |
| m_code_validation_examples.m | M code examples | Adding validation to Power BI |
| requirements.txt | Python dependencies | Setting up environment |

---

## 💡 Tips

1. **Start simple**: Begin with manual testing, then add automation
2. **Test incrementally**: Validate after each major transformation
3. **Document everything**: Keep notes on expected vs actual results
4. **Version control**: Save M code and test configs in Git
5. **Automate regularly**: Run validation weekly on production data

---

## 🆘 Need Help?

1. Check [QUICK_START.md](QUICK_START.md) for common tasks
2. Review [COMPLETE_EXAMPLE.md](COMPLETE_EXAMPLE.md) for detailed workflow
3. See troubleshooting section in [README.md](README.md)
4. Look at M code comments in [m_code_validation_examples.m](m_code_validation_examples.m)

---

## 📊 Example Workflow

```
1. Create Power BI transformations with M code
   ↓
2. Export transformed table to CSV
   ↓
3. Create test configuration (copy test_config_example.json)
   ↓
4. Run Python validation script
   ↓
5. Review results and fix issues
   ↓
6. Add M code validation queries to Power BI
   ↓
7. Use TESTING_CHECKLIST.md for final validation
   ↓
8. Document results
   ↓
9. Deploy to production
```

---

Happy Testing! 🚀
