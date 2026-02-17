"""
Advanced ETL Pipeline with Error Handling and Auto-Rectification
- Graceful error recovery
- Detailed error logging
- Automatic data validation and correction
- Pipeline health monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging
import traceback
import json
from typing import Dict, List, Tuple, Optional

# Configure logging with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)


class PipelineError(Exception):
    """Custom exception for pipeline errors"""
    pass


class ErrorHandler:
    """Handles and rectifies pipeline errors"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.corrections = []
    
    def log_error(self, stage, error_msg, details=None):
        """Log error with stage information"""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'error': error_msg,
            'details': details,
            'traceback': traceback.format_exc()
        }
        self.errors.append(error_record)
        logger.error(f"[{stage}] {error_msg}")
        if details:
            logger.error(f"  Details: {details}")
    
    def log_warning(self, stage, warning_msg):
        """Log warning"""
        warning_record = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'warning': warning_msg
        }
        self.warnings.append(warning_record)
        logger.warning(f"[{stage}] {warning_msg}")
    
    def log_correction(self, stage, action, affected_rows):
        """Log automatic correction"""
        correction_record = {
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'action': action,
            'affected_rows': affected_rows
        }
        self.corrections.append(correction_record)
        logger.info(f"[{stage}] Correction: {action} ({affected_rows} rows)")
    
    def get_error_report(self):
        """Generate error report"""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'total_corrections': len(self.corrections),
            'errors': self.errors,
            'warnings': self.warnings,
            'corrections': self.corrections
        }
    
    def save_error_log(self, output_path):
        """Save error log to file"""
        error_log_path = output_path / 'error_log.json'
        with open(error_log_path, 'w') as f:
            json.dump(self.get_error_report(), f, indent=2)
        logger.info(f"Error log saved to: {error_log_path}")


class DataValidator:
    """Validates and rectifies data"""
    
    def __init__(self, error_handler):
        self.error_handler = error_handler
    
    def validate_file_exists(self, file_path):
        """Check if file exists"""
        if not file_path.exists():
            self.error_handler.log_error(
                'validation',
                f"File not found: {file_path}",
                "This file is required for processing"
            )
            return False
        logger.info(f"✓ File exists: {file_path}")
        return True
    
    def validate_dataframe(self, df, source_name):
        """Validate dataframe structure"""
        issues = []
        
        if df is None or df.empty:
            issues.append("DataFrame is empty")
        
        if len(df.columns) == 0:
            issues.append("DataFrame has no columns")
        
        if len(df) == 0:
            issues.append("DataFrame has no rows")
        
        if issues:
            self.error_handler.log_warning(source_name, f"Issues: {', '.join(issues)}")
            return False
        
        logger.info(f"✓ DataFrame valid: {len(df)} rows, {len(df.columns)} columns")
        return True
    
    def rectify_missing_columns(self, df, required_columns, source_name):
        """Rectify missing columns by adding them with null values"""
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            self.error_handler.log_warning(
                source_name,
                f"Missing columns detected: {missing_cols}"
            )
            for col in missing_cols:
                df[col] = None
                self.error_handler.log_correction(
                    source_name,
                    f"Added missing column: {col} (filled with None)",
                    len(df)
                )
        
        return df
    
    def rectify_data_types(self, df):
        """Rectify data type issues"""
        corrections_made = 0
        
        for col in df.columns:
            try:
                if 'date' in col.lower() or 'dob' in col.lower():
                    # Try to convert to datetime
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    corrections_made += 1
                elif 'salary' in col.lower() or col in ['salary', 'pay', 'annual_salary', 'compensation']:
                    # Try to convert to numeric
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    corrections_made += 1
            except Exception as e:
                self.error_handler.log_warning(
                    'type_rectification',
                    f"Could not convert {col}: {str(e)}"
                )
        
        if corrections_made > 0:
            self.error_handler.log_correction(
                'data_type_fix',
                f"Rectified data types for {corrections_made} columns",
                len(df)
            )
        
        return df
    
    def rectify_duplicates(self, df, source_name):
        """Rectify duplicate rows"""
        initial_count = len(df)
        df = df.drop_duplicates()
        removed = initial_count - len(df)
        
        if removed > 0:
            self.error_handler.log_correction(
                source_name,
                f"Removed duplicate rows",
                removed
            )
        
        return df
    
    def rectify_missing_values(self, df, fill_rules=None):
        """Rectify missing values"""
        if fill_rules is None:
            fill_rules = {}
        
        for col, fill_value in fill_rules.items():
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    df[col] = df[col].fillna(fill_value)
                    self.error_handler.log_correction(
                        'missing_values',
                        f"Filled {missing_count} missing values in {col} with '{fill_value}'",
                        missing_count
                    )
        
        return df


