import os
import shutil
import tempfile
import pandas as pd
import pytest

from export_to_excel import create_empty_excel, make_excel_file, columns

@pytest.fixture(autouse=True)
def cleanup_excel_files():
    # Remove 'excel_files' directory before and after each test to ensure isolation
    if os.path.exists('excel_files'):
        shutil.rmtree('excel_files')
    yield
    if os.path.exists('excel_files'):
        shutil.rmtree('excel_files')

def test_create_empty_excel_creates_file_and_directory():
    filename = 'testfile.xlsx'
    sheet_name = 'test_sheet'
    filepath, df = create_empty_excel(columns, filename, sheet_name=sheet_name)
    assert os.path.exists('excel_files')
    assert os.path.isfile(filepath)
    # Check that the Excel file contains the correct sheet and columns
    excel = pd.ExcelFile(filepath)
    assert sheet_name in excel.sheet_names
    read_df = pd.read_excel(filepath, sheet_name=sheet_name)
    assert list(read_df.columns) == columns

def test_make_excel_file_populates_data_correctly(monkeypatch):
    # Prepare a minimal DataFrame and dict for population
    filename = 'test_populate.xlsx'
    filepath, df = create_empty_excel(columns, filename)
    # Prepare a dict with two files, each with all columns
    test_dict = {
        '1': [1, 'text1', 'clean1', 'judge1', 'case1', '2020-01-01', 'art1', 100, 'claim1', 'def1', 'data1', 'loc1', 'dec1'],
        '2': [2, 'text2', 'clean2', 'judge2', 'case2', '2020-01-02', 'art2', 200, 'claim2', 'def2', 'data2', 'loc2', 'dec2'],
    }
    # Patch the global dict and df in the module
    import export_to_excel
    export_to_excel.dict = test_dict
    export_to_excel.df = df
    excel_directory = filepath
    make_excel_file(2, excel_directory)
    result_df = pd.read_excel(filepath)
    # There should be two rows, and their values should match test_dict
    assert len(result_df) == 2
    for i, row in result_df.iterrows():
        expected = test_dict[str(i+1)]
        assert list(row) == expected

def test_create_empty_excel_returns_filepath_and_dataframe():
    filename = 'test_returns.xlsx'
    filepath, df = create_empty_excel(columns, filename)
    assert isinstance(filepath, str)
    assert filepath.endswith(filename)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == columns

def test_make_excel_file_with_zero_files(monkeypatch):
    filename = 'test_zero.xlsx'
    filepath, df = create_empty_excel(columns, filename)
    import export_to_excel
    export_to_excel.dict = {}
    export_to_excel.df = df
    excel_directory = filepath
    make_excel_file(0, excel_directory)
    result_df = pd.read_excel(filepath)
    # Should only have headers, no rows
    assert result_df.empty
    assert list(result_df.columns) == columns

def test_make_excel_file_with_missing_data(monkeypatch):
    filename = 'test_missing.xlsx'
    filepath, df = create_empty_excel(columns, filename)
    # Only provide partial data for one file
    test_dict = {
        '1': [1, 'text1', 'clean1'],  # Only 3 out of 13 columns
    }
    import export_to_excel
    export_to_excel.dict = test_dict
    export_to_excel.df = df
    excel_directory = filepath
    make_excel_file(1, excel_directory)
    result_df = pd.read_excel(filepath)
    assert len(result_df) == 1
    # The first three columns should be filled, the rest should be NaN
    row = result_df.iloc[0]
    assert row['index'] == 1
    assert row['text'] == 'text1'
    assert row['clean_text'] == 'clean1'
    # All other columns should be NaN (pandas uses NaN for missing data)
    for col in columns[3:]:
        assert pd.isna(row[col])

def test_create_empty_excel_permission_error(tmp_path):
    # Try to create an Excel file in a directory without write permission
    # On Unix, /root is usually not writable; on Windows, use an invalid path
    if os.name == 'nt':
        invalid_dir = 'Z:\\this\\path\\does\\not\\exist'
    else:
        invalid_dir = '/root/excel_files'
    filename = 'should_fail.xlsx'
    # Temporarily patch os.makedirs to raise PermissionError
    orig_makedirs = os.makedirs
    def raise_perm(*args, **kwargs):
        raise PermissionError("No permission to create directory")
    os.makedirs = raise_perm
    try:
        with pytest.raises(PermissionError):
            create_empty_excel(columns, filename)
    finally:
        os.makedirs = orig_makedirs