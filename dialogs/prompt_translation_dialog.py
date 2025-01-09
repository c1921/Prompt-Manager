from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox

class PromptTranslationDialog(QDialog):
    """提示词编辑对话框"""
    def __init__(self, prompt="", translation="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑提示词")
        
        layout = QVBoxLayout(self)
        
        # 英文提示词输入
        layout.addWidget(QLabel("提示词:"))
        self.prompt_edit = QLineEdit(prompt)
        layout.addWidget(self.prompt_edit)
        
        # 中文翻译输入
        layout.addWidget(QLabel("中文翻译:"))
        self.translation_edit = QLineEdit(translation)
        layout.addWidget(self.translation_edit)
        
        # 确定取消按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons) 