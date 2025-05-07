import unittest
from unittest.mock import patch, MagicMock
import extract_data
import re

class TestExtractData(unittest.TestCase):
    @patch('extract_data.Doc')
    @patch('extract_data.segmenter')
    @patch('extract_data.morph_vocab')
    @patch('extract_data.morph_tagger')
    def test_lemmatize_text(self, mock_morph_tagger, mock_morph_vocab, mock_segmenter, mock_Doc):
        # Setup
        mock_doc = MagicMock()
        mock_token = MagicMock()
        mock_token.lemma = 'тест'
        mock_doc.tokens = [mock_token, mock_token]
        mock_Doc.return_value = mock_doc

        # Call
        result = extract_data.lemmatize_text("тест тест")

        # Assert
        self.assertEqual(result, "тест тест")
        mock_Doc.assert_called_once()
        mock_doc.segment.assert_called_once_with(mock_segmenter)
        mock_doc.tag_morph.assert_called_once_with(mock_morph_tagger)
        for token in mock_doc.tokens:
            token.lemmatize.assert_called_with(mock_morph_vocab)

    def test_extract_articles_basic(self):
        # Prepare
        text = "статья 12, 13 гражданский кодекс российский федерация"
        pattern = extract_data.re.compile(
            r"\bстатья\s+((?:\d+[,-]?\s*)+)((?:[А-Яа-я]+(?:\s+[А-Яа-я]+)*)?) кодекс российский федерация", re.IGNORECASE
        )
        with patch('extract_data.lemmatize_text', return_value=text):
            result = extract_data.extract_articles(text, pattern)
        self.assertIn('гк', result)
        self.assertEqual(result['гк'], [12, 13])

    def test_extract_articles_range(self):
        text = "статья 10-12 гражданский кодекс российский федерация"
        pattern = extract_data.re.compile(
            r"\bстатья\s+((?:\d+[,-]?\s*)+)((?:[А-Яа-я]+(?:\s+[А-Яа-я]+)*)?) кодекс российский федерация", re.IGNORECASE
        )
        with patch('extract_data.lemmatize_text', return_value=text):
            result = extract_data.extract_articles(text, pattern)
        self.assertIn('гк', result)
        self.assertEqual(result['гк'], [10, 11, 12])

    @patch('extract_data.Doc')
    @patch('extract_data.segmenter')
    @patch('extract_data.ner_tagger')
    def test_ustanovil(self, mock_ner_tagger, mock_segmenter, mock_Doc):
        # Setup
        text = "Some text stop_point Some more text start_point"
        ust = "stop_point"
        resh = "start_point"
        mock_doc = MagicMock()
        # Simulate two orgs and one person
        org_span = MagicMock()
        org_span.type = "ORG"
        org_span.text = "Org1"
        org_span.start = 1
        per_span = MagicMock()
        per_span.type = "PER"
        per_span.text = "Person1"
        per_span.start = 2
        mock_doc.spans = [org_span, per_span]
        mock_Doc.return_value = mock_doc

        result = extract_data.ustanovil(ust, text, resh)
        self.assertEqual(result[0], "Org1")
        self.assertEqual(result[1], "Person1")
        self.assertIsInstance(result[2], str)


if __name__ == '__main__':
    unittest.main()