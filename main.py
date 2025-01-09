import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QPushButton
from PyQt6.QtCore import Qt

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.model().rowsMoved.connect(self.update_text)

    def add_prompt(self, prompt):
        item = QListWidgetItem(prompt)
        self.addItem(item)

    def update_text(self):
        # Emit a custom signal or directly update the text
        self.parent().update_input_field()

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
        self.add_button = QPushButton("添加提示词")
        self.add_button.clicked.connect(self.add_prompts)

        left_layout.addWidget(self.input_field)
        left_layout.addWidget(self.add_button)

        # 右侧可拖动列表
        self.prompt_list = DraggableListWidget()
        self.prompt_list.setParent(self)  # Set parent to access update_input_field

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.prompt_list)

        self.setLayout(main_layout)

    def add_prompts(self):
        # 获取输入框中的文本
        text = self.input_field.toPlainText()
        # 按逗号分割文本
        prompts = [prompt.strip() for prompt in text.split(',') if prompt.strip()]
        # 清空当前列表
        self.prompt_list.clear()
        # 添加每个提示词到列表
        for prompt in prompts:
            self.prompt_list.add_prompt(prompt)

    def update_input_field(self):
        # 获取当前列表中的所有提示词
        prompts = [self.prompt_list.item(i).text() for i in range(self.prompt_list.count())]
        # 更新输入框中的文本
        self.input_field.setPlainText(', '.join(prompts))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = PromptEditor()
    editor.show()
    sys.exit(app.exec())