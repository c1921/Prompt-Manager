"""提示词编辑对话框"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                          QDialogButtonBox, QComboBox)
from ..styles.dialog_style import DIALOG_BASE_STYLE
from ..data.prompt_library import PROMPT_LIBRARY

class PromptEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加提示词")
        self.setMinimumWidth(300)
        self.setStyleSheet(DIALOG_BASE_STYLE)
        
        layout = QVBoxLayout(self)
        
        # 添加分类选择下拉菜单
        layout.addWidget(QLabel("分类:"))
        self.category_combo = QComboBox()
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 5px;
                color: #e0e0e0;
            }
            QComboBox:hover {
                border: 1px solid #666666;
            }
            QComboBox:focus {
                border: 1px solid #1976d2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(src/assets/icons/arrow-down.svg);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                selection-background-color: #1976d2;
                selection-color: white;
                color: #e0e0e0;
            }
        """)
        # 加载分类列表
        for category in PROMPT_LIBRARY.categories.values():
            self.category_combo.addItem(category.name)
        layout.addWidget(self.category_combo)
        
        # 提示词输入
        layout.addWidget(QLabel("英文:"))
        self.en_edit = QLineEdit()
        layout.addWidget(self.en_edit)
        
        layout.addWidget(QLabel("中文:"))
        self.zh_edit = QLineEdit()
        layout.addWidget(self.zh_edit)
        
        # 按钮
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
            'category': self.category_combo.currentText(),
            'en': self.en_edit.text().strip(),
            'zh': self.zh_edit.text().strip()
        } 