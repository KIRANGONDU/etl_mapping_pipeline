"""
Multi-Source ETL Pipeline Example
Demonstrates consolidating data from multiple files with different column names
"""

from multi_source_etl import MultiSourceETLPipeline
from pathlib import Path


def main():
    """Main execution"""
    
    print("\n" + "="*70)
    print("MULTI-SOURCE ETL PIPELINE EXAMPLE")
    print("="*70)
    
    # Setup paths relative to this script
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'data'
    output_dir = script_dir / 'output'
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Create pipeline
    pipeline = MultiSourceETLPipeline(input_dir, output_dir)
    
    # ===================================
    # REGISTER DATA SOURCES
    # ===================================
    
    # Source 1: dataset_1.csv with different column names
    source1_mapping = {
        'emp_id': 'employee_id',
        'fname': 'first_name',
        'lname': 'last_name',
        'sex': 'gender',
        'birth_date': 'date_of_birth',
        'joining_date': 'hire_date',
        'annual_salary': 'salary',
        'dept': 'department',
        'yrs_old': 'age',
        'active_status': 'status'
    }
    
    pipeline.register_source(
        source_name='dataset_1',
        filename='dataset_1.csv',
        column_mapping=source1_mapping
    )
    
    # Source 2: dataset_2.csv with standard column names
    source2_mapping = {
        'employee_id': 'employee_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'date_of_birth': 'date_of_birth',
        'hire_date': 'hire_date',
        'salary': 'salary',
        'department': 'department',
        'age': 'age',
        'status': 'status'
    }
    
    pipeline.register_source(
        source_name='dataset_2',
        filename='dataset_2.csv',
        column_mapping=source2_mapping
    )
    
    # ===================================
    # DEFINE TRANSFORMATION CONFIG
    # ===================================
    
    config = {
        'date_columns': ['date_of_birth', 'hire_date'],
        'remove_duplicates': True,
        'fill_missing_values': {
            'gender': 'Unknown',
            'status': 'unknown'
        },
        'final_columns': [
            'source',
            'employee_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'hire_date',
            'salary',
            'department',
            'age'
        ]
    }
    
    # ===================================
    # RUN PIPELINE
    # ===================================
    
    try:
        result = pipeline.run(
            output_filename='consolidated_employees.csv',
            config=config
        )
        
        print("\n" + "="*70)
        print("CONSOLIDATED DATA PREVIEW")
        print("="*70)
        print(result.to_string())
        
        print("\n" + "="*70)
        print("DATA GROUPING BY SOURCE")
        print("="*70)
        print(result.groupby('source').size())
        
        print("\n" + "="*70)
        print("GENDER DISTRIBUTION")
        print("="*70)
        print(result['gender'].value_counts())
        
        print("\n" + "="*70)
        print("DEPARTMENT DISTRIBUTION")
        print("="*70)
        print(result['department'].value_counts())
        
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
