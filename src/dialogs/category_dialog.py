"""分类编辑对话框"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox
from ..styles.dialog_style import DIALOG_BASE_STYLE

class CategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加分类")
        self.setMinimumWidth(300)
        self.setStyleSheet(DIALOG_BASE_STYLE)
        
        layout = QVBoxLayout(self)
        
        self.name_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        
        layout.addWidget(QLabel("分类名称:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("描述:"))
        layout.addWidget(self.desc_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_data(self):
        """获取输入数据"""
        return {
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.text().strip()
        } 