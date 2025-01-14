import PyInstaller.__main__
import os
import shutil
import time
import psutil

def is_file_locked(filepath):
    """检查文件是否被占用"""
    try:
        # 尝试打开文件
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
                proc.wait(timeout=3)  # 等待进程终止
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            pass

def clean_dist():
    """清理之前的构建文件"""
    exe_path = 'dist/prompt_manager.exe'
    
    if os.path.exists(exe_path) and is_file_locked(exe_path):
        print("检测到应用正在运行，正在尝试关闭...")
        terminate_process('prompt_manager.exe')
        # 等待文件解锁
        for _ in range(5):  # 最多等待5秒
            if not is_file_locked(exe_path):
                break
            time.sleep(1)
    
    try:
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('prompt_manager.spec'):
            os.remove('prompt_manager.spec')
    except Exception as e:
        print(f"清理文件时出错: {e}")
        print("请手动关闭应用后重试")
        exit(1)

def build_app():
    """构建应用"""
    PyInstaller.__main__.run([
        'app.py',                    # 主程序文件
        '--name=prompt_manager',     # 生成的exe名称
        '--onefile',                 # 打包为单个文件
        '--windowed',                # 不显示控制台窗口
        '--add-data=templates;templates',  # 包含模板目录
        '--add-data=static;static',        # 包含静态文件目录
        '--add-data=config;config',        # 包含配置目录
        '--add-data=services;services',    # 包含服务目录
        '--hidden-import=config',          # 隐式导入
        '--hidden-import=services',
        '--hidden-import=webview',         # 添加 webview 依赖
        '--clean',                   # 清理临时文件
        '--noconfirm',              # 不确认覆盖
    ])

def main():
    """主函数"""
    print("开始构建应用...")
    
    # 清理之前的构建
    print("清理旧的构建文件...")
    clean_dist()
    
    # 构建应用
    print("正在构建应用...")
    build_app()
    
    print("构建完成！")
    print("可执行文件位置: dist/prompt_manager.exe")

if __name__ == '__main__':
    main() 