"""
Example Usage of ETL Pipeline

This script demonstrates how to use the ETL pipeline with sample data.
"""

from etl_pipeline import ETLPipeline, create_sample_data
from pathlib import Path


def main():
    """Main execution function"""
    
    # Define paths relative to this script
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'data'
    output_dir = script_dir / 'output'
    
    # Ensure directories exist
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Create and save sample data
    print("Creating sample data...")
    sample_df = create_sample_data()
    input_file = input_dir / 'input_data.csv'
    sample_df.to_csv(input_file, index=False)
    print(f"Sample data created at: {input_file}\n")
    
    # ===================================
    # EXAMPLE 1: Basic transformation
    # ===================================
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Data Transformation")
    print("="*60 + "\n")
    
    config = {
        'date_columns': ['dob', 'hire_date'],
        'remove_duplicates': True,
        'fill_missing_values': {
            'gender': 'Unknown'
        },
        'column_mapping': {
            'emp_id': 'employee_id',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'gender': 'gender',
            'dob': 'date_of_birth',
            'salary': 'annual_salary'
        }
    }
    
    pipeline = ETLPipeline(input_dir, output_dir)
    pipeline.run('input_data.csv', 'output_basic.csv', config)
    
    print("\nTransformed Data Preview:")
    print(pipeline.transformed_data.head(10))
    
    
    # ===================================
    # EXAMPLE 2: With aggregation
    # ===================================
    print("\n" + "="*60)
    print("EXAMPLE 2: Data with Aggregation by Department")
    print("="*60 + "\n")
    
    pipeline2 = ETLPipeline(input_dir, output_dir)
    pipeline2.extract('input_data.csv')
    
    # Transform first
    pipeline2.transform(config)
    
    # Then aggregate
    aggregated = pipeline2.transformer.aggregate_data(
        pipeline2.data,
        group_by_column='department',
        agg_dict={
            'salary': 'mean',
            'age': 'mean',
            'emp_id': 'count'
        }
    )
    
    aggregated.to_csv(output_dir / 'output_aggregated.csv', index=False)
    print("\nAggregated Data:")
    print(aggregated)
    
    
    # ===================================
    # EXAMPLE 3: With filtering
    # ===================================
    print("\n" + "="*60)
    print("EXAMPLE 3: Data Transformation with Filtering")
    print("="*60 + "\n")
    
    pipeline3 = ETLPipeline(input_dir, output_dir)
    pipeline3.extract('input_data.csv')
    
    # Filter: only active employees with salary >= 55000
    filter_conditions = {
        'status': 'active',
        'salary': (55000, 100000)
    }
    filtered_data = pipeline3.transformer.filter_data(
        pipeline3.data,
        filter_conditions
    )
    
    # Transform the filtered data
    config['column_mapping']['status'] = 'employment_status'
    pipeline3.transformed_data = pipeline3.transformer.transform(filtered_data, config)
    pipeline3.load('output_filtered.csv')
    
    print("\nFiltered & Transformed Data Preview:")
    print(pipeline3.transformed_data.head())


if __name__ == "__main__":
    main()
