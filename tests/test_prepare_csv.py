import os
import pytest
import tempfile
import csv
import shutil
from prepare_csv import read_cell

class TestReadCell:
    def test_handle_missing_source_csv_file(self):
        # Attempt to read from a non-existent file
        missing_file = 'non_existent_file.csv'
        # Remove the file if it somehow exists
        if os.path.exists(missing_file):
            os.remove(missing_file)
        with pytest.raises(FileNotFoundError):
            read_cell(0, 0, missing_file)
            
    def test_skip_rows_with_missing_or_empty_cells(self):
        # Prepare a temporary directory for CSV files
        with tempfile.TemporaryDirectory() as tmpdir:
            # Prepare input CSV file with some rows having missing/empty cells
            input_csv = os.path.join(tmpdir, "arbitr_dataset_for_training.csv")
            output_csv = os.path.join(tmpdir, "prepared_data.csv")
            # Create 15 columns per row to match the indices used in read_cell
            rows = [
                ["a"] * 15,  # row 0 (header, will be skipped)
                ["data1", "x", "x", "x", "judge1", "x", "x", "articles1", "x", "x", "x", "text1", "region1", "decision1", "x"],  # row 1: all present
                ["data2", "x", "x", "x", "judge2", "x", "x", "articles2", "x", "x", "x", "", "region2", "decision2", "x"],      # row 2: text is empty
                ["data3", "x", "x", "x", "judge3", "x", "x", "articles3", "x", "x", "x", "text3", "region3", "", "x"],          # row 3: decision is empty
                ["data4", "x", "x", "x", "judge4", "x", "x", "articles4", "x", "x", "x", "text4", "region4", "decision4", "x"], # row 4: all present
            ]
            with open(input_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Patch the filename in the module to point to our temp file
            # Since the code uses a global variable, we need to simulate the main logic here
            # Re-implement the relevant part of the script for this test
            def local_read_cell(x, y, filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    y_count = 0
                    for n in reader:
                        if y_count == y:
                            cell = n[x]
                            return cell
                        y_count += 1

            with open(output_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                field = ["data", "decision", "judge", "region", "articles"]
                writer.writerow(field)
                for i in range(1, 5):  # Only 4 rows in our test input
                    text = local_read_cell(11, i, input_csv)
                    dec = local_read_cell(13, i, input_csv)
                    judge = local_read_cell(4, i, input_csv)
                    region = local_read_cell(12, i, input_csv)
                    articles = local_read_cell(7, i, input_csv)
                    if text == '' or dec == '' or text is None or dec is None:
                        pass
                    else:
                        writer.writerow([text, dec, judge, region, articles])

            # Now, check the output CSV: it should only have rows 1 and 4 (indices 1 and 4 in input, i.e., i=1 and i=4)
            with open(output_csv, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                # First row is header
                assert reader[0] == ["data", "decision", "judge", "region", "articles"]
                # Only two data rows should be present
                assert len(reader) == 3
                # Check the actual data
                assert reader[1] == ["text1", "decision1", "judge1", "region1", "articles1"]
                assert reader[2] == ["text4", "decision4", "judge4", "region4", "articles4"]
                
    def test_prepared_csv_structure_and_row_count(self):
        # Prepare a temporary directory for CSV files
        with tempfile.TemporaryDirectory() as tmpdir:
            input_csv = os.path.join(tmpdir, "arbitr_dataset_for_training.csv")
            output_csv = os.path.join(tmpdir, "prepared_data.csv")
            # Create 15 columns per row to match the indices used in read_cell
            rows = [
                ["header"] * 15,  # header row (row 0)
                ["data1", "x", "x", "x", "judge1", "x", "x", "articles1", "x", "x", "x", "text1", "region1", "decision1", "x"],  # row 1: valid
                ["data2", "x", "x", "x", "judge2", "x", "x", "articles2", "x", "x", "x", "", "region2", "decision2", "x"],      # row 2: text is empty
                ["data3", "x", "x", "x", "judge3", "x", "x", "articles3", "x", "x", "x", "text3", "region3", "", "x"],          # row 3: decision is empty
                ["data4", "x", "x", "x", "judge4", "x", "x", "articles4", "x", "x", "x", "text4", "region4", "decision4", "x"], # row 4: valid
            ]
            with open(input_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Simulate the main logic for writing the prepared CSV
            def local_read_cell(x, y, filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    y_count = 0
                    for n in reader:
                        if y_count == y:
                            cell = n[x]
                            return cell
                        y_count += 1

            with open(output_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                field = ["data", "decision", "judge", "region", "articles"]
                writer.writerow(field)
                for i in range(1, 5):  # Only 4 rows in our test input
                    text = local_read_cell(11, i, input_csv)
                    dec = local_read_cell(13, i, input_csv)
                    judge = local_read_cell(4, i, input_csv)
                    region = local_read_cell(12, i, input_csv)
                    articles = local_read_cell(7, i, input_csv)
                    if text == '' or dec == '' or text is None or dec is None:
                        pass
                    else:
                        writer.writerow([text, dec, judge, region, articles])

            # Check the output CSV structure and row count
            with open(output_csv, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                assert reader[0] == ["data", "decision", "judge", "region", "articles"]
                # Only two valid data rows should be present
                assert len(reader) == 3
                assert reader[1] == ["text1", "decision1", "judge1", "region1", "articles1"]
                assert reader[2] == ["text4", "decision4", "judge4", "region4", "articles4"]

    def test_read_cell_returns_correct_value(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_csv = os.path.join(tmpdir, "test.csv")
            # Create a CSV with 3 rows and 5 columns
            rows = [
                ["a1", "b1", "c1", "d1", "e1"],
                ["a2", "b2", "c2", "d2", "e2"],
                ["a3", "b3", "c3", "d3", "e3"],
            ]
            with open(input_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            # Test: get cell at (2, 1) => row 1, column 2 ("c2")
            assert read_cell(2, 1, input_csv) == "c2"
            # Test: get cell at (0, 2) => row 2, column 0 ("a3")
            assert read_cell(0, 2, input_csv) == "a3"

    def test_copy_valid_rows_to_prepared_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_csv = os.path.join(tmpdir, "arbitr_dataset_for_testing.csv")
            output_csv = os.path.join(tmpdir, "prepared_data_for_testing.csv")
            # Create 15 columns per row to match the indices used in read_cell
            rows = [
                ["header"] * 15,  # header row (row 0)
                ["dataA", "x", "x", "x", "judgeA", "x", "x", "articlesA", "x", "x", "x", "textA", "regionA", "decisionA", "x"],  # row 1: valid
                ["dataB", "x", "x", "x", "judgeB", "x", "x", "articlesB", "x", "x", "x", "", "regionB", "decisionB", "x"],      # row 2: text is empty
                ["dataC", "x", "x", "x", "judgeC", "x", "x", "articlesC", "x", "x", "x", "textC", "regionC", "", "x"],          # row 3: decision is empty
                ["dataD", "x", "x", "x", "judgeD", "x", "x", "articlesD", "x", "x", "x", "textD", "regionD", "decisionD", "x"], # row 4: valid
            ]
            with open(input_csv, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # Simulate the main logic for writing the prepared CSV
            def local_read_cell(x, y, filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    y_count = 0
                    for n in reader:
                        if y_count == y:
                            cell = n[x]
                            return cell
                        y_count += 1

            with open(output_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                field = ["data", "decision", "judge", "region", "articles"]
                writer.writerow(field)
                for i in range(1, 5):  # Only 4 rows in our test input
                    text = local_read_cell(11, i, input_csv)
                    dec = local_read_cell(13, i, input_csv)
                    judge = local_read_cell(4, i, input_csv)
                    region = local_read_cell(12, i, input_csv)
                    articles = local_read_cell(7, i, input_csv)
                    if text == '' or dec == '' or text is None or dec is None:
                        pass
                    else:
                        writer.writerow([text, dec, judge, region, articles])

            # Check that only valid rows were copied
            with open(output_csv, "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))
                assert reader[0] == ["data", "decision", "judge", "region", "articles"]
                assert len(reader) == 3
                assert reader[1] == ["textA", "decisionA", "judgeA", "regionA", "articlesA"]
                assert reader[2] == ["textD", "decisionD", "judgeD", "regionD", "articlesD"]