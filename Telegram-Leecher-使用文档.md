# Telegram Leecher Bot 使用文档

## 📖 项目概述

Telegram Leecher 是一个基于 Pyrogram 的 Telegram 机器人，用于从各种来源下载文件并上传到 Telegram 或 Google Drive。该程序支持多种下载源、文件处理和转换功能。

## 🚀 程序启动

### 启动命令
```bash
python -m colab_leecher
```

### 前置要求
1. 已配置 `credentials.json` 文件
2. 安装所有依赖包：`pip install -r requirements.txt`
3. Windows 环境需安装 aria2c 并添加到 PATH

## 🎯 可用命令详解

### 1. `/start` - 机器人状态检查
**功能**: 检查机器人是否在线并显示基本信息
**执行后**: 显示欢迎信息和项目链接
**后续操作**: 可以选择查看仓库或加入支持群组

---

### 2. `/tupload` - Telegram 上传模式 
**功能**: 下载文件并上传到 Telegram
**使用流程**:
1. 发送 `/tupload` 命令
2. 按提示格式发送下载链接
3. 选择处理类型（Regular/Compress/Extract/UnDoubleZip）
4. 等待下载和上传完成

**链接格式示例**:
```
https://example.com/file1.mp4
https://example.com/file2.zip
[自定义文件名.mp4]
{压缩包密码}
(解压密码)
```

**处理类型选择**:
- **Regular**: 直接下载上传，不做额外处理
- **Compress**: 先压缩文件再上传（适合多个小文件）
- **Extract**: 先解压文件再上传（适合压缩包）
- **UnDoubleZip**: 先解压再重新压缩（处理嵌套压缩包）

---

### 3. `/gdupload` - Google Drive 上传模式
**功能**: 下载文件并上传到 Google Drive
**使用流程**: 与 `/tupload` 相同，但上传目标为 Google Drive
**后续操作**: 
- 上传完成后会显示 Google Drive 文件链接
- 可以直接在 Drive 中查看和管理文件

---

### 4. `/drupload` - 本地目录上传
**功能**: 上传本地文件夹到 Telegram
**使用示例**:
```
/drupload
然后发送: /home/user/Downloads/folder
```
**后续操作**: 选择处理类型并等待上传完成

---

### 5. `/ytupload` - YouTube 专用下载
**功能**: 使用 yt-dlp 下载 YouTube 等视频平台内容
**支持平台**: YouTube、Bilibili 等 2000+ 视频网站
**特殊功能**: 
- 自动选择最佳质量
- 提取视频缩略图
- 支持播放列表下载

---

### 6. `/settings` - 机器人设置
**功能**: 配置机器人各项参数
**可配置项目**:

#### 上传设置
- **Media**: 以媒体文件形式上传（可预览）
- **Document**: 以文档形式上传（保留原始文件名）

#### 视频设置
- **Split Videos**: 大视频文件分割上传
- **Zip Videos**: 大视频文件压缩上传
- **Convert**: 是否转换视频格式
- **Format**: 转换为 MP4 或 MKV
- **Quality**: 高质量或低质量转换

#### 字幕设置
- **Caption Font**: 设置文件描述的字体样式
  - Monospace（等宽字体）
  - Regular（常规字体）
  - Bold（粗体）
  - Italic（斜体）
  - Underlined（下划线）

#### 文件名设置
- **Prefix**: 为文件名添加前缀
- **Suffix**: 为文件名添加后缀

#### 缩略图设置
- 可以设置自定义缩略图（发送图片即可）

---

### 7. `/setname` - 设置自定义文件名
**格式**: `/setname 新文件名.扩展名`
**示例**: `/setname 我的视频.mp4`
**作用范围**: 仅对下一次下载的文件生效
**注意**: 15秒后消息自动删除

---

### 8. `/zipaswd` - 设置压缩密码
**格式**: `/zipaswd 密码`
**功能**: 为输出的压缩文件设置密码
**应用场景**: 当选择 Compress 模式时使用
**安全性**: 命令执行后消息会被删除

---

### 9. `/unzipaswd` - 设置解压密码
**格式**: `/unzipaswd 密码`
**功能**: 设置解压压缩包的密码
**应用场景**: 下载受密码保护的压缩包时使用

---

### 10. `/help` - 帮助信息
**功能**: 显示所有可用命令的简要说明
**包含链接**: 
- 详细使用说明
- 官方频道
- 讨论群组

## 🔗 支持的下载源

