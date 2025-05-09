import os
import tempfile
import shutil
import logging
import pytest
from unittest import mock

import fitz

from important_features import CleanText


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
    file_path = os.path.join(dir_path, filename)
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(
        (72, 72),
        text,
        fontsize=12,
        fontname="notos",
        color=(0, 0, 0)
    )

    doc.save(file_path)
    doc.close()
    return file_path


def test_cleantext_happy_path():
    russian_text = "Москва - столица России. Иван Иванов работает в компании Газпром."
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test.pdf"
        filepath = create_pdf_with_text(russian_text, tmpdir, filename)

        # Передаём директорию с завершающим слэшем и имя файла отдельно
        directory = tmpdir + os.sep  # гарантируем, что есть слэш в конце
        clean_text, last_per = CleanText(directory, filename)

        text_lower = clean_text.lower()
        assert isinstance(clean_text, str)
        assert "москва" in text_lower
        assert "россии" in text_lower
        assert "иван" in text_lower
        assert "газпром" in text_lower

        assert isinstance(last_per, str)
        last_per_lower = last_per.lower()
        assert "иван" in last_per_lower or "иванов" in last_per_lower


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
    russian_text = "Санкт-Петербург - красивый город."

    logging.basicConfig(
        filename='py_log.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        encoding='utf-8',
        force=True
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        filename = "test.pdf"
        create_pdf_with_text(russian_text, tmpdir, filename)
        from important_features import CleanText
        CleanText(tmpdir + os.sep, filename)

    log_path = os.path.abspath("py_log.log")
    assert os.path.exists(log_path)
    with open(log_path, encoding="utf-8") as f:
        log_content = f.read()

    assert "Загрузка файла..." in log_content
    assert "Извлечение данных завершено" in log_content
    assert "Время выполнения операции:" in log_content
    assert "INFO" in log_content or "INFO:" in log_content