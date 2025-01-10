# 通用对话框样式
DIALOG_BASE_STYLE = """
QDialog, QMessageBox {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QLabel {
    color: #e0e0e0;
}

QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 5px;
    color: #e0e0e0;
}

QLineEdit:focus {
    border: 1px solid #1976d2;
}

QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    padding: 6px 16px;
    border-radius: 4px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #2196f3;
}

QPushButton:pressed {
    background-color: #1565c0;
}

QDialogButtonBox > QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    padding: 6px 16px;
    border-radius: 4px;
    min-width: 80px;
}

QDialogButtonBox > QPushButton:hover {
    background-color: #2196f3;
}

QDialogButtonBox > QPushButton:pressed {
    background-color: #1565c0;
}
""" 