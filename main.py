import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.dragged_item = None  # 添加跟踪变量
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.model().rowsMoved.connect(self.update_text)

    def add_prompt(self, prompt):
        item = QListWidgetItem(prompt)
        self.addItem(item)

    def update_text(self):
        # Emit a custom signal or directly update the text
        self.parent().update_input_field()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 记录开始拖动时选中的项
        self.dragged_item = self.currentItem()

    def dropEvent(self, event):
        super().dropEvent(event)
        # 拖放完成后，重新选中之前拖动的项
        if self.dragged_item:
            self.setCurrentItem(self.dragged_item)
            self.dragged_item = None  # 重置跟踪变量
        self.itemSelectionChanged.emit()

class PromptEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD 提示词编辑器")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        # 左侧多行输入框和按钮
        left_layout = QVBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("输入提示词，用逗号分隔")
        self.add_button = QPushButton("生成提示词列表")
        self.add_button.clicked.connect(self.generate_prompt_list)

        left_layout.addWidget(self.input_field)
        left_layout.addWidget(self.add_button)

        # 右侧可拖动列表
        self.prompt_list = DraggableListWidget()
        self.prompt_list.setParent(self)  # Set parent to access update_input_field

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.prompt_list)

        self.setLayout(main_layout)

        # 在初始化时添加列表项选择事件的连接
        self.prompt_list.itemSelectionChanged.connect(self.highlight_selected_text)

        # 添加拖动完成后的信号连接
        self.prompt_list.model().rowsMoved.connect(self.on_rows_moved)

    def normalize_text(self, text):
        """规范化提示词文本格式
        将输入文本转换为标准格式：使用英文逗号和单个空格分隔提示词
        
        Args:
            text (str): 输入的原始文本
            
        Returns:
            str: 规范化后的文本，格式如："prompt1, prompt2, prompt3"
        """
        # 替换中文逗号为英文逗号
        text = text.replace('，', ',')
        
        # 分割文本，同时处理多个连续逗号的情况
        parts = [part.strip() for part in text.split(',')]
        # 过滤掉空字符串
        parts = [part for part in parts if part]
        
        # 使用标准格式重新组合（逗号+空格）
        return ', '.join(parts)
    
    def generate_prompt_list(self):
        """将文本规范化并生成提示词列表"""
        text = self.input_field.toPlainText()
        normalized_text = self.normalize_text(text)
        
        # 更新文本编辑框的内容为规范化后的文本
        self.input_field.setPlainText(normalized_text)
        
        # 清空列表并添加规范化后的提示词
        self.prompt_list.clear()
        prompts = normalized_text.split(', ')
        self.prompt_list.addItems(prompts)

    def update_input_field(self):
        # 获取当前列表中的所有提示词
        prompts = [self.prompt_list.item(i).text() for i in range(self.prompt_list.count())]
        # 更新输入框中的文本
        self.input_field.setPlainText(', '.join(prompts))

    def highlight_selected_text(self):
        """当列表项被选中时，高亮对应的文本"""
        # 获取当前选中的列表项
        selected_items = self.prompt_list.selectedItems()
        if not selected_items:
            # 如果没有选中项，清除所有高亮
            cursor = self.input_field.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(QTextCharFormat())
            cursor.clearSelection()
            return
            
        # 获取选中项的文本
        selected_text = selected_items[0].text()
        
        # 在文本编辑框中查找并高亮对应文本
        document = self.input_field.document()
        cursor = QTextCursor(document)
        
        # 创建高亮格式
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("yellow"))
        
        # 清除之前的高亮
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        
        # 查找并高亮新的选中文本
        cursor = QTextCursor(document)
        while not cursor.isNull():
            cursor = document.find(selected_text, cursor)
            if not cursor.isNull():
                cursor.mergeCharFormat(highlight_format)

    def on_rows_moved(self, parent, start, end, destination, row):
        """当列表项被拖动后，重新高亮选中项"""
        # 获取当前拖动的项
        moved_item = self.prompt_list.item(row)
        if moved_item:
            # 选中被拖动的项
            self.prompt_list.setCurrentItem(moved_item)
            # 触发高亮
            self.highlight_selected_text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = PromptEditor()
    editor.show()
    sys.exit(app.exec())