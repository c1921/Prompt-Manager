class Config:
    """基础配置类"""
    DEBUG = False
    TRANSLATION_MIN_INTERVAL = 1.0  # 翻译请求最小间隔（秒）
    NETWORK_CHECK_INTERVAL = 30.0   # 网络检测间隔（秒）
    GOOGLE_TEST_URL = "https://translate.google.com"
    WEBVIEW_DEBUG = False

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TRANSLATION_MIN_INTERVAL = 1.0
    NETWORK_CHECK_INTERVAL = 10.0   # 开发环境更频繁检测

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TRANSLATION_MIN_INTERVAL = 2.0
    NETWORK_CHECK_INTERVAL = 60.0   # 生产环境降低检测频率

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 