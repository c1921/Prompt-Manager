import PyInstaller.__main__
import os
from string import Template
from src.version import *

def generate_version_info():
    """生成版本信息文件"""
    # 添加版本信息日志
    print(f"当前版本号: {VERSION_STR}")
    
    # 读取模板文件
    with open('version_info.template', 'r', encoding='utf-8') as f:
        template = Template(f.read())
    
    # 准备替换变量
    version_tuple = VERSION + (0,)  # 添加一个0作为第四个版本号
    variables = {
        'VERSION_TUPLE': str(version_tuple),
        'VERSION_STR': VERSION_STR,
        'APP_NAME': APP_NAME,
        'COMPANY': COMPANY,
        'DESCRIPTION': DESCRIPTION,
        'COPYRIGHT': COPYRIGHT
    }
    
    # 替换变量生成最终内容
    version_info = template.substitute(variables)
    
    # 写入文件
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)

# 生成版本信息
generate_version_info()

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 构建输出文件名
output_name = f"SD_Prompt_Manager_v{VERSION_STR}"

PyInstaller.__main__.run([
    'main.py',
    f'--name={output_name}',
    '--windowed',
    '--onefile',
    '--icon=assets/icon.ico',
    '--version-file=version_info.txt',
    '--add-data=src/styles;src/styles',
    '--clean',
    '--noconfirm'
]) 