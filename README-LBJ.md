# Telegram Leecher Bot - Windows适配修改记录

## 项目概述

本文档记录了将原本为Google Colab环境设计的Telegram Leecher Bot成功适配到Windows环境的完整过程，包括遇到的问题、解决方案和代码修改。

## 修改历程

### 1. 项目分析与入口点确认

#### 问题发现
- 用户误认为`main.py`是程序启动入口
- `main.py`实际上是Google Colab环境的配置脚本

#### 解决方案
- 确认真正的程序入口是`colab_leecher/__main__.py`
- 正确的启动命令：`python -m colab_leecher`

### 2. 依赖问题修复

#### 问题描述
```
ModuleNotFoundError: No module named 'moviepy.editor'
```

#### 根本原因
- moviepy包的导入语句过时
- 新版本moviepy的模块结构发生变化

#### 修改文件：`colab_leecher/utility/converters.py`
```python
# 原代码（第14行）
from moviepy.editor import VideoFileClip as VideoClip

# 修改后
from moviepy.video.io.VideoFileClip import VideoFileClip as VideoClip
```

#### 附加解决
```bash
pip uninstall moviepy
pip install moviepy
```

### 3. 路径配置问题修复

#### 问题描述
- 程序使用硬编码的Linux路径
- Windows环境下路径分隔符不兼容

#### 修改文件：`colab_leecher/utility/variables.py`

**原代码：**
```python
class Paths:
    WORK_PATH = "/content/BOT_WORK"
    THMB_PATH = "/content/Telegram-Leecher/colab_leecher/Thumbnail.jpg"
    VIDEO_FRAME = "/content/BOT_WORK/video_frame.jpg"
    HERO_IMAGE = "/content/BOT_WORK/Hero.jpg"
    DEFAULT_HERO = "/content/custom_thmb.jpg"
    MOUNTED_DRIVE = "/content/drive"
    down_path = "/content/BOT_WORK/Downloads"
    # ... 其他路径
```

**修改后：**
```python
class Paths:
    # Use current working directory as base path for cross-platform compatibility
    BASE_PATH = os.getcwd()
    WORK_PATH = os.path.join(BASE_PATH, "BOT_WORK")
    THMB_PATH = os.path.join(BASE_PATH, "colab_leecher", "Thumbnail.jpg")
    VIDEO_FRAME = os.path.join(WORK_PATH, "video_frame.jpg")
    HERO_IMAGE = os.path.join(WORK_PATH, "Hero.jpg")
    DEFAULT_HERO = os.path.join(BASE_PATH, "custom_thmb.jpg")
    MOUNTED_DRIVE = os.path.join(BASE_PATH, "drive")
    down_path = os.path.join(WORK_PATH, "Downloads")
    temp_dirleech_path = os.path.join(WORK_PATH, "dir_leech_temp")
    mirror_dir = os.path.join(BASE_PATH, "drive", "MyDrive", "Colab Leecher Uploads")
    temp_zpath = os.path.join(WORK_PATH, "Leeched_Files")
    temp_unzip_path = os.path.join(WORK_PATH, "Unzipped_Files")
    temp_files_dir = os.path.join(WORK_PATH, "leech_temp")
    thumbnail_ytdl = os.path.join(WORK_PATH, "ytdl_thumbnails")
    access_token = os.path.join(BASE_PATH, "token.pickle")
```

#### 目录结构创建
同时修改了`colab_leecher/__main__.py`以确保必要目录的创建：
```python
# Create necessary directories
for path in [Paths.WORK_PATH, Paths.down_path, Paths.temp_dirleech_path, 
             Paths.temp_zpath, Paths.temp_unzip_path, Paths.temp_files_dir, 
             Paths.thumbnail_ytdl]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
```

### 4. Git管理优化

#### 修改文件：`.gitignore`
```gitignore
# 添加敏感配置文件
credentials.json
```

### 5. aria2c安装与配置

#### Windows环境aria2安装
1. 下载aria2-1.37.0-win-64bit-build1.zip
2. 解压到`D:\install\aria2-1.37.0-win-64bit-build1\`
3. 添加到系统PATH环境变量

#### PowerShell配置命令
```powershell
$env:PATH += ";D:\install\aria2-1.37.0-win-64bit-build1\"
```

### 6. YouTube下载问题诊断与修复

#### 问题现象
- 用户输入`@https://www.youtube.com/watch?v=n23fACkNBg0`（错误格式）
- 程序下载了Hero.jpg图片而非视频
- 出现"Peer id invalid: -1002608974306"错误

