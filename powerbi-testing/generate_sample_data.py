# Sample Data Generator for Testing

This script generates sample Excel files to test the validation framework.

import pandas as pd
from datetime import datetime, timedelta
import random

# Generate sample source data
def generate_sample_data(num_rows=100):
    """Generate sample sales data"""
    
    # Random data generation
    customer_ids = range(1, num_rows + 1)
    customer_names = [f"Customer_{i}" for i in customer_ids]
    
    # Random dates in 2024
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 365)) for _ in range(num_rows)]
    
    # Random amounts
    amounts = [round(random.uniform(10, 1000), 2) for _ in range(num_rows)]
    
    # Random categories
    categories = random.choices(['Electronics', 'Clothing', 'Food', 'Books', 'Toys'], k=num_rows)
    
    # Random quantities
    quantities = [random.randint(1, 10) for _ in range(num_rows)]
    
    # Create DataFrame
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'CustomerName': customer_names,
        'OrderDate': dates,
        'TotalAmount': amounts,
        'ProductCategory': categories,
        'Quantity': quantities
    })
    
    return df

def generate_transformed_data(source_df):
    """Simulate a Power BI transformation"""
    
    # Copy the source data
    df = source_df.copy()
    
    # Add calculated columns (simulating Power BI calculations)
    df['UnitPrice'] = (df['TotalAmount'] / df['Quantity']).round(2)
    df['Year'] = df['OrderDate'].dt.year
    df['Month'] = df['OrderDate'].dt.month
    df['Quarter'] = df['OrderDate'].dt.quarter
    
    # Filter: Only amounts > 50 (example transformation)
    df = df[df['TotalAmount'] > 50].copy()
    
    return df

if __name__ == '__main__':
    print("Generating sample data...")
    
    # Generate source data
    source_df = generate_sample_data(100)
    print(f"✅ Generated source data: {len(source_df)} rows")
    
    # Save source data
    source_df.to_excel('sample_source.xlsx', index=False)
    print("✅ Saved to sample_source.xlsx")
    
    # Generate transformed data (simulating Power BI export)
    transformed_df = generate_transformed_data(source_df)
    print(f"✅ Generated transformed data: {len(transformed_df)} rows")
    
    # Save transformed data
    transformed_df.to_csv('sample_powerbi_export.csv', index=False)
    print("✅ Saved to sample_powerbi_export.csv")
    
    print("\n📊 Sample Data Summary:")
    print(f"Source rows: {len(source_df)}")
    print(f"Transformed rows: {len(transformed_df)}")
    print(f"Rows filtered out: {len(source_df) - len(transformed_df)}")
    print(f"Source columns: {len(source_df.columns)}")
    print(f"Transformed columns: {len(transformed_df.columns)}")
    print(f"New columns added: {len(transformed_df.columns) - len(source_df.columns)}")
    
    print("\n🎯 You can now test the validation script:")
    print("python validate_powerbi_data.py --source sample_source.xlsx --export sample_powerbi_export.csv")
