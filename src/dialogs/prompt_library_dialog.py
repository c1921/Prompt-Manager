from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                          QTreeWidgetItem, QPushButton, QLabel, QHeaderView, QWidget, 
                          QFileDialog, QLineEdit, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon
from ..data.prompt_library import PROMPT_LIBRARY
from ..styles.dark_theme import *
import json

class PromptLibraryDialog(QDialog):
    # 添加自定义信号
    promptsSelected = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("提示词库")
        self.setMinimumSize(600, 400)
        
        # 设置无边框窗口，并添加独立窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Window  # 只保留这两个标志
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建标题栏
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        # 标题文本
        title_label = QLabel("提示词库")
        title_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
        """)
        
        # 关闭按钮
        close_button = QPushButton("×")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #e0e0e0;
                font-size: 20px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #c42b1c;
                border-radius: 4px;
            }
        """)
        close_button.clicked.connect(self.reject)
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_button)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)
        
        # 内容布局
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        
        # 创建树形控件
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["提示词", "中文"])
        self.tree.setAlternatingRowColors(True)
        
        # 设置初始列宽为1:1，但允许用户调整
        total_width = self.tree.width()
        self.tree.setColumnWidth(0, total_width // 2)
        self.tree.setColumnWidth(1, total_width // 2)
        
        # 修改为勾选框模式
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.NoSelection)
        self.tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid #404040;
                border-radius: 4px;
                background-color: #1e1e1e;
                alternate-background-color: #252525;
                color: #e0e0e0;
            }
            QTreeWidget::item {
                height: 28px;
                padding: 4px;
                border-radius: 2px;
            }
            QTreeWidget::item:hover {
                background-color: #2a2a2a;
            }
            QTreeWidget::branch {
                background-color: transparent;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                image: url(src/assets/icons/arrow-right.svg);
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                image: url(src/assets/icons/arrow-down.svg);
            }
            QTreeWidget::indicator {
                width: 18px;
                height: 18px;
                margin-right: 5px;
                border-radius: 3px;
            }
            QTreeWidget::indicator:unchecked {
                border: 2px solid #555555;
                background: transparent;
            }
            QTreeWidget::indicator:unchecked:hover {
                border-color: #666666;
                background: #2d2d2d;
            }
            QTreeWidget::indicator:checked {
                border: 2px solid #1976d2;
                background: #1976d2;
            }
            QTreeWidget::indicator:checked:hover {
                border-color: #2196f3;
                background: #2196f3;
            }
            QTreeWidget::indicator:indeterminate {
                border: 2px solid #1976d2;
                background: transparent;
            }
            QTreeWidget::indicator:indeterminate:hover {
                border-color: #2196f3;
                background: #2d2d2d;
            }
            QHeaderView::section {
                background-color: #252525;
                color: #e0e0e0;
                padding: 8px;
                border: none;
                border-right: 1px solid #404040;
            }
        """)
        
        # 加载提示词库
        self.load_library()
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_button = QPushButton("添加选中项")
        self.cancel_button = QPushButton("取消")
        
        for btn in (self.add_button, self.cancel_button):
            btn.setMinimumHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976d2;
                    color: white;
                    border: none;
                    padding: 8px 24px;
                    border-radius: 4px;
                    min-width: 120px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2196f3;
                }
                QPushButton:pressed {
                    background-color: #1565c0;
                }
            """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        
        # 添加工具栏
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)
        
        # 添加工具栏按钮
        self.import_button = QPushButton("导入")
        self.export_button = QPushButton("导出")
        self.add_category_button = QPushButton("添加分类")
        self.add_prompt_button = QPushButton("添加提示词")
        self.delete_button = QPushButton("删除")
        
        for btn in (self.import_button, self.export_button, 
                   self.add_category_button, self.add_prompt_button, 
                   self.delete_button):
            btn.setMinimumHeight(32)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border: none;
                    padding: 4px 12px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #404040;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
            """)
            toolbar_layout.addWidget(btn)
        
        toolbar_layout.addStretch()
        
        # 连接信号
        self.import_button.clicked.connect(self._import_library)
        self.export_button.clicked.connect(self._export_library)
        self.add_category_button.clicked.connect(self._add_category)
        self.add_prompt_button.clicked.connect(self._add_prompt)
        self.delete_button.clicked.connect(self._delete_selected)
        
        # 添加工具栏到布局
        content_layout.insertLayout(0, toolbar_layout)
        
        # 添加到主布局
        content_layout.addWidget(self.tree)
        content_layout.addLayout(button_layout)
        
        # 将标题栏和内容容器添加到主布局
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_widget)
        
        # 连接信号
        self.add_button.clicked.connect(self._handle_add_button)
        self.cancel_button.clicked.connect(self.close)
        
        # 添加窗口拖动支持
        self._drag_pos = None
        title_bar.mousePressEvent = self._title_bar_mouse_press
        title_bar.mouseMoveEvent = self._title_bar_mouse_move
    
    def _title_bar_mouse_press(self, event):
        """记录鼠标按下位置"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.pos()
    
    def _title_bar_mouse_move(self, event):
        """处理窗口拖动"""
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
    
    def load_library(self):
        """加载提示词库到树形控件"""
        for category_key, category in PROMPT_LIBRARY.categories.items():
            # 创建分类项
            category_item = QTreeWidgetItem([category.name, category.description])
            category_item.setFlags(category_item.flags() | 
                                 Qt.ItemFlag.ItemIsAutoTristate | 
                                 Qt.ItemFlag.ItemIsUserCheckable)
            self.tree.addTopLevelItem(category_item)
            
            # 添加提示词
            for prompt in category.prompts:
                prompt_item = QTreeWidgetItem([prompt["en"], prompt["zh"]])
                prompt_item.setFlags(prompt_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                prompt_item.setCheckState(0, Qt.CheckState.Unchecked)
                category_item.addChild(prompt_item)
            
            # 默认展开分类
            category_item.setExpanded(True)
    
    def get_selected_prompts(self):
        """获取选中的提示词"""
        selected_prompts = []
        # 遍历所有顶级项（分类）
        for i in range(self.tree.topLevelItemCount()):
            category = self.tree.topLevelItem(i)
            # 遍历分类下的所有子项（提示词）
            for j in range(category.childCount()):
                child = category.child(j)
                if child.checkState(0) == Qt.CheckState.Checked:
                    selected_prompts.append((child.text(0), child.text(1)))
        return selected_prompts 
    
    def _handle_add_button(self):
        """处理添加按钮点击事件"""
        selected = self.get_selected_prompts()
        if selected:
            self.promptsSelected.emit(selected)
            # 清除所有选中状态
            for i in range(self.tree.topLevelItemCount()):
                category = self.tree.topLevelItem(i)
                for j in range(category.childCount()):
                    child = category.child(j)
                    child.setCheckState(0, Qt.CheckState.Unchecked) 
    
    def _import_library(self):
        """导入提示词库"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入提示词库", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # 合并到现有库
                PROMPT_LIBRARY.merge_library(data)
                # 重新加载树形控件
                self.tree.clear()
                self.load_library()
                QMessageBox.information(self, "成功", "提示词库导入成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")
    
    def _export_library(self):
        """导出提示词库"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出提示词库", "", "JSON Files (*.json)")
        if file_path:
            try:
                data = PROMPT_LIBRARY.export_library()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "成功", "提示词库导出成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
    
    def _add_category(self):
        """添加新分类"""
        dialog = QDialog(self)
        dialog.setWindowTitle("添加分类")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        # 添加输入框
        name_label = QLabel("分类名称:")
        name_edit = QLineEdit()
        desc_label = QLabel("描述:")
        desc_edit = QLineEdit()
        
        layout.addWidget(name_label)
        layout.addWidget(name_edit)
        layout.addWidget(desc_label)
        layout.addWidget(desc_edit)
        
        # 添加按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = name_edit.text().strip()
            desc = desc_edit.text().strip()
            if name:
                PROMPT_LIBRARY.add_category(name, desc)
                self.tree.clear()
                self.load_library()
    
    def _add_prompt(self):
        """添加新提示词"""
        # 获取当前选中的分类
        current = self.tree.currentItem()
        if not current:
            QMessageBox.warning(self, "错误", "请先选择一个分类")
            return
            
        # 如果选中的是提示词，获取其父分类
        if current.parent():
            current = current.parent()
            
        dialog = QDialog(self)
        dialog.setWindowTitle("添加提示词")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        # 添加输入框
        en_label = QLabel("英文:")
        en_edit = QLineEdit()
        zh_label = QLabel("中文:")
        zh_edit = QLineEdit()
        
        layout.addWidget(en_label)
        layout.addWidget(en_edit)
        layout.addWidget(zh_label)
        layout.addWidget(zh_edit)
        
        # 添加按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            en = en_edit.text().strip()
            zh = zh_edit.text().strip()
            if en and zh:
                category_name = current.text(0)
                PROMPT_LIBRARY.add_prompt(category_name, en, zh)
                self.tree.clear()
                self.load_library()
    
    def _delete_selected(self):
        """删除选中的项"""
        current = self.tree.currentItem()
        if not current:
            return
            
        if current.parent():  # 删除提示词
            category = current.parent().text(0)
            prompt = current.text(0)
            if QMessageBox.question(
                self, 
                "确认删除", 
                f"确定要删除提示词 '{prompt}' 吗？"
            ) == QMessageBox.StandardButton.Yes:
                PROMPT_LIBRARY.delete_prompt(category, prompt)
        else:  # 删除分类
            category = current.text(0)
            if QMessageBox.question(
                self, 
                "确认删除", 
                f"确定要删除分类 '{category}' 及其所有提示词吗？"
            ) == QMessageBox.StandardButton.Yes:
                PROMPT_LIBRARY.delete_category(category)
                
        self.tree.clear()
        self.load_library() 