# 对话框基本样式
DIALOG_STYLE = """
QDialog {
    background-color: transparent;
}
"""

# 标题栏样式
TITLE_BAR_STYLE = """
QWidget {
    background-color: #1e1e1e;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
"""

TITLE_LABEL_STYLE = """
QLabel {
    color: #e0e0e0;
    font-size: 14px;
}
"""

CLOSE_BUTTON_STYLE = """
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
"""

# 内容区样式
CONTENT_WIDGET_STYLE = """
QWidget {
    background-color: #1e1e1e;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}
"""

# 树形控件样式
TREE_WIDGET_STYLE = """
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
"""

# 工具栏按钮样式
TOOLBAR_BUTTON_STYLE = """
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
"""

# 主要操作按钮样式
ACTION_BUTTON_STYLE = """
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
""" 