| 类型 | 图标 | 说明 | 示例 |
|------|------|------|------|
| Google Drive | ♻️ | 自动认证，支持大文件 | drive.google.com/file/... |
| Telegram | 💬 | 支持私聊和频道文件 | t.me/channel/123 |
| MEGA | 💾 | 云存储服务 | mega.nz/file/... |
| Terabox | 🍑 | 百度网盘国际版 | terabox.com/s/... |
| YouTube | 🏮 | 视频平台，支持2000+网站 | youtube.com/watch?v=... |
| 磁力链接 | 🧲 | BT下载（谨慎使用） | magnet:?xt=urn:btih:... |
| 直链 | 🔗 | HTTP/HTTPS 直接下载链接 | https://example.com/file.zip |
| 本地路径 | 📂 | 本地文件系统路径 | /home/user/file.mp4 |

## 🎮 使用流程示例

### 示例1: 下载 YouTube 视频到 Telegram
1. 发送 `/tupload`
2. 发送视频链接：`https://www.youtube.com/watch?v=VIDEO_ID`
3. 选择 "Regular" 处理类型
4. 等待下载和上传完成
5. 在 Telegram 中收到视频文件

### 示例2: 批量下载多个文件并压缩
1. 发送 `/tupload`
2. 发送多个链接：
   ```
   https://example.com/file1.pdf
   https://example.com/file2.docx
   https://example.com/file3.jpg
   [我的文档合集]
   {mypassword}
   ```
3. 选择 "Compress" 处理类型
4. 文件将被打包成密码保护的压缩包并上传

### 示例3: 解压并重新整理文件
1. 发送 `/tupload`
2. 发送压缩包链接：`https://example.com/archive.rar`
3. 发送解压密码：`/unzipaswd original_password`
4. 选择 "UnDoubleZip" 处理类型
5. 文件将被解压，然后重新压缩为无密码压缩包

## ⚙️ 高级功能

### 视频转换
- 自动检测视频格式并转换为 MP4/MKV
- 支持质量调整（高质量/压缩质量）
- 自动生成视频缩略图
- 大视频自动分割或压缩

### 文件分割
- 超过 2GB 的文件自动分割（免费用户）
- Premium 用户支持 4GB 文件上传
- 分割文件自动编号

### 智能文件名处理
- 自动截短过长文件名（最大60字符）
- 支持自定义前缀后缀
- 保持文件扩展名

### 实时状态显示
- 显示下载/上传进度
- 显示传输速度
- 显示系统资源使用情况
- 显示预计完成时间

## 🚨 注意事项

### 1. 文件大小限制
- 免费 Telegram: 最大 2GB
- Premium Telegram: 最大 4GB
- Google Drive: 无限制

### 2. 下载源限制
- 避免下载版权内容
- 磁力链接谨慎使用（Google Colab 禁止）
- 某些网站可能有访问限制

### 3. 系统资源
- 监控磁盘空间使用
- 大文件下载需要足够存储空间
- 并发任务数量限制

### 4. 安全建议
- 不要在公共频道分享敏感文件
- 使用密码保护重要压缩包
- 定期清理临时文件

## 🛠️ 故障排除

### 常见问题

**1. "I am Already Working"错误**
- 等待当前任务完成
- 或发送取消命令停止当前任务

**2. 下载失败**
- 检查链接是否有效
- 检查网络连接
- 检查磁盘空间

**3. 上传失败**
- 检查文件大小是否超限
- 检查 Telegram 机器人权限
- 检查 Google Drive 配置

**4. 视频转换失败**
- 检查 FFmpeg 是否正确安装
- 检查源视频格式是否支持
- 尝试降低转换质量

### 日志信息
程序运行时会显示详细的状态信息，包括：
- 当前任务类型和进度
- 系统资源使用情况
- 错误信息和警告
- 下载/上传速度统计

## 📞 支持与反馈

- **频道**: https://t.me/Colab_Leecher
- **讨论群**: https://t.me/Colab_Leecher_Discuss  
- **项目仓库**: https://github.com/XronTrix10/Telegram-Leecher
- **使用说明**: https://github.com/XronTrix10/Telegram-Leecher/wiki/INSTRUCTIONS

## 📋 更新日志

最新版本支持：
- Windows 系统兼容性优化
- 新增多种下载源支持
- 改进视频转换功能
- 优化错误处理机制
- 增强安全性和稳定性

---

**注意**: 本程序仅供学习和个人使用，请遵守相关法律法规和平台使用条款。 