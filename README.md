# SD Prompt Manager

一个简单的 Stable Diffusion 提示词管理工具。

## 功能

- 中英文提示词自动翻译
- 提示词顺序拖拽排序
- 实时文本同步和高亮
- 提示词规范化
- 便于在设备间同步的提示词库

## 下载安装

1. 从 [Releases](https://github.com/c1921/Prompt-Manager/releases) 页面下载最新版本
2. 下载 `SD_Prompt_Manager_v*.exe` 文件
3. 双击运行，无需安装

## 使用说明

- 输入提示词
  - 在左侧文本框输入提示词
  - 使用中文或英文逗号分隔
  - 支持中英文混合输入
- 翻译功能
  - 输入中文时自动翻译为英文
  - 点击"翻译所有提示词"批量翻译
  - 保留原中文内容作为参考
- 列表管理
  - 拖拽调整提示词顺序
  - 点击列表项高亮对应文本
  - 自动同步更新文本内容
- 提示词库
  - 从提示词库中选择添加
  - 编辑个人词库
  - 使用 `.json` 文件存储，便于同步

## 开发相关

### 环境要求

- Python 3.10+
- PyQt6
- deep-translator

### 安装依赖

```bash
pip install -r requirements.txt
```

### 从源码运行

```bash
python main.py
```

### 构建可执行文件

```bash
python build.py
```

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
