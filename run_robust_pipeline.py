"""
Robust Four-Source ETL Pipeline with Error Handling
Handles 4 input files with automatic error detection and correction
"""

from robust_etl import RobustMultiSourceETL
from pathlib import Path
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution - handles all 4 input files with robust error handling"""
    
    print("\n" + "="*80)
    print(" "*20 + "ROBUST FOUR-SOURCE ETL PIPELINE")
    print(" "*15 + "With Error Handling & Auto-Rectification")
    print("="*80)
    
    # Setup paths relative to this script
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'data'
    output_dir = script_dir / 'output'
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Create robust pipeline
    pipeline = RobustMultiSourceETL(input_dir, output_dir)
    
    # ===================================
    # SOURCE 1: dataset_1.csv
    # ===================================
    print("\n📁 Registering Source 1: dataset_1.csv")
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
        source_name='source_1_abbreviated',
        filename='dataset_1.csv',
        column_mapping=source1_mapping
    )
    
    # ===================================
    # SOURCE 2: dataset_2.csv
    # ===================================
    print("📁 Registering Source 2: dataset_2.csv")
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
        source_name='source_2_standard',
        filename='dataset_2.csv',
        column_mapping=source2_mapping
    )
    
    # ===================================
    # SOURCE 3: input_data.csv
    # ===================================
    print("📁 Registering Source 3: input_data.csv")
    source3_mapping = {
        'emp_id': 'employee_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'dob': 'date_of_birth',
        'hire_date': 'hire_date',
        'salary': 'salary',
        'department': 'department',
        'age': 'age',
        'status': 'status'
    }
    
    pipeline.register_source(
        source_name='source_3_mixed',
        filename='input_data.csv',
        column_mapping=source3_mapping
    )
    
    # ===================================
    # SOURCE 4: sample_employee_data.csv
    # ===================================
    print("📁 Registering Source 4: sample_employee_data.csv")
    source4_mapping = {
        'emp_id': 'employee_id',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'dob': 'date_of_birth',
        'hire_date': 'hire_date',
        'salary': 'salary',
        'department': 'department',
        'age': 'age',
        'status': 'status'
    }
    
    pipeline.register_source(
        source_name='source_4_sample',
        filename='sample_employee_data.csv',
        column_mapping=source4_mapping
    )
    
    # ===================================
    # TRANSFORMATION CONFIGURATION
    # ===================================
    config = {
        'date_columns': ['date_of_birth', 'hire_date'],
        'remove_duplicates': True,
        'fill_missing_values': {
            'gender': 'Unknown',
            'status': 'unknown',
            'department': 'Unassigned'
        },
        'final_columns': [
            'employee_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'salary'
        ]
    }
    
    print("\n" + "="*80)
    print("PIPELINE CONFIGURATION")
    print("="*80)
    print("✓ Sources: 4 files")
    print("✓ Output Columns: 6")
    print("✓ Date Formatting: YYYY-MM-DD")
    print("✓ Gender Normalization: M/F/Unknown")
    print("✓ Error Handling: Enabled with auto-rectification")
    print("✓ Error Logging: Enabled (error_log.json)")
    print("="*80)
    
    # ===================================
    # RUN PIPELINE
    # ===================================
    try:
        success = pipeline.run(
            output_filename='consolidated_all_sources_robust.csv',
            config=config
        )
        
        if success:
            print("\n" + "="*80)
            print("✓✓✓ PIPELINE EXECUTION SUCCESSFUL ✓✓✓")
            print("="*80)
            
            # Display results
            if pipeline.transformed_data is not None:
                print("\n📊 OUTPUT DATA SUMMARY")
                print("-" * 80)
                print(f"Total Rows: {len(pipeline.transformed_data)}")
                print(f"Total Columns: {len(pipeline.transformed_data.columns)}")
                print(f"Output File: output/consolidated_all_sources_robust.csv")
                
                print("\n📋 FINAL COLUMNS")
                print("-" * 80)
                for i, col in enumerate(pipeline.transformed_data.columns, 1):
                    print(f"  {i}. {col}")
                
                print("\n📈 DATA PREVIEW (First 10 rows)")
                print("-" * 80)
                print(pipeline.transformed_data.head(10).to_string())
                
                print("\n📊 STATISTICS")
                print("-" * 80)
                print("\nGender Distribution:")
                print(pipeline.transformed_data['gender'].value_counts())
                
                print("\nSalary Statistics:")
                print(pipeline.transformed_data['salary'].describe())
        
        else:
            print("\n" + "="*80)
            print("✗✗✗ PIPELINE EXECUTION FAILED ✗✗✗")
            print("="*80)
            print("\nStatus:", pipeline.pipeline_status)
            print("Check 'output/error_log.json' for detailed error information")
            
            # Try to display what was processed
            if pipeline.consolidated_data is not None:
                print(f"\nPartially processed data: {len(pipeline.consolidated_data)} rows")
        
        print("\n" + "="*80)
        print("Pipeline Status: " + pipeline.pipeline_status.upper())
        print("="*80)
        
        return 0 if success else 1
    
    except Exception as e:
        print("\n" + "="*80)
        print("✗✗✗ UNEXPECTED ERROR ✗✗✗")
        print("="*80)
        print(f"Error: {str(e)}")
        print("\nPlease check 'output/error_log.json' for details")
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
