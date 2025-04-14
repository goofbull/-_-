from PySide6.QtWidgets import * 
from untitled_ui import Ui_MainWindow


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        self.ui.InputFilenameButton.clicked.connect(self.get_filename)
        
    def get_filename(self):
        filename = self.ui.filename.text()
        print("Введённый текст:", filename)


if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()


