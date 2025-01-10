from deep_translator import GoogleTranslator
from typing import List, Tuple, Optional

class TranslationService:
    def __init__(self):
        self.en_to_zh = GoogleTranslator(source='en', target='zh-CN')
        self.zh_to_en = GoogleTranslator(source='zh-CN', target='en')
    
    def translate_text(self, text: str, to_english: bool = False) -> str:
        """翻译单个文本"""
        try:
            translator = self.zh_to_en if to_english else self.en_to_zh
            return translator.translate(text)
        except Exception as e:
            raise TranslationError(f"翻译失败: {str(e)}")
    
    def batch_translate(self, texts: List[str], to_english: bool = False) -> List[str]:
        """批量翻译文本"""
        if not texts:
            return []
            
        try:
            translator = self.zh_to_en if to_english else self.en_to_zh
            combined = "\n".join(texts)
            results = translator.translate(combined)
            return [r.strip() for r in results.split("\n")]
        except Exception as e:
            raise TranslationError(f"批量翻译失败: {str(e)}")
    
    def translate_prompts(self, prompts: List[Tuple[int, str]], 
                        to_english: bool = False) -> List[Tuple[int, str, str]]:
        """翻译提示词列表，保持原始顺序"""
        if not prompts:
            return []
            
        # 提取需要翻译的文本
        texts = [prompt for _, prompt in prompts]
        
        try:
            # 批量翻译
            translations = self.batch_translate(texts, to_english)
            
            # 组合结果，保持原始索引
            results = []
            for (idx, original), translated in zip(prompts, translations):
                if to_english:
                    results.append((idx, translated, original))
                else:
                    results.append((idx, original, translated))
            
            return results
        except Exception as e:
            raise TranslationError(f"提示词翻译失败: {str(e)}")


class TranslationError(Exception):
    """翻译错误异常类"""
    pass 