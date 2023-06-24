
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
    df1['gender'] = [x[0].upper() if type(x) == str and x[0].upper() in ['M', 'F'] else df1['gender'].mode()[0] 
                     for x in df1['gender']]

    return df1

def clean_number_of_complains_column(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function cleans the 'number_of_complains' column by parsing 
    the date format column and getting the value in the month position
    as the number of complains.
    
    Inputs:
    data: input dataframe that includes a 'number_of_open_complaints' column
    
    Outputs:
    DataFrame with a cleaned 'number_of_open_complaints' column.
    '''
    df1 = df.copy()

    df1['number_of_open_complaints'] = [ str(x).split('/')[1] if (type(x) is str) and ('/' in x) else x 
                                         for x in df1['number_of_open_complaints']]
    
    return df1


def clean_column_by_replacing_string(df: pd.DataFrame, column:str, replacements: list) -> pd.DataFrame:
    '''
    This function takes a Dataframe and replaces the strings 
    in the input replacements to the specified column.
    
    Inputs:
    df: input DataFrame
    column: column to apply transformations
    replacements: list of lists with replacements 
        [[old_value1, new_value1],[old_value2, new_value2],...]
        
    Output:
    pandas DataFrame with the clean column
    '''
    df1 = df.copy()
    
    for item in replacements:
        df1[column] = df1[column].str.replace(item[0],item[1]) # replace items in column
        
    return df1

def reassign_column_data_type(df: pd.DataFrame, columns: Dict[str, str]) -> pd.DataFrame:
    '''
    This function takes a DataFrame and reassigns data types as specified in the columns parameter.
    
    Input: 
    df: pandas DataFrame
    columns: Dictionary with column and data type assignment
    
    Output:
    Dataframe with data type reassign columns
    '''
    
    for key, value in columns.items():
        df[key] = df[key].astype(value)

    return df


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


def clean_and_format_data(df: pd.DataFrame, 
                          cols_to_rename: Dict[str, str], 
                          cols_to_replace: Dict[str, list],
                          cols_to_reassign_datatype: Dict[str,str]) -> pd.DataFrame:
    '''
    This function executes all the cleaning functions on the input df in 4 steps:
    (1) formats and renames column names
    (2) removes duplicate and empty rows
    (3) cleans the gender column
    (4) cleans number_of_complaints column
    (5) applies character replacements
    (6) reassigns data types
    
    Inputs:
    df: input Dataframe
    cols_to_rename: Dictionary with columns to rename
    cols_to_replace: Dictionary with columns to apply replacements
    cols_to_reassign_datatype: Dictionary with columns to reassign datatype
    
    Output:
    pandas DataFrame with clean and formatted data
    '''
    df1 = df.copy()
    
    df1 = format_columns(df1,cols_to_rename)# format & rename columns
    df1 = remove_duplicate_and_empty_rows(df1)# remove duplicate and empty rows
    df1 = clean_gender_column(df1)# clean gender column
    df1 = clean_number_of_complains_column(df1)# clean number_of_complain_column
    for key, value in cols_to_replace.items():
        df1 = clean_column_by_replacing_string(df1, key, value)# replace cleaning
    df1 = reassign_column_data_type(df1, cols_to_reassign_datatype)# reassign data types
        
    return df1