#### 根本原因分析
1. **Hero.jpg下载问题**：程序会先下载随机图片作为Hero.jpg，导致SSL握手失败
2. **DUMP_ID配置无效**：导致程序无法发送消息到指定频道
3. **流程设计问题**：下载图片失败导致整个任务流程中断

#### 修改文件：`colab_leecher/utility/task_manager.py`

**修改前的问题代码：**
```python
try:
    system(f"aria2c -d {Paths.WORK_PATH} -o Hero.jpg {Aria2c.pic_dwn_url}")
except Exception:
    Paths.HERO_IMAGE = Paths.DEFAULT_HERO
```

**修改后：**
```python
# try:
#     system(f"aria2c -d {Paths.WORK_PATH} -o Hero.jpg {Aria2c.pic_dwn_url}")
# except Exception:
#     Paths.HERO_IMAGE = Paths.DEFAULT_HERO

# Use default hero image instead of downloading
Paths.HERO_IMAGE = Paths.DEFAULT_HERO
```

**DUMP_ID错误处理改进：**
```python
try:
    MSG.sent_msg = await colab_bot.send_message(chat_id=DUMP_ID, text=src_text[0])
except Exception as e:
    logging.warning(f"Failed to send to DUMP_ID {DUMP_ID}, using OWNER instead: {e}")
    MSG.sent_msg = await colab_bot.send_message(chat_id=OWNER, text=src_text[0])
```

### 7. 支持的下载链接类型

程序支持以下类型的下载链接：

- **Google Drive链接** (♻️)
- **Telegram链接** (💬)  
- **MEGA云储存** (💾)
- **Terabox链接** (🍑)
- **YouTube和视频平台** (🏮) - 通过yt-dlp
- **磁力链接/种子** (🧲)
- **通用HTTP/HTTPS直链** (🔗)
- **本地文件路径** (📂)

### 8. 使用说明

#### 正确的使用步骤：

1. **启动程序**
   ```bash
   python -m colab_leecher
   ```

2. **发送命令**
   ```
   /tupload
   ```

3. **输入链接**（注意格式）
   ```
   https://www.youtube.com/watch?v=n23fACkNBg0
   ```
   ⚠️ **不要**添加`@`前缀

4. **选择处理类型**
   - Regular：正常文件上传
   - Compress：压缩后上传
   - Extract：解压后上传
   - UnDoubleZip：先解压再压缩

5. **等待处理完成**

#### 上传目标
- **主要目标**：DUMP_ID指定的Telegram频道/群组
- **备用目标**：OWNER个人聊天（当DUMP_ID无效时）

### 9. 测试结果

#### 成功测试案例：
1. **视频1**: `n23fACkNBg0.mp4` (917.43KiB) - 下载成功
2. **视频2**: `WME7tnOumNU.mp4` (118.09MiB) - 下载成功

#### 性能表现：
- 下载速度：1.08MiB/s - 5.06MiB/s
- 上传目标：Telegram频道/群组
- 连接状态：Pyrogram正常连接和断开

## 技术要点总结

### 跨平台兼容性
- 使用`os.path.join()`替代硬编码路径
- 使用`os.getcwd()`作为基础路径
- 支持Windows路径分隔符

### 错误处理改进
- 添加DUMP_ID失败回退机制
- 移除有问题的Hero.jpg下载
- 改进异常日志记录

### 依赖管理
- 修复moviepy导入问题
- 确保aria2c可执行文件可访问
- 添加必要目录自动创建

## 环境要求

- **操作系统**: Windows 10+
- **Python**: 3.10+
- **必需工具**: aria2c
- **必需包**: 见requirements.txt

## 注意事项

1. **配置文件安全**: credentials.json包含敏感信息，已添加到.gitignore
2. **网络代理**: 支持SOCKS5代理配置
3. **文件大小限制**: 超过2GB的文件会自动分割
4. **路径编码**: 支持中文路径名

## 贡献者

- **原作者**: Xron Trix (https://github.com/Xrontrix10)
- **Windows适配**: LBJ修改版

---

*本文档记录了完整的调试和修改过程，为后续维护和开发提供参考。* 