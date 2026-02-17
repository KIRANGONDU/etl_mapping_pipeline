"""
Advanced ETL Pipeline with Multi-Source Header Mapping
Handles multiple input files with different column names and consolidates them
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HeaderMapper:
    """Maps different column names from multiple sources to unified schema"""
    
    def __init__(self):
        self.mapping_rules = {}
        self.unified_schema = {}
    
    def add_mapping(self, source_name, column_mapping):
        """
        Add header mapping for a specific source
        
        Example:
        mapper.add_mapping('file1', {
            'emp_id': 'employee_id',
            'fname': 'first_name',
            'lname': 'last_name',
            'sex': 'gender'
        })
        """
        self.mapping_rules[source_name] = column_mapping
        logger.info(f"Added mapping for source: {source_name}")
    
    def set_unified_schema(self, schema_dict):
        """
        Define the unified target schema
        
        Example:
        mapper.set_unified_schema({
            'employee_id': 'int',
            'first_name': 'string',
            'last_name': 'string',
            'gender': 'string',
            'date_of_birth': 'date',
            'annual_salary': 'float'
        })
        """
        self.unified_schema = schema_dict
        logger.info(f"Unified schema set with {len(schema_dict)} fields")
    
    def map_dataframe(self, df, source_name):
        """
        Apply header mapping to a dataframe from specific source
        """
        if source_name not in self.mapping_rules:
            logger.warning(f"No mapping found for source: {source_name}")
            return df
        
        mapping = self.mapping_rules[source_name]
        
        # Check which columns exist in the dataframe
        available_mappings = {}
        for old_col, new_col in mapping.items():
            if old_col in df.columns:
                available_mappings[old_col] = new_col
            else:
                logger.warning(f"Column '{old_col}' not found in {source_name}")
        
        # Rename columns
        df_mapped = df[list(available_mappings.keys())].copy()
        df_mapped = df_mapped.rename(columns=available_mappings)
        
        logger.info(f"Mapped {source_name}: {len(available_mappings)} columns")
        return df_mapped


class MultiSourceETLPipeline:
    """ETL Pipeline that handles multiple sources with different headers"""
    
    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.header_mapper = HeaderMapper()
        self.data_sources = {}
        self.consolidated_data = None
        self.transformed_data = None
    
    def register_source(self, source_name, filename, column_mapping):
        """
        Register a data source with its header mapping
        
        Args:
            source_name: Unique identifier for the source
            filename: Name of the file in input folder
            column_mapping: Dict mapping source columns to unified column names
        """
        self.header_mapper.add_mapping(source_name, column_mapping)
        self.data_sources[source_name] = {
            'filename': filename,
            'mapping': column_mapping,
            'data': None
        }
        logger.info(f"Registered source: {source_name} <- {filename}")
    
    def extract_and_map(self):
        """Extract data from all sources and apply header mapping"""
        logger.info("=" * 60)
        logger.info("Extracting from Multiple Sources")
        logger.info("=" * 60)
        
        for source_name, source_info in self.data_sources.items():
            try:
                file_path = self.input_path / source_info['filename']
                logger.info(f"\nExtracting from: {file_path}")
                
                # Read file
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                elif file_path.suffix in ['.xlsx', '.xls']:
                    df = pd.read_excel(file_path)
                else:
                    raise ValueError(f"Unsupported format: {file_path.suffix}")
                
                logger.info(f"  Original columns: {list(df.columns)}")
                logger.info(f"  Rows: {len(df)}")
                
                # Apply header mapping
                df_mapped = self.header_mapper.map_dataframe(df, source_name)
                logger.info(f"  Mapped columns: {list(df_mapped.columns)}")
                
                # Add source tracking column
                df_mapped['source'] = source_name
                
                self.data_sources[source_name]['data'] = df_mapped
                
            except Exception as e:
                logger.error(f"Error extracting from {source_name}: {e}")
                raise
        
        return self.data_sources
    
    def consolidate(self, how='concat'):
        """
        Consolidate data from all sources
        
        Args:
            how: 'concat' (stack all rows) or 'merge' (join by key)
        """
        logger.info("\n" + "=" * 60)
        logger.info("Consolidating Data from Multiple Sources")
        logger.info("=" * 60)
        
        dataframes = []
        for source_name, source_info in self.data_sources.items():
            if source_info['data'] is not None:
                dataframes.append(source_info['data'])
        
        if not dataframes:
            raise ValueError("No data to consolidate")
        
        if how == 'concat':
            self.consolidated_data = pd.concat(dataframes, ignore_index=True, sort=False)
            logger.info(f"Concatenated {len(dataframes)} sources")
        
        logger.info(f"Consolidated data shape: {self.consolidated_data.shape}")
        logger.info(f"Consolidated columns: {list(self.consolidated_data.columns)}")
        
        return self.consolidated_data
    
    def normalize_gender(self, gender_value):
        """Normalize gender values"""
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
    
    def format_date(self, date_value):
        """Format date to YYYY-MM-DD"""
        try:
            if pd.isna(date_value):
                return None
            
            parsed_date = pd.to_datetime(date_value)
            return parsed_date.strftime('%Y-%m-%d')
        except Exception as e:
            logger.warning(f"Could not parse date: {date_value}")
            return None
    
    def transform(self, config=None):
        """Transform consolidated data"""
        logger.info("\n" + "=" * 60)
        logger.info("Transforming Consolidated Data")
        logger.info("=" * 60)
        
        if self.consolidated_data is None:
            raise ValueError("No consolidated data. Run consolidate() first.")
        
        transformed = self.consolidated_data.copy()
        
        # 1. Normalize gender
        if 'gender' in transformed.columns:
            logger.info("Normalizing gender values...")
            transformed['gender'] = transformed['gender'].apply(self.normalize_gender)
        
        # 2. Format dates
        date_columns = config.get('date_columns', []) if config else []
        for col in date_columns:
            if col in transformed.columns:
                logger.info(f"Formatting date column: {col}")
                transformed[col] = transformed[col].apply(self.format_date)
        
        # 3. Remove duplicates
        if config and config.get('remove_duplicates', True):
            logger.info("Removing duplicate rows...")
            transformed = transformed.drop_duplicates()
        
        # 4. Fill missing values
        if config and config.get('fill_missing_values'):
            fill_rules = config.get('fill_missing_values')
            for col, fill_value in fill_rules.items():
                if col in transformed.columns:
                    logger.info(f"Filling missing values in {col}...")
                    transformed[col] = transformed[col].fillna(fill_value)
        
        # 5. Select final columns
        if config and config.get('final_columns'):
            final_cols = config.get('final_columns')
            available_cols = [col for col in final_cols if col in transformed.columns]
            transformed = transformed[available_cols]
            logger.info(f"Selected final columns: {available_cols}")
        
        self.transformed_data = transformed
        logger.info(f"Transformation complete. Shape: {transformed.shape}")
        
        return transformed
    
    def load(self, output_filename='consolidated_output.csv'):
        """Load transformed data to output folder"""
        if self.transformed_data is None:
            raise ValueError("No transformed data. Run transform() first.")
        
        try:
            output_file = self.output_path / output_filename
            self.transformed_data.to_csv(output_file, index=False)
            logger.info(f"\nData loaded to: {output_file}")
            
            logger.info(f"\nOutput Summary:")
            logger.info(f"  Rows: {len(self.transformed_data)}")
            logger.info(f"  Columns: {len(self.transformed_data.columns)}")
            logger.info(f"  Columns: {list(self.transformed_data.columns)}")
            
            return output_file
        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def run(self, output_filename='consolidated_output.csv', config=None):
        """Execute full multi-source ETL pipeline"""
        logger.info("\n" + "="*60)
        logger.info("MULTI-SOURCE ETL PIPELINE")
        logger.info("="*60)
        
        try:
            self.extract_and_map()
            self.consolidate()
            self.transform(config)
            self.load(output_filename)
            
            logger.info("="*60)
            logger.info("Pipeline Completed Successfully!")
            logger.info("="*60)
            
            return self.transformed_data
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


if __name__ == "__main__":
    pass
