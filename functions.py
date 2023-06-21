
import pandas as pd
import numpy as np
from typing import Dict

def format_columns(df: pd.DataFrame, column_renames: Dict[str, str] ) -> pd.DataFrame:
    '''
    This function takes a DataFrame and 
    (1) formats column names to lower case and removes white spaces and
    (2) renames columns according to the input dictionary.
    
    Inputs:
    df: input DataFrame
    column_renames: Dictionary with column renaming
    
    Outputs:
    formatted DataFrame
    '''
    df_formatted = df.copy()
    df_formatted.columns = [col.lower().replace(' ','_') for col in df.columns] # remove white spaces & lower cased
    df_formatted.rename(columns = column_renames, inplace = True) # rename columns according to dictionary
    
    return df_formatted


def clean_gender_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function cleans the 'gender' column by homogenizeing 
    all values to either 'M' or 'F' according to its first character.
    Unknnown values will be filled with its modal value.
    
    Inputs:
    data: input dataframe that includes a 'gender' column
    
    Outputs:
    DataFrame with a cleaned 'gender' column.
    '''
    df1 = df.copy()
    
    # transform to upper case & homogenize values to M or F according to first character. Unknowns -> mode
    df1['gender'] = [x[0].upper() if type(x) == str and x[0].upper() in ['M', 'F'] else df1['gender'].mode()[0] for x in df1['gender']]

    return df1


def replace_and_transform_to_numerical_column(df: pd.DataFrame, column:str, replacements: list) -> pd.DataFrame:
    '''
    This function takes a Dataframe and applies the following transformations:
    (1) replaces specified values in the columns listed in replacements
    (2) assigns float data type to column
    
    Inputs:
    df: input DataFrame
    column: column to apply transformations
    replacements: list of lists with replacements 
        [[old_value1, new_value1],[old_value2, new_value2],...]
    '''
    df1 = df.copy()
    
    for item in replacements:
        df1[column] = df1[column].str.replace(item[0],item[1]) # replace items in column
        
    df1[column] = df1[column].astype(float) # reassign column data type to float
        
    return df1


def remove_duplicate_and_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function removes duplicate rows and rows with all the columns empty.
    
    Input:
    df: input DataFrame
    
    Output:
    df: output DataFrame
    '''
    df1 = df.copy()
    
    df1.drop_duplicates(inplace = True) # drop all duplicate rows
    df1.dropna(inplace = True) # drop all empty rows
    
    return df1


def clean_and_format_data(df: pd.DataFrame, column_renames: Dict[str, str], 
                          numerical_cols_to_replace: Dict[str, list], ) -> pd.DataFrame:
    '''
    
    '''
    df1 = df.copy()
    
    df1 = format_columns(df1,column_renames)# format & rename columns
    
    df1 = clean_gender_column(df1)# clean gender column
    
    for key, value in numerical_cols_to_replace.items():
        df1 = replace_and_transform_to_numerical_column(df1, key, value)# replace and turn to numerical cols
        
    df1 = remove_duplicate_and_empty_rows(df1)# remove duplicate and empty rows
    
    return df1
