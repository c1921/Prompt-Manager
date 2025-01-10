from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QPushButton, QTreeWidgetItem, QMessageBox, QStyle, QLabel,
                            QDialog)
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QPalette
from PyQt6.QtCore import Qt
from .draggable_tree import DraggableTreeWidget
from ..styles.dark_theme import *  # 导入样式
from ..services.translator import TranslationService, TranslationError

class PromptEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SD Prompt Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置窗口样式
        self.setStyleSheet(MAIN_WINDOW)
        self.setObjectName("mainWindow")
        
        # 设置窗口标志
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建自定义标题栏
        title_bar = QWidget()
        title_bar.setStyleSheet(TITLE_BAR)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 10, 5)
        
        # 标题文本
        title_label = QLabel("SD Prompt Manager")
        title_label.setStyleSheet(TITLE_LABEL)
        
        # 最小化和关闭按钮
        min_button = QPushButton("－")
        close_button = QPushButton("×")
        
        for btn in (min_button, close_button):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(TITLE_BUTTONS)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(min_button)
        title_bar_layout.addWidget(close_button)
        
        # 连接按钮信号
        min_button.clicked.connect(self.showMinimized)
        close_button.clicked.connect(self.close)
        
        # 创建主要内容布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("输入提示词，用逗号分隔")
        self.input_field.setMinimumWidth(300)
        self.input_field.setStyleSheet(TEXT_EDIT)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("生成提示词列表")
        self.translate_button = QPushButton("翻译所有提示词")
        self.library_button = QPushButton("打开提示词库")
        
        for btn in (self.add_button, self.translate_button, self.library_button):
            btn.setStyleSheet(ACTION_BUTTONS)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.translate_button)
        button_layout.addWidget(self.library_button)
        
        left_layout.addWidget(self.input_field)
        left_layout.addLayout(button_layout)
        
        # 右侧可拖动列表
        self.prompt_list = DraggableTreeWidget()
        self.prompt_list.setParent(self)
        
        # 连接信号
        self.add_button.clicked.connect(self.generate_prompt_list)
        self.translate_button.clicked.connect(self.translate_all_prompts)
        self.prompt_list.itemSelectionChanged.connect(self.highlight_selected_text)
        self.prompt_list.model().rowsMoved.connect(self.on_rows_moved)
        self.library_button.clicked.connect(self.show_prompt_library)
        
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.prompt_list)
        
        # 创建内容容器
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #1e1e1e;")
        content_widget.setLayout(main_layout)
        
        # 主容器布局
        main_container = QVBoxLayout()
        main_container.setContentsMargins(0, 0, 0, 0)
        main_container.setSpacing(0)
        
        main_container.addWidget(title_bar)
        main_container.addWidget(content_widget)
        
        self.setLayout(main_container)
        
        # 添加窗口拖动支持
        self._drag_pos = None
        title_bar.mousePressEvent = self._title_bar_mouse_press
        title_bar.mouseMoveEvent = self._title_bar_mouse_move

    def _title_bar_mouse_press(self, event):
        """记录鼠标按下位置"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def _title_bar_mouse_move(self, event):
        """处理窗口拖动"""
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos is not None:
            diff = event.globalPosition().toPoint() - self._drag_pos
            new_pos = self.pos() + diff
            self.move(new_pos)
            self._drag_pos = event.globalPosition().toPoint()

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
        
        # 使用元组存储 (索引, 提示词)
        indexed_prompts = list(enumerate(prompts))
        
        # 分别收集中文和其他提示词，保留原始索引
        chinese_prompts = []
        other_prompts = []
        
        for idx, prompt in indexed_prompts:
            if not prompt:
                continue
            
            # 检查是否包含中文字符
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in prompt)
            if has_chinese:
                chinese_prompts.append((idx, prompt))
            else:
                other_prompts.append((idx, prompt, ""))
        
        # 批量翻译中文提示词
        if chinese_prompts:
            try:
                translation_service = TranslationService()
                translated_prompts = translation_service.translate_prompts(
                    chinese_prompts, 
                    to_english=True
                )
                other_prompts.extend(translated_prompts)
                    
            except TranslationError as e:
                QMessageBox.warning(self, "翻译错误", str(e))
                # 翻译失败时使用原文
                for idx, prompt in chinese_prompts:
                    other_prompts.append((idx, prompt, ""))
        
        # 按原始索引排序
        sorted_prompts = sorted(other_prompts, key=lambda x: x[0])
        
        # 添加所有提示词到列表，现在已经按原始顺序排序
        for _, prompt, translation in sorted_prompts:
            item = QTreeWidgetItem([prompt, translation])
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
        highlight_format.setBackground(QColor("#2d5a88"))  # 深蓝色
        highlight_format.setForeground(QColor("#ffffff"))  # 白色
        
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

    def show_prompt_library(self):
        """显示提示词库对话框"""
        from ..dialogs.prompt_library_dialog import PromptLibraryDialog
        
        # 创建对话框
        self.prompt_library_dialog = PromptLibraryDialog(self)
        
        # 连接选中信号
        self.prompt_library_dialog.promptsSelected.connect(self._handle_prompts_selected)
        
        # 显示对话框
        self.prompt_library_dialog.show()

    def _handle_prompts_selected(self, selected_prompts):
        """处理提示词选中事件"""
        if selected_prompts:
            # 获取当前文本
            current_text = self.input_field.toPlainText()
            
            # 添加选中的提示词到输入框
            new_prompts = [prompt[0] for prompt in selected_prompts]
            if current_text:
                current_text += ", "
            current_text += ", ".join(new_prompts)
            self.input_field.setPlainText(current_text)
            
            # 直接添加到列表，包含中文翻译
            for en, zh in selected_prompts:
                item = QTreeWidgetItem([en, zh])
                self.prompt_list.addTopLevelItem(item) 