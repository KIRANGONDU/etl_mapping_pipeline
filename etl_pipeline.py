"""
ETL Pipeline for Data Transformation and Loading
- Extract: Read input data from CSV
- Transform: Clean, normalize, and aggregate data
- Load: Write to target table/database and output folder
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataTransformer:
    """Handles all data transformation operations"""
    
    def __init__(self):
        self.input_data = None
        self.transformed_data = None
        
    def normalize_gender(self, gender_value):
        """
        Normalize gender values:
        - m, mm, male -> M
        - f, ff, female -> F
        - 0, empty, null -> Unknown
        """
        if pd.isna(gender_value):
            return 'Unknown'
        
        gender_str = str(gender_value).strip().lower()
        
        if gender_str in ['m', 'mm', 'male']:
            return 'M'
        elif gender_str in ['f', 'ff', 'female']:
            return 'F'
        elif gender_str == '0':
            return 'Unknown'
        else:
            return 'Unknown'
    
    def format_date(self, date_value, format_to='YYYY-MM-DD'):
        """
        Format date to YYYY-MM-DD format
        Handles various input date formats
        """
        try:
            if pd.isna(date_value):
                return None
            
            # Try to parse the date
            parsed_date = pd.to_datetime(date_value)
            
            if format_to == 'YYYY-MM-DD':
                return parsed_date.strftime('%Y-%m-%d')
            else:
                return parsed_date.strftime(format_to)
        except Exception as e:
            logger.warning(f"Could not parse date: {date_value} - Error: {e}")
            return None
    
    def filter_data(self, df, filter_conditions=None):
        """
        Filter data based on conditions
        filter_conditions: dict with column names and filter values
        Example: {'age': (18, 65), 'status': 'active'}
        """
        if filter_conditions is None:
            return df
        
        filtered_df = df.copy()
        
        for column, condition in filter_conditions.items():
            if column not in filtered_df.columns:
                logger.warning(f"Column '{column}' not found in dataframe")
                continue
            
            if isinstance(condition, tuple) and len(condition) == 2:
                # Range filter (min, max)
                filtered_df = filtered_df[
                    (filtered_df[column] >= condition[0]) & 
                    (filtered_df[column] <= condition[1])
                ]
            else:
                # Exact match filter
                filtered_df = filtered_df[filtered_df[column] == condition]
        
        logger.info(f"Filtered data: {len(df)} rows -> {len(filtered_df)} rows")
        return filtered_df
    
    def aggregate_data(self, df, group_by_column, agg_dict=None):
        """
        Aggregate data by grouping
        group_by_column: column to group by
        agg_dict: aggregation functions dictionary
        Example: {'salary': 'mean', 'age': 'max', 'count': 'count'}
        """
        if agg_dict is None:
            agg_dict = {col: 'count' for col in df.select_dtypes(include=['number']).columns}
        
        try:
            aggregated = df.groupby(group_by_column).agg(agg_dict).reset_index()
            logger.info(f"Aggregated data by '{group_by_column}'")
            return aggregated
        except Exception as e:
            logger.error(f"Error during aggregation: {e}")
            return df
    
    def transform(self, df, config=None):
        """
        Main transformation function
        config: transformation configuration dictionary
        """
        logger.info("Starting data transformation...")
        transformed_df = df.copy()
        
        # 1. Normalize gender column if it exists
        if 'gender' in transformed_df.columns:
            logger.info("Normalizing gender values...")
            transformed_df['gender'] = transformed_df['gender'].apply(self.normalize_gender)
        
        # 2. Format date columns
        date_columns = config.get('date_columns', []) if config else []
        for col in date_columns:
            if col in transformed_df.columns:
                logger.info(f"Formatting date column: {col}")
                transformed_df[col] = transformed_df[col].apply(
                    self.format_date
                )
        
        # 3. Remove duplicates
        if config and config.get('remove_duplicates', True):
            logger.info("Removing duplicate rows...")
            transformed_df = transformed_df.drop_duplicates()
        
        # 4. Handle missing values
        if config and config.get('fill_missing_values'):
            fill_rules = config.get('fill_missing_values')
            for col, fill_value in fill_rules.items():
                if col in transformed_df.columns:
                    logger.info(f"Filling missing values in {col} with {fill_value}")
                    transformed_df[col] = transformed_df[col].fillna(fill_value)
        
        # 5. Select and rename columns (column mapping)
        if config and config.get('column_mapping'):
            column_mapping = config.get('column_mapping')
            logger.info(f"Selecting and renaming columns...")
            
            # Select only specified columns
            selected_cols = list(column_mapping.keys())
            available_cols = [col for col in selected_cols if col in transformed_df.columns]
            
            transformed_df = transformed_df[available_cols]
            
            # Rename columns
            transformed_df = transformed_df.rename(columns=column_mapping)
            logger.info(f"Reduced columns from {len(df.columns)} to {len(transformed_df.columns)}")
        
        logger.info("Transformation completed successfully!")
        self.transformed_data = transformed_df
        return transformed_df


class ETLPipeline:
    """Main ETL Pipeline orchestrator"""
    
    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.transformer = DataTransformer()
        self.data = None
        self.transformed_data = None
        
    def extract(self, filename):
        """Extract data from input file"""
        file_path = self.input_path / filename
        
        try:
            logger.info(f"Extracting data from: {file_path}")
            
            if file_path.suffix == '.csv':
                self.data = pd.read_csv(file_path)
            elif file_path.suffix in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            logger.info(f"Extracted {len(self.data)} rows and {len(self.data.columns)} columns")
            logger.info(f"Columns: {list(self.data.columns)}")
            
            return self.data
        
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            raise
    
    def transform(self, config=None):
        """Transform data"""
        if self.data is None:
            raise ValueError("No data to transform. Run extract() first.")
        
        self.transformed_data = self.transformer.transform(self.data, config)
        return self.transformed_data
    
    def load(self, output_filename='output.csv', database_table=None):
        """Load transformed data to output and optionally to database"""
        if self.transformed_data is None:
            raise ValueError("No transformed data to load. Run transform() first.")
        
        try:
            # Save to CSV
            output_file = self.output_path / output_filename
            self.transformed_data.to_csv(output_file, index=False)
            logger.info(f"Data loaded to: {output_file}")
            
            # Display summary
            logger.info(f"\nOutput Summary:")
            logger.info(f"Rows: {len(self.transformed_data)}")
            logger.info(f"Columns: {len(self.transformed_data.columns)}")
            logger.info(f"Columns: {list(self.transformed_data.columns)}")
            
            return output_file
        
        except Exception as e:
            logger.error(f"Error during load: {e}")
            raise
    
    def run(self, input_filename, output_filename='output.csv', config=None):
        """Execute full ETL pipeline"""
        logger.info("=" * 60)
        logger.info("Starting ETL Pipeline")
        logger.info("=" * 60)
        
        try:
            self.extract(input_filename)
            self.transform(config)
            self.load(output_filename)
            
            logger.info("=" * 60)
            logger.info("ETL Pipeline Completed Successfully!")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


def create_sample_data():
    """Create sample input data for testing"""
    sample_data = {
        'emp_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
        'last_name': ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez'],
        'gender': ['M', 'F', 'male', 'female', 'MM', 'ff', '0', 'M', 'F', None],
        'dob': ['1990-01-15', '1992-03-22', '1988-06-10', '1995-12-05', '1987-04-18', 
                '1993-07-30', '1991-09-12', '1989-02-28', '1994-11-08', '1986-05-25'],
        'hire_date': ['2015-06-01', '2016-08-15', '2014-03-20', '2017-01-10', '2018-07-05',
                      '2015-11-18', '2019-02-14', '2016-09-30', '2017-05-22', '2015-12-01'],
        'salary': [50000, 65000, 55000, 72000, 48000, 68000, 52000, 61000, 58000, 70000],
        'department': ['IT', 'HR', 'IT', 'Finance', 'Sales', 'HR', 'IT', 'Finance', 'Sales', 'IT'],
        'age': [34, 32, 36, 29, 37, 31, 33, 35, 30, 38],
        'status': ['active', 'active', 'inactive', 'active', 'active', 'active', 'inactive', 'active', 'active', 'active']
    }
    
    df = pd.DataFrame(sample_data)
    return df


if __name__ == "__main__":
    # Define paths relative to the script location
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'data'
    output_dir = script_dir / 'output'
    
    # Create sample data
    sample_df = create_sample_data()
    input_dir.mkdir(exist_ok=True)
    sample_df.to_csv(input_dir / 'input_data.csv', index=False)
    logger.info(f"Sample data created at: {input_dir / 'input_data.csv'}")
    
    # Define transformation configuration
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
    
    # Run ETL pipeline
    pipeline = ETLPipeline(input_dir, output_dir)
    pipeline.run('input_data.csv', 'transformed_output.csv', config)
