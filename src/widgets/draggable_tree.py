from PyQt6.QtWidgets import (QTreeWidget, QHeaderView, QMenu, QDialog, QMessageBox, 
                          QApplication, QPushButton, QHBoxLayout, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..dialogs.prompt_translation_dialog import PromptTranslationDialog
from deep_translator import GoogleTranslator
import time
from ..styles.dark_theme import TREE_WIDGET
from ..services.translator import TranslationService, TranslationError

class DraggableTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.dragged_item = None
        
        # 设置样式
        self.setStyleSheet(TREE_WIDGET)
        
        # 设置列头
        self.setHeaderLabels(["提示词", "中文翻译", "权重", "操作"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 100)
        
        # 启用交替行颜色
        self.setAlternatingRowColors(True)
        
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
        
        # 使用翻译服务
        self.translation_service = TranslationService()
    
    def _find_prompt_editor(self):
        """查找 PromptEditor 父窗口"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'update_input_field'):
                return parent
            parent = parent.parent()
        return None
    
    def dropEvent(self, event):
        """重写拖放事件，统一处理拖放位置"""
        if event.source() != self:
            event.ignore()
            return
        
        # 获取当前拖动的项
        current_item = self.currentItem()
        if not current_item:
            return
        
        # 保存禁用状态
        is_disabled = current_item.data(0, Qt.ItemDataRole.UserRole)
        
        # 获取目标位置
        drop_pos = event.position().toPoint()
        target_item = self.itemAt(drop_pos)
        
        # 确定插入位置
        if target_item:
            target_index = self.indexOfTopLevelItem(target_item)
        else:
            # 如果拖到空白处，插入到最后
            target_index = self.topLevelItemCount() - 1
        
        # 移除当前项
        current_index = self.indexOfTopLevelItem(current_item)
        taken_item = self.takeTopLevelItem(current_index)
        
        # 在目标位置插入
        self.insertTopLevelItem(target_index, taken_item)
        
        # 恢复禁用状态
        taken_item.setData(0, Qt.ItemDataRole.UserRole, is_disabled)
        
        # 保持选中状态
        self.setCurrentItem(taken_item)
        
        # 重新创建所有项的操作列
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            action_widget = self._create_action_widget(item)
            self.setItemWidget(item, 3, action_widget)
        
        # 更新输入框
        prompt_editor = self._find_prompt_editor()
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
            weight=item.text(2) or "1",
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item.setText(0, dialog.prompt_edit.text())
            item.setText(1, dialog.translation_edit.text())
            item.setText(2, dialog.weight_edit.text())
            prompt_editor = self._find_prompt_editor()
            if prompt_editor:
                prompt_editor.update_input_field()
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        item = self.itemAt(position)
        menu = QMenu()
        
        if item:
            edit_action = menu.addAction("编辑提示词")
            translate_action = menu.addAction("翻译此提示词")
        
        translate_all_action = menu.addAction("翻译所有提示词")
        action = menu.exec(self.mapToGlobal(position))
        
        if item and action == edit_action:
            self.edit_prompt(item)
        elif item and action == translate_action:
            self.translate_prompt(item)
        elif action == translate_all_action:
            self.translate_all_prompts()
    
    def translate_prompt(self, item):
        """翻译单个提示词"""
        try:
            text = item.text(0)
            translation = self.translation_service.translate_text(text)
            item.setText(1, translation)
        except TranslationError as e:
            QMessageBox.warning(self, "翻译错误", str(e))
    
    def translate_all_prompts(self):
        """批量翻译所有提示词"""
        # 收集需要翻译的提示词
        to_translate = []
        items = []
        
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if not item.text(1):  # 如果没有翻译
                to_translate.append((i, item.text(0)))
                items.append(item)
        
        if not to_translate:
            return
        
        try:
            # 使用翻译服务进行批量翻译
            results = self.translation_service.translate_prompts(to_translate)
            
            # 更新界面
            for item, (_, _, translation) in zip(items, results):
                item.setText(1, translation)
                
        except TranslationError as e:
            QMessageBox.warning(self, "翻译错误", str(e))
        
        # 让界面及时刷新
        QApplication.processEvents() 
    
    def _create_action_widget(self, item):
        """创建操作按钮组"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        
        # 禁用/启用按钮
        toggle_button = QPushButton("🛇")
        toggle_button.setFixedSize(24, 24)
        toggle_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #e0e0e0;
                font-family: "Segoe UI Emoji";
            }
            QPushButton[disabled="false"] {
                color: rgba(224, 224, 224, 0.5);
            }
            QPushButton[disabled="true"] {
                color: #e0e0e0;
            }
            QPushButton:hover {
                background: #404040;
                border-radius: 4px;
            }
        """)
        
        # 删除按钮
        delete_button = QPushButton("×")
        delete_button.setFixedSize(24, 24)
        delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                color: #e0e0e0;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #c42b1c;
                border-radius: 4px;
            }
        """)
        
        def update_toggle_button():
            """更新禁用按钮状态"""
            is_disabled = item.data(0, Qt.ItemDataRole.UserRole)
            toggle_button.setProperty("disabled", str(is_disabled).lower())
            toggle_button.style().unpolish(toggle_button)
            toggle_button.style().polish(toggle_button)
            toggle_button.setToolTip("启用" if is_disabled else "禁用")
        
        def toggle_disabled():
            """切换禁用状态"""
            current_state = item.data(0, Qt.ItemDataRole.UserRole)
            item.setData(0, Qt.ItemDataRole.UserRole, not current_state)
            update_toggle_button()
            # 更新输入框
            prompt_editor = self._find_prompt_editor()
            if prompt_editor:
                prompt_editor.update_input_field()
        
        # 初始化按钮状态
        is_disabled = item.data(0, Qt.ItemDataRole.UserRole)
        if is_disabled is None:  # 如果是新项
            item.setData(0, Qt.ItemDataRole.UserRole, False)
        update_toggle_button()  # 设置初始状态
        
        toggle_button.clicked.connect(toggle_disabled)
        delete_button.clicked.connect(lambda: self._delete_item(item))
        
        layout.addWidget(toggle_button)
        layout.addWidget(delete_button)
        layout.addStretch()
        
        return widget
    
    def _delete_item(self, item):
        """删除项目"""
        if QMessageBox.question(
            self, 
            "确认删除", 
            "确定要删除这个提示词吗？"
        ) == QMessageBox.StandardButton.Yes:
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
            prompt_editor = self._find_prompt_editor()
            if prompt_editor:
                prompt_editor.update_input_field()
    
    def addTopLevelItem(self, item):
        """重写添加项方法，添加操作按钮"""
        super().addTopLevelItem(item)
        action_widget = self._create_action_widget(item)
        self.setItemWidget(item, 3, action_widget) 