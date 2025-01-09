MAIN_WINDOW = """
QWidget#mainWindow {
    background-color: #1e1e1e;
    border: 1px solid #404040;
    border-radius: 4px;
}
"""

TITLE_BAR = """
QWidget {
    background-color: #1e1e1e;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
"""

TITLE_LABEL = """
color: #e0e0e0; 
font-weight: bold;
font-size: 14px;
padding: 5px;
"""

TITLE_BUTTONS = """
QPushButton {
    background-color: transparent;
    color: #e0e0e0;
    border: none;
    font-size: 16px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #404040;
}
QPushButton:pressed {
    background-color: #333333;
}
"""

TEXT_EDIT = """
QTextEdit {
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px;
    background-color: #2d2d2d;
    color: #e0e0e0;
    selection-background-color: #264f78;
}
"""

ACTION_BUTTONS = """
QPushButton {
    background-color: #0d47a1;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 100px;
}
QPushButton:hover {
    background-color: #1565c0;
}
QPushButton:pressed {
    background-color: #0a3d91;
}
"""

TREE_WIDGET = """
QTreeWidget {
    border: 1px solid #404040;
    border-radius: 4px;
    background-color: #2d2d2d;
    alternate-background-color: #262626;
    color: #e0e0e0;
}
QTreeWidget::item {
    height: 30px;
    padding: 4px;
}
QTreeWidget::item:selected {
    background-color: #264f78;
    color: white;
}
QTreeWidget::item:hover {
    background-color: #333333;
}
QHeaderView::section {
    background-color: #1e1e1e;
    color: #e0e0e0;
    padding: 8px;
    border: none;
    border-right: 1px solid #404040;
}
"""

DIALOG = """
QDialog {
    background-color: #1e1e1e;
}
QLabel {
    color: #e0e0e0;
    font-weight: bold;
    margin-bottom: 4px;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #404040;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}
QPushButton {
    background-color: #0d47a1;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #1565c0;
}
""" 