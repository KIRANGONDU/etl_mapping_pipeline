"""
Four-Source ETL Pipeline
Consolidates data from 4 input files with different column names
- dataset_1.csv (abbrev columns: emp_id, fname, lname, sex, birth_date, joining_date, annual_salary, dept, yrs_old, active_status)
- dataset_2.csv (standard columns: employee_id, first_name, last_name, gender, date_of_birth, hire_date, salary, department, age, status)
- input_data.csv (mixed columns: emp_id, first_name, last_name, gender, dob, hire_date, salary, department, age, status)
- sample_employee_data.csv (mixed columns: emp_id, first_name, last_name, gender, dob, hire_date, salary, department, age, status)
"""

from multi_source_etl import MultiSourceETLPipeline
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution - handles all 4 input files"""
    
    print("\n" + "="*70)
    print("FOUR-SOURCE ETL PIPELINE")
    print("Processing 4 input files with different column structures")
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
    # SOURCE 1: dataset_1.csv
    # Columns: emp_id, fname, lname, sex, birth_date, joining_date, annual_salary, dept, yrs_old, active_status
    # ===================================
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
    print("\n✓ Registered Source 1: dataset_1.csv (abbreviated columns)")
    
    # ===================================
    # SOURCE 2: dataset_2.csv
    # Columns: employee_id, first_name, last_name, gender, date_of_birth, hire_date, salary, department, age, status
    # ===================================
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
    print("✓ Registered Source 2: dataset_2.csv (standard columns)")
    
    # ===================================
    # SOURCE 3: input_data.csv
    # Columns: emp_id, first_name, last_name, gender, dob, hire_date, salary, department, age, status
    # ===================================
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
    print("✓ Registered Source 3: input_data.csv (mixed columns)")
    
    # ===================================
    # SOURCE 4: sample_employee_data.csv
    # Columns: emp_id, first_name, last_name, gender, dob, hire_date, salary, department, age, status
    # ===================================
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
    print("✓ Registered Source 4: sample_employee_data.csv (mixed columns)")
    
    # ===================================
    # TRANSFORMATION CONFIGURATION
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
    
    print("\n" + "="*70)
    print("TRANSFORMATION CONFIGURATION")
    print("="*70)
    print("✓ Date formatting: YYYY-MM-DD")
    print("✓ Gender normalization: M/male/MM→M, F/female/ff→F, 0→Unknown")
    print("✓ Remove duplicates: Yes")
    print("✓ Fill missing values: gender→Unknown, status→unknown")
    print("✓ Output columns: 10 (reduced from input)")
    
    # ===================================
    # RUN PIPELINE
    # ===================================
    try:
        print("\n" + "="*70)
        print("RUNNING PIPELINE")
        print("="*70)
        
        result = pipeline.run(
            output_filename='consolidated_all_four_sources.csv',
            config=config
        )
        
        # ===================================
        # DISPLAY RESULTS
        # ===================================
        
        print("\n" + "="*70)
        print("CONSOLIDATION COMPLETE!")
        print("="*70)
        
        print("\n📊 CONSOLIDATED DATA SUMMARY")
        print("-" * 70)
        print(f"Total Rows: {len(result)}")
        print(f"Total Columns: {len(result.columns)}")
        print(f"Output File: output/consolidated_all_four_sources.csv")
        
        print("\n📋 COLUMN NAMES")
        print("-" * 70)
        for i, col in enumerate(result.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\n📈 DATA PREVIEW (First 10 rows)")
        print("-" * 70)
        print(result.head(10).to_string(index=False))
        
        print("\n🔍 DATA BY SOURCE")
        print("-" * 70)
        source_counts = result['source'].value_counts().sort_index()
        for source, count in source_counts.items():
            print(f"  {source:20s}: {count:3d} rows")
        print(f"  {'TOTAL':20s}: {len(result):3d} rows")
        
        print("\n👥 GENDER DISTRIBUTION")
        print("-" * 70)
        gender_counts = result['gender'].value_counts()
        for gender, count in gender_counts.items():
            percentage = (count / len(result)) * 100
            print(f"  {gender:10s}: {count:3d} ({percentage:5.1f}%)")
        
        print("\n🏢 DEPARTMENT DISTRIBUTION")
        print("-" * 70)
        dept_counts = result['department'].value_counts().sort_values(ascending=False)
        for dept, count in dept_counts.items():
            percentage = (count / len(result)) * 100
            print(f"  {dept:15s}: {count:3d} ({percentage:5.1f}%)")
        
        print("\n💰 SALARY STATISTICS")
        print("-" * 70)
        print(f"  Average Salary: ${result['salary'].mean():,.2f}")
        print(f"  Min Salary:     ${result['salary'].min():,.2f}")
        print(f"  Max Salary:     ${result['salary'].max():,.2f}")
        print(f"  Median Salary:  ${result['salary'].median():,.2f}")
        
        print("\n👤 AGE STATISTICS")
        print("-" * 70)
        print(f"  Average Age: {result['age'].mean():.1f}")
        print(f"  Min Age:     {result['age'].min()}")
        print(f"  Max Age:     {result['age'].max()}")
        print(f"  Median Age:  {result['age'].median()}")
        
        print("\n" + "="*70)
        print("✅ PIPELINE EXECUTION SUCCESSFUL!")
        print("="*70)
        
        return result
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    result = main()
