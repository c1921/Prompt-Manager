class Config:
    """基础配置类"""
    DEBUG = False
    TRANSLATION_MIN_INTERVAL = 1.0  # 翻译请求最小间隔（秒）

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TRANSLATION_MIN_INTERVAL = 1.0

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TRANSLATION_MIN_INTERVAL = 2.0  # 生产环境使用更长的间隔

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 