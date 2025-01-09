import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt6.QtWidgets import QApplication
from src.widgets.prompt_editor import PromptEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = PromptEditor()
    editor.show()
    sys.exit(app.exec())