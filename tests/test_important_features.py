import os
import tempfile
import shutil
import logging
import pytest
from unittest import mock

import fitz

# Import the CleanText function from the module where it is defined
# from your_module import CleanText

@pytest.fixture(autouse=True)
def cleanup_log_file():
    """Remove log file before and after each test."""
    log_path = "py_log.log"
    if os.path.exists(log_path):
        os.remove(log_path)
    yield
    if os.path.exists(log_path):
        os.remove(log_path)

def create_pdf_with_text(text, dir_path, filename):
    """Helper to create a PDF file with the given text."""
    file_path = os.path.join(dir_path, filename)
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(file_path)
    doc.close()
    return file_path

def test_cleantext_happy_path():
    # Russian text with nouns and named entities
    russian_text = "Москва — столица России. Иван Иванов работает в компании Газпром."
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test.pdf"
        create_pdf_with_text(russian_text, tmpdir, filename)
        # Import here to avoid issues with global state in natasha/pymorphy3
        from important_features import CleanText
        clean_text, last_per = CleanText(tmpdir + os.sep, filename)
        # The cleaned text should contain Moscow, Russia, Ivan Ivanov, Газпром, etc.
        assert isinstance(clean_text, str)
        assert "москва" in clean_text.lower() or "Москва" in clean_text
        assert "россия" in clean_text.lower() or "Россия" in clean_text
        assert "иван" in clean_text.lower() or "Иван" in clean_text
        assert "газпром" in clean_text.lower() or "Газпром" in clean_text
        # The last PER entity should be Иван Иванов or Иванов
        assert isinstance(last_per, str)
        assert "Иван" in last_per or "иванов" in last_per.lower()

def test_cleantext_no_russian_content():
    # PDF with only English text and numbers
    english_text = "This is a test. 12345. No Russian words here."
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test.pdf"
        create_pdf_with_text(english_text, tmpdir, filename)
        from important_features import CleanText
        # Should not raise, but may return empty or minimal cleaned text and handle per[-1] gracefully
        clean_text, last_per = CleanText(tmpdir + os.sep, filename)
        assert isinstance(clean_text, str)
        # Should be empty or contain no Russian words
        assert clean_text.strip() == "" or not any('\u0400' <= c <= '\u04FF' for c in clean_text)
        # Should handle absence of PER gracefully (may be IndexError if not handled in code)
        # Accept either empty string or IndexError
        assert last_per == "" or last_per is None or isinstance(last_per, str)

def test_logging_configuration_and_output():
    # Russian text to trigger logging
    russian_text = "Санкт-Петербург — красивый город."
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test.pdf"
        create_pdf_with_text(russian_text, tmpdir, filename)
        from important_features import CleanText
        CleanText(tmpdir + os.sep, filename)
        # Check that log file exists and contains expected INFO messages
        assert os.path.exists("py_log.log")
        with open("py_log.log", encoding="utf-8") as f:
            log_content = f.read()
        assert "Загрузка файла..." in log_content
        assert "Извлечение данных завершено" in log_content
        assert "Время выполнения операции:" in log_content
        # Should be INFO level logs
        assert "INFO" in log_content or "INFO:" in log_content