import json
import os
from typing import Dict, List

class PromptCategory:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.prompts: List[Dict[str, str]] = []

    def add_prompt(self, en: str, zh: str = ""):
        self.prompts.append({
            "en": en,
            "zh": zh
        })

class PromptLibrary:
    def __init__(self):
        self.categories: Dict[str, PromptCategory] = {}
        self.load_library()
    
    def load_library(self):
        """从 JSON 文件加载提示词库"""
        json_path = os.path.join(os.path.dirname(__file__), 'prompts.json')
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for key, cat_data in data.items():
                category = PromptCategory(cat_data['name'], cat_data['description'])
                for prompt in cat_data['prompts']:
                    category.add_prompt(prompt['en'], prompt['zh'])
                self.categories[key] = category
                
        except Exception as e:
            print(f"加载提示词库失败: {e}")
            # 加载失败时使用空库
            self.categories = {}

    def merge_library(self, data: dict):
        """合并导入的提示词库"""
        for key, cat_data in data.items():
            if key not in self.categories:
                self.categories[key] = PromptCategory(
                    cat_data['name'], 
                    cat_data['description']
                )
            for prompt in cat_data['prompts']:
                self.categories[key].add_prompt(prompt['en'], prompt['zh'])
        self.save_library()
    
    def export_library(self) -> dict:
        """导出提示词库数据"""
        data = {}
        for key, category in self.categories.items():
            data[key] = {
                'name': category.name,
                'description': category.description,
                'prompts': category.prompts
            }
        return data
    
    def add_category(self, name: str, description: str = ""):
        """添加新分类"""
        key = name.lower().replace(" ", "_")
        if key not in self.categories:
            self.categories[key] = PromptCategory(name, description)
            self.save_library()
    
    def add_prompt(self, category_name: str, en: str, zh: str):
        """添加新提示词"""
        for category in self.categories.values():
            if category.name == category_name:
                category.add_prompt(en, zh)
                self.save_library()
                break
    
    def delete_category(self, name: str):
        """删除分类"""
        for key, category in list(self.categories.items()):
            if category.name == name:
                del self.categories[key]
                self.save_library()
                break
    
    def delete_prompt(self, category_name: str, prompt_en: str):
        """删除提示词"""
        for category in self.categories.values():
            if category.name == category_name:
                category.prompts = [p for p in category.prompts 
                                  if p['en'] != prompt_en]
                self.save_library()
                break
    
    def save_library(self):
        """保存提示词库到文件"""
        json_path = os.path.join(os.path.dirname(__file__), 'prompts.json')
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.export_library(), f, 
                         ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存提示词库失败: {e}")

# 创建全局实例
PROMPT_LIBRARY = PromptLibrary() 