from PyQt6.QtWidgets import QTreeWidget, QHeaderView, QMenu, QDialog
from PyQt6.QtCore import Qt
from dialogs.prompt_translation_dialog import PromptTranslationDialog

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