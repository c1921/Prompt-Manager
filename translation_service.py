from deep_translator import GoogleTranslator
from typing import List, Tuple, Optional
import time

class TranslationService:
    def __init__(self):
        self.en_to_zh = GoogleTranslator(source='en', target='zh-CN')
        self.zh_to_en = GoogleTranslator(source='zh-CN', target='en')
        self.last_request_time = 0
        self.min_interval = 1.0  # 最小请求间隔（秒）
    
    def _check_rate_limit(self):
        """检查是否可以发送新的请求"""
        current_time = time.time()
        time_passed = current_time - self.last_request_time
        
        if time_passed < self.min_interval:
            raise TranslationError(f"请求过于频繁，请等待 {(self.min_interval - time_passed):.1f} 秒")
        
        self.last_request_time = current_time
    
    def translate_text(self, text: str, to_english: bool = False) -> str:
        """翻译单个文本"""
        try:
            self._check_rate_limit()  # 检查请求限制
            translator = self.zh_to_en if to_english else self.en_to_zh
            return translator.translate(text)
        except TranslationError as e:
            raise e
        except Exception as e:
            raise TranslationError(f"翻译失败: {str(e)}")

class TranslationError(Exception):
    """翻译错误异常类"""
    pass 