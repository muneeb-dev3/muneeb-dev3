#!/usr/bin/env python3
"""
Power BI Data Validation Script

This script compares source Excel data with exported Power BI data
to validate transformations and ensure data integrity.

Usage:
    python validate_powerbi_data.py --source source.xlsx --export powerbi_export.csv
    python validate_powerbi_data.py --source source.xlsx --export powerbi_export.csv --config test_config.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Install with: pip install pandas openpyxl")
    sys.exit(1)


class PowerBIValidator:
    """Validates Power BI transformations against source data"""
    
    def __init__(self, source_path: str, export_path: str, config: Dict = None):
        self.source_path = source_path
        self.export_path = export_path
        self.config = config or {}
        self.results = []
        
    def load_source_data(self) -> pd.DataFrame:
        """Load source Excel file"""
        print(f"📂 Loading source file: {self.source_path}")
        
        # Support reading specific sheet if configured
        sheet_name = self.config.get('source_sheet', 0)
        
        try:
            df = pd.read_excel(self.source_path, sheet_name=sheet_name)
            print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns from source")
            return df
        except Exception as e:
            print(f"❌ Error loading source file: {e}")
            sys.exit(1)
    
    def load_export_data(self) -> pd.DataFrame:
        """Load Power BI exported data (CSV or Excel)"""
        print(f"📂 Loading Power BI export: {self.export_path}")
        
        try:
            if self.export_path.endswith('.csv'):
                df = pd.read_csv(self.export_path)
            elif self.export_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(self.export_path)
            else:
                print(f"❌ Unsupported file format: {self.export_path}")
                sys.exit(1)
            
            print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns from export")
            return df
        except Exception as e:
            print(f"❌ Error loading export file: {e}")
            sys.exit(1)
    
    def validate_row_count(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate row counts match (or meet expected criteria)"""
        source_count = len(source_df)
        export_count = len(export_df)
        
        expected_count = self.config.get('expected_row_count')
        
        if expected_count is not None:
            passed = export_count == expected_count
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"\n{status} - Row Count Validation")
            print(f"  Expected: {expected_count}, Got: {export_count}")
        else:
            passed = source_count == export_count
            status = "✅ PASS" if passed else "⚠️  WARN"
            print(f"\n{status} - Row Count Comparison")
            print(f"  Source: {source_count}, Export: {export_count}")
            if not passed:
                diff = export_count - source_count
                print(f"  Difference: {diff:+d} rows")
        
        self.results.append({
            'test': 'Row Count',
            'passed': passed,
            'source_count': source_count,
            'export_count': export_count
        })
        
        return passed
    
    def validate_column_count(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate column counts"""
        source_cols = len(source_df.columns)
        export_cols = len(export_df.columns)
        
        passed = source_cols <= export_cols  # Allow more columns in export (calculated columns)
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"\n{status} - Column Count Validation")
        print(f"  Source: {source_cols}, Export: {export_cols}")
        
        self.results.append({
            'test': 'Column Count',
            'passed': passed,
            'source_count': source_cols,
            'export_count': export_cols
        })
        
        return passed
    
    def validate_columns_exist(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate expected columns exist in export"""
        expected_columns = self.config.get('expected_columns', [])
        
        if not expected_columns:
            print("\n⏭️  Skipping column existence check (no expected_columns configured)")
            return True
        
        missing_columns = [col for col in expected_columns if col not in export_df.columns]
        passed = len(missing_columns) == 0
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"\n{status} - Column Existence Validation")
        if passed:
            print(f"  All {len(expected_columns)} expected columns found")
        else:
            print(f"  Missing columns: {missing_columns}")
        
        self.results.append({
            'test': 'Column Existence',
            'passed': passed,
            'missing_columns': missing_columns
        })
        
        return passed
    
    def validate_data_types(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate data types for common columns"""
        common_columns = set(source_df.columns) & set(export_df.columns)
        
        if not common_columns:
            print("\n⏭️  Skipping data type validation (no common columns)")
            return True
        
        print(f"\n📊 Data Type Validation for {len(common_columns)} common columns")
        
        type_mismatches = []
        for col in common_columns:
            source_type = source_df[col].dtype
            export_type = export_df[col].dtype
            
            # Allow some flexibility in numeric types
            if source_type != export_type:
                if not (pd.api.types.is_numeric_dtype(source_type) and 
                       pd.api.types.is_numeric_dtype(export_type)):
                    type_mismatches.append({
                        'column': col,
                        'source_type': str(source_type),
                        'export_type': str(export_type)
                    })
        
        passed = len(type_mismatches) == 0
        status = "✅ PASS" if passed else "⚠️  WARN"
        
        print(f"{status} - Data Types")
        if type_mismatches:
            for mismatch in type_mismatches[:5]:  # Show first 5
                print(f"  {mismatch['column']}: {mismatch['source_type']} → {mismatch['export_type']}")
        
        self.results.append({
            'test': 'Data Types',
            'passed': passed,
            'mismatches': type_mismatches
        })
        
        return passed
    
    def validate_null_counts(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Compare null counts for common columns"""
        common_columns = set(source_df.columns) & set(export_df.columns)
        
        if not common_columns:
            print("\n⏭️  Skipping null count validation (no common columns)")
            return True
        
        print(f"\n🔍 Null Count Validation")
        
        differences = []
        for col in common_columns:
            source_nulls = source_df[col].isna().sum()
            export_nulls = export_df[col].isna().sum()
            
            if source_nulls != export_nulls:
                differences.append({
                    'column': col,
                    'source_nulls': int(source_nulls),
                    'export_nulls': int(export_nulls),
                    'difference': int(export_nulls - source_nulls)
                })
        
        if differences:
            print(f"⚠️  Null count differences found in {len(differences)} columns:")
            for diff in differences[:5]:  # Show first 5
                print(f"  {diff['column']}: {diff['source_nulls']} → {diff['export_nulls']} ({diff['difference']:+d})")
        else:
            print(f"✅ Null counts match for all common columns")
        
        self.results.append({
            'test': 'Null Counts',
            'passed': len(differences) == 0,
            'differences': differences
        })
        
        return len(differences) == 0
    
    def validate_aggregates(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate aggregate values for numeric columns"""
        aggregate_tests = self.config.get('aggregate_tests', [])
        
        if not aggregate_tests:
            print("\n⏭️  Skipping aggregate validation (no aggregate_tests configured)")
            return True
        
        print(f"\n🧮 Aggregate Validation")
        all_passed = True
        
        for test in aggregate_tests:
            column = test.get('column')
            operation = test.get('operation', 'sum')  # sum, mean, min, max, count
            tolerance = test.get('tolerance', 0.01)  # Allow small differences
            
            if column not in source_df.columns or column not in export_df.columns:
                print(f"⚠️  Column '{column}' not found in both datasets")
                continue
            
            # Calculate aggregates
            if operation == 'sum':
                source_val = source_df[column].sum()
                export_val = export_df[column].sum()
            elif operation == 'mean':
                source_val = source_df[column].mean()
                export_val = export_df[column].mean()
            elif operation == 'min':
                source_val = source_df[column].min()
                export_val = export_df[column].min()
            elif operation == 'max':
                source_val = source_df[column].max()
                export_val = export_df[column].max()
            elif operation == 'count':
                source_val = source_df[column].count()
                export_val = export_df[column].count()
            else:
                print(f"⚠️  Unknown operation: {operation}")
                continue
            
            # Compare with tolerance
            diff = abs(export_val - source_val)
            passed = diff <= tolerance
            status = "✅ PASS" if passed else "❌ FAIL"
            
            print(f"  {status} {operation}({column}): {source_val:.2f} → {export_val:.2f} (diff: {diff:.2f})")
            
            if not passed:
                all_passed = False
        
        self.results.append({
            'test': 'Aggregates',
            'passed': all_passed
        })
        
        return all_passed
    
    def validate_sample_values(self, source_df: pd.DataFrame, export_df: pd.DataFrame) -> bool:
        """Validate sample values for specific columns"""
        sample_tests = self.config.get('sample_tests', [])
        
        if not sample_tests:
            print("\n⏭️  Skipping sample value validation (no sample_tests configured)")
            return True
        
        print(f"\n🔬 Sample Value Validation")
        all_passed = True
        
        for test in sample_tests:
            column = test.get('column')
            row_index = test.get('row_index', 0)
            expected_value = test.get('expected_value')
            
            if column not in export_df.columns:
                print(f"⚠️  Column '{column}' not found in export")
                continue
            
            if row_index >= len(export_df):
                print(f"⚠️  Row index {row_index} out of range")
                continue
            
            actual_value = export_df.iloc[row_index][column]
            passed = str(actual_value) == str(expected_value)
            status = "✅ PASS" if passed else "❌ FAIL"
            
            print(f"  {status} {column}[{row_index}]: expected '{expected_value}', got '{actual_value}'")
            
            if not passed:
                all_passed = False
        
        self.results.append({
            'test': 'Sample Values',
            'passed': all_passed
        })
        
        return all_passed
    
    def run_validation(self) -> bool:
        """Run all validation checks"""
        print("=" * 60)
        print("🚀 Power BI Data Validation")
        print("=" * 60)
        
        # Load data
        source_df = self.load_source_data()
        export_df = self.load_export_data()
        
        # Run validations
        self.validate_row_count(source_df, export_df)
        self.validate_column_count(source_df, export_df)
        self.validate_columns_exist(source_df, export_df)
        self.validate_data_types(source_df, export_df)
        self.validate_null_counts(source_df, export_df)
        self.validate_aggregates(source_df, export_df)
        self.validate_sample_values(source_df, export_df)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Validation Summary")
        print("=" * 60)
        
        passed_tests = sum(1 for r in self.results if r['passed'])
        total_tests = len(self.results)
        
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        
        for result in self.results:
            status = "✅" if result['passed'] else "❌"
            print(f"  {status} {result['test']}")
        
        all_passed = passed_tests == total_tests
        
        if all_passed:
            print("\n🎉 All validations passed!")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} validation(s) failed")
        
        print("=" * 60)
        
        return all_passed


def load_config(config_path: str) -> Dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Validate Power BI transformations against source data'
    )
    parser.add_argument(
        '--source',
        required=True,
        help='Path to source Excel file'
    )
    parser.add_argument(
        '--export',
        required=True,
        help='Path to Power BI exported data (CSV or Excel)'
    )
    parser.add_argument(
        '--config',
        help='Path to test configuration JSON file'
    )
    
    args = parser.parse_args()
    
    # Validate file existence
    if not Path(args.source).exists():
        print(f"❌ Source file not found: {args.source}")
        sys.exit(1)
    
    if not Path(args.export).exists():
        print(f"❌ Export file not found: {args.export}")
        sys.exit(1)
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Run validation
    validator = PowerBIValidator(args.source, args.export, config)
    success = validator.run_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