class RobustMultiSourceETL:
    """Robust ETL Pipeline with comprehensive error handling"""
    
    def __init__(self, input_path, output_path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.error_handler = ErrorHandler()
        self.validator = DataValidator(self.error_handler)
        self.data_sources = {}
        self.consolidated_data = None
        self.transformed_data = None
        self.pipeline_status = 'initialized'
    
    def register_source(self, source_name, filename, column_mapping):
        """Register a data source"""
        try:
            self.data_sources[source_name] = {
                'filename': filename,
                'mapping': column_mapping,
                'data': None,
                'status': 'registered'
            }
            logger.info(f"✓ Registered source: {source_name} ← {filename}")
        except Exception as e:
            self.error_handler.log_error(
                'registration',
                f"Failed to register source {source_name}",
                str(e)
            )
    
    def extract_source(self, source_name):
        """Extract data from single source with error handling"""
        try:
            source_info = self.data_sources[source_name]
            file_path = self.input_path / source_info['filename']
            
            # Validate file exists
            if not self.validator.validate_file_exists(file_path):
                self.data_sources[source_name]['status'] = 'file_not_found'
                return None
            
            # Read file
            try:
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                elif file_path.suffix in ['.xlsx', '.xls']:
                    df = pd.read_excel(file_path)
                else:
                    raise ValueError(f"Unsupported file format: {file_path.suffix}")
                
                logger.info(f"✓ Extracted {source_name}: {len(df)} rows, {len(df.columns)} columns")
                self.data_sources[source_name]['status'] = 'extracted'
                
            except Exception as e:
                self.error_handler.log_error(
                    f'extraction_{source_name}',
                    f"Failed to read file: {file_path}",
                    str(e)
                )
                self.data_sources[source_name]['status'] = 'extraction_failed'
                return None
            
            # Validate dataframe
            if not self.validator.validate_dataframe(df, source_name):
                self.data_sources[source_name]['status'] = 'validation_failed'
                return None
            
            return df
        
        except Exception as e:
            self.error_handler.log_error(
                'extract_source',
                f"Unexpected error extracting {source_name}",
                str(e)
            )
            self.data_sources[source_name]['status'] = 'error'
            return None
    
    def map_columns(self, df, source_name):
        """Map columns with error handling"""
        try:
            mapping = self.data_sources[source_name]['mapping']
            
            # Check for missing columns and rectify
            available_cols = [col for col in mapping.keys() if col in df.columns]
            missing_cols = [col for col in mapping.keys() if col not in df.columns]
            
            if missing_cols:
                self.error_handler.log_warning(
                    f'mapping_{source_name}',
                    f"Missing columns in mapping: {missing_cols}"
                )
            
            # Select and rename available columns
            if available_cols:
                df_mapped = df[available_cols].copy()
                df_mapped = df_mapped.rename(columns={col: mapping[col] for col in available_cols})
                df_mapped['source'] = source_name
                
                logger.info(f"✓ Mapped {source_name}: {len(available_cols)} columns")
                self.data_sources[source_name]['status'] = 'mapped'
                return df_mapped
            else:
                self.error_handler.log_error(
                    f'mapping_{source_name}',
                    "No columns could be mapped",
                    f"Available cols: {df.columns.tolist()}"
                )
                self.data_sources[source_name]['status'] = 'mapping_failed'
                return None
        
        except Exception as e:
            self.error_handler.log_error(
                f'map_columns_{source_name}',
                "Error during column mapping",
                str(e)
            )
            self.data_sources[source_name]['status'] = 'mapping_error'
            return None
    
    def extract_and_map_all(self):
        """Extract and map all sources with graceful failure handling"""
        logger.info("\n" + "="*70)
        logger.info("EXTRACT & MAP PHASE")
        logger.info("="*70)
        
        successful_sources = 0
        failed_sources = []
        
        for source_name in self.data_sources.keys():
            try:
                logger.info(f"\nProcessing {source_name}...")
                
                # Extract
                df = self.extract_source(source_name)
                if df is None:
                    failed_sources.append(source_name)
                    continue
                
                # Map columns
                df_mapped = self.map_columns(df, source_name)
                if df_mapped is None:
                    failed_sources.append(source_name)
                    continue
                
                # Rectify data types
                df_mapped = self.validator.rectify_data_types(df_mapped)
                
                # Rectify duplicates
                df_mapped = self.validator.rectify_duplicates(df_mapped, source_name)
                
                self.data_sources[source_name]['data'] = df_mapped
                successful_sources += 1
                logger.info(f"✓ {source_name} processed successfully")
            
            except Exception as e:
                self.error_handler.log_error(
                    f'extract_and_map_{source_name}',
                    f"Unexpected error processing {source_name}",
                    str(e)
                )
                failed_sources.append(source_name)
        
        logger.info(f"\n✓ Successfully processed: {successful_sources} sources")
        if failed_sources:
            logger.warning(f"⚠ Failed sources: {failed_sources}")
        
        return successful_sources > 0
    
    def consolidate(self):
        """Consolidate all sources"""
        try:
            logger.info("\n" + "="*70)
            logger.info("CONSOLIDATION PHASE")
            logger.info("="*70)
            
            dataframes = []
            for source_name, source_info in self.data_sources.items():
                if source_info['data'] is not None:
                    dataframes.append(source_info['data'])
            
            if not dataframes:
                self.error_handler.log_error(
                    'consolidation',
                    "No data sources to consolidate",
                    "All sources failed to process"
                )
                return False
            
            self.consolidated_data = pd.concat(dataframes, ignore_index=True, sort=False)
            logger.info(f"✓ Consolidated {len(dataframes)} sources into {len(self.consolidated_data)} rows")
            return True
        
        except Exception as e:
            self.error_handler.log_error(
                'consolidation',
                "Failed to consolidate data",
                str(e)
            )
            return False
    
    def normalize_gender(self, gender_value):
        """Normalize gender values"""
        try:
            if pd.isna(gender_value):
                return 'Unknown'
            
            gender_str = str(gender_value).strip().lower()
            
            if gender_str in ['m', 'mm', 'male', '1']:
                return 'M'
            elif gender_str in ['f', 'ff', 'female', '2']:
                return 'F'
            elif gender_str in ['0', 'unknown']:
                return 'Unknown'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def format_date(self, date_value):
        """Format date to YYYY-MM-DD"""
        try:
            if pd.isna(date_value):
                return None
            
            parsed_date = pd.to_datetime(date_value, errors='coerce')
            if pd.isna(parsed_date):
                return None
            
            return parsed_date.strftime('%Y-%m-%d')
        except:
            return None
    
    def transform(self, config=None):
        """Transform consolidated data"""
        try:
            logger.info("\n" + "="*70)
            logger.info("TRANSFORMATION PHASE")
            logger.info("="*70)
            
            if self.consolidated_data is None:
                self.error_handler.log_error(
                    'transform',
                    "No consolidated data to transform",
                    "Run consolidate() first"
                )
                return False
            
            transformed = self.consolidated_data.copy()
            
            # Normalize gender
            if 'gender' in transformed.columns:
                logger.info("Normalizing gender values...")
                transformed['gender'] = transformed['gender'].apply(self.normalize_gender)
                logger.info("✓ Gender normalized")
            
            # Format dates
            date_columns = config.get('date_columns', []) if config else []
            for col in date_columns:
                if col in transformed.columns:
                    logger.info(f"Formatting date column: {col}")
                    transformed[col] = transformed[col].apply(self.format_date)
            
            if date_columns:
                logger.info(f"✓ Formatted {len(date_columns)} date columns")
            
            # Rectify missing values
            fill_rules = config.get('fill_missing_values', {}) if config else {}
            if fill_rules:
                logger.info("Filling missing values...")
                transformed = self.validator.rectify_missing_values(transformed, fill_rules)
            
            # Remove duplicates
            if config and config.get('remove_duplicates', True):
                logger.info("Removing duplicates...")
                transformed = self.validator.rectify_duplicates(transformed, 'transform')
            
            # Select final columns
            if config and config.get('final_columns'):
                final_cols = config.get('final_columns')
                available_cols = [col for col in final_cols if col in transformed.columns]
                missing_cols = [col for col in final_cols if col not in transformed.columns]
                
                if missing_cols:
                    self.error_handler.log_warning(
                        'transform',
                        f"Requested columns not in data: {missing_cols}"
                    )
                
                transformed = transformed[available_cols]
                logger.info(f"✓ Selected {len(available_cols)}/{len(final_cols)} final columns")
            
            self.transformed_data = transformed
            logger.info(f"✓ Transformation complete: {len(transformed)} rows, {len(transformed.columns)} columns")
            return True
        
        except Exception as e:
            self.error_handler.log_error(
                'transform',
                "Transformation failed",
                str(e)
            )
            return False
    
    def load(self, output_filename='consolidated_output.csv'):
        """Load transformed data"""
        try:
            logger.info("\n" + "="*70)
            logger.info("LOAD PHASE")
            logger.info("="*70)
            
            if self.transformed_data is None:
                self.error_handler.log_error(
                    'load',
                    "No transformed data to load",
                    "Run transform() first"
                )
                return False
            
            output_file = self.output_path / output_filename
            self.transformed_data.to_csv(output_file, index=False)
            
            logger.info(f"✓ Data saved to: {output_file}")
            logger.info(f"  Rows: {len(self.transformed_data)}")
            logger.info(f"  Columns: {len(self.transformed_data.columns)}")
            
            return True
        
        except Exception as e:
            self.error_handler.log_error(
                'load',
                "Failed to save data",
                str(e)
            )
            return False
    
    def run(self, output_filename='consolidated_output.csv', config=None):
        """Execute full pipeline with comprehensive error handling"""
        logger.info("\n" + "="*80)
        logger.info("ROBUST MULTI-SOURCE ETL PIPELINE")
        logger.info("="*80)
        
        try:
            # Phase 1: Extract and Map
            if not self.extract_and_map_all():
                self.error_handler.log_error(
                    'pipeline',
                    "Extract and map phase failed",
                    "No sources processed successfully"
                )
                self.pipeline_status = 'failed_extract'
                return False
            
            # Phase 2: Consolidate
            if not self.consolidate():
                self.error_handler.log_error(
                    'pipeline',
                    "Consolidation phase failed",
                    "Could not merge sources"
                )
                self.pipeline_status = 'failed_consolidate'
                return False
            
            # Phase 3: Transform
            if not self.transform(config):
                self.error_handler.log_error(
                    'pipeline',
                    "Transformation phase failed",
                    "Could not transform data"
                )
                self.pipeline_status = 'failed_transform'
                return False
            
            # Phase 4: Load
            if not self.load(output_filename):
                self.error_handler.log_error(
                    'pipeline',
                    "Load phase failed",
                    "Could not save output"
                )
                self.pipeline_status = 'failed_load'
                return False
            
            self.pipeline_status = 'completed_successfully'
            logger.info("\n" + "="*80)
            logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*80)
            return True
        
        except Exception as e:
            self.error_handler.log_error(
                'pipeline',
                "Unexpected pipeline error",
                str(e)
            )
            self.pipeline_status = 'failed_unexpected'
            return False
        
        finally:
            # Save error logs
            self.error_handler.save_error_log(self.output_path)
            self.print_error_summary()
    
    def print_error_summary(self):
        """Print error summary"""
        report = self.error_handler.get_error_report()
        
        logger.info("\n" + "="*80)
        logger.info("ERROR & CORRECTION SUMMARY")
        logger.info("="*80)
        logger.info(f"Total Errors: {report['total_errors']}")
        logger.info(f"Total Warnings: {report['total_warnings']}")
        logger.info(f"Total Corrections Made: {report['total_corrections']}")
        logger.info("="*80)
        
        if report['total_errors'] > 0:
            logger.error("\nERRORS:")
            for i, err in enumerate(report['errors'], 1):
                logger.error(f"  {i}. [{err['stage']}] {err['error']}")
                if err['details']:
                    logger.error(f"     {err['details']}")
        
        if report['total_warnings'] > 0:
            logger.warning("\nWARNINGS:")
            for i, warn in enumerate(report['total_warnings'], 1):
                logger.warning(f"  {i}. [{warn['stage']}] {warn['warning']}")
        
        if report['total_corrections'] > 0:
            logger.info("\nCORRECTIONS APPLIED:")
            for i, corr in enumerate(report['corrections'], 1):
                logger.info(f"  {i}. [{corr['stage']}] {corr['action']} ({corr['affected_rows']} rows)")
