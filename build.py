import PyInstaller.__main__
import os
import sys
import shutil
import time
import psutil
from string import Template
from src.version import *

def is_file_locked(filepath):
    """检查文件是否被占用"""
    try:
        with open(filepath, 'a'):
            return False
    except:
        return True

def terminate_process(exe_name):
    """终止指定名称的进程"""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == exe_name:
                proc.terminate()
                proc.wait(timeout=3)
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass

def generate_version_info():
    """生成版本信息文件"""
    print(f"当前版本号: {VERSION_STR}")
    
    try:
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
            
    except Exception as e:
        print(f"生成版本信息时出错: {str(e)}")
        raise

def clean_dist():
    """清理之前的构建文件"""
    output_name = "SD Prompt Manager"
    exe_path = f'dist/{output_name}.exe'
    
    if os.path.exists(exe_path) and is_file_locked(exe_path):
        print("检测到应用正在运行，正在尝试关闭...")
        terminate_process(f'{output_name}.exe')
        for _ in range(5):
            if not is_file_locked(exe_path):
                break
            time.sleep(1)
    
    try:
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('version_info.txt'):
            os.remove('version_info.txt')
        if os.path.exists(f'{output_name}.spec'):
            os.remove(f'{output_name}.spec')
    except Exception as e:
        print(f"清理文件时出错: {e}")
        print("请手动关闭应用后重试")
        exit(1)

def build_app():
    """构建应用"""
    output_name = "SD Prompt Manager"
    PyInstaller.__main__.run([
        'app.py',
        f'--name={output_name}',
        '--onefile',
        '--windowed',
        '--add-data=templates;templates',
        '--add-data=static;static',
        '--add-data=config;config',
        '--add-data=services;services',
        '--hidden-import=config',
        '--hidden-import=services',
        '--hidden-import=webview',
        '--version-file=version_info.txt',
        '--clean',
        '--noconfirm',
    ])

def main():
    """主函数"""
    print("开始构建应用...")
    
    # 确保在正确的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 清理之前的构建
    print("清理旧的构建文件...")
    clean_dist()
    
    # 生成版本信息
    print("生成版本信息...")
    try:
        generate_version_info()
    except Exception as e:
        print(f"生成版本信息失败: {e}")
        return
    
    if not os.path.exists('version_info.txt'):
        print("错误：version_info.txt 文件未生成")
        return
        
    # 构建应用
    print("正在构建应用...")
    try:
        build_app()
        print("构建完成！")
        print(f'可执行文件位置: dist/SD Prompt Manager.exe')  # 修改为实际的文件名
    except Exception as e:
        print(f"构建失败: {e}")
    finally:
        # 清理临时文件
        if os.path.exists('version_info.txt'):
            os.remove('version_info.txt')

if __name__ == '__main__':
    main() 