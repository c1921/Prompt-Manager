import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QPushButton, QMenu, QInputDialog, QTreeWidget, QTreeWidgetItem, QHeaderView, QDialog, QLabel, QLineEdit, QDialogButtonBox, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

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

class DraggableTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.dragged_item = None
        
        # 设置列头
        self.setHeaderLabels(["提示词", "中文翻译"])
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # 设置拖放模式
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        
        # 禁止展开/折叠和子项
        self.setExpandsOnDoubleClick(False)
        self.setRootIsDecorated(False)
        self.setIndentation(0)  # 设置缩进为0，防止显示层级
        
        # 启用双击和右键菜单编辑
        self.itemDoubleClicked.connect(self.edit_prompt)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def dropEvent(self, event):
        """重写拖放事件，只允许改变顺序"""
        if event.source() != self:
            event.ignore()
            return
            
        # 获取拖放的目标位置
        drop_pos = event.position().toPoint()
        target_item = self.itemAt(drop_pos)
        
        if not target_item:
            # 如果拖到空白处，添加到末尾
            super().dropEvent(event)
        else:
            # 获取目标项的索引
            target_index = self.indexOfTopLevelItem(target_item)
            # 获取当前拖动的项
            current_item = self.currentItem()
            if current_item:
                # 移除当前项
                current_index = self.indexOfTopLevelItem(current_item)
                taken_item = self.takeTopLevelItem(current_index)
                # 在目标位置插入
                self.insertTopLevelItem(target_index, taken_item)
                # 保持选中状态
                self.setCurrentItem(taken_item)
        
        # 通知父窗口更新文本编辑框
        prompt_editor = self.parent()
        if prompt_editor:
            prompt_editor.update_input_field()
    
    def edit_prompt(self, item=None, column=None):
        """编辑提示词和翻译"""
        if not item:
            item = self.currentItem()
        if not item:
            return
            
        dialog = PromptTranslationDialog(
            prompt=item.text(0),
            translation=item.text(1),
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item.setText(0, dialog.prompt_edit.text())
            item.setText(1, dialog.translation_edit.text())
            # 通知父窗口更新文本编辑框
            prompt_editor = self.parent()
            if prompt_editor:
                prompt_editor.update_input_field()
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        item = self.itemAt(position)
        if not item:
            return
            
        menu = QMenu()
        edit_action = menu.addAction("编辑提示词")
        action = menu.exec(self.mapToGlobal(position))
        
        if action == edit_action:
            self.edit_prompt(item)

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
        self.prompt_list = DraggableTreeWidget()
        self.prompt_list.setParent(self)

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
        
        self.input_field.setPlainText(normalized_text)
        
        self.prompt_list.clear()
        prompts = normalized_text.split(', ')
        for prompt in prompts:
            # 创建两列的树形项：提示词和空的中文翻译
            item = QTreeWidgetItem([prompt, ""])
            self.prompt_list.addTopLevelItem(item)

    def update_input_field(self):
        """更新文本编辑框内容"""
        prompts = []
        for i in range(self.prompt_list.topLevelItemCount()):
            item = self.prompt_list.topLevelItem(i)
            prompts.append(item.text(0))  # 只使用英文提示词
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
            
        # 获取选中项的文本（第0列是提示词）
        selected_text = selected_items[0].text(0)  # 添加列号参数
        
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

    def update_text_area(self):
        """更新文本编辑框内容"""
        prompts = []
        for i in range(self.prompt_list.count()):
            prompts.append(self.prompt_list.item(i).text())
        self.text_area.setPlainText(', '.join(prompts))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = PromptEditor()
    editor.show()
    sys.exit(app.exec())