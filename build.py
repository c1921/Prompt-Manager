import PyInstaller.__main__
import os
from string import Template
from src.version import *

def generate_version_info():
    """生成版本信息文件"""
    version_info = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={VERSION + (0,)},
    prodvers={VERSION + (0,)},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404B0',
        [StringStruct(u'CompanyName', u'{COMPANY}'),
        StringStruct(u'FileDescription', u'{DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{VERSION_STR}'),
        StringStruct(u'InternalName', u'SDPromptManager'),
        StringStruct(u'LegalCopyright', u'{COPYRIGHT}'),
        StringStruct(u'OriginalFilename', u'SDPromptManager.exe'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{VERSION_WITH_META}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
"""
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