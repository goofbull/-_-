import pytest
import os
import tempfile
import fitz
from important_features import (
    CleanText,
    remove_strings_with_english,
    remove_non_russian_alpha_lines,
    remove_lines_with_multiple_spaces,
)

@pytest.fixture
def russian_pdf_file_with_person(tmp_path):
    # Create a temporary PDF file with Russian text and a person entity
    file_path = tmp_path / "test_russian.pdf"
    doc = fitz.open()
    page = doc.new_page()
    # Natasha NER recognizes "Иван Иванов" as PER
    page.insert_text((72, 72), "Это решение суда. Иван Иванов был признан виновным.")
    doc.save(str(file_path))
    doc.close()
    return str(tmp_path) + os.sep, "test_russian.pdf"

@pytest.fixture
def russian_pdf_file_no_person(tmp_path):
    # Create a temporary PDF file with Russian text but no person entity
    file_path = tmp_path / "test_russian_no_per.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Это решение суда. Компания Рога и Копыта признана победителем.")
    doc.save(str(file_path))
    doc.close()
    return str(tmp_path) + os.sep, "test_russian_no_per.pdf"

@pytest.fixture
def empty_pdf_file(tmp_path):
    # Create an empty PDF file
    file_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(str(file_path))
    doc.close()
    return str(tmp_path) + os.sep, "empty.pdf"

def test_cleantext_extracts_cleaned_text_and_last_person(russian_pdf_file_with_person):
    directory, filename = russian_pdf_file_with_person
    clean_text, last_person = CleanText(directory, filename)
    # The cleaned text should contain "Иван Иванов"
    assert "Иван Иванов" in clean_text
    # The last person entity should be "Иван Иванов"
    assert last_person == "Иван Иванов"
    assert isinstance(clean_text, str)
    assert isinstance(last_person, str)

def test_remove_strings_with_english_filters_english_words():
    input_list = ["привет", "hello", "мир", "world", "тест"]
    result = remove_strings_with_english(input_list)
    assert result == ["привет", "мир", "тест"]

def test_remove_non_russian_alpha_lines_filters_non_russian():
    input_lines = ["привет", "hello", "мир123", "тест", "Москва", "123", "Париж"]
    result = remove_non_russian_alpha_lines(input_lines)
    # Only lines with Russian letters only
    assert result == ["привет", "тест", "Москва", "Париж"]

def test_cleantext_no_person_entities(russian_pdf_file_no_person):
    directory, filename = russian_pdf_file_no_person
    clean_text, last_person = CleanText(directory, filename)
    # There should be no person entity, so per list is empty and last_person should raise IndexError or be handled
    # According to the code, if per is empty, accessing per[-1] will raise IndexError
    # So we expect an IndexError or a handled case (if code is changed to handle it)
    # Let's check for IndexError
    with pytest.raises(IndexError):
        _ = last_person

def test_remove_lines_with_multiple_spaces_removes_lines():
    input_lines = ["Москва", "Санкт  Петербург", "Новосибирск", "Казань  ", "Екатеринбург"]
    result = remove_lines_with_multiple_spaces(input_lines)
    # Only lines without two or more consecutive spaces
    assert result == ["Москва", "Новосибирск", "Екатеринбург"]

def test_cleantext_empty_or_missing_file(empty_pdf_file, tmp_path):
    # Test with empty file
    directory, filename = empty_pdf_file
    clean_text, last_person = CleanText(directory, filename)
    # Clean text should be empty or very short, and last_person should raise IndexError
    assert isinstance(clean_text, str)
    assert clean_text.strip() == ""
    with pytest.raises(IndexError):
        _ = last_person

    # Test with missing file
    missing_directory = str(tmp_path) + os.sep
    missing_filename = "nonexistent.pdf"
    with pytest.raises(RuntimeError):
        CleanText(missing_directory, missing_filename)