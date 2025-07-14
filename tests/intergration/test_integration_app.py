import os
import pytest
from PySide6.QtWidgets import QApplication
from unittest.mock import patch
from Program import MyApp
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
def test_show_result_integration(qtbot):
    test_filename = "test_input"

    window = MyApp()
    qtbot.addWidget(window)

    window.ui.filename.setText(test_filename)

    with patch("Program.create_single_excel") as mock_excel, \
         patch("Program.convert") as mock_convert, \
         patch("Program.prepare_csv") as mock_prepare, \
         patch("Program.show_new_prediction", return_value="Sample Prediction") as mock_predict, \
         patch("Program.accuracy", 0.9), \
         patch("Program.precision", 0.85), \
         patch("Program.recall", 0.88), \
         patch("Program.f1", 0.86):

        window.show_result()

        mock_convert.assert_called_with(test_filename)
        mock_prepare.assert_called_with(test_filename)
        mock_predict.assert_called_with(test_filename)

        assert window.ui.Result.text() == "Sample Prediction"
        assert window.ui.accuracy.text() == "0.9"
        assert window.ui.precision.text() == "0.85"
        assert window.ui.recall.text() == "0.88"
        assert window.ui.f1_score.text() == "0.86"