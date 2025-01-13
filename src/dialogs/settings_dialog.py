from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                          QLineEdit, QPushButton, QFileDialog, QDialogButtonBox, 
                          QMessageBox, QCheckBox)
from ..styles.dialog_style import DIALOG_BASE_STYLE
import json
import os
from datetime import datetime

class SettingsDialog(QDialog):
    def __init__(self, current_path="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumWidth(500)
        self.setStyleSheet(DIALOG_BASE_STYLE)
        
        layout = QVBoxLayout(self)
        
        # 提示词库路径设置
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("提示词库路径:"))
        
        self.path_edit = QLineEdit(current_path)
        self.path_edit.setReadOnly(True)
        path_layout.addWidget(self.path_edit)
        
        # 添加两个按钮
        button_layout = QHBoxLayout()
        self.browse_button = QPushButton("选择文件...")
        self.browse_button.clicked.connect(self._browse_file)
        
        self.new_button = QPushButton("从模板创建...")
        self.new_button.clicked.connect(self._create_from_template)
        
        button_layout.addWidget(self.browse_button)
        button_layout.addWidget(self.new_button)
        path_layout.addLayout(button_layout)
        
        layout.addLayout(path_layout)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _browse_file(self):
        """选择提示词库文件"""
        current_dir = os.path.dirname(self.path_edit.text()) if self.path_edit.text() else ""
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择提示词库文件", 
            current_dir,
            "JSON Files (*.json)",
            options=QFileDialog.Option.DontConfirmOverwrite
        )
        
        if file_path:
            if not os.path.exists(file_path):
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump({}, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"创建文件失败: {str(e)}")
                    return
            
            self.path_edit.setText(file_path)
    
    def _create_from_template(self):
        """从模板创建新文件"""
        # 选择目标目录
        dir_path = QFileDialog.getExistingDirectory(
            self, 
            "选择保存位置",
            os.path.dirname(self.path_edit.text()) if self.path_edit.text() else ""
        )
        
        if dir_path:
            try:
                # 生成文件名
                timestamp = datetime.now().strftime("%Y%m%d%H%M")
                file_name = f"prompts-{timestamp}.json"
                file_path = os.path.join(dir_path, file_name)
                
                # 读取模板内容
                template_path = os.path.join(os.path.dirname(__file__), 
                                          '..', 'data', 'prompts.json')
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                # 写入新文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, ensure_ascii=False, indent=4)
                
                self.path_edit.setText(file_path)
                QMessageBox.information(self, "成功", "已成功创建提示词库文件")
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建文件失败: {str(e)}")
    
    def get_library_path(self):
        """获取设置的路径"""
        return self.path_edit.text() 