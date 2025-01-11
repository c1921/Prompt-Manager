from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                          QDialogButtonBox, QDoubleSpinBox, QPushButton)
from src.styles.dark_theme import DIALOG
from PyQt6.QtCore import Qt

class PromptTranslationDialog(QDialog):
    """提示词编辑对话框"""
    def __init__(self, prompt="", translation="", weight="1", parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑提示词")
        self.setMinimumWidth(400)
        
        # 设置对话框样式
        self.setStyleSheet(DIALOG)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 英文提示词输入
        layout.addWidget(QLabel("提示词:"))
        self.prompt_edit = QLineEdit(prompt)
        layout.addWidget(self.prompt_edit)
        
        # 中文翻译输入
        layout.addWidget(QLabel("中文翻译:"))
        self.translation_edit = QLineEdit(translation)
        layout.addWidget(self.translation_edit)
        
        # 权重编辑
        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("权重:"))
        
        self.weight_edit = QDoubleSpinBox()
        self.weight_edit.setRange(0.1, 10.0)
        self.weight_edit.setSingleStep(0.1)
        self.weight_edit.setDecimals(1)
        self.weight_edit.setValue(float(weight))
        self.weight_edit.setFixedWidth(70)
        self.weight_edit.setFixedHeight(32)
        self.weight_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weight_edit.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 2px 5px;
                color: #e0e0e0;
                font-size: 14px;
            }
            QDoubleSpinBox:hover {
                border: 1px solid #666666;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #1976d2;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 20px;
                background-color: #404040;
                border: none;
                border-radius: 2px;
                margin: 1px;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #505050;
            }
            QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                background-color: #303030;
            }
            QDoubleSpinBox::up-arrow {
                image: url(src/assets/icons/arrow-up.svg);
                width: 12px;
                height: 12px;
            }
            QDoubleSpinBox::down-arrow {
                image: url(src/assets/icons/arrow-down.svg);
                width: 12px;
                height: 12px;
            }
        """)
        weight_layout.addWidget(self.weight_edit)
        
        # 添加快捷按钮
        for value in [0.5, 1.0, 1.5, 2.0]:
            btn = QPushButton(str(value))
            btn.setFixedWidth(40)
            btn.clicked.connect(lambda checked, v=value: self.weight_edit.setValue(v))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    color: #e0e0e0;
                    border: none;
                    padding: 4px;
                    border-radius: 2px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #303030;
                }
            """)
            weight_layout.addWidget(btn)
        
        weight_layout.addStretch()
        layout.addLayout(weight_layout)
        
        # 确定取消按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons) 