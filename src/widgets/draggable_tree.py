from PyQt6.QtWidgets import QTreeWidget, QHeaderView, QMenu, QDialog, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from dialogs.prompt_translation_dialog import PromptTranslationDialog
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
        self.setHeaderLabels(["提示词", "中文翻译", "权重"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(2, 60)
        
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
        
        # 修改这里：通过遍历父窗口层级找到 PromptEditor 实例
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