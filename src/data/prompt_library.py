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

# 创建全局实例
PROMPT_LIBRARY = PromptLibrary() 