from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, 
                          QTreeWidgetItem, QPushButton, QLabel, QHeaderView, QWidget)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon
from ..data.prompt_library import PROMPT_LIBRARY
from ..styles.dark_theme import *

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