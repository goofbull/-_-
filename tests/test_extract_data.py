import unittest
from unittest.mock import patch
from extract_data import lemmatize_text, extract_articles, ustanovil, get_data_from_file, get_dict_with_data

class TestCourtCaseProcessing(unittest.TestCase):

    @patch('extract_data.CleanText')
    def test_get_data_from_file(self, mock_clean_text):
        # Мокаем возвращаемые значения
        mock_clean_text.return_value = ("cleaned_text", "judge_name")

        result = get_data_from_file("some_directory", 1)

        self.assertEqual(result, ("cleaned_text", "judge_name"))

    @patch('extract_data.get_data_from_file')
    def test_get_dict_with_data(self, mock_get_data):
        # Мокаем возвращаемые данные
        mock_get_data.return_value = ("cleaned_text", "judge_name")

        result = get_dict_with_data("some_directory")

        self.assertEqual(result, {'cleaned_text': 'judge_name'})

    def test_extract_articles(self):
        result = extract_articles("some_text_with_article_codes")
        self.assertEqual(result, {'зк': [12, 13]})

    def test_lemmatize_text(self):
        result = lemmatize_text("судья рассмотреть дело")
        self.assertEqual(result.capitalize(), "Судья рассмотреть дело")

    def test_ustanovil(self):
        result = ustanovil("Компания подала иск")
        self.assertEqual(result[0], "Компания")

if __name__ == '__main__':
    unittest.main()
