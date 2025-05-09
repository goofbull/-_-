import re
import unittest
from unittest.mock import patch
from extract_data import lemmatize_text, extract_articles, ustanovil, get_data_from_file, get_dict_with_data

class TestCourtCaseProcessing(unittest.TestCase):

    @patch('extract_data.get_data_from_file')
    def test_get_dict_with_data(self, mock_get_data):
        number_of_docs = "1"
        # Мокаем возвращаемые данные
        mock_get_data.return_value = {"cleaned_text": "judge_name"}

        result = get_dict_with_data("some_directory", 1)

        self.assertEqual(result, {number_of_docs: {"cleaned_text": "judge_name"}})

    def test_extract_articles(self):
        article_pattern = re.compile(r"(\d+)\s+(\d+)", re.IGNORECASE)
        text = "12 13"
        result = extract_articles(text, article_pattern)
        self.assertEqual(result, {'13': [12]})

    def test_lemmatize_text(self):
        result = lemmatize_text("судья рассмотреть дело")
        self.assertEqual(result.capitalize(), "Судья рассмотреть дело")

    def test_ustanovil(self):
        text = "ООО Компания подала иск в суд"
        result = ustanovil(" ", text, " ")
        self.assertEqual("ООО", result[0])


if __name__ == '__main__':
    unittest.main()
