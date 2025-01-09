from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTreeWidgetItem, QMessageBox
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from .draggable_tree import DraggableTreeWidget

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

        # 添加翻译按钮
        self.translate_button = QPushButton("翻译所有提示词")
        self.translate_button.clicked.connect(self.translate_all_prompts)
        
        # 将翻译按钮添加到左侧布局
        left_layout.addWidget(self.translate_button)

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
        """规范化提示词文本格式"""
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
        
        # 分割提示词
        prompts = normalized_text.split(', ')
        self.prompt_list.clear()
        
        for prompt in prompts:
            if not prompt:
                continue
            
            # 检查是否包含中文字符
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in prompt)
            
            if has_chinese:
                try:
                    # 使用DraggableTreeWidget中的translator实例
                    translator = self.prompt_list.translator
                    # 临时修改翻译方向
                    translator.source = 'zh-CN'
                    translator.target = 'en'
                    # 将中文翻译为英文
                    english = translator.translate(prompt)
                    # 恢复翻译方向
                    translator.source = 'en'
                    translator.target = 'zh-CN'
                    # 创建树形项：英文提示词和中文原文
                    item = QTreeWidgetItem([english.strip(), prompt])
                except Exception as e:
                    # 如果翻译失败，保持原文
                    QMessageBox.warning(self, "翻译错误", f"翻译失败: {str(e)}")
                    item = QTreeWidgetItem([prompt, ""])
            else:
                # 非中文提示词，保持原样
                item = QTreeWidgetItem([prompt, ""])
            
            self.prompt_list.addTopLevelItem(item)
        
        # 更新输入框内容为规范化的英文提示词
        self.update_input_field()

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
        selected_text = selected_items[0].text(0)
        
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
        moved_item = self.prompt_list.topLevelItem(row)
        if moved_item:
            # 选中被拖动的项
            self.prompt_list.setCurrentItem(moved_item)
            # 触发高亮
            self.highlight_selected_text() 

    def translate_all_prompts(self):
        """触发所有提示词的翻译"""
        self.prompt_list.translate_all_prompts() 