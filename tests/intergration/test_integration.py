import pytest
import extract_data
import important_features
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# @pytest.mark.parametrize("test_directory, test_file_number", [
#     ("tests/intergration/test_files/", "1"),
# ])
def test_case_data_integration():
    # Извлекаем данные из файла с использованием функции get_data_from_file
    extracted = extract_data.get_data_from_file("tests/intergration/test_files/", '1')
    assert extracted is not None, "Данные не были извлечены"

    # Фильтруем текст с использованием CleanText (предполагаем, что она возвращает кортеж)
    filtered = important_features.CleanText("tests/intergration/test_files/", "case_1.pdf")
    
    assert filtered is not None, "Фильтрация признаков не сработала"

    # Проверим ключевые данные
    assert filtered[0] not in (None, '', "Не найдено"), "Текст не был извлечен корректно"
    assert filtered[1] not in (None, '', "Не найдено"), "Судья не была извлечена корректно"